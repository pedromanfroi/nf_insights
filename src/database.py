from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Compra(Base):
    __tablename__ = 'compras'

    id = Column(Integer, primary_key=True)
    data_compra = Column(DateTime)
    fornecedor = Column(String)
    item = Column(String)
    quantidade_comprada = Column(Float)

def get_engine():
    return create_engine('sqlite:///data/compras.db')

def create_tables(engine):
    Base.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()