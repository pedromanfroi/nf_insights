from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Compra(Base):
    __tablename__ = 'compras'

    id = Column(Integer, primary_key=True)
    data_compra = Column(String)
    fornecedor = Column(String)
    item = Column(String)
    quantidade_comprada = Column(Float)
    unidade = Column(String)  # Nova coluna 'unidade'
    ncm = Column(String)
    valor_unitario = Column(Float)

def get_engine():
    return create_engine('sqlite:///data/compras.db')

def create_tables(engine=None):
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()