import pandas as pd
from requests_html import HTML, HTMLSession

#launch url
url = "https://globoesporte.globo.com/futebol/brasileirao-serie-a/"

# Fetch a web page
session = HTMLSession()
r = session.get(url)
r.html.render(timeout = 60)

teams = r.html.find("table.tabela__equipes", first=True)
points = r.html.find("table.tabela__pontos", first=True)

teams_df = pd.read_html(teams.html, header = 0)[0]
classification_df = pd.read_html(points.html, header = 0)[0]

classification_df.drop('ÚLT. JOGOS', axis=1, inplace=True)
classification_df.insert(0, "Classificacao", teams_df[['Classificação']])
classification_df.insert(1, "Team", teams_df[['Classificação.1']])
