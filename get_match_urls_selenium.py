from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd

#launch url
url = "https://globoesporte.globo.com/futebol/brasileirao-serie-a/"

def get_current_round():
    round_text = driver.find_element_by_class_name("lista-jogos__navegacao--rodada").text
    round_text = round_text.split('ª')[0]
    return int(round_text)

def navigate_rounds(right_direction):
    if right_direction:
        driver.find_element_by_class_name("lista-jogos__navegacao--seta-direita").click()
    else:
        driver.find_element_by_class_name("lista-jogos__navegacao--seta-esquerda").click()
    
    # wait until 'lista-jogos__jogo' is loaded
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "lista-jogos__jogo")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

# create a new Chrome session
driver = webdriver.Chrome()
# maximize window to prevent the GDPR banner appears in front of navigation arrows
driver.maximize_window()
driver.implicitly_wait(30)
driver.get(url)

# GDPR consent
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "cookie-banner-lgpd_accept-button"))).click()

# goes to the first round
current_round = get_current_round()
while current_round != 1:
    navigate_rounds(right_direction = False)
    current_round = get_current_round()

all_matches = []
while True:
    soup = BeautifulSoup(driver.page_source, "lxml")
    matches = soup.find_all("li", class_="lista-jogos__jogo")

    for match in matches:
        match_url_element = match.select_one("a", class_="jogo__transmissao--link", href=True)
        home_team_element = match.find("div", class_="placar__equipes--mandante")
        home_team_abv = home_team_element.find("span", class_="equipes__sigla").text
        home_team_name = home_team_element.find("span", class_="equipes__nome").text

        away_team_element = match.find("div", class_="placar__equipes--visitante")
        away_team_abv = away_team_element.find("span", class_="equipes__sigla").text
        away_team_name = away_team_element.find("span", class_="equipes__nome").text

        match_url = ""
        if match_url_element != None:
            match_url = match_url_element['href']

        match_dic = {'round' : current_round, 
            'home_team_name' : home_team_name, 
            'home_team_abv' : home_team_abv,
            'away_team_name' : away_team_name,
            'away_team_abv' : away_team_abv,
            'url' : match_url
        }

        all_matches.append(match_dic)

    if current_round == 38:
        break;
    else:
        navigate_rounds(True)
        current_round = get_current_round()

driver.close()

df = pd.DataFrame(all_matches)
df.to_csv(r'datasets/urls_matches.csv', index = False)
