import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(DATABASE_URL)

engine.execute((
    'CREATE TABLE IF NOT EXISTS nulls_users ('
    'user_id bigint unique primary key not null, '
    'mal_username text, '
    'gender text, '
    'birthdate date, '
    'country text, '
    'languages text, '
    'prog_languages text, '
    'bio text, '
    'timezone text)'))
engine.execute((
    'CREATE TABLE IF NOT EXISTS nulls_projects ('
    'user_id bigint references nulls_users(user_id), '
    'project_name text, '
    'project_description text, '
    'project_link text)'))
engine.execute((
    'CREATE TABLE IF NOT EXISTS nulls_social ('
    'user_id bigint references nulls_users(user_id), '
    'social_name text, '
    'social_link text)'))


Session = sessionmaker(bind=engine)

Base = declarative_base()
