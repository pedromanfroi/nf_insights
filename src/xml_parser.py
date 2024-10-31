from lxml import etree

def parse_nfe_xml(file_path):
    namespaces = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Extrair data da compra
    data_compra = root.find('.//ns:ide/ns:dhEmi', namespaces)
    if data_compra is not None:
        data_compra = data_compra.text

    # Extrair fornecedor
    fornecedor = root.find('.//ns:emit/ns:xNome', namespaces)
    if fornecedor is not None:
        fornecedor = fornecedor.text

    items = []
    # Extrair itens
    for det in root.findall('.//ns:det', namespaces):
        produto = det.find('.//ns:prod/ns:xProd', namespaces)
        quantidade = det.find('.//ns:prod/ns:qCom', namespaces)

        if produto is not None and quantidade is not None:
            item = {
                'data_compra': data_compra,
                'fornecedor': fornecedor,
                'item': produto.text,
                'quantidade_comprada': quantidade.text
            }
            items.append(item)

    return items