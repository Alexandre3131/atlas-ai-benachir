#!/usr/bin/env python3
"""Analyse des traces Atlas AI."""

import json
from pathlib import Path

import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table

TRACES_PATH = Path("./data/traces.jsonl")

# GPT-4o pricing (avril 2026)
GPT4O_INPUT_COST_PER_TOKEN = 2.50 / 1_000_000
GPT4O_OUTPUT_COST_PER_TOKEN = 10.00 / 1_000_000

console = Console()


def load_traces(path: Path) -> pd.DataFrame:
    if not path.exists():
        console.print(f"[red]Fichier introuvable : {path}[/red]")
        raise SystemExit(1)
    records = [
        json.loads(line) for line in path.read_text().splitlines() if line.strip()
    ]
    return pd.DataFrame(records)


def print_latency_stats(df: pd.DataFrame) -> None:
    valid = df[df["latency_ms"] > 0]["latency_ms"]
    if valid.empty:
        console.print("[yellow]Pas encore de données de latence.[/yellow]")
        return

    table = Table(title="⏱  Latence (ms)", box=box.ROUNDED)
    table.add_column("Métrique", style="cyan")
    table.add_column("Valeur", justify="right", style="green")

    table.add_row("Médiane", f"{valid.median():.0f} ms")
    table.add_row("P95", f"{valid.quantile(0.95):.0f} ms")
    table.add_row("Max", f"{valid.max():.0f} ms")
    table.add_row("Moyenne", f"{valid.mean():.0f} ms")

    console.print(table)


def print_top_slowest(df: pd.DataFrame, n: int = 5) -> None:
    valid = df[df["latency_ms"] > 0].nlargest(n, "latency_ms")
    if valid.empty:
        return

    table = Table(title=f"🐢  Top {n} requêtes les plus lentes", box=box.ROUNDED)
    table.add_column("Latence (ms)", justify="right", style="red")
    table.add_column("Message", style="white")
    table.add_column("Guardrail", style="yellow")

    for _, row in valid.iterrows():
        table.add_row(
            str(int(row["latency_ms"])),
            str(row.get("user_message", ""))[:60],
            str(row.get("guardrail_triggered") or "—"),
        )

    console.print(table)


def print_prompt_distribution(df: pd.DataFrame) -> None:
    tokens = df["prompt_tokens"].dropna()
    if tokens.empty:
        return

    table = Table(title="Distribution tailles de prompt (tokens)", box=box.ROUNDED)
    table.add_column("Tranche", style="cyan")
    table.add_column("Nb requêtes", justify="right", style="green")

    bins = [0, 50, 100, 200, 500, float("inf")]
    labels = ["0–50", "51–100", "101–200", "201–500", "500+"]
    counts = pd.cut(tokens, bins=bins, labels=labels).value_counts().sort_index()

    for label, count in counts.items():
        table.add_row(str(label), str(count))

    console.print(table)


def print_cost_estimate(df: pd.DataFrame) -> None:
    total_input = df["prompt_tokens"].fillna(0).sum()
    total_output = df["completion_tokens"].fillna(0).sum()

    cost_input = total_input * GPT4O_INPUT_COST_PER_TOKEN
    cost_output = total_output * GPT4O_OUTPUT_COST_PER_TOKEN
    cost_total = cost_input + cost_output

    table = Table(title="Coût estimé si GPT-4o (tarifs avril 2026)", box=box.ROUNDED)
    table.add_column("Poste", style="cyan")
    table.add_column("Tokens", justify="right")
    table.add_column("Coût (USD)", justify="right", style="green")

    table.add_row("Input", f"{total_input:,.0f}", f"${cost_input:.4f}")
    table.add_row("Output", f"{total_output:,.0f}", f"${cost_output:.4f}")
    table.add_row("[bold]Total[/bold]", "", f"[bold]${cost_total:.4f}[/bold]")

    console.print(table)
    console.print(
        "[dim]Tarifs : $2.50/M tokens input — $10.00/M tokens output (GPT-4o, OpenAI)[/dim]"
    )


def print_guardrail_stats(df: pd.DataFrame) -> None:
    triggered = df["guardrail_triggered"].dropna()
    triggered = triggered[triggered != ""]
    if triggered.empty:
        console.print("[dim]Aucun guardrail déclenché dans les traces.[/dim]")
        return

    table = Table(title="🛡  Guardrails déclenchés", box=box.ROUNDED)
    table.add_column("Règle", style="cyan")
    table.add_column("Nb", justify="right", style="red")

    for rule, count in triggered.value_counts().items():
        table.add_row(str(rule), str(count))

    console.print(table)


def main() -> None:
    console.rule("[bold blue]Atlas AI — Analyse des traces[/bold blue]")
    df = load_traces(TRACES_PATH)
    console.print(f"[dim]{len(df)} traces chargées depuis {TRACES_PATH}[/dim]\n")

    print_latency_stats(df)
    console.print()
    print_top_slowest(df)
    console.print()
    print_prompt_distribution(df)
    console.print()
    print_guardrail_stats(df)
    console.print()
    print_cost_estimate(df)


if __name__ == "__main__":
    main()
