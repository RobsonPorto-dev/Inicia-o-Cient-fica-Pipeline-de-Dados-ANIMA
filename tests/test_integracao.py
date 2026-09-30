"""
Validações da tabela curated municipios_populacao_internet.
Rode com: pytest tests/ -v
"""
import re
import sys
import os
import pandas as pd
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data", "src", "transform"))
from integrar_ibge import integrar  # noqa: E402

UFS_VALIDAS = {
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",
    "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO",
}


@pytest.fixture(scope="module")
def tabela():
    return integrar()


def test_codigo_ibge_tem_sete_digitos(tabela):
    assert (tabela["cod_municipio"].str.len() == 7).all()
    assert tabela["cod_municipio"].str.isnumeric().all()


def test_uf_pertence_ao_conjunto_das_27(tabela):
    ufs_encontradas = set(tabela["uf_sigla"].unique())
    assert ufs_encontradas.issubset(UFS_VALIDAS), ufs_encontradas - UFS_VALIDAS


def test_percentual_entre_0_e_100(tabela):
    assert tabela["pct_internet_total"].between(0, 100).all()
    assert tabela["pct_internet_60mais"].between(0, 100).all()


def test_chave_nao_se_repete(tabela):
    assert tabela["cod_municipio"].is_unique


def test_nenhum_municipio_ausente_da_referencia(tabela):
    # nenhum município deve ficar sem UF correspondente após o join
    assert tabela["pct_internet_total"].notna().all()


def test_populacao_e_positiva(tabela):
    assert (tabela["populacao_2022"] > 0).all()


# --- Validação deliberadamente quebrada, para provar que a checagem funciona ---
def test_validacao_pega_percentual_invalido_de_proposito():
    tabela_corrompida = pd.DataFrame({
        "cod_municipio": ["1100015"],
        "pct_internet_total": [150.0],  # valor impossível, injetado de propósito
    })
    with pytest.raises(AssertionError):
        assert tabela_corrompida["pct_internet_total"].between(0, 100).all()
