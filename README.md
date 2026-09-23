# Iniciação Científica — Pipeline de Dados

Fundação de um pipeline de dados (camadas raw/staged/curated) para o projeto
de iniciação científica.

## Estrutura
- `data/raw`: dados exatamente como vieram da fonte, sem alteração
- `data/staged`: mesmo conteúdo, convertido para formato de trabalho (Parquet),
  com colunas e tipos padronizados
- `data/curated`: dados limpos, categorias padronizadas, duplicidades e
  ausentes tratados
- `data/src/extract`: scripts de ingestão (baixam/copiam arquivos para raw e
  registram a procedência)
- `docs/arquitetura.md`: descrição das camadas e diagrama

## Como reproduzir
1. Rode os scripts em `src/extract/` para popular `data/raw`

## Fontes de dados

- **IBGE (Tabela 7334)** — versionado em `data/raw/`
- **Disque 100 (1º semestre 2026)** — ~1,79 GB, não versionado no Git por exceder
  o limite de 100 MB do GitHub. A procedência completa (fonte, data, tamanho,
  linhas, hash SHA-256) está registrada em `docs/procedencia.jsonl`, garantindo
  reprodutibilidade mesmo sem o arquivo estar no repositório.