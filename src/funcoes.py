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


def converter_para_numerico(df, coluna):
    """
    Converte uma coluna para tipo numérico. Valores que não podem ser
    convertidos viram NaN, e a quantidade deles é informada.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    coluna : str
        Nome da coluna a converter.

    Retorna
    -------
    pandas.DataFrame
        Nova tabela com a coluna convertida.
    """
    df = df.copy()
    faltantes_antes = df[coluna].isna().sum()

    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    novos_faltantes = df[coluna].isna().sum() - faltantes_antes
    if novos_faltantes > 0:
        print(
            f"Aviso: {novos_faltantes} valor(es) de '{coluna}' não eram numéricos e viraram NaN.")

    return df


def preencher_faltantes(df, coluna, valor):
    """
    Preenche os valores faltantes de uma coluna com um valor fixo.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    coluna : str
        Nome da coluna a preencher.
    valor : qualquer tipo
        Valor usado no preenchimento.

    Retorna
    -------
    pandas.DataFrame
        Nova tabela com os faltantes da coluna preenchidos.
    """
    df = df.copy()
    quantidade = df[coluna].isna().sum()

    df[coluna] = df[coluna].fillna(valor)

    print(f"{quantidade} valor(es) faltante(s) em '{coluna}' preenchido(s) com {valor!r}.")
    return df
