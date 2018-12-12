from datetime import datetime, date
import pytz
import aiohttp
import discord
from discord.ext import commands
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from postgre_session import Base, engine, Session
from .User import User
from .EditingSession import EditingSession
from core import SakanyaCore

import sys

session = Session() # Extract session

class UserCommand():
  """
  This class provides functions for the commands `>user setup` and `>user update`.
  """

  def __init__(self, bot):
    self.bot = bot

  def get_all_user_fields(self, id):
    try:
      result_user = session.query(User).filter(User.user_id == id).first()
    except NoResultFound:
      return False
    return result_user

  def calculate_age(self, born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

  def get_name(self, author):
    return author.display_name

  def get_user_title(self, author, user_profile):
    if self.get_name(author) == user_profile.mal_username:
      return user_profile.mal_username
    return self.get_name(author) + ' - ' + user_profile.mal_username

  def render_description_text(self, author, user_profile):
    """
    Compile a string of information from the User class passed in the parameter.
    This will be used in discord.Embed(description) directly.
    """
    text = ''
    if user_profile.gender is not None:
      text += f'**Gender**: {user_profile.gender} \n'
    if user_profile.birthdate is not None:
      text += f'**Age**: {self.calculate_age(user_profile.birthdate)} \n'
    if user_profile.country is not None:
      text += f'**Country**: {user_profile.country} \n'
    if user_profile.timezone is not None:
      tz = pytz.timezone(user_profile.timezone)
      try:
        local_time = datetime.now(tz).strftime('%c')
      except ValueError:
        local_time = '*Invalid timezone provided*'
      text += f'**Local time**: {local_time} ({user_profile.timezone}) \n'
    if user_profile.languages:
      text += f'**Spoken languages**: {user_profile.languages} \n'
    if user_profile.prog_languages:
      text += f'**Programming languages**: {user_profile.prog_languages} \n'
    if user_profile.bio:
      text += f'**About {self.get_name(author)}**: {user_profile.bio} \n'

    return text


  async def send_update_message(self, author):
    """
    Creates and sends the update message dialogue, featuring three individual messages.
    This is only sent if the profile already exists.
    """
    user_profile = self.get_all_user_fields(author.id)

    # If for some reason the user profile was not present there
    if user_profile is None:
      return False

    description = self.render_description_text(author, user_profile)
    user_embed = discord.Embed(
        color=SakanyaCore().embed_color,
        type='rich',
        title=self.get_user_title(author, user_profile),
        url=(
            f'https://myanimelist.net/profile/{user_profile.mal_username}'
            if user_profile.mal_username is not None else None
        ),
        description=description
    )

    # Add image if it exists
    async with aiohttp.ClientSession() as client_session:
      async with client_session.get(
          f'https://api.jikan.moe/v3/user/{user_profile.mal_username}',
          headers=SakanyaCore().headers
      ) as b:
        c = await b.json(encoding='utf8')
        user_embed.set_thumbnail(url=c['image_url'])

        await self.bot.send_message(author, 'Here\'s a preview of how your profile looks!')
        await self.bot.send_message(author, embed=user_embed)
        await self.bot.send_message(author, (
            'You can edit any of the following fields (just type its name, or `done` to stop '
            'updating your profile): \n'
            '`mal_name`, `gender`, `birthdate`, `country`, `languages`, `prog_languages`, '
            '`bio`, `timezone` and `projects`'
        ))
  
  def check_dm(self, message):
    return message.channel.type == discord.ChannelType.private
  
  async def send_first_message(self, author):
    await self.bot.send_message(author, (
        'Hi there! I\'m going to assist you on building your profile at Nulls! \n'
        'Let\'s start with the most important question: What is your MAL username?'
    ))
    mal_username = await self.bot.wait_for_message(timeout=30, author=author, check=self.check_dm)
    if mal_username is None:
      await self.bot.send_message(author, (
          f'*Dear diary, today I was completely ignored by {self.get_name(author)}. Sob...*\n'
          '[This means the command has timed out, you need to start again to continue]'
      ))
      return
    try:
      new_user = User(author.id, mal_username.content, None, None, None, None, None, None, None)
      session.add(new_user)
      session.commit()
    except Exception as e:
      print(e)


  async def initiate_user_setup(self, author, does_exist):
    # Add a session, if it exists update it
    try:
      editing_session = EditingSession(author.id, func.now())
      session.add(editing_session)
      session.commit()
    except IntegrityError:
      session.rollback()
      editing_session = session.query(EditingSession).filter(
          EditingSession.user_id == author.id
      ).first()
      editing_session.since = func.now()
      session.commit()

    if does_exist:
      await self.send_update_message(author)
    else:
      await self.send_first_message(author)

  @commands.group(pass_context=True)
  async def user(self, context):
    """
    Show the usages for >user
    """
    if context.invoked_subcommand is None:
      await self.bot.say('Try `>user setup` or `>user update`!')

  @user.command(pass_context=True)
  async def setup(self, context):
    """
    Sets up profile in a DM session.
    """
    does_exist = session.query(
        sqlalchemy.exists().where(User.user_id == context.message.author.id)
    ).scalar()

    if not does_exist:
      print('no result')
  
    print('oho')

    await self.initiate_user_setup(context.message.author, does_exist)

    if context.message.server is not None:
      await self.bot.say(context.message.author.mention + ' I\'ve sent you a DM!')

def setup(bot):
  bot.add_cog(UserCommand(bot))
