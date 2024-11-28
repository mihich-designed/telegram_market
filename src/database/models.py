from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
db_path = os.getenv('DB_LOCAL_PATH')
engine = create_engine(f'sqlite:///{db_path}')
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    cart_id = Column(String, nullable=True)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(String)
    image_id = Column(String)

Base.metadata.create_all(engine)

# # Определение структуры таблицы accounts
# users_table = Table('users', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('user_id', String),
#     Column('cart_id', String, nullable=True)
# )
#
# # Определение структуры таблицы items
# products_table = Table('products', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String),
#     Column('description', String),
#     Column('price', String),
#     Column('image_id', String)
# )

# metadata.create_all(engine)




