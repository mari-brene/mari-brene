"""Gera dist/stats.svg (tema Dracula) contando também contribuições privadas."""

import os
from datetime import datetime
from html import escape
from zoneinfo import ZoneInfo

import requests

USER = "mari-brene"
ANO = datetime.now(ZoneInfo("America/Sao_Paulo")).year

QUERY = """
query($login: String!, $from: DateTime!) {
  user(login: $login) {
    ano: contributionsCollection(from: $from) {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar { totalContributions }
    }
    pullRequests(states: MERGED) { totalCount }
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
  }
}
"""


def buscar():
    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"login": USER, "from": f"{ANO}-01-01T00:00:00Z"}},
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
        timeout=30,
    )
    r.raise_for_status()
    u = r.json()["data"]["user"]
    a = u["ano"]
    return [
        ("Contribuições", a["contributionCalendar"]["totalContributions"]),
        ("Commits", a["totalCommitContributions"] + a["restrictedContributionsCount"]),
        ("Pull requests", a["totalPullRequestContributions"]),
        ("PRs mesclados", u["pullRequests"]["totalCount"]),
        ("Repositórios", u["repositories"]["totalCount"]),
        ("Estrelas", sum(n["stargazerCount"] for n in u["repositories"]["nodes"])),
    ]


def svg(linhas):
    w, h = 495, 60 + 26 * len(linhas) + 50
    rows = []
    for i, (rotulo, valor) in enumerate(linhas):
        y = 82 + i * 26
        rows.append(
            f'<text x="25" y="{y}" class="l">{escape(rotulo)}:</text>'
            f'<text x="220" y="{y}" class="v">{valor}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
text {{ font-family: 'JetBrains Mono','Fira Code',Consolas,monospace; font-size: 14px; }}
.p {{ fill: #bd93f9; }} .g {{ fill: #50fa7b; }} .f {{ fill: #f8f8f2; }}
.t {{ fill: #282a36; font-weight: 700; }} .l {{ fill: #8be9fd; }} .v {{ fill: #f1fa8c; font-weight: 700; }}
.c {{ fill: #f8f8f2; animation: b 1s steps(1) infinite; }}
@keyframes b {{ 50% {{ opacity: 0; }} }}
</style>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="6" fill="#282a36" stroke="#44475a"/>
<text x="25" y="30" xml:space="preserve"><tspan class="p">mari</tspan><tspan class="f">@</tspan><tspan class="l">github</tspan><tspan class="f"> ~ $ </tspan><tspan class="g">stats</tspan><tspan class="f"> --ano {ANO}</tspan></text>
<rect x="22" y="44" width="150" height="20" fill="#ff79c6"/>
<text x="30" y="59" class="t">GitHub Stats {ANO}</text>
{"".join(rows)}
<rect x="25" y="{h-22}" width="9" height="15" class="c"/>
</svg>
'''


if __name__ == "__main__":
    os.makedirs("dist", exist_ok=True)
    with open("dist/stats.svg", "w", encoding="utf-8") as f:
        f.write(svg(buscar()))
    print("INFO: dist/stats.svg gerado")
