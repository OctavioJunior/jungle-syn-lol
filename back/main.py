from fastapi import FastAPI
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import json
from fastapi.middleware.cors import CORSMiddleware

# Criação da aplicação FastAPI
app = FastAPI()

# Adicionando CORS à aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem (ajuste conforme necessário)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP, como POST, GET, etc.
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


# Modelo de entrada para o nome do campeão
class ChampionRequest(BaseModel):
    champion_name: str

# Função para fazer o scraping
def scrape_champion_synergy(champion_name):
    # Configurando o Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executa em segundo plano
    driver = webdriver.Chrome(options=options)

    try:
        # URL do site baseado no campeão passado
        url = f"https://rankedboost.com/league-of-legends/synergy/{champion_name}/"
        driver.get(url)

        # Aguarde até que a div com o atributo "data-table-id=jungle-synergy" esteja visível
        wait = WebDriverWait(driver, 10)  # Timeout de 10 segundos
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-table-id='jungle-synergy']")))

        # Obtenha o HTML da página
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Localize a div com o atributo "data-table-id"
        target_div = soup.find("div", {"data-table-id": "jungle-synergy"})
        if target_div:
            # Encontre todas as tags <a> dentro da div
            links = target_div.find_all("a", href=True)
            champion_data = {}  # Dicionário para armazenar os campeões e suas porcentagens de vitória

            for link in links:
                href = link["href"]  # Obtenha o href do link
                # Extraia o nome final do link
                if "/league-of-legends/synergy/" in href:
                    champ_name = href.split("/league-of-legends/synergy/")[1].strip("/")

                    # Encontre a div com a class "rbgg-synergy-item-winrate" que contém a taxa de vitória
                    winrate_div = link.find("div", class_="rbgg-synergy-item-winrate")
                    if winrate_div:
                        winrate_text = winrate_div.get_text(strip=True)  # Porcentagem de vitória como texto
                        # Usando regex para encontrar números com ponto decimal
                        winrate = re.search(r'\d+\.\d+', winrate_text)
                        if winrate:
                            champion_data[champ_name] = winrate.group(0)  # Adiciona a taxa de vitória com decimal

            return champion_data  # Retorna o dicionário com os dados
        else:
            return {}  # Retorna um dicionário vazio caso não encontre a div
    finally:
        driver.quit()  # Feche o navegador

# Definindo o endpoint da API
@app.post("/synergy")
async def get_champion_synergy(request: ChampionRequest):
    champion_name = request.champion_name
    data = scrape_champion_synergy(champion_name)
    if data:
        return {"synergies": data}
    else:
        return {"message": "Não foi possível obter os dados ou o campeão não tem sinergias."}

