from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = 'postgresql://neondb_owner:npg_0S2zoWuOBswD@ep-polished-dew-arq4509h.c-4.us-west-2.aws.neon.tech/TodoApplicationDatabase?sslmode=require&channel_binding=require'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
#     'check_same_thread': False
# })

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()