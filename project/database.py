from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

database_url="mysql+pymysql://sampleproject:sampleproject123@127.0.0.1/sample_project" 
engine = create_engine(database_url)
Sessionlocal = sessionmaker(bind=engine, autocommit=False,autoflush=False)
Base = declarative_base()
