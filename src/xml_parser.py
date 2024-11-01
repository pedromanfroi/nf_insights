from lxml import etree
from datetime import datetime

def parse_nfe_xml(file_path):
    namespaces = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Extrair data da compra
    data_compra_elem = root.find('.//ns:ide/ns:dhEmi', namespaces)
    if data_compra_elem is not None:
        data_compra_iso = data_compra_elem.text
        # Converter para objeto datetime
        data_compra_dt = datetime.fromisoformat(data_compra_iso)
        # Formatar para DD/MM/YYYY
        data_compra = data_compra_dt.strftime('%d/%m/%Y')
    else:
        data_compra = None

    # Extrair fornecedor
    fornecedor_elem = root.find('.//ns:emit/ns:xNome', namespaces)
    fornecedor = fornecedor_elem.text if fornecedor_elem is not None else None

    items = []
    # Extrair itens
    for det in root.findall('.//ns:det', namespaces):
        produto_elem = det.find('.//ns:prod/ns:xProd', namespaces)
        quantidade_elem = det.find('.//ns:prod/ns:qCom', namespaces)
        unidade_elem = det.find('.//ns:prod/ns:uCom', namespaces)  # Nova linha para extrair 'unidade'
        ncm_elem = det.find('.//ns:prod/ns:NCM', namespaces)
        valor_unitario_elem = det.find('.//ns:prod/ns:vUnCom', namespaces)

        if produto_elem is not None and quantidade_elem is not None:
            item = {
                'data_compra': data_compra,
                'fornecedor': fornecedor,
                'item': produto_elem.text,
                'quantidade_comprada': quantidade_elem.text,
                'unidade': unidade_elem.text if unidade_elem is not None else None,  # Adiciona 'unidade' ao item
                'ncm': ncm_elem.text if ncm_elem is not None else None,
                'valor_unitario': valor_unitario_elem.text if valor_unitario_elem is not None else None
            }
            items.append(item)

    return items