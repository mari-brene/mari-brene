"""Gera dist/langs.svg (tema Dracula) com as linguagens mais usadas."""

import os
from collections import Counter
from html import escape

import requests

USER = "mari-brene"
TOP = 6
IGNORAR = {"mari-brene"}  # repositório do próprio perfil

QUERY = """
query($login: String!) {
  user(login: $login) {
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100) {
      nodes {
        name
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def buscar():
    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"login": USER}},
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}"},
        timeout=30,
    )
    r.raise_for_status()
    tamanhos, cores = Counter(), {}
    for repo in r.json()["data"]["user"]["repositories"]["nodes"]:
        if repo["name"] in IGNORAR:
            continue
        for e in repo["languages"]["edges"]:
            tamanhos[e["node"]["name"]] += e["size"]
            cores[e["node"]["name"]] = e["node"]["color"] or "#6272a4"
    total = sum(tamanhos.values()) or 1
    return [(n, t / total * 100, cores[n]) for n, t in tamanhos.most_common(TOP)]


def svg(langs):
    w = 495
    h = 60 + 26 * len(langs) + 50
    barra_x, barra_w = 170, 230
    rows = []
    for i, (nome, pct, cor) in enumerate(langs):
        y = 82 + i * 26
        rows.append(
            f'<text x="25" y="{y}" class="l">{escape(nome)}</text>'
            f'<rect x="{barra_x}" y="{y-10}" width="{barra_w}" height="10" rx="2" fill="#44475a"/>'
            f'<rect x="{barra_x}" y="{y-10}" width="{max(barra_w * pct / 100, 2):.1f}" height="10" rx="2" fill="{cor}"/>'
            f'<text x="{barra_x + barra_w + 12}" y="{y}" class="v">{pct:.1f}%</text>'
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
<text x="25" y="30" xml:space="preserve"><tspan class="p">mari</tspan><tspan class="f">@</tspan><tspan class="l">github</tspan><tspan class="f"> ~ $ </tspan><tspan class="g">linguagens</tspan><tspan class="f"> --top {TOP}</tspan></text>
<rect x="22" y="44" width="190" height="20" fill="#ff79c6"/>
<text x="30" y="59" class="t">Linguagens mais usadas</text>
{"".join(rows)}
<rect x="25" y="{h-22}" width="9" height="15" class="c"/>
</svg>
'''


if __name__ == "__main__":
    os.makedirs("dist", exist_ok=True)
    with open("dist/langs.svg", "w", encoding="utf-8") as f:
        f.write(svg(buscar()))
    print("INFO: dist/langs.svg gerado")
