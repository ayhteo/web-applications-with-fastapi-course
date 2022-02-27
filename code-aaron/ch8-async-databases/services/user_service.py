from data.user import User
from typing import Optional
import sqlalchemy as sa
import data.db_session as db_session
from sqlalchemy.future import select

from passlib.handlers.sha2_crypt import sha512_crypt as crypto


async def create_account(name: str, email: str, password: str):
    user = User()
    user.email = email
    user.hash_password = crypto.hash(password, rounds=172_434)
    user.name = name

    async with db_session.create_async_session() as session:
        session.add(user)
        await session.commit()
    return user


async def login_user(email: str, password: str) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == email)
        results = await session.execute(query)
        user = results.scalar_one_or_none()
        if not user:
            return user
        if not crypto.verify(password, user.hash_password):
            return None
        return user


async def get_user_by_id(user_id: int) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_by_email(user_email: str) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == user_email)
        result = await session.execute(query)
        return result.scalar_one_or_none()
