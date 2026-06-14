# Mobills Webcore API Reference

The Mobills web app uses an internal webcore API. This reference is based on observed web app behavior and may drift without notice. Prefer live verification against the current web bundle or API responses when precision matters.

Base URL:

```text
https://api.mobills.com.br/webcore/api/
```

Required headers:

```text
Authorization: Bearer <MOBILLS_ACCESS_TOKEN>
Mobills-Version: 2.174.0
Mobills-Platform: Web
x-api-version: 1
Content-Type: application/json
```

## General Practices

- Treat all endpoints as internal and unstable.
- Use `GET` endpoints to inspect current records before writes.
- Use read-after-write verification for every create or edit.
- For bulk imports, put an idempotency marker in `observacao` or another durable field and search for it before creating records.
- Do not assume tags, category granularity, account naming, or personal/business separation conventions. Those are user choices.
- Preserve unknown fields when editing records, especially when the web app sends full objects or wrapper objects.
- Dates are generally ISO strings. The web app often sends UTC-style timestamps such as `YYYY-MM-DDT00:00:00.000Z`.

## Accounts

List:

```text
GET Contas
```

Create:

```text
POST Contas/Create
```

Minimal observed payload:

```json
{
  "nome": "Example Account",
  "saldo": 0,
  "saldoInicial": 0,
  "saldoPrevisto": 0,
  "cor": 6723840,
  "telaInicial": true,
  "tipoConta": 5,
  "instituicaoBancariaId": "4ebfc7cd-7d1b-4638-a4cf-79769b04be44"
}
```

Edit:

```text
POST Contas/Edit
```

Use the fetched account object with changed fields merged in.

Account type IDs observed from `GET Contas/TipoConta`:

| id | descricao |
|---:|---|
| 1 | Conta Corrente |
| 2 | Dinheiro |
| 3 | Poupanca |
| 4 | Investimentos |
| 5 | Outros |
| 6 | Conta de pagamentos |
| 7 | Conta de pagamentos |
| 8 | VR/VA |

Useful institution IDs observed:

| name | instituicaoBancariaId |
|---|---|
| Banco do Brasil | `0a0c72e8-bb6f-416d-b154-58d06bf66241` |
| Bradesco | `3ea0b0c4-2708-492c-b051-5b654843807c` |
| C6 Bank | `53ecea51-0153-42e1-b9e1-ef2078542646` |
| Caixa | `11687177-9a7b-44a1-9fea-9205f41cf117` |
| Itau | `8df8a4c9-b0ed-41a4-81f3-c5ec3ab11098` |
| Inter | `f6aac1fa-8aef-4843-9dff-6357dab2268f` |
| Nubank | `d27af8e1-cf9f-4157-a4e8-3e0a35ad6ce9` |
| Wise | `28f3cd2b-6e8c-4fcb-924a-bb46f73341d5` |
| Other/default | `4ebfc7cd-7d1b-4638-a4cf-79769b04be44` |

## Credit Cards

List:

```text
GET CartaoCredito
```

Create:

```text
POST CartaoCredito/Create
```

Minimal observed payload:

```json
{
  "nome": "Example Card",
  "limite": 5000,
  "bandeira": 1,
  "diaPagamento": 28,
  "diaFechamento": 7,
  "contaId": 21914343,
  "emissorId": null,
  "instituicaoBancariaId": null,
  "cor": 6723840
}
```

Edit:

```text
POST CartaoCredito/Edit
```

Use the fetched card object with changed fields merged in.

Invoice helpers:

```text
GET DespesaCartao/MudarFaturaPorData?cartaoId={cardId}&dia={day}&mes={month}&ano={year}
GET DespesaCartao/MudarFaturaPorCartao?cartaoId={cardId}
GET CartaoCredito/HistoricoFaturas?CartaoId={cardId}&ano={year}
GET Relatorios/Faturas?cartaoId={cardId}
```

Card brand IDs observed from `GET CartaoCredito/TipoCartaoCredito`:

| id | descricao |
|---:|---|
| 0 | Visa |
| 1 | MasterCard |
| 2 | HiperCard |
| 3 | American Express |
| 4 | SoroCard |
| 5 | BNDES |
| 6 | Dinners |
| 7 | Elo |
| 8 | Outra bandeira |

## Categories

Expense categories:

```text
GET Categorias/1
GET Categorias/CategoriasCombobox?categoriaId=1
```

Income categories:

```text
GET Categorias/2
GET Categorias/CategoriasCombobox?categoriaId=2
```

Create category:

```text
POST Categorias/Create
```

Observed payload:

```json
{
  "nome": "Example Category",
  "cor": 39372,
  "icon": 1,
  "ativo": true,
  "tipoCategoria": 1,
  "tipoCategoriaPaiId": null
}
```

Notes:

- `tipoCategoria` is `1` for expenses and `2` for incomes.
- Parent categories have `tipoCategoriaPaiId: null`.
- Subcategories use `tipoCategoriaPaiId` pointing to the parent category.
- For transactions, use the parent category id in `tipoDespesaId` or `tipoReceitaId`; use `subcategoriaId` only when the user wants subcategory-level classification.

## Tags

List:

```text
GET Etiquetas
```

Create:

```text
POST Etiquetas/Create
```

Edit:

```text
POST Etiquetas/Edit
```

Delete:

```text
POST Etiquetas/Delete?id={tagId}
```

Notes:

- Transaction forms send both `etiquetas` as a comma-separated tag-name string and `tags` as an array of tag objects.
- Tags may be constrained by product/subscription limits. If an operation fails around tags, retry without tags only if that matches user intent.

## Account Expenses

List monthly expenses:

```text
GET Despesas?mes={month}&ano={year}
```

Create:

```text
POST Despesas/Create
```

Observed payload:

```json
{
  "valor": 50,
  "efetivado": true,
  "status": 0,
  "dataDespesa": "2026-06-01T00:00:00.000Z",
  "descricao": "Example expense",
  "favorito": false,
  "tipoDespesaId": 163926688,
  "subcategoriaId": null,
  "contaId": 21914773,
  "etiquetas": null,
  "tags": [],
  "observacao": "optional notes",
  "isDespesaFixa": false,
  "repetir": false,
  "quantidadeRepeticao": "2",
  "periodoRepeticao": "3",
  "ignorada": false,
  "anexo": null,
  "verificarDespesas": false
}
```

Edit:

```text
POST Despesas/Edit
```

Observed edit shape:

```json
{
  "despesas": [
    {
      "id": 1355130358,
      "valor": 50,
      "efetivado": true,
      "status": 0,
      "dataDespesa": "2026-06-01T00:00:00.000Z",
      "descricao": "Example expense",
      "tipoDespesaId": 163926688,
      "subcategoriaId": null,
      "contaId": 21914773,
      "observacao": "optional notes",
      "controleRepeticaoDespesa": null,
      "descricaoValidadoRepeticao": "Example expense"
    }
  ]
}
```

Notes:

- `status: 0` means paid/effective; `status: 1` means pending.
- The API validates `quantidadeRepeticao` between `2` and `99`, even when `repetir` is false.
- For fixed or repeated expenses, the web app may add fields such as `dataOriginalDespesa`, `opcaoEditarDespesaFixa`, `despesaFixaId`, `OpcaoExcluirDespesaRepetida`, and `isDespesaRepetida`.

## Account Incomes

List monthly incomes:

```text
GET Receitas?mes={month}&ano={year}
```

Create:

```text
POST Receitas/Create
```

Observed payload:

```json
{
  "valor": 100,
  "efetivado": false,
  "status": 1,
  "dataReceita": "2026-06-01T00:00:00.000Z",
  "descricao": "Example income",
  "favorito": false,
  "tipoReceitaId": 77422406,
  "subcategoriaId": null,
  "contaId": 21914773,
  "etiquetas": null,
  "tags": [],
  "observacao": "optional notes",
  "isReceitaFixa": false,
  "repetir": false,
  "quantidadeRepeticao": "2",
  "periodoRepeticao": "3",
  "ignorada": false,
  "anexo": null,
  "verificarReceitas": false
}
```

Edit:

```text
POST Receitas/Edit
```

Observed edit shape:

```json
{
  "receitas": [
    {
      "id": 277883238,
      "valor": 100,
      "efetivado": false,
      "status": 1,
      "dataReceita": "2026-06-01T00:00:00.000Z",
      "descricao": "Example income",
      "tipoReceitaId": 77422406,
      "subcategoriaId": null,
      "contaId": 21914773,
      "observacao": "optional notes",
      "controleRepeticaoReceita": null,
      "descricaoValidadoRepeticao": "Example income"
    }
  ]
}
```

Notes:

- `status: 0` means received/effective; `status: 1` means pending.
- The API validates `quantidadeRepeticao` between `2` and `99`, even when `repetir` is false.

## Credit Card Expenses

List card expenses by invoice month:

```text
GET DespesaCartao?cartaoId={cardId}&mes={month}&ano={year}
```

Create:

```text
POST DespesaCartao/Create
```

Observed payload:

```json
{
  "valor": 25,
  "dataDespesa": "2026-06-17T00:00:00.000Z",
  "descricao": "Example card expense",
  "tipoDespesaId": 163923754,
  "subcategoriaId": null,
  "cartaoCreditoId": 5976499,
  "fatura": "2026-07-02T00:00:00.000Z",
  "etiquetas": null,
  "observacao": "optional notes",
  "parcelado": false,
  "quantidadeParcelas": "2",
  "contaId": 25976385,
  "ignorada": false,
  "verificarDespesas": false
}
```

Edit:

```text
POST DespesaCartao/Edit
```

Observed edit payload:

```json
{
  "originalInvoice": "2026-07-02T00:00:00.000Z",
  "id": 496381959,
  "valor": 25,
  "dataDespesa": "2026-06-17T00:00:00.000Z",
  "descricao": "Example card expense",
  "tipoDespesaId": 163923754,
  "subcategoriaId": null,
  "cartaoCreditoId": 5976499,
  "fatura": "2026-07-02T00:00:00.000Z",
  "etiquetas": null,
  "observacao": "optional notes",
  "parcelado": false,
  "quantidadeParcelas": "2",
  "ignorada": false,
  "parcelNumber": ""
}
```

Create fixed card expense:

```text
POST DespesaCartao/CreateFixa
```

Observed payload:

```json
{
  "descricao": "Example fixed card expense",
  "valor": 25,
  "tipoDespesaId": 163923754,
  "subcategoriaId": null,
  "cartaoCreditoId": 5976499,
  "observacao": "optional notes",
  "diaPagamento": 10
}
```

Notes:

- `fatura` should be the invoice due date selected for that card expense.
- The API validates `quantidadeParcelas` between `2` and `99`, even when `parcelado` is false.
- If creating actual installments, use `parcelado: true` and the intended `quantidadeParcelas`; verify how the API creates child records before bulk use.

## Transfers

List monthly transfers:

```text
GET Transferencias?mes={month}&ano={year}
```

List fixed transfers:

```text
GET Transferencias/TransferenciasFixas
```

Create:

```text
POST Transferencias/Create
```

Observed payload:

```json
{
  "valor": 50,
  "deConta": {
    "id": 21914343,
    "nome": "Origin Account"
  },
  "deContaId": 21914343,
  "paraConta": {
    "id": 21914773,
    "nome": "Destination Account"
  },
  "paraContaId": 21914773,
  "dataTransferencia": "2026-06-01T00:00:00.000Z",
  "observacao": "optional notes",
  "transferenciaFixa": false,
  "isTransferenciaFixa": false,
  "diaTransferenciaFixa": 0,
  "etiquetas": null,
  "tags": [],
  "verificarTransferencias": false
}
```

Edit:

```text
POST Transferencias/Edit
```

Use the create shape plus `id` when editing.

Notes:

- Creating transfers with only ids can return a generic HTTP 500. Include both account ids and the `deConta`/`paraConta` account objects.
- Include `transferenciaFixa`, `isTransferenciaFixa`, `diaTransferenciaFixa`, and `verificarTransferencias`.
- The transfer form validates `observacao` to 128 characters. Keep idempotency markers compact.

## Combined Transactions

Monthly combined transaction view:

```text
GET Transacoes?mes={month}&ano={year}
```

Filter endpoint:

```text
POST Transacoes/Filtro
```

The combined view returns `movimentacoes` that may represent expenses, incomes, transfers, card expenses, or invoice-related movements. Use the resource-specific endpoints for reliable edits.

## Known Caveats

- `https://api.mobills.com.br/` without `/webcore/api/` returns 404 for these routes.
- The web app may change header requirements and payloads.
- Equal `diaFechamento` and `diaPagamento` are rejected by the UI and may be rejected by API validation.
- Existing card records may have different `diaFechamento` from another source system; treat the chosen source of truth explicitly.
- `Despesas/Edit` and `Receitas/Edit` expect wrapper objects; `DespesaCartao/Edit` does not.
- Some endpoints return generic HTTP 500 for malformed payloads instead of validation details.
- Avoid delete/archive endpoints unless specifically requested and confirmed.
