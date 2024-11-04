from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import CONFIG


class DataBase:

    def __init__(self):
        self._engine = None
        self._url = URL.create(
            drivername=CONFIG.database.driver,
            database=CONFIG.database.database,
            username=CONFIG.database.username,
            password=CONFIG.database.password,
            host=CONFIG.database.host,
            port=CONFIG.database.port,
        )
        self._create_session = sessionmaker(
            bind=self.engine,
            class_=Session,
            expire_on_commit=False,
        )

    @property
    def engine(self):
        if not self._engine:
            self._engine = create_engine(
                self._url,
                echo=CONFIG.database.echo,
            )
        return self._engine

    def session(self):
        return self._create_session()


DATABASE = DataBase()
