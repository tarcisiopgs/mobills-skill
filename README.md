# mobills-skill

Agent skill for the Mobills web API.

## Install

From GitHub:

```bash
npx skills add tarcisiopgs/mobills-skill -y --full-depth --skill mobills
npx skills add tarcisiopgs/mobills-skill -g -y --full-depth --skill mobills
```

From a local checkout:

```bash
npx skills add . -y --full-depth
npx skills add . -g -y --full-depth
```

## Authentication

Set:

```bash
export MOBILLS_ACCESS_TOKEN=...
```

The token is a sensitive bearer token. Do not commit it or print it in chat/logs.

## Included helper

The skill includes `mobills/scripts/mobills_api.py`, a small standard-library CLI for repeatable account and credit-card operations:

```bash
python3 mobills/scripts/mobills_api.py list-accounts
python3 mobills/scripts/mobills_api.py list-cards
```
