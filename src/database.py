from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import json

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
    descricao_ncm = Column(String)  # Nova coluna
    
class NCM(Base):
    __tablename__ = 'ncm'

    codigo = Column(String, primary_key=True)
    descricao = Column(String)

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

def importar_ncm_json(json_file_path, engine):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        ncm_data = json.load(file)

    Session = sessionmaker(bind=engine)
    session = Session()

    for ncm_entry in ncm_data:
        ncm = NCM(
            codigo=ncm_entry['codigo'],
            descricao=ncm_entry['descricao']
        )
        session.merge(ncm)  # Usa merge para evitar duplicatas

    session.commit()
    session.close()