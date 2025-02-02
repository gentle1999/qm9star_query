from sqlmodel import Session, create_engine, select

from qm9star_query.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
with engine.begin() as conn:
    conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector")
    conn.commit()


# make sure all SQLModel models are imported (qm9star_query.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from qm9star_query.core.engine import engine
    # This works because the models are already imported and registered from qm9star_query.models
    # SQLModel.metadata.create_all(engine)
    ...
