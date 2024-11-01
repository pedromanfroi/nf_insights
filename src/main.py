import os
from datetime import datetime
from xml_parser import parse_nfe_xml
from database import (
    create_tables, get_session, importar_ncm_json,
    Compra, NCM, get_engine
)

def main():
    # Criar as tabelas no banco de dados
    engine = get_engine()
    create_tables(engine)
    session = get_session()

    # Importar o JSON de NCMs
    json_file_path = os.path.join('data', 'ncm.json')  # Ajuste o caminho conforme necessário
    importar_ncm_json(json_file_path, engine)

    # Diretório com os arquivos XML
    xml_directory = os.path.join('data', 'exemplos_nfe')

    # Processar cada arquivo XML
    for filename in os.listdir(xml_directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(xml_directory, filename)
            items = parse_nfe_xml(file_path)

            # Inserir dados no banco
            for item_data in items:
                ncm_codigo = item_data['ncm']
                ncm_descricao = None
                if ncm_codigo:
                    # Remover pontos e traços do código NCM extraído do XML
                    ncm_codigo_sem_pontos = ncm_codigo.replace('.', '').replace('-', '').strip()
                    # Buscar a descrição usando o código sem pontos
                    ncm_obj = session.query(NCM).filter_by(codigo=ncm_codigo_sem_pontos).first()
                    if ncm_obj:
                        ncm_descricao = ncm_obj.descricao
                    else:
                        print(f"Descrição não encontrada para NCM: {ncm_codigo}")

                compra = Compra(
                    data_compra=item_data['data_compra'],
                    fornecedor=item_data['fornecedor'],
                    item=item_data['item'],
                    quantidade_comprada=float(item_data['quantidade_comprada']),
                    unidade=item_data['unidade'],
                    ncm=ncm_codigo,
                    valor_unitario=float(item_data['valor_unitario']) if item_data['valor_unitario'] else None,
                    descricao_ncm=ncm_descricao
                )
                session.add(compra)

    # Salvar e fechar a sessão
    session.commit()
    session.close()

if __name__ == '__main__':
    main()