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
