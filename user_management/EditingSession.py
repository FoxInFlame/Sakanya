from sqlalchemy import Column, BigInteger, DateTime
from postgre_session import Base, engine

class EditingSession(Base):

  __tablename__ = 'editing_sessions'

  user_id = Column(BigInteger, unique=True, primary_key=True, nullable=False)
  since = Column(DateTime(timezone=True))

  def __init__(self, user_id, since):
    self.user_id = user_id
    self.since = since

Base.metadata.create_all(engine)
