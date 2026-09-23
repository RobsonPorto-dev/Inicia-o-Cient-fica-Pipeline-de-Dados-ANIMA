import time, os
import pandas as pd

COLUNA_CODIGO = 1  

df = pd.read_excel("data/raw/ibge_internet_por_idade_tabela7334_2026-09-19.xlsx", sheet_name="Tabela", header=None)

df = df.drop(columns=[5, 6], errors="ignore")                    # coluna 5 vazia + coluna fantasma (6)
df = df[~df[0].astype(str).str.contains("Fonte", na=False)]      # remove linha de fonte (índice 58)
df = df.iloc[5:].reset_index(drop=True)                          # remove as 5 linhas de cabeçalho reais

for col in df.columns:
    if col == COLUNA_CODIGO:
        df[col] = df[col].astype(str)
        continue
    convertido = pd.to_numeric(df[col], errors="coerce")
    if convertido.notna().mean() > 0.5:
        df[col] = convertido
    else:
        df[col] = df[col].astype(str)

df.to_csv("data/staged/teste.csv", index=False)
df.to_parquet("data/staged/teste.parquet", index=False)

tam_csv = os.path.getsize("data/staged/teste.csv")
tam_parquet = os.path.getsize("data/staged/teste.parquet")

def medir(funcao, repeticoes=5):
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        funcao()
        tempos.append(time.perf_counter() - t0)
    return sum(tempos) / len(tempos), min(tempos)

t_csv_medio, t_csv_min = medir(lambda: pd.read_csv("data/staged/teste.csv"))
t_parquet_medio, t_parquet_min = medir(lambda: pd.read_parquet("data/staged/teste.parquet"))

print(f"CSV:     {tam_csv/1024:.1f} KB | média {t_csv_medio:.4f}s | melhor {t_csv_min:.4f}s")
print(f"Parquet: {tam_parquet/1024:.1f} KB | média {t_parquet_medio:.4f}s | melhor {t_parquet_min:.4f}s")