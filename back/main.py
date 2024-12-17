from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------
# Configurações da aplicação FastAPI
# ------------------------------
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de entrada para o endpoint
class ChampionRequest(BaseModel):
    champion_name: str

# ------------------------------
# Configurações globais
# ------------------------------
BASE_URL = "https://rankedboost.com/league-of-legends/synergy/"
SELENIUM_TIMEOUT = 10  # Tempo de espera do Selenium em segundos

# ------------------------------
# Função: Configurar o WebDriver
# ------------------------------
def get_webdriver():
    """Inicializa o WebDriver do Selenium com as configurações necessárias."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executa em segundo plano
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

# ------------------------------
# Função: Realizar scraping no site
# ------------------------------
def scrape_champion_synergy(champion_name: str):
    """
    Realiza scraping no site para obter as sinergias do campeão.
    
    Args:
        champion_name (str): Nome do campeão a ser pesquisado.

    Returns:
        dict: Dicionário com campeões e suas respectivas porcentagens de vitória.
    """
    driver = get_webdriver()
    url = f"{BASE_URL}{champion_name}/"

    try:
        driver.get(url)
        # Espera o carregamento da tabela alvo
        wait = WebDriverWait(driver, SELENIUM_TIMEOUT)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-table-id='jungle-synergy']")))

        # Extrai o HTML e analisa com BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        return extract_synergy_data(soup)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante o scraping: {str(e)}")

    finally:
        driver.quit()  # Encerra o WebDriver

# ------------------------------
# Função: Extrair dados da sinergia
# ------------------------------
def extract_synergy_data(soup):
    """
    Extrai os dados de sinergia do HTML da página.

    Args:
        soup (BeautifulSoup): Objeto BeautifulSoup com o HTML analisado.

    Returns:
        dict: Dicionário com campeões e suas porcentagens de vitória.
    """
    champion_data = {}
    target_div = soup.find("div", {"data-table-id": "jungle-synergy"})

    if target_div:
        links = target_div.find_all("a", href=True)
        for link in links:
            champ_name = extract_champion_name(link["href"])
            winrate = extract_winrate(link)

            if champ_name and winrate:
                champion_data[champ_name] = winrate

    return champion_data

# ------------------------------
# Funções Auxiliares
# ------------------------------
def extract_champion_name(href: str):
    """
    Extrai o nome do campeão da URL.

    Args:
        href (str): URL do link.

    Returns:
        str | None: Nome do campeão, se encontrado.
    """
    match = re.search(r'/league-of-legends/synergy/([^/]+)/', href)
    return match.group(1) if match else None

def extract_winrate(link):
    """
    Extrai a porcentagem de vitória de um link.

    Args:
        link: Tag HTML do link.

    Returns:
        str | None: Porcentagem de vitória, se encontrada.
    """
    winrate_div = link.find("div", class_="rbgg-synergy-item-winrate")
    if winrate_div:
        winrate_text = winrate_div.get_text(strip=True)
        winrate = re.search(r'\d+\.\d+', winrate_text)
        return winrate.group(0) if winrate else None
    return None

# ------------------------------
# Endpoint da API
# ------------------------------
@app.post("/synergy")
async def get_champion_synergy(request: ChampionRequest):
    """
    Endpoint para retornar as sinergias de um campeão específico.
    """
    champion_name = request.champion_name.strip().lower().replace(" ", "-")  # Ajuste do nome para a URL
    data = scrape_champion_synergy(champion_name)

    if data:
        return {"synergies": data}
    else:
        raise HTTPException(status_code=404, detail="Campeão não encontrado ou sem sinergias disponíveis.")
