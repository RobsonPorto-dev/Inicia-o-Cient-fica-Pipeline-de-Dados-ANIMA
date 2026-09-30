# Integração: Tabela 7334 (uso de internet) + Tabela 9514 (população, Censo 2022)

## 1. Chave de junção

A Tabela 9514 traz o código IBGE de 7 dígitos por município (ex: `1100015` —
os 2 primeiros dígitos são o código da UF). A Tabela 7334 traz o código IBGE
de 2 dígitos por UF (coluna "Cód."). O nome do município na 9514 vem no
formato `"Alta Floresta D'Oeste (RO)"` — nome seguido da sigla da UF entre
parênteses.

**Tentei primeiro casar por nome** (sigla extraída do nome do município,
ex: `"RO"`, contra o nome completo da UF na 7334, ex: `"Rondônia"`) — e essa
tentativa **falhou 100% das vezes** (0 de 5.570 municípios casaram), porque
as duas fontes usam vocabulários diferentes para a mesma coisa: sigla de
2 letras numa fonte, nome por extenso na outra. Não é uma diferença de
acento ou grafia — é uma representação completamente diferente da mesma
informação.

**A chave que funciona** é o código IBGE de UF: os 2 primeiros dígitos do
código do município (`cod_municipio[:2]`) contra o código de 2 dígitos da
UF na 7334 (`cod_uf`). Com essa chave, **5.570 de 5.570 municípios casaram**
(100%).

## 2. Resultado da junção em números

- Municípios na Tabela 9514: **5.570**
- UFs na Tabela 7334: **27**
- Municípios que casaram (join por código de UF): **5.570 / 5.570 (100%)**
- Municípios que não casaram: **0**
- UFs da 7334 sem nenhum município correspondente: **nenhuma**

Não houve necessidade de classificar causas de não-casamento (grafia,
ausência, município extinto) porque, usando a chave correta (código IBGE),
o casamento foi perfeito — todas as 5.570 entradas da 9514 têm código de UF
dentro do conjunto das 27 UFs cobertas pela 7334. Isso é um resultado
esperado: código IBGE de UF é um identificador padronizado e estável, sem
as inconsistências que apareceriam se a chave fosse baseada em texto livre.

## 3. Granularidade

As duas fontes **não estão no mesmo grão**. A Tabela 9514 é por **município**
(5.570 linhas). A Tabela 7334 para no nível de **UF** (27 linhas) — não tem
dado de uso de internet por município.

O nível mais fino comum às duas é, portanto, **UF**, não município. Para
montar uma tabela final "por município" (como pedido), a decisão tomada foi:
manter uma linha por município (população real, específica de cada um) e
**repetir o valor de uso de internet da UF em todos os municípios daquela
UF**. Ou seja: a coluna de população tem granularidade real de município; a
coluna de uso de internet tem granularidade real de UF, apenas *repetida*
por município — não é um dado observado naquele nível.

Essa é uma decisão registrada, não um erro: repetir o valor da UF é
necessário para produzir uma tabela no grão pedido, mas não cria informação
que não existe. Qualquer análise que use a coluna de internet por município
precisa saber que, na prática, ela é uma informação de UF.

## 4. Tempo

A Tabela 7334 se refere a **2025** (PNAD Contínua, 1º semestre). A Tabela
9514 se refere ao **Censo 2022**. São anos diferentes, com uma defasagem de
cerca de 3 anos.

Decisão: usei os dados mais recentes disponíveis de cada fonte, sem tentar
interpolar ou ajustar um ano para o outro. Isso significa que a tabela final
combina população de 2022 com uso de internet de 2025 — uma aproximação
razoável para essa etapa exploratória, mas que precisa ser deixada explícita
em qualquer análise: não é o mesmo ano de referência.

## 5. Validações

Implementadas em `tests/test_integracao.py`, rodando com `pytest`:

- Código IBGE do município tem exatamente 7 dígitos numéricos
- Sigla de UF pertence ao conjunto das 27 UFs válidas
- Percentual de uso de internet está entre 0 e 100
- Código do município não se repete (chave única)
- Nenhum município da tabela final ficou sem o valor de internet da UF
- População é um valor positivo
- **Validação testada de propósito:** um teste injeta um percentual inválido
  (150%, impossível) numa tabela de teste e confirma que a checagem de
  intervalo 0–100 realmente rejeita esse valor (`pytest.raises(AssertionError)`)

Todos os 7 testes passam.

## 6. Fechamento

Com essas duas fontes integradas, a tabela resultante **consegue responder**:
perguntas sobre população por município cruzadas com o contexto de uso de
internet da sua UF (ex: "municípios de UFs com maior uso de internet
concentram quanta população?").

Ela **não consegue responder**: qual município especificamente tem maior ou
menor uso de internet — porque esse dado não existe nessas fontes nesse
grão. O valor de internet é o mesmo para todos os municípios de uma mesma
UF, por construção, não por medição.
