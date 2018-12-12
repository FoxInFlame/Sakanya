from sqlalchemy import Column, String, BigInteger, Date
from postgre_session import Base

class User(Base):

  __tablename__ = 'nulls_users'

  user_id = Column(BigInteger, unique=True, primary_key=True, nullable=False)
  mal_username = Column(String)
  gender = Column(String)
  birthdate = Column(Date)
  country = Column(String)
  languages = Column(String)
  prog_languages = Column(String)
  bio = Column(String)
  timezone = Column(String)

  def __init__(self, user_id, mal_username, gender, birthdate, country, languages, prog_languages, bio, timezone):
    self.user_id = user_id
    self.mal_username = mal_username
    self.gender = gender
    self.birthdate = birthdate
    self.country = country
    self.languages = languages
    self.prog_languages = prog_languages
    self.bio = bio
    self.timezone = timezone
