from .models import Cart, Product
from .db_session import get_session

def add_user(user_id):
    '''
    Проверяет существование пользователя в БД
    и добавляет его id в таблицу users, если такого id еще нет
    '''
    with get_session() as session:
        try:
            user_exists = session.query(Cart).filter(Cart.user_id == user_id).first()
            if not user_exists:
                new_user = Cart(user_id=user_id)
                session.add(new_user)
                session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении пользователя: {e}")

def add_product(name, desc, price, image):
    '''Добавление товаров в БД'''
    with get_session() as session:
        try:
            new_product = Product(
                name=name,
                description=desc,
                price=price,
                image_id=image,
            )
            session.add(new_product)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Ошибка при добавлении товара: {e}")






