"""Gera o GIF de terminal do perfil (x0rzavi/github-readme-terminal)."""

from datetime import datetime
from zoneinfo import ZoneInfo

import os

import gifos
import requests

USER = "mari-brene"
TZ = ZoneInfo("America/Sao_Paulo")

# Cores ANSI
R = "\x1b[0m"
ROXO = "\x1b[95m"
AZUL = "\x1b[94m"
CIANO = "\x1b[96m"
VERDE = "\x1b[92m"
AMARELO = "\x1b[93m"
VERMELHO = "\x1b[91m"
TITULO = "\x1b[30;105m"


def commits_do_ano(ano: str):
    """Commits (públicos + privados) de 1º de janeiro até agora."""
    query = """
    query($login: String!, $from: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from) {
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }"""
    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": {"login": USER, "from": f"{ano}-01-01T00:00:00Z"}},
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
        timeout=30,
    )
    c = r.json()["data"]["user"]["contributionsCollection"]
    return c["totalCommitContributions"] + c["restrictedContributionsCount"]


def buscar_stats(ano: str):
    try:
        s = gifos.utils.fetch_github_stats(USER)
        langs = ", ".join(lang[0] for lang in s.languages_sorted[:5]) or "-"
        return {
            "rank": s.user_rank.level,
            "commits": commits_do_ano(ano),
            "prs": s.total_pull_requests_made,
            "estrelas": s.total_stargazers,
            "repos": s.total_repo_contributions,
            "langs": langs,
        }
    except Exception as e:  # sem token ou API fora do ar
        print(f"WARNING: não foi possível buscar estatísticas: {e}")
        return {k: "-" for k in ("rank", "commits", "prs", "estrelas", "repos", "langs")}


def main():
    t = gifos.Terminal(750, 500, 15, 15)
    t.set_prompt(f"{ROXO}mari{R}@{AZUL}github{R} {CIANO}~{R} $ ")

    # --- Boot ---
    t.gen_text("", 1, count=15)
    t.toggle_show_cursor(False)
    ano = datetime.now(TZ).strftime("%Y")
    t.gen_text("MARI-BIOS v2.0.26", 1)
    t.gen_text(f"Copyright (C) {ano}, {ROXO}Maria Clara Brene{R}", 2)
    t.gen_text(f"{AZUL}GitHub Profile Terminal - Joinville/SC{R}", 4)
    t.gen_text("CPU: Cafe(tm) Dual Core @ 3.0GHz", 6)
    for i in range(0, 65537, 8192):
        t.delete_row(7)
        t.gen_text(f"Memory Test: {i}KB", 7, count=2, contin=True)
    t.delete_row(7)
    t.gen_text(f"Memory Test: 64MB {VERDE}OK{R}", 7, count=10, contin=True)

    t.clear_frame()
    t.gen_text("Iniciando sistema ", 1, contin=True)
    t.gen_typing_text(".....", 1, contin=True)
    t.gen_text("", 1, count=5, contin=True)

    # --- Login ---
    t.clear_frame()
    t.gen_text(f"{AMARELO}MariOS 2.0 (tty1){R}", 1, count=5)
    t.gen_text("login: ", 3, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text(USER, 3, contin=True)
    t.toggle_show_cursor(False)
    t.gen_text("password: ", 4, count=5)
    t.toggle_show_cursor(True)
    t.gen_typing_text("**********", 4, contin=True)
    t.toggle_show_cursor(False)
    agora = datetime.now(TZ).strftime("%d/%m/%Y %H:%M")
    t.gen_text(f"Último login: {agora} em tty1", 6)

    # --- whoami ---
    t.gen_prompt(8, count=5)
    col = t.curr_col
    t.toggle_show_cursor(True)
    t.gen_typing_text(f"{VERMELHO}clea", 8, contin=True)
    t.delete_row(8, col)
    t.gen_text(f"{VERDE}clear{R}", 8, count=3, contin=True)

    st = buscar_stats(ano)

    t.clear_frame()
    t.gen_prompt(1)
    col = t.curr_col
    t.clone_frame(8)
    t.gen_typing_text(f"{VERMELHO}neofet", 1, contin=True)
    t.delete_row(1, col)
    t.gen_text(f"{VERDE}neofetch{R}", 1, contin=True)
    t.gen_typing_text(f" -u {USER}", 1, contin=True)
    t.toggle_show_cursor(False)

    info = f"""
{TITULO} mari-brene@GitHub {R}
-------------------
{CIANO}Nome:      {AMARELO}Maria Clara Brene{R}
{CIANO}Cargo:     {AMARELO}Desenvolvedora Júnior{R}
{CIANO}Local:     {AMARELO}Joinville, SC{R}
{CIANO}Formação:  {AMARELO}ADS (IFTM){R}
{CIANO}Stack:     {AMARELO}Next.js, React, Supabase{R}
{CIANO}Projeto:   {AMARELO}Sistema Leads MVP (CRM + IA){R}

{TITULO} GitHub Stats {R}
-------------------
{CIANO}Rank:           {AMARELO}{st['rank']}{R}
{CIANO}Commits ({ano}): {AMARELO}{st['commits']}{R}
{CIANO}PRs:            {AMARELO}{st['prs']}{R}
{CIANO}Estrelas:       {AMARELO}{st['estrelas']}{R}
{CIANO}Top linguagens: {AMARELO}{st['langs']}{R}
"""
    t.gen_text(info, 3, count=5, contin=True)
    t.gen_prompt(t.curr_row)
    t.toggle_show_cursor(True)
    t.gen_typing_text(
        f"{VERDE}# Obrigada pela visita! Vamos conversar? :D{R}",
        t.curr_row,
        contin=True,
    )
    t.gen_text("", t.curr_row, count=100, contin=True)

    t.gen_gif()


if __name__ == "__main__":
    main()
