---
name: mobills
description: Work with the Mobills web API. Use this skill when Codex needs to inspect, create, update, migrate, reconcile, or audit Mobills accounts, cards, categories, transactions, transfers, tags, invoices, or related financial records through the internal Mobills webcore API.
---

# Mobills

## Overview

Use this skill for Mobills operations through the webcore API used by the Mobills web app. Treat this API as internal and unstable: verify current records before writes, preserve fields you do not understand, and run read-after-write checks for any mutation.

This skill is intentionally generic. Do not assume a user's naming convention, category granularity, tagging strategy, personal/professional separation, or migration source. Ask or infer from the current task and existing Mobills data.

For detailed endpoints, payload shapes, and known API caveats, read `references/api.md`.

## Authentication

Use `MOBILLS_ACCESS_TOKEN` as a bearer token. Do not paste, print, commit, or expose access tokens, refresh tokens, cookies, or local-storage dumps.

Required headers:

```text
Authorization: Bearer <token>
Mobills-Version: 2.174.0
Mobills-Platform: Web
x-api-version: 1
Content-Type: application/json
```

If the token is unavailable or expired, ask the user for an explicit source or have them authenticate in the browser. Do not extract browser storage unless the user explicitly requests local browser-token recovery for Mobills.

## Workflow

1. Identify the requested Mobills resource: accounts, cards, categories, transactions, card expenses, transfers, tags, reports, or invoices.
2. List or fetch existing records before comparing or writing.
3. Normalize names only for matching; preserve the user's visible names unless asked to change them.
4. For updates, fetch the current record and merge changes into the expected payload shape.
5. For migrations or bulk writes, use an idempotency marker in a durable field such as `observacao`, then check for existing markers before creating.
6. After each write or batch, read back the affected month/resource and verify the intended state.
7. Report created, updated, skipped, and failed records, including assumptions and any API caveats encountered.

## Common Commands

Prefer the bundled CLI for supported account/card operations:

```bash
export MOBILLS_ACCESS_TOKEN="..."
python3 scripts/mobills_api.py list-accounts
python3 scripts/mobills_api.py list-cards
```

Set optional environment overrides only when needed:

```bash
export MOBILLS_API_BASE="https://api.mobills.com.br/webcore/api/"
export MOBILLS_VERSION="2.174.0"
```

Create a manual account:

```bash
python3 scripts/mobills_api.py create-account \
  --name "Example Account" \
  --type-id 1 \
  --institution-id "d27af8e1-cf9f-4157-a4e8-3e0a35ad6ce9" \
  --yes
```

Update an account while preserving existing fields:

```bash
python3 scripts/mobills_api.py update-account \
  --current-name "Example Account" \
  --name "Renamed Example Account" \
  --yes
```

Create a credit card:

```bash
python3 scripts/mobills_api.py create-card \
  --name "Example Card" \
  --limit 5000 \
  --closing-day 7 \
  --due-day 28 \
  --account-name "Example Account" \
  --brand 1 \
  --yes
```

Update a credit card:

```bash
python3 scripts/mobills_api.py update-card \
  --current-name "Example Card" \
  --name "Renamed Example Card" \
  --limit 6000 \
  --closing-day 7 \
  --due-day 28 \
  --account-name "Example Account" \
  --yes
```

## Safety Rules

- Never reveal access tokens, refresh tokens, cookies, or local-storage dumps.
- Confirm source and destination before transmitting financial data into Mobills unless the user has already explicitly requested that specific operation.
- Do not call delete/archive endpoints unless the user explicitly asks and confirms at action time.
- Be cautious with bulk writes: prefer dry-run, pilot write, and idempotent full run.
- For edits, preserve unknown fields where the API expects full records or wrapper objects.
- Tags, categories, subcategories, and naming schemes are user/workspace choices, not skill defaults.

## Resource Notes

- Accounts and cards are top-level financial containers.
- Categories can be parent categories or subcategories. Use parent-only or subcategory-level classification according to the user's requested granularity.
- Tags are optional and may be constrained by subscription/product limits.
- Account transactions, card expenses, and transfers use different endpoints and different edit payload shapes.
- Card expense invoice placement depends on card closing and due dates; verify the invoice month when writing card expenses.
