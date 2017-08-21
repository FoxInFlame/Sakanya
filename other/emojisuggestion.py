# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import re for RegEx
import re
# Import csv to save reactions to CSV
import csv
# Import URLlib.request for requests
import urllib.request
# Import URLlib.error to handle error
import urllib.error

class EmojiSuggestion():
  def __init__(self, bot):
    self.bot = bot

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
  
  async def getMessageIDs(self, filename):
    """
    Get the list() of lines from filename
    """
    messages = [];
    with open(filename, 'r') as data_file:
      reader = csv.reader(data_file)
      messages = list(reader)
    return messages

  async def writeMessageIDs(self, filename, arr):
    """
    Write the list() of lines to filename
    """
    with open(filename, 'w') as data_file:
      writer = csv.writer(data_file)
      writer.writerow(arr)

  async def checkReactionRatioMessage(self, msg):
    """
    Check if a message has at least 5 upvotes, and the ratio is less than 2
    """
    reactions = msg.reactions # List of reactions
    amountofthumbsup = 0
    amountofthumbsdown = 0
    for reaction in reactions:
      if reaction.emoji == '👍': # 6:3 will fail
        for user in await self.bot.get_reaction_users(discord.Reaction(message=msg, emoji='👍')):
          amountofthumbsup += 1 # 7.3 will pass
      if reaction.emoji == '👎':
        for user in await self.bot.get_reaction_users(discord.Reaction(message=msg, emoji='👎')):
          amountofthumbsdown += 1
    if amountofthumbsup < 5:
      # Thumbs up is less than 5 (minimum is not fulfilled)
      return False
    if amountofthumbsdown != 0 and amountofthumbsup / amountofthumbsdown <= 2: 
      # Thumbs up / Thumbs down is less than 2 (minimum is not fulfilled)
      return False
    # Add custom emoji now weee

  async def add_custom_emoji(self, message):
    """
    Remove the emoji suggestion from the suggestion list (csv) and add it to the await list (csv)
    """
    messagelist = await self.getMessageIDs('emojisuggestions.csv')
    new_messagelist = []
    for messageid in messagelist:
      if len(messageid) == 0: continue
      if messageid[0] != message.id: new_messagelist.append(messageid)
    await self.writeMessageIDs('emojisuggestions.csv', new_messagelist)
    regex = re.compile(r':(.*?):')
    try:
      suggestionemojiname = regex.findall(message.content)[0]
      url = message.content.split('\n')[1]

      foxinflame = await self.bot.get_user_info('202501452596379648')
      waitforapproval = await self.bot.send_message(foxinflame, content='Please add the following emoji: *' + suggestionemojiname + '*\n' + url)

      print("adding to await list")
      with open(r'waitforapprovals.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([str(message.id), str(waitforapproval.id), suggestionemojiname])
      print("added")
    except IndexError as e:
      print('Somehow the emoji code didn\'t exist when it existed I checked last time (only a few seconds ago)')
      await self.bot.remove_reaction(message, '🔄', message.server.me)
      await self.bot.add_reaction(message, '❎')
      return False


  async def on_ready(self):
    """
    Check if any suggestions were passed during the time Sakanya was offline.
    """
    messagelist = await self.getMessageIDs('emojisuggestions.csv')
    for message in messagelist:
      # Check each message to see if criteria has been met during offline time
      if len(message) == 0: continue # Empty line
      try:
        discordmessage = await self.bot.get_message(self.bot.get_channel('341874607651029003'), message[0]) # optionally use jsonmsg['d']['channel_id']
        # suggestion in Null
        regexp = re.compile(r'Emoji Suggestion - :[^:]+:\nhttps?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
        if regexp.search(discordmessage.content) is False:
          # If edited and format somehow doesn't fit
          print('Message is no longer fitting the RegExp, maybe they changed it?')
          return
        # Check if it's already processing/rejected/or done - if so stop
        emojis = ['🔄', '❎', '✅']
        for emoji in emojis:
          users = await self.bot.get_reaction_users(reaction=discord.Reaction(message=discordmessage, emoji='🔄'))
          for user in users:
            if bot.user.id == user.id:
              print('I already marked it processing')
              return # I already marked it as processing
        valid = await self.checkReactionRatioMessage(discordmessage)
        if valid is not False:
          emojis = ['🇴', '🇵', '🇪', '🇳'] # Remove open letters
          for emoji in emojis: # Not just mine, but everyone's
            users = await self.bot.get_reaction_users(reaction=discord.Reaction(message=discordmessage, emoji=emoji))
            for user in users:
              member = discordmessage.server.get_member(user.id)
              await self.bot.remove_reaction(discordmessage, emoji, member)
          await self.bot.add_reaction(discordmessage, '🔄') # Add processing unicode (arrow_counterclockwise)
          await self.add_custom_emoji(discordmessage)
      except discord.errors.NotFound as e:
        print(e)
        continue

  async def on_message(self, message):
    """
    Check if the message is an emoji suggestion, if so, add it to the list.
    """
    if message.channel.id == '341874607651029003': # suggestion in Null
      if message.content.startswith('Emoji Suggestion - '):
        regexp = re.compile(r'Emoji Suggestion - :[^:]+:\nhttps?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
        if regexp.search(message.content):
          imageurl = message.content.split('\n')[1]
          req = urllib.request.Request(url=imageurl, data=None, headers=self.headers)
          try:
            response = urllib.request.urlopen(req)
            # Check main mimetype
            if response.info().get_content_maintype() == 'image':
              with open(r'emojisuggestions.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(message.id), '0', '0'])
              await self.bot.add_reaction(message, '🇴') # Just to show it's open to voting
              await self.bot.add_reaction(message, '🇵')
              await self.bot.add_reaction(message, '🇪')
              await self.bot.add_reaction(message, '🇳')
              await self.bot.add_reaction(message, '👍')
              await self.bot.add_reaction(message, '👎')
              print('A new emoji has been added to the queue.')
            else:
              await self.bot.send_message(message.channel, 'I could\'t identify your link as a wonderful image... \n｡･ﾟﾟ\*(>д<)\*ﾟﾟ･｡')
          except (urllib.error.HTTPError, urllib.error.URLError) as e:
            await self.bot.send_message(message.channel, 'I ran into an HTTPError... \n。゜゜(´Ｏ`) ゜゜。 Error code: ' + str(e.code))

        else:
          await self.bot.send_message(message.channel, 'Format for new Emoji:', embed=discord.Embed(
            color = 15839636,
            type = 'rich',
            description = '```Emoji Suggestion - :suggestion:\n<icon url>```'
          ))

  async def on_socket_response(self, jsonmsg):
    """
    Check if the reaction made the suggestion pass. If it passed, check the ratio then call add_custom_emoji()
    """
    if jsonmsg['t'] == 'MESSAGE_REACTION_REMOVE':
      message = await self.bot.get_message(self.bot.get_channel(jsonmsg['d']['channel_id']), jsonmsg['d']['message_id'])

      if jsonmsg['d']['channel_id'] == '341874607651029003':
        # In #suggestions
        messagelist = await self.getMessageIDs('emojisuggestions.csv')
        for suggestionid in messagelist:
          if len(suggestionid) == 0: continue # Empty line
          if suggestionid[0] == jsonmsg['d']['message_id']:
            try:
              regexp = re.compile(r'Emoji Suggestion - :[^:]+:\nhttps?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
              if regexp.search(message.content) is False:
                # If edited and format somehow doesn't fit
                print('Message is no longer fitting the RegExp, maybe they changed it?')
                return
              # Check if it's already processing/rejected/or done - if so stop
              emojis = ['🔄', '❎', '✅']
              for emoji in emojis:
                users = await self.bot.get_reaction_users(reaction=discord.Reaction(message=message, emoji='🔄'))
                for user in users:
                  if self.bot.user.id == user.id: 
                    print('I already marked it as processing')
                    return # I already marked it as processing
              valid = await self.checkReactionRatioMessage(message)
              if valid is not False:
                emojis = ['🇴', '🇵', '🇪', '🇳'] # Remove open letters
                for emoji in emojis: # Not just mine, but everyone's
                  users = await self.bot.get_reaction_users(reaction=discord.Reaction(message=message, emoji=emoji))
                  for user in users:
                    member = message.server.get_member(user.id)
                    await self.bot.remove_reaction(message, emoji, member)
                await self.bot.add_reaction(message, '🔄') # Add processing unicode (arrow_counterclockwise)
                await self.add_custom_emoji(message)
            except discord.errors.NotFound as e:
              print(e)

    if jsonmsg['t'] == 'MESSAGE_REACTION_ADD':
      message = await self.bot.get_message(self.bot.get_channel(jsonmsg['d']['channel_id']), jsonmsg['d']['message_id'])

      if jsonmsg['d']['channel_id'] == '341874607651029003':
        # In #suggestions
        # Check if it's an Emoji Suggestion
        messagelist = await self.getMessageIDs('emojisuggestions.csv')
        for suggestionid in messagelist:
          if len(suggestionid) == 0: continue # Empty line
          if suggestionid[0] == jsonmsg['d']['message_id']:
            try:
              regexp = re.compile(r'Emoji Suggestion - :[^:]+:\nhttps?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')
              if regexp.search(message.content) is False:
                # If edited and format somehow doesn't fit
                print('Message is no longer fitting the RegExp, maybe they changed it?')
                return
              # Check if it's already processing/rejected/or done - if so stop
              emojis = ['🔄', '❎', '✅']
              for emoji in emojis:
                users = await self.bot.get_reaction_users(reaction=discord.Reaction(message=message, emoji='🔄'))
                for user in users:
                  if self.bot.user.id == user.id:
                    print('I already marked it as processing')
                    return # I already marked it as processing
              valid = await self.checkReactionRatioMessage(message)
              if valid is not False:
                emojis = ['🇴', '🇵', '🇪', '🇳'] # Remove open letters
                for emoji in emojis: # Not just mine, but everyone's
                  users = await self.bot.get_reaction_users(reaction=discord.Reaction(message=message, emoji=emoji))
                  for user in users:
                    member = message.server.get_member(user.id)
                  await self.bot.remove_reaction(message, emoji, member)
                await self.bot.add_reaction(message, '🔄') # Add processing unicode (arrow_counterclockwise)
                await self.add_custom_emoji(message)
            except discord.errors.NotFound as e:
              print(e)

      if jsonmsg['d']['channel_id'] == '':
        # Private DM with FoxInFlame
        # Remove message from approval list, and confirm add
        messagelist = await self.getMessageIDs('waitforapprovals.csv')
        new_approvalmessageids = []
        for index, approvalid in enumerate(messagelist):
          if len(approvalid) == 0: continue #Empty line
          if approvalid[1] == jsonmsg['d']['message_id']: # it was the approval message
            try:
              originalsuggestionmessage = await self.bot.get_message(self.bot.get_channel('341874607651029003'), approvalid[0])
              await self.bot.remove_reaction(originalsuggestionmessage, '🔄', originalsuggestionmessage.server.me)
              await self.bot.add_reaction(originalsuggestionmessage, '✅')
              await self.bot.send_message(self.bot.get_channel('317924870950223872'), 'An new emoji is now present in this server: `' + approvalid[2] + '`') # general in Null
            except discord.errors.NotFound as e:
              print(e)
          else:
            new_approvalmessageids.append(approvalid)
        await self.writeMessageIDs('waitforapprovals.csv', new_approvalmessageids)

def setup(bot):
  bot.add_cog(EmojiSuggestion(bot))