from typing import List, Optional
from data.package import Package
from data.release import Release
from data.user import User
import datetime
import data.db_session as db_session
import sqlalchemy.orm as orm
from sqlalchemy.future import select
from sqlalchemy import func


async def release_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Release.id))
        results = await session.execute(query)
        return results.scalar()


async def package_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(Package.id))
        result = await session.execute(query)
        return result.scalar()


async def user_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(User.email))  # prepare the query with a function call
        result = await session.execute(query)  # now we talk to the database
        return result.scalar()


async def latest_packages(limit: int = 5) -> List:
    async with db_session.create_async_session() as session:
        query = (
            select(Release)
            .options(orm.joinedload(Release.package))
            .order_by(Release.created_date.desc())
            .limit(limit)
        )
        results = await session.execute(query)
        latest_releases = results.scalars()
        return list({r.package for r in latest_releases})


async def get_package_by_id(package_name: str) -> Optional[Package]:
    async with db_session.create_async_session() as session:
        query = select(Package).filter(Package.id == package_name)
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def get_latest_release_for_package(package_name: str) -> Optional[Release]:
    async with db_session.create_async_session() as session:
        query = (
            select(Release)
            .filter(Release.package_id == package_name)
            .order_by(Release.created_date.desc())
        )
        result = await session.execute(query)
        return result.scalar()
