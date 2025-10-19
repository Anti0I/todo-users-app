from typing import Any
from flask import Flask
from sqlalchemy import create_engine
from dataclasses import dataclass
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from routes import register_routes


@dataclass
class Settings:
    DATABASE_URL: str


class AppFlask(Flask):
    def __init__(self, *args, settings: Settings = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._settings = settings
        self._session = None

    def run(
        self,
        host: str | None = None,
        port: int | None = None,
        debug: bool | None = None,
        load_dotenv: bool = True,
        **options: Any,
    ) -> None:
        engine = create_engine(self._settings.DATABASE_URL)
        self._session = scoped_session(sessionmaker(engine))
        Base.metadata.create_all(engine)
        Base.query = self._session.query_property()
        super().run(
            host=host,
            port=port,
            debug=debug,
            load_dotenv=load_dotenv,
            **options,
        )


settings = Settings(
    DATABASE_URL="postgresql://admin:admin@localhost:5431/db",
)

app = AppFlask(__name__, settings=settings)
register_routes(app)

if __name__ == '__main__':
    app.run()