
import re
import pandas as pd

CAMINHO_7334 = "data/raw/ibge_internet_por_idade_tabela7334_2026-09-19.xlsx"
CAMINHO_9514 = "data/raw/tabela9514.xlsx"
SAIDA = "data/curated/municipios_populacao_internet.parquet"


def carregar_uf_internet(caminho: str) -> pd.DataFrame:
    df = pd.read_excel(caminho, sheet_name="Tabela", header=None)
    uf = df[df[0] == "UF"].copy()
    uf.columns = ["nivel", "cod_uf", "nome_uf", "pct_internet_total", "pct_internet_60mais", "_blank", "_ghost"]
    uf["cod_uf"] = uf["cod_uf"].astype(str).str.zfill(2)
    return uf[["cod_uf", "nome_uf", "pct_internet_total", "pct_internet_60mais"]].reset_index(drop=True)


def carregar_municipios_populacao(caminho: str) -> pd.DataFrame:
    df = pd.read_excel(caminho, sheet_name="Total; População residente", header=None)
    mu = df[(df[0] == "MU") & (df[3] == "Total")].copy()
    mu = mu.iloc[:, :5]
    mu.columns = ["nivel", "cod_municipio", "nome_raw", "sexo", "populacao_2022"]
    mu = mu[["cod_municipio", "nome_raw", "populacao_2022"]].reset_index(drop=True)
    mu["cod_municipio"] = mu["cod_municipio"].astype(str).str.zfill(7)
    mu["uf_sigla"] = mu["nome_raw"].str.extract(r"\((\w{2})\)\s*$")
    mu["nome_municipio"] = mu["nome_raw"].str.replace(r"\s*\(\w{2}\)\s*$", "", regex=True)
    mu["cod_uf"] = mu["cod_municipio"].str[:2]
    mu["populacao_2022"] = pd.to_numeric(mu["populacao_2022"], errors="coerce")
    return mu.drop(columns=["nome_raw"])


def integrar() -> pd.DataFrame:
    uf = carregar_uf_internet(CAMINHO_7334)
    mu = carregar_municipios_populacao(CAMINHO_9514)

    final = mu.merge(uf, on="cod_uf", how="left", indicator=True)

    nao_casou = final[final["_merge"] != "both"]
    if len(nao_casou):
        print(f"AVISO: {len(nao_casou)} municípios não casaram com nenhuma UF da 7334:")
        print(nao_casou[["cod_municipio", "nome_municipio", "cod_uf"]])

    final = final.drop(columns=["_merge"])
    final = final[[
        "cod_municipio", "nome_municipio", "uf_sigla", "cod_uf",
        "populacao_2022", "pct_internet_total", "pct_internet_60mais",
    ]]
    return final


if __name__ == "__main__":
    tabela = integrar()
    tabela.to_parquet(SAIDA, index=False)
    print(f"\n{len(tabela)} municípios salvos em {SAIDA}")
    print(tabela.head())
