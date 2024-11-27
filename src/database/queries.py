from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('DB_LOCAL_PATH')
engine = create_engine(f'sqlite:///{db_path}')
metadata = MetaData()

# Определение структуры таблицы accounts
accounts_table = Table('accounts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('cart_id', String)
)

# Определение структуры таблицы items
items_table = Table('items', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String),
    Column('description', String),
    Column('price', String),
    Column('image', String)
)

metadata.create_all(engine)






