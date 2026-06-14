# Mobills Webcore API Reference

The Mobills web app uses an internal API. This reference is based on observed web app behavior and may drift without notice.

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

## Accounts

List:

```text
GET Contas
```

Returned account fields observed:

```json
{
  "id": 21914238,
  "nome": "C6 Bank",
  "saldo": 0.0,
  "cor": 6723840,
  "telaInicial": true,
  "tipoConta": 1,
  "arquivado": false,
  "instituicaoBancariaId": "53ecea51-0153-42e1-b9e1-ef2078542646",
  "saldoPrevisto": 0.0,
  "saldoInicial": 0.0
}
```

Create:

```text
POST Contas/Create
```

Minimal observed payload:

```json
{
  "nome": "PF - Caju",
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

Use the full fetched account object with changed fields merged in.

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

Returned card fields observed:

```json
{
  "id": 4976082,
  "nome": "C6 Bank",
  "limite": 8820.00,
  "bandeira": 1,
  "diaPagamento": 25,
  "diaFechamento": 18,
  "contaId": 21914238,
  "emissorId": null,
  "instituicaoBancariaId": null,
  "arquivado": false
}
```

Create:

```text
POST CartaoCredito/Create
```

Minimal observed payload:

```json
{
  "nome": "PF - Nubank",
  "limite": 8800,
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

Use the full fetched card object with changed fields merged in.

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

## Known Caveats

- `https://api.mobills.com.br/` without `/webcore/api/` returns 404 for these legacy routes.
- The web app may change header requirements and payloads.
- Equal `diaFechamento` and `diaPagamento` are rejected by the UI and likely by API validation.
- Existing card records may have different `diaFechamento` from another source system; treat the chosen source of truth explicitly.
- Avoid delete/archive endpoints unless specifically requested and confirmed.
