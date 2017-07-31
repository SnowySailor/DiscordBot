import discord
from utilities.utilities import getValue, setValue

def isRateLimited(redis, server, msg, bot):
    if msg.channel.id in bot.servers[msg.server.id].whitelistChannels:
        # The channel is whitelisted
        return
    if len(bot.servers[msg.server.id].whitelistRoles
            .intersection(
            set([x.id for x in msg.author.roles]))) > 0:
        # At least 1 of the user's roles were whitelisted
        return
    key = msg.server.id + "." + msg.author.id
    if redis.get(key) is None:
        redis.psetex(key, 3000, False)
        return False
    else:
        expireTime = redis.pttl(key)
        if expireTime > 10000:
            # Expire time exceeds rate limit
            return True
#        elif expireTime > 6000:
#            return 
# Figure something out to return as a "warning"
        elif expireTime is -1:
            # No expire time set
            return False
        elif expireTime is -2:
            # Invalid key (doesn't make much sense)
            # Only way this could happen is if the key expired
            # between the "if" condition and now.
            # In that case they wouldn't be limited
            return False
        else:
            expireTime = expireTime + 3000
            redis.pexpire(key, expireTime)
    return False

# settings is settings['spamFilter'] dict!
async def handleRateLimit(bot, client, msg, settings):
    if ("muteUser" in settings and
            settings['muteUser']):
        await muteUser(client, msg, bot)
    if ("notifyAdmin" in settings and 
            settings['notifyAdmin']):
        await messageAdmins(client, msg)
    return

async def messageAdmins(client, msg):
    # Notify the server administrators
    # If the server is larger than 250 members we can't see all members
    # online/offline so we need to request a list of offline people
    if msg.server.large:
        await client.request_offline_members(msg.server)
    admins = []
    # Find the admins
    # It's likely more efficient to look them up this way considering
    # spam isn't likely to happen often and checking to see if a user
    # is an admin on every single user update would cost a lot in the
    # long run.
    for member in msg.server.members:
        perms = msg.channel.permissions_for(member)
        if perms.administrator:
            admins.append(member)
    for admin in admins:
        try:
            # Message the admins of the server about the spam
            await client.send_message(admin, "{0.author.mention} has sent "\
            "a lot of messages in a short amount of time in {0.server.name}."\
            " Channel #{0.channel.name}".format(msg))
        except Exception:
            pass
    return

async def muteUser(client, msg, bot):
    # Locate the muted user role
    timeoutRole = tryGetMuteRole(client, msg)
    # If we couldn't locate, need to create one
    if timeoutRole is None:
        timeoutRole = await tryCreateMuteRole(client, msg)
        # If we still couldn't create one, then we have to stop here
        if timeoutRole is None:
            return
    # Try to edit channel permissions to block messages from being sent
    _ = await tryOverwriteChannelPermissions(client, msg, timeoutRole, bot,
        send_messages=False, send_tts_messages=False)
    # Try to mute the user
    muted = await tryAddMuteRole(client, msg, timeoutRole)
    if muted:
        # Message the user that got muted
        await client.send_message(msg.author, "You have been silenced "\
            "in {0.server.name} due to too many messages being sent in "\
            "a short period of time. Please message the server admins "\
            "if you have questions or if this shouldn't have heppened."
            .format(msg))
    return

async def giveUserWarning(client, msg):
    await client.send_message(msg.channel, "{0.author.mention} please slow "\
        "your messages down or type in full sentences.".format(msg))
    return

def tryGetMuteRole(client, msg):
    return discord.utils.get(msg.server.roles, permissions__value=66560,
        name="timeout")

async def tryCreateMuteRole(client, msg):
    try:
        # Create permissions that don't allow the user to send messages
        newPerm = discord.Permissions(permissions=66560,
            send_messages=False, send_tts_messages=False)
        # Create the actual role
        timeoutRole = await client.create_role(msg.server,
            permissions=newPerm, name="timeout",
            color=discord.Colour.default(), hoist=False,
            mentionable=False)
        return timeoutRole
    except discord.Forbidden:
        # Can't create role, message owner.
        await client.send_message(msg.server.owner, "I can't create a "\
            "role to place silenced users into. Please create a role in "\
            "{0.server.name} that is not allowed to send messages or "\
            "send TTS messages.".format(msg))
        return None
    return None

async def tryAddMuteRole(client, msg, role):
    try:
        # Try to give the role to the user
        await client.add_roles(msg.author, role)
        return True
    except discord.Forbidden:
        # Can't add the role, message owner.
        await client.send_message(msg.server.owner, "I can't add "\
            "a timeout role to a spamming user in {0.server.name}. "\
            "Please grant me those permissions or disable spam "\
            "prevention with the $settings command.".format(msg))
        return False
    return

async def tryOverwriteChannelPermissions(client, msg, muteRole, bot, **kwargs):
    serverId = msg.server.id
    serverChanOW = bot.servers[serverId].channelOverwrites
    failures = []
    # Get a default channel overwrite
    overwrite = discord.PermissionOverwrite()
    # Apply settings from kwargs
    for k, v in kwargs.items():
        setattr(overwrite, k, v)
    for channel in msg.server.channels:
        # Ignore the voice channels
        if channel.type is discord.ChannelType.voice:
            continue
        # Check to see if we've already modified the channels for this role
        # If not, we need to modify them
        if channel.id not in serverChanOW:
            # Create the empty set
            serverChanOW[channel.id] = set()
        if muteRole.id not in serverChanOW[channel.id]:
            try:
                await client.edit_channel_permissions(channel, muteRole,
                    overwrite)
                serverChanOW[channel.id].add(muteRole.id)
                bot.servers[serverId].dumpToYamlData("channelOverwrites")
            except discord.Forbidden:
                failures.append(channel.name)
    # If there were any failures due to permissions, we need to tell the owner
    # to either allow us to edit the permissions or have them do it
    if len(failures) > 0:
        await client.send_message(msg.server.owner, "I was unable to edit "\
            "channel permissions in these channels for {}: {}. Please give "\
            "me channel manage permissions or edit the `timeout` role so "\
            "it cannot send messages or send TTS messages in those channels."
            .format(msg.server.name, ', '.join(failures)))
    return failures
