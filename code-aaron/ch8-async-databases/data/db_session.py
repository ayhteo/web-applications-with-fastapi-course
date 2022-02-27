import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from typing import Optional, Callable
from pathlib import Path
from data.modelbase import SqlAlchemyBase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio.engine import create_async_engine

__factory: Optional[Callable[[], Session]] = None

__async_engine: Optional[AsyncEngine] = None

# other databases have their own way of writing a connection
# SQLLite only requires a connection string
def global_init(db_file: str):
    global __factory, __async_engine

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    folder = Path(db_file).parent
    folder.mkdir(parents=True, exist_ok=True)

    conn_str = "sqlite:///" + db_file.strip()
    # conn_str = "sqlite+aiosqlite:///:memory:" + db_file.strip()
    print(f"Connecting to DB with {conn_str}.")

    # Adding check_same_thread = False after the recording. This can be an issue about
    # creating / owner thread when cleaning up sessions, etc. This is a sqlite restriction
    # that we probably don't care about in this example.

    engine = sa.create_engine(
        conn_str, echo=False, connect_args={"check_same_thread": False}
    )

    __async_engine = create_async_engine(
        conn_str, echo=False, connect_args={"check_same_thread": False}
    )

    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False
    return session


def create_async_session() -> AsyncSession:
    global __async_engine

    if not __async_engine:
        raise Exception("You must call global_init() before using this method.")

    session: AsyncSession = AsyncSession(__async_engine)
    session.sync_session.expire_on_commit = False

    return session
