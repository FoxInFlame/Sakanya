# Import discord
import discord
# Import undocumented part of Discord to use commands
from discord.ext import commands
# Import sys to import from parent directory
import sys
sys.path.append("..")
# Import Sakanya Core
from core import SakanyaCore
# Import collections to use Named Tuples
import collections
# Import URLlib.parse to manipulate URLs
import urllib.parse
# Import asyncio for more async stuff
import asyncio
# Import aiohttp for asynchronous HTTP requests
import aiohttp
# Import Pillow to manipulate images
from PIL import Image
# Import BytesIO for using URL with Pillow
from io import BytesIO
# Import base64 to parse images
import base64
# Import JSON to handle json responses
import json
# Import lxml to parse XML and HTML
from lxml import etree
# Import URLlib.error to handle error

class Saka():
  def __init__(self, bot):
    self.bot = bot

  async def updateProgressBar(self, message, percentage):
    """
    Update the progress bar message with a cute little kaomoji.
    """
    await self.bot.send_typing(message.channel)
    if message is None: return
    if percentage == 100:
      await self.bot.delete_message(message=message)
      return
    outoften = round(percentage / 10)
    await self.bot.edit_message(message=message, new_content='`' + ('__' * outoften)[:-1] + 'φ(．．)`')
    await self.bot.edit_message(message=message, new_content='`' + ('__' * outoften) + 'φ(．．)`')

  async def getTopImageResult(self, progressmsg, source: str, url: str):
    """
    Find the top image result from the specified sources.
    Sources available: saucenao (sourcenao, sourcenow), whatanime (anime), iqdb [WIP]
    """
    await self.updateProgressBar(progressmsg, 10)
    ReturnMessage = collections.namedtuple('ReturnMessage', ['new_content', 'embed'])

    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=SakanyaCore().headers) as b:
          await self.updateProgressBar(progressmsg, 20)
          # Check main mimetype
          if 'image' not in b.headers['Content-Type']:
            # Invalid (html, xml, etc)
            await self.updateProgressBar(progressmsg, 100)
            return ReturnMessage('The URL is not a valid image!', None)
          else:
            # Valid image (image/png, jpeg, gif, etc)
            c = None # Response data
            if source == 'saucenao' or source == 'sourcenao' or source == 'sourcenow':
              sourcefinder_url = 'https://saucenao.com/search.php'
              sourcefinder_params = {
                'db': 999,
                'api_key': '9517b2f1b0fe90f23c2893c386868778baff1cfe',
                'output_type': 2,
                'numres': 1,
                'url': url
              }
              c = await session.get(url=sourcefinder_url, params=sourcefinder_params, headers=SakanyaCore().headers)
            elif source == 'whatanime' or source == 'anime':
              imageBytes = await b.read()
              img = Image.open(BytesIO(imageBytes))
              img = img.convert('RGB') # Remove alpha
              buffered = BytesIO()
              img.save(buffered, format='JPEG', optimize=True, quality=85)
              base64_str = base64.b64encode(buffered.getvalue())
              sourcefinder_data = {
                'image': base64_str.decode('utf8') # make it string to put it in JSON
              }
              sourcefinder_url = 'https://whatanime.ga/api/search'
              sourcefinder_params = {
                'token': '5ea595796f30ed390813a0c6e7be4216fb1c4419'
              }
              c = await session.post(url=sourcefinder_url, params=sourcefinder_params, data=sourcefinder_data, headers=SakanyaCore().headers)
            elif source == 'iqdb':
              sourcefinder_url = 'https://iqdb.org/',
              sourcefinder_params = {
                'url': url,
                'more': 1
              }
              c = await session.get(url=sourcefinder_url, params=sourcefinder_params, headers=SakanyaCore().headers)
              # db=999 is everything | numres=1 is number of results
            else:
              # !saka <somethingelse> <url>
              return ReturnMessage('Provider not found. Available providers are Saucenao and WhatAnime.', None)

            await self.updateProgressBar(progressmsg, 40)
            async with c:
              await self.updateProgressBar(progressmsg, 50)
              if source == 'saucenao' or source == 'sourcenao' or source == 'sourcenow':
                urlresult = await c.json(encoding='utf8')
                await self.updateProgressBar(progressmsg, 60)
                topresult = urlresult['results'][0]
                description = 'Submitted image <:arrow_right:346575669477769216>\n\n**Similarity:** ' + topresult['header']['similarity'] + '%\n'
                resulturl = '' # Default value
                if ('title' in topresult['data']) and (topresult['data']['title'] == ''): topresult['data']['title'] = '<Untitled>'
                if ('source' in topresult['data']) and (topresult['data']['source'] == ''): topresult['data']['source'] = '<Untitled>'
                if 'da_id' in topresult['data']:
                  # If deviantart
                  description += '**Title:** ' + topresult['data']['title'] + '\n**Author:** ' + (topresult['data']['author_name'] if topresult['data']['author_name'] is not None else 'Unknown') + '\n**Source:** DeviantArt'
                  resulturl = 'https://deviantart.com/view/' + str(topresult['data']['da_id'])
                elif 'creator' in topresult['data'] and isinstance(topresult['data']['creator'], list):
                  # If creator is an array
                  description += '**Title:** ' + (topresult['data']['eng_name'] if topresult['data']['eng_name'] is not None else '<Untitled>') + '\n**Author:** ' + ', '.join(topresult['data']['creator'])
                elif 'pixiv_id' in topresult['data']:
                  # If pixiv
                  description += '**Title:** ' + topresult['data']['title'] + '\n**Author:** ' + (topresult['data']['member_name'] if topresult['data']['member_name'] is not None else 'Unknown') + ('#' + str(topresult['data']['member_id']) if topresult['data']['member_id'] is not None else '') + '\n**Source:** Pixiv'
                  resulturl = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + str(topresult['data']['pixiv_id'])
                elif 'anidb_aid' in topresult['data']:
                  # If aniDB anime
                  description += '**Title:** ' + topresult['data']['source'] + (' (' + topresult['data']['year'] + ')' if topresult['data']['year'] is not None else '<Unknown Year>') + '\n*Episode ' + (topresult['data']['part'] if topresult['data']['part'] is not None else 'Unknown Episode') + (' ' + topresult['data']['est_time'] if topresult['data']['est_time'] is not None else '') + '*\n**Source:** AniDB'
                  resulturl = 'https://anidb.net/perl-bin/animedb.pl?show=anime&aid=' + str(topresult['data']['anidb_aid'])
                elif 'imdb_id' in topresult['data']:
                  # Imdb show/film
                  description += '**IMDb database id:** ' + str(topresult['data']['imdb_id']) + ('\nReleased in ' + topresult['data']['year'] + '' if topresult['data']['year'] is not None else '<Unknown Year>') + '\n*' + (topresult['data']['part'] if topresult['data']['part'] is not None else 'Unknown Part') + (' ' + topresult['data']['est_time'] if topresult['data']['est_time'] is not None else '') + '*\n**Source:** IMDb'
                  resulturl = 'https://www.imdb.com/title/' + str(topresult['data']['imdb_id'])
                elif 'seiga_id' in topresult['data']:
                  # If Nico nico seiga drawing
                  description += '**Title:** ' + topresult['data']['title'] + '\n**Author:**' + (topresult['data']['member_name'] if topresult['data']['member_name'] is not None else 'Unknown') + ('#' + str(topresult['data']['member_id']) if topresult['data']['member_id'] is not None else '') + '\n**Source:** Nico Nico Seiga'
                  resulturl = 'http://seiga.nicovideo.jp/seiga/im' + str(topresult['data']['seiga_id'])  
                elif 'danbooru_id' in topresult['data']:
                  # If danbooru
                  description += '**Title:** ' + topresult['data']['source'] + '\n**Author:** ' + (topresult['data']['creator'] if topresult['data']['creator'] is not None else 'Unknown') + '\n**Source:** Danbooru'
                  resulturl = 'https://danbooru.donmai.us/post/show/' + str(topresult['data']['danbooru_id'])
                  if 'sankaku_id' in topresult['data']: description += '\n***Sankaku id:*** ' + str(topresult['data']['sankaku_id'])
                  if 'gelbooru_id' in topresult['data']: description += '\n***Gelbooru id:*** ' + str(topresult['data']['gelbooru_id'])
                elif 'sankaku_id' in topresult['data']:
                  # If sankaku
                  description += '**Title:**'  + topresult['data']['source'] + '\n**Author:** ' + (topresult['data']['creator'] if topresult['data']['creator'] is not None else 'Unknown') + '\n**Source:** Sankaku'
                  resulturl = 'https://chan.sankakucomplex.com/post/show/' + str(topresult['data']['sankaku_id'])
                if 'gelbooru_id' in topresult['data']: description += '\n***Gelbooru id:*** ' + str(topresult['data']['gelbooru_id']) 
                elif 'gelbooru_id' in topresult['data']:
                  # If gelbooru
                  description += '**Title:** ' + topresult['data']['source'] + '\n**Author:** ' + (topresult['data']['creator'] if topresult['data']['creator'] is not None else 'Unknown') + '\n**Source:** Gelbooru'
                  resulturl = 'http://gelbooru.com/index.php?page=post&s=view&id=' + str(topresult['data']['gelbooru_id'])
                elif 'bcy_id' in topresult['data']:
                  # If bcy.net
                  description += '**Title:** ' + topresult['data']['title'] + '\n**Author:** ' + (topresult['data']['member_name'] if topresult['data']['member_name'] is not None else 'Unknown') + ('#' + topresult['data']['member_id'] if topresult['data']['member_id'] is not None else '') + '\n**Source:** bcy.net'
                  resulturl = 'http://bcy.net/coser/detail/' + str(topresult['data']['member_link_id']) + '/' + str(topresult['data']['bcy_id'])
                elif 'mu_id' in topresult['data']:
                  # If MangaUpdates
                  description += '**Title:** ' + topresult['data']['part'] + '\n**Series**: ' + topresult['data']['source'] + '\n**Source:** mangaupdates.com'
                  resulturl = topresult['data']['ext_urls'][0]
                elif 'url' in topresult['data'] and 'medibang' in topresult['data']['url']:
                  # If medibang
                  description += '**Title:** ' + topresult['data']['title'] + '\n**Author:** ' + (topresult['data']['member_name'] if topresult['data']['member_name'] is not None else 'Unknown') + ('#' + topresult['data']['member_id'] if topresult['data']['member_id'] is not None else '') + '\n**Source:** Medibang'
                  resulturl = topresult['data']['url']
                await self.updateProgressBar(progressmsg, 80)
                resultembed = discord.Embed(
                  color = SakanyaCore().embed_color,
                  type = 'rich',
                  title = topresult['header']['index_name'],
                  url = resulturl,
                  description = description
                )
                resultembed.set_thumbnail(url=url)
                resultembed.set_image(url=topresult['header']['thumbnail'].replace(' ', '%20'))
                resultembed.set_footer(text=SakanyaCore().name + ' image results on Saucenao', icon_url='http://www.userlogos.org/files/logos/zoinzberg/SauceNAO.png')
                await self.updateProgressBar(progressmsg, 100)
                return ReturnMessage(
                  SakanyaCore().name + ' Image Search on Saucenao:',
                  resultembed
                )
              elif source == 'whatanime' or source == 'anime':
                urlresult = json.loads(await c.text())
                
                await self.updateProgressBar(progressmsg, 60)
                topresult = urlresult['docs'][0]
                description = 'Submitted image <:arrow_right:346575669477769216>\n\n**Similarity:** ' + str("%.2f" % round((topresult['similarity'] * 100), 2)) + '%\n'
                description += '**Title:** ' + (topresult['title'] if 'title_romaji' not in topresult else topresult['title_romaji']) + '\n'
                description += '**Other titles:** ' + ', '.join(topresult['synonyms']) + (', ' if len(topresult['synonyms']) != 0 else '') + topresult['title_english'] + '\n'
                description += '**Release:** ' + topresult['season'] + '\n'
                if topresult['episode'] != '': description += '*Episode ' + str(topresult['episode']) + '*' 
                if topresult['at'] != None: description += (', *at ' if topresult['episode'] != '' else '') + str(round(topresult['at'] / 60)) + ' minutes in.*'
                resulturl = 'https://anilist.co/anime/' + str(topresult['anilist_id'])
                await self.updateProgressBar(progressmsg, 80)
                resultembed = discord.Embed(
                  color = SakanyaCore().embed_color,
                  type = 'rich',
                  title = topresult['filename'],
                  url = resulturl,
                  description = description
                )
                resultembed.set_thumbnail(url=url)
                resultembed.set_image(url='https://whatanime.ga/thumbnail.php?season=' + topresult['season'] + '&anime=' + urllib.parse.quote_plus(topresult['anime']) + '&file=' + urllib.parse.quote_plus(topresult['filename']) + '&t=' + str(topresult['at']) + '&token=' + topresult['tokenthumb'])
                resultembed.set_footer(text=SakanyaCore().name + ' image results on Whatanime', icon_url='https://whatanime.ga/favicon128.png')
                await self.updateProgressBar(progressmsg, 100)
                return ReturnMessage(
                  SakanyaCore().name + ' Image Search on Whatanime:',
                  resultembed
                )
              elif source == 'iqdb':
                # Scrape (no API is provided)
                urlresult = await c.text()
                tree = etree.HTML(urlresult)
                await self.updateProgressBar(progressmsg, 70)
                relevant = tree.xpath('//*[@id="pages"]/div[2]')
                print(relevant)
                print(relevant[0].xpath('/table/tbody/tr[1]/th'))
                if relevant.xpath('/table/tbody/tr[1]/th') == 'No relevant matches':
                  relevant = tree.xpath('//*[@id="pages"]/div[3]')[0]
                resultimage = relevant[0].xpath('/table/tbody/tr[2]/td/a/img/@src')
                await self.updateProgressBar(progressmsg, 80)
                print(relevant)
                print(resultimage)
                await self.updateProgressBar(progressmsg, 90)
                resultembed = discord.Embed(
                  color = SakanyaCore().embed_color,
                  type = 'rich',
                  title = 'IQDb Match',
                  url = 'hi',
                  description = 'ha'
                )
                resultembed.set_thumbnail(url=url)
                resultembed.set_image(url=resultimage)
                resultembed.set_footer(text=SakanyaCore().name + ' image results on iQDB', icon_url=discord.Embed.Empty)
                await self.updateProgressBar(progressmsg, 100)
                return ReturnMessage(
                  SakanyaCore().name + ' Image Search on IQDb:',
                  resultembed
                )
    except Exception as e:
      await self.updateProgressBar(progressmsg, 100)
      return ReturnMessage('Couldn\'t access image.' + e, None)

  @commands.command(pass_context=True)
  async def saka(self, context, left: str=None, right: str=None):
    """
    General command to reverse image search.
    
    Format:
      >saka [source] [url]

    Examples:
      >saka saucenao https://i.imgur.com/WoASgyW.png
      >saka anime (attachment image)
    """
    if not context.message.attachments: # No attachments
      if left is None:
        # >saka
        await self.bot.say('Format\n`' + SakanyaCore().prefix + 'saka [source] <url>`')
        return
      elif right is None:
        # >saka <something>
        a = urllib.parse.urlparse(left)
        if bool(a.scheme) is False:
          # >saka <noturl>
          await self.bot.say('Format\n`' + SakanyaCore().prefix + 'saka [source] <url>`')
          return
        # >saka <url>
        url = left
        tmpmsg = await self.bot.say('Please wait, this might take a while... ')
        progressmsg = await self.bot.say('`φ(．．)`')
        topresult = await self.getTopImageResult(progressmsg, 'saucenao', url)
        await self.bot.send_message(context.message.channel, content=(topresult.new_content if topresult is not None else topresult), embed=(topresult.embed if topresult is not None else topresult))
        await self.bot.delete_message(tmpmsg)
      else:
        # >saka <something> <something>
        # When right is defined, left HAS to be defined, so no check
        a = urllib.parse.urlparse(right)
        if bool(a.scheme) is False:
          # !saka <noturl>
          await self.bot.say('Format\n`' + SakanyaCore().prefix + 'saka [source] <url>`')
          return
        # >saka <saucenao|whatanime> <url>
        url = right
        tmpmsg = await self.bot.say('Please wait, this might take a while...')
        progressmsg = await self.bot.say('`φ(．．)`')
        topresult = await self.getTopImageResult(progressmsg, left.lower(), url)
        await self.bot.send_message(context.message.channel, content=(topresult.new_content if topresult is not None else topresult), embed=(topresult.embed if topresult is not None else topresult))
        await self.bot.delete_message(tmpmsg)
        return
    else:
      # Attachments were found!
      # >saka
      # >saka <saucenao|whatanime>
      for attachment in context.message.attachments:
        url = attachment['url']
        tmpmsg = await self.bot.say('Please wait, this might take a while...')
        progressmsg = await self.bot.say('`φ(．．)`')
        topresult = await self.getTopImageResult(progressmsg, (left.lower() if left is not None else 'saucenao'), url)
        await self.bot.send_message(context.message.channel, content=(topresult.new_content if topresult is not None else topresult), embed=(topresult.embed if topresult is not None else topresult))
        await self.bot.delete_message(tmpmsg)

def setup(bot):
  bot.add_cog(Saka(bot))
