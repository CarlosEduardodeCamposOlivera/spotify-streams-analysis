"""
Funções reutilizáveis do projeto de análise do dataset
Most Streamed Spotify Songs 2023 (Kaggle).
"""

import os
import pandas as pd
import numpy as np


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


def marcar_como_faltante(df, coluna, condicao, motivo=""):
    """
    Substitui por NaN os valores de uma coluna nas linhas que atendem a uma
    condição. Usado para invalidar valores identificados como erros.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    coluna : str
        Coluna cujos valores serão invalidados.
    condicao : pandas.Series de bool
        Série com True nas linhas a invalidar (mesmo índice de df).
    motivo : str, opcional
        Justificativa exibida na mensagem.

    Retorna
    -------
    pandas.DataFrame
        Nova tabela com os valores invalidados.
    """
    df = df.copy()
    quantidade = condicao.sum()

    df.loc[condicao, coluna] = np.nan

    print(f"{quantidade} valor(es) de '{coluna}' marcado(s) como faltante(s). {motivo}")
    return df


def remover_duplicatas(df, chave, coluna_criterio):
    """
    Remove linhas duplicadas segundo uma chave, mantendo em cada grupo
    a linha com o maior valor de uma coluna de critério.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    chave : list of str
        Colunas que definem uma duplicata (ex.: nome da música e artista).
    coluna_criterio : str
        Coluna usada para escolher a linha mantida (fica a de maior valor).

    Retorna
    -------
    pandas.DataFrame
        Nova tabela sem duplicatas, na ordem original das linhas.
    """
    linhas_antes = len(df)

    df = (
        df.sort_values(coluna_criterio, ascending=False, kind="stable")
          .drop_duplicates(subset=chave, keep="first")
          .sort_index()
    )

    removidas = linhas_antes - len(df)
    print(f"{removidas} linha(s) duplicada(s) removida(s) (mantida a de maior '{coluna_criterio}').")
    return df


def criar_coluna_data(df, col_ano, col_mes, col_dia, nome_nova="data_lancamento"):
    """
    Cria uma coluna de data (datetime) a partir de colunas separadas de
    ano, mês e dia. Combinações inválidas ou incompletas viram NaT.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    col_ano, col_mes, col_dia : str
        Nomes das colunas de ano, mês e dia.
    nome_nova : str, opcional
        Nome da nova coluna. Padrão: "data_lancamento".

    Retorna
    -------
    pandas.DataFrame
        Nova tabela com a coluna de data adicionada.
    """
    df = df.copy()

    partes = df[[col_ano, col_mes, col_dia]].rename(columns={
        col_ano: "year",
        col_mes: "month",
        col_dia: "day",
    })
    df[nome_nova] = pd.to_datetime(partes, errors="coerce")

    invalidas = df[nome_nova].isna().sum()
    if invalidas > 0:
        print(
            f"Aviso: {invalidas} data(s) não puderam ser montadas e ficaram como NaT.")

    return df


def corrigir_valores(df, coluna, condicao, novo_valor, motivo=""):
    """
    Substitui os valores de uma coluna, nas linhas que atendem a uma
    condição, por um valor correto verificado em fonte externa.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela original.
    coluna : str
        Coluna cujos valores serão corrigidos.
    condicao : pandas.Series de bool
        Série com True nas linhas a corrigir (mesmo índice de df).
    novo_valor : qualquer tipo
        Valor correto.
    motivo : str, opcional
        Justificativa e fonte, exibidas na mensagem.

    Retorna
    -------
    pandas.DataFrame
        Nova tabela com os valores corrigidos.
    """
    df = df.copy()
    quantidade = condicao.sum()

    df.loc[condicao, coluna] = novo_valor

    print(f"{quantidade} valor(es) de '{coluna}' corrigido(s) para {novo_valor!r}. {motivo}")
    return df


# ---------------------------------------------------------------------
# Específicas para o dataset Spotify 2023:
# ---------------------------------------------------------------------
COLUNAS_SPOTIFY = [
    "track_name", "artist(s)_name", "artist_count",
    "released_year", "released_month", "released_day",
    "streams", "in_spotify_playlists", "in_spotify_charts",
    "bpm", "key", "mode",
    "danceability_%", "valence_%", "energy_%", "acousticness_%",
    "instrumentalness_%", "liveness_%", "speechiness_%",
]

NOVOS_NOMES = {
    "artist(s)_name": "artist_name",
    "danceability_%": "danceability",
    "valence_%": "valence",
    "energy_%": "energy",
    "acousticness_%": "acousticness",
    "instrumentalness_%": "instrumentalness",
    "liveness_%": "liveness",
    "speechiness_%": "speechiness",
}


def limpar_dados(df_bruto):
    """
    Aplica todas as etapas de limpeza do dataset Spotify 2023, na ordem
    definida no notebook 02 (ver diagnóstico do notebook 01).

    Parâmetros
    ----------
    df_bruto : pandas.DataFrame
        Dataset original, como carregado do CSV.

    Retorna
    -------
    pandas.DataFrame
        Dataset limpo, com as colunas `data_lancamento` (datetime) e
        `data_suspeita` (bool) adicionadas.
    """
    # Etapas 1 e 2: seleção e renomeação
    df = selecionar_colunas(df_bruto, COLUNAS_SPOTIFY)
    df = renomear_colunas(df, NOVOS_NOMES)

    # Etapa 3: streams numérico e valor com erro de coleta
    df = converter_para_numerico(df, "streams")
    erro_streams = (
        (df["track_name"] == "Que Vuelvas")
        & (df["artist_name"] == "Carin Leon, Grupo Frontera")
    )
    df = marcar_como_faltante(df, "streams", erro_streams,
                              motivo="Erro de coleta (Que Vuelvas).")

    # Etapa 4: faltantes de key correspondem à nota C
    df = preencher_faltantes(df, "key", "C")

    # Etapa 5: duplicatas
    df = remover_duplicatas(
        df, ["track_name", "artist_name"], "in_spotify_playlists")

    # Etapa 6: datas
    ano_errado = (
        df["track_name"].str.startswith("Agudo")
        & df["artist_name"].str.contains("Styrx", regex=False)
    )

    fonte = "Fonte: página da faixa no Spotify."

    df = corrigir_valores(df, "released_year", ano_errado, 2022, motivo=fonte)
    df = corrigir_valores(df, "released_month", ano_errado, 10, motivo=fonte)
    df = corrigir_valores(df, "released_day", ano_errado, 9, motivo=fonte)

    df = criar_coluna_data(df, "released_year",
                           "released_month", "released_day")
    df["data_suspeita"] = (df["released_month"] == 1) & (
        df["released_day"] == 1)

    return df


def salvar_dados(df, caminho):
    """
    Salva um DataFrame em CSV, preservando o índice original como a
    coluna `id_original`.

    Parâmetros
    ----------
    df : pandas.DataFrame
        Tabela a salvar.
    caminho : str
        Caminho do arquivo de saída.

    Retorna
    -------
    None
    """
    df.reset_index(names="id_original").to_csv(caminho, index=False)
    print(
        f"Dados salvos em {caminho}: {df.shape[0]} linhas e {df.shape[1]} colunas.")
