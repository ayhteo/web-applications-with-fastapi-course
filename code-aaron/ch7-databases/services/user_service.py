from data.user import User
from typing import Optional
import sqlalchemy as sa
import data.db_session as db_session

from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def create_account(name: str, email: str, password: str):
    session = db_session.create_session()
    try:
        user = User()
        user.email = email
        user.hash_password = crypto.hash(password, rounds=172_434)
        user.name = name

        session.add(user)
        session.commit()
        return user
    finally:
        session.close()


def login_user(email: str, password: str) -> Optional[User]:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return user
        if not crypto.verify(password, user.hash_password):
            return None
        return user
    finally:
        session.close()


def get_user_by_id(user_id: int) -> Optional[User]:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()  #


def get_user_by_email(user_email: str) -> Optional[User]:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.email == user_email).first()
    finally:
        session.close()
