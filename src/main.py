
from typing import Any
from flask import Flask
from sqlalchemy import create_engine
from dataclasses import dataclass
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from routes import register_routes
import os

@dataclass
class Settings:
    DATABASE_URL: str

class AppFlask(Flask):
    def __init__(self, *args, settings: Settings = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not settings:
            db_url = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5431/db")
            settings = Settings(DATABASE_URL=db_url)
        self.settings = settings
        engine = create_engine(self.settings.DATABASE_URL, future=True)
        SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        self.session = scoped_session(SessionFactory)

        Base.metadata.create_all(bind=engine)

    def teardown_appcontext(self, exc):
        try:
            self.session.remove()
        except Exception:
            pass

settings = Settings(
    DATABASE_URL=os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5431/db"),
)

app = AppFlask(__name__, settings=settings)
register_routes(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
