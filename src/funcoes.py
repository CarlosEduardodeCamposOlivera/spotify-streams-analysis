"""
Funções reutilizáveis do projeto de análise do dataset
Most Streamed Spotify Songs 2023 (Kaggle).
"""

import os
import pandas as pd


def carregar_dados(caminho, encoding="utf-8"):
    """
    Carrega um arquivo CSV em um DataFrame do pandas.

    Parâmetros
    ----------
    caminho : str
        Caminho até o arquivo CSV.
    encoding : str, opcional
        Codificação de caracteres do arquivo. O padrão é "utf-8",
        que é a codificação do dataset do Spotify. Observação: o arquivo
        original já contém caracteres de substituição (�) no lugar de
        algumas letras acentuadas; isso vem da fonte, não da leitura.

    Retorna
    -------
    pandas.DataFrame
        Tabela com os dados do arquivo.

    Levanta
    -------
    FileNotFoundError
        Se o arquivo não existir no caminho informado.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    df = pd.read_csv(caminho, encoding=encoding)
    print(f"Dados carregados: {df.shape[0]} linhas e {df.shape[1]} colunas.")
    return df


def selecionar_colunas(df, colunas):
    """
    Seleciona um subconjunto de colunas de um DataFrame.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    colunas : list of str
        Nomes das colunas a manter, na ordem desejada.

    Retorna
    -------
    pandas.DataFrame
        Cópia da tabela contendo apenas as colunas pedidas.

    Levanta
    -------
    KeyError
        Se alguma coluna pedida não existir no DataFrame.
    """
    faltando = [coluna for coluna in colunas if coluna not in df.columns]
    if faltando:
        raise KeyError(f"Colunas não encontradas no DataFrame: {faltando}")

    return df[colunas].copy()


def renomear_colunas(df, mapeamento):
    """
    Renomeia colunas de um DataFrame.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    mapeamento : dict
        Dicionário no formato {"nome_antigo": "nome_novo"}. Colunas que
        não aparecem no dicionário mantêm o nome.

    Retorna
    -------
    pandas.DataFrame
        Nova tabela com as colunas renomeadas.
    """
    return df.rename(columns=mapeamento)
