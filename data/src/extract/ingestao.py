import shutil, hashlib, json, os, sys
from datetime import datetime, timezone

def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()

def contar_linhas(caminho):
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)

def ingerir(origem, destino, url_fonte):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if os.path.abspath(origem) != os.path.abspath(destino):
        shutil.copy(origem, destino)
    registro = {
        "arquivo": os.path.basename(destino),
        "fonte": url_fonte,
        "data_download": datetime.now(timezone.utc).isoformat(),
        "tamanho_bytes": os.path.getsize(destino),
        "n_linhas": contar_linhas(destino),
        "sha256": sha256_arquivo(destino),
    }
    with open("docs/procedencia.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")
    print(json.dumps(registro, indent=2, ensure_ascii=False))
    return registro

if __name__ == "__main__":
    origem, destino = sys.argv[1], sys.argv[2]
    url = sys.argv[3] if len(sys.argv) > 3 else "desconhecida"
    ingerir(origem, destino, url)