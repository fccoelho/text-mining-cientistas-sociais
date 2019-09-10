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
