import os, glob
import pandas as pd


def tabula_verbete(arquivos, n=None):
    """
    Carrega todos os verbetes disponíveis, ou os primeiros n.
    arquivos: lista de arquivos de verbetes
    n:  número de verbetes a tabular
    """
    if n is None:
        n = len(arquivos)
    linhas = []
    for a in arquivos[:n]:
        with open(a, 'r') as f:
            verbete = f.read()
        cabeçalho = verbete.split('---')[1]
        campos = {l.split(':')[0].strip(): l.split(':')[1].strip() for l in cabeçalho.split('\n')[:4] if l}
        campos['arquivo'] = os.path.split(a)[1]
        if 'cargos' in cabeçalho:
            campos['cargos'] = cabeçalho.split('cargos:')[1]
        else:
            campos['cargos'] = pd.np.nan
        campos['corpo'] = verbete.split('---')[2]
        linhas.append(campos)
    tabela = pd.DataFrame(data=linhas, columns=['arquivo', 'title', 'natureza', 'sexo', 'cargos', 'corpo'])
    return tabela

def parse_progenitores(linha):
    '''
    A partir de uma linha do DHBB contendo nomes de pai e mãe, extrai os nomes e os retorna
    '''
    right = linha.right[1:]
    try:
        pos_virg = right.index(',')
    except ValueError:
        pos_virg = 100
    try:
        pos_pt = right.index('.')
    except ValueError:
        pos_pt = 100
    fim = min(pos_virg, pos_pt)
    pais = right[:fim]
    if 'e' in pais:
        pai = " ".join(pais[:pais.index('e')])
        mae = " ".join([p for p in pais[pais.index('e'):] if p not in [',', 'de', 'e']])
    else:
        pai = " ".join(pais)
        mae = "desconhecida."
    return pai, mae

def encontra_pais(tc):
    linhas = tc.concordance_list('filho',width=180, lines=50000) + tc.concordance_list('filha',width=180, lines=50000)
    print("Processando {} linhas".format(len(linhas)))
    i = 0
    progenitores = []
    for linha in linhas:
        if linha.right[0] not in ['de', 'da', 'do']:
            continue
        pai, mae = parse_progenitores(linha)
        i += 1
        progenitores.append((pai, mae))
    #print("Encontramos progenitores em {} linhas".format(i))
    return progenitores