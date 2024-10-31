import os
from datetime import datetime
from xml_parser import parse_nfe_xml
from database import create_tables, get_session, Compra

def main():
    # Criar as tabelas no banco de dados
    create_tables(None)
    session = get_session()

    # Diretório com os arquivos XML
    xml_directory = os.path.join('data', 'exemplos_nfe')

    # Processar cada arquivo XML
    for filename in os.listdir(xml_directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(xml_directory, filename)
            items = parse_nfe_xml(file_path)

            # Inserir dados no banco
            for item_data in items:
                compra = Compra(
                    data_compra=datetime.fromisoformat(item_data['data_compra']),
                    fornecedor=item_data['fornecedor'],
                    item=item_data['item'],
                    quantidade_comprada=float(item_data['quantidade_comprada'])
                )
                session.add(compra)

    # Salvar e fechar a sessão
    session.commit()
    session.close()

if __name__ == '__main__':
    main()