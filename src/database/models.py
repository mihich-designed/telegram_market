from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.orm import relationship, configure_mappers

load_dotenv()

Base = declarative_base()
db_path = os.getenv('DB_LOCAL_PATH')
engine = create_engine(f'sqlite:///{db_path}')
class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    cart_id = Column(String, nullable=True)
    items = relationship("CartItem", back_populates="cart") # Связь many-to-many через CartItem
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(String)
    image_id = Column(String)
    cart_items = relationship("CartItem", back_populates="product") # Связь many-to-many через CartItem

class CartItem(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)  # Количество товара в корзине

    # Обратные связи
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")

# configure_mappers()
Base.metadata.create_all(engine)





