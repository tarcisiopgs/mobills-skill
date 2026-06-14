---
name: mobills
description: Work with the Mobills web API. Use this skill when Codex needs to list, compare, create, or update Mobills accounts or credit cards; migrate data into Mobills; audit Mobills records; or operate the internal Mobills webcore API safely.
---

# Mobills

## Overview

Use this skill for Mobills account and credit-card operations through the Mobills web API discovered from the web app. Treat the API as internal and unstable: verify current records before writes, keep payloads minimal, and never expose tokens in chat or logs.

## Quick Start

Prefer the bundled CLI for repeatable API calls:

```bash
export MOBILLS_ACCESS_TOKEN="..."
python3 /path/to/mobills/scripts/mobills_api.py list-accounts
python3 /path/to/mobills/scripts/mobills_api.py list-cards
```

Set optional environment overrides only when needed:

```bash
export MOBILLS_API_BASE="https://api.mobills.com.br/webcore/api/"
export MOBILLS_VERSION="2.174.0"
```

For detailed endpoints, payloads, and known caveats, read `references/api.md`.

## Authentication

Use `MOBILLS_ACCESS_TOKEN` as a bearer token. Do not paste, print, or save the token in source files.

Required headers:

```text
Authorization: Bearer <token>
Mobills-Version: 2.174.0
Mobills-Platform: Web
x-api-version: 1
Content-Type: application/json
```

If the token is unavailable or expired, ask the user for an explicit source or have them authenticate in the browser. Do not silently extract browser storage unless the user explicitly requests local browser-token recovery for Mobills.

## Workflow

1. List existing records first.
2. Normalize names before comparing, especially `PF - ...` and `PJ - ...` prefixes.
3. For writes, build the smallest payload that preserves existing fields.
4. Run a read-after-write verification.
5. Report created/updated records and any assumptions.

## Common Commands

List active accounts:

```bash
python3 scripts/mobills_api.py list-accounts
```

Create a manual account:

```bash
python3 scripts/mobills_api.py create-account \
  --name "PJ - Nubank" \
  --type-id 1 \
  --institution-id "d27af8e1-cf9f-4157-a4e8-3e0a35ad6ce9" \
  --yes
```

Rename or update an account while preserving existing fields:

```bash
python3 scripts/mobills_api.py update-account \
  --current-name "Nubank" \
  --name "PF - Nubank" \
  --yes
```

Create a credit card:

```bash
python3 scripts/mobills_api.py create-card \
  --name "PF - Nubank" \
  --limit 8800 \
  --closing-day 7 \
  --due-day 28 \
  --account-name "PF - Nubank" \
  --brand 1 \
  --yes
```

Update a credit card:

```bash
python3 scripts/mobills_api.py update-card \
  --current-name "Inter" \
  --name "PF - Inter" \
  --limit 5100 \
  --closing-day 7 \
  --due-day 28 \
  --account-name "PF - Inter" \
  --yes
```

## Safety Rules

- Never reveal access tokens, refresh tokens, cookies, or full local-storage dumps.
- Confirm source and destination before transmitting financial data into Mobills unless the user already explicitly requested that specific migration.
- Do not call delete/archive endpoints unless the user explicitly asks and confirms at action time.
- For cards, Mobills rejects equal closing and due days. If source data has `1/1`, preserve closing day `1` and use due day `2`, then report the adjustment.
- When editing existing records, fetch the current record and merge changes into it instead of sending a sparse unknown payload.

## Naming Strategy

For mixed personal/professional data, prefer stable visible prefixes:

- `PF - Name` for personal accounts/cards.
- `PJ - Name` for professional accounts/cards.

This avoids collisions in Mobills for common bank names such as Nubank, Itau, Banco do Brasil, and C6 Bank.
