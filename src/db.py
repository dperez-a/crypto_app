import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base  # importa la metadata de todos tus modelos

# URI: usa sqlite en el folder data
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'portfolio.db')
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

SessionLocal = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)

def init_db():
    """
    Crea las tablas en la base de datos si no existen.
    """
    # Asegura que la carpeta data exista
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    Base.metadata.create_all(bind=ENGINE)