#!/usr/bin/env python3
"""Small CLI for the Mobills webcore API used by the mobills skill."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


DEFAULT_BASE = "https://api.mobills.com.br/webcore/api/"
DEFAULT_VERSION = "2.174.0"
DEFAULT_COLOR = 6723840
DEFAULT_INSTITUTION_ID = "4ebfc7cd-7d1b-4638-a4cf-79769b04be44"


def token() -> str:
    value = os.environ.get("MOBILLS_ACCESS_TOKEN", "").strip()
    if not value:
        raise SystemExit("MOBILLS_ACCESS_TOKEN is required")
    return value


def base_url() -> str:
    value = os.environ.get("MOBILLS_API_BASE", DEFAULT_BASE).strip()
    return value if value.endswith("/") else value + "/"


def headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token()}",
        "Content-Type": "application/json",
        "Mobills-Version": os.environ.get("MOBILLS_VERSION", DEFAULT_VERSION),
        "Mobills-Platform": "Web",
        "x-api-version": "1",
    }


def request(endpoint: str, method: str = "GET", body: dict | None = None):
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(base_url() + endpoint, data=data, headers=headers(), method=method)
    try:
        with urllib.request.urlopen(req) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"{method} {endpoint} failed: HTTP {exc.code}: {detail[:500]}")


def require_yes(args):
    if not getattr(args, "yes", False):
        raise SystemExit("Refusing write without --yes")


def find_by_name(items, name: str, label: str):
    matches = [item for item in items if item.get("nome") == name]
    if not matches:
        raise SystemExit(f"{label} not found by exact name: {name}")
    if len(matches) > 1:
        raise SystemExit(f"Multiple {label} records match exact name: {name}")
    return matches[0]


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))


def list_accounts(_args):
    data = request("Contas")
    print_json(data)


def list_cards(_args):
    data = request("CartaoCredito")
    print_json(data)


def create_account(args):
    require_yes(args)
    payload = {
        "nome": args.name,
        "saldo": args.balance,
        "saldoInicial": args.balance,
        "saldoPrevisto": args.balance,
        "cor": args.color,
        "telaInicial": not args.hide_from_dashboard,
        "tipoConta": args.type_id,
        "instituicaoBancariaId": args.institution_id,
    }
    print_json(request("Contas/Create", "POST", payload))


def update_account(args):
    require_yes(args)
    accounts = request("Contas")
    account = next((item for item in accounts if str(item.get("id")) == str(args.id)), None) if args.id else find_by_name(accounts, args.current_name, "account")
    payload = dict(account)
    if args.name is not None:
        payload["nome"] = args.name
    if args.type_id is not None:
        payload["tipoConta"] = args.type_id
    if args.institution_id is not None:
        payload["instituicaoBancariaId"] = args.institution_id
    print_json(request("Contas/Edit", "POST", payload))


def create_card(args):
    require_yes(args)
    accounts = request("Contas")
    account_id = args.account_id
    if account_id is None:
        account_id = find_by_name(accounts, args.account_name, "account")["id"]
    payload = {
        "nome": args.name,
        "limite": args.limit,
        "bandeira": args.brand,
        "diaPagamento": args.due_day,
        "diaFechamento": args.closing_day,
        "contaId": account_id,
        "emissorId": None,
        "instituicaoBancariaId": None,
        "cor": args.color,
    }
    print_json(request("CartaoCredito/Create", "POST", payload))


def update_card(args):
    require_yes(args)
    cards = request("CartaoCredito")
    card = next((item for item in cards if str(item.get("id")) == str(args.id)), None) if args.id else find_by_name(cards, args.current_name, "card")
    payload = dict(card)
    if args.account_name is not None:
        payload["contaId"] = find_by_name(request("Contas"), args.account_name, "account")["id"]
    if args.account_id is not None:
        payload["contaId"] = args.account_id
    for attr, key in [
        ("name", "nome"),
        ("limit", "limite"),
        ("brand", "bandeira"),
        ("due_day", "diaPagamento"),
        ("closing_day", "diaFechamento"),
    ]:
        value = getattr(args, attr)
        if value is not None:
            payload[key] = value
    print_json(request("CartaoCredito/Edit", "POST", payload))


def add_common_write(parser):
    parser.add_argument("--yes", action="store_true", help="confirm this write operation")


def build_parser():
    parser = argparse.ArgumentParser(description="Mobills webcore API helper")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-accounts").set_defaults(func=list_accounts)
    sub.add_parser("list-cards").set_defaults(func=list_cards)

    p = sub.add_parser("create-account")
    p.add_argument("--name", required=True)
    p.add_argument("--balance", type=float, default=0)
    p.add_argument("--type-id", type=int, default=5)
    p.add_argument("--institution-id", default=DEFAULT_INSTITUTION_ID)
    p.add_argument("--color", type=int, default=DEFAULT_COLOR)
    p.add_argument("--hide-from-dashboard", action="store_true")
    add_common_write(p)
    p.set_defaults(func=create_account)

    p = sub.add_parser("update-account")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--id", type=int)
    target.add_argument("--current-name")
    p.add_argument("--name")
    p.add_argument("--type-id", type=int)
    p.add_argument("--institution-id")
    add_common_write(p)
    p.set_defaults(func=update_account)

    p = sub.add_parser("create-card")
    p.add_argument("--name", required=True)
    p.add_argument("--limit", type=float, required=True)
    p.add_argument("--closing-day", type=int, required=True)
    p.add_argument("--due-day", type=int, required=True)
    p.add_argument("--brand", type=int, default=1)
    p.add_argument("--color", type=int, default=DEFAULT_COLOR)
    account = p.add_mutually_exclusive_group(required=True)
    account.add_argument("--account-id", type=int)
    account.add_argument("--account-name")
    add_common_write(p)
    p.set_defaults(func=create_card)

    p = sub.add_parser("update-card")
    target = p.add_mutually_exclusive_group(required=True)
    target.add_argument("--id", type=int)
    target.add_argument("--current-name")
    p.add_argument("--name")
    p.add_argument("--limit", type=float)
    p.add_argument("--closing-day", type=int)
    p.add_argument("--due-day", type=int)
    p.add_argument("--brand", type=int)
    account = p.add_mutually_exclusive_group()
    account.add_argument("--account-id", type=int)
    account.add_argument("--account-name")
    add_common_write(p)
    p.set_defaults(func=update_card)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
