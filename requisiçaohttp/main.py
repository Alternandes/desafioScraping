# Importações necessárias
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from supabase_py import create_client, Client

# Configurações do Supabase
url = "https://nuvegxwtajlgqflpodkb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im51dmVneHd0YWpsZ3FmbHBvZGtiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0OTA1ODksImV4cCI6MjA0MTA2NjU4OX0.r2FLGzRCsXNWlB8CZn-bjrqwY-8Hw5VsYx3rs3i5R1A"
supabase: Client = create_client(url, key)

# Configurações do Selenium
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL a ser acessada
url = "https://www.vivareal.com.br/venda/ceara/eusebio/lote-terreno_residencial/#onde=,Ceará,Eusébio,,,,,city,BR%3ECeara%3ENULL%3EEusebio,-14.791623,-39.283324,&itl_id=1000183&itl_name=vivareal_-_botao-cta_buscar_to_vivareal_resultado-pesquisa"
driver.get(url)

# Coleta de dados com Selenium
prices = driver.find_elements(By.CLASS_NAME, "property-card__price")
dimensions = driver.find_elements(By.CLASS_NAME, "property-card__detail-value")
addresses = driver.find_elements(By.CLASS_NAME, "property-card__address")

# Extração do texto de cada elemento
all_prices = [price.text for price in prices]
all_dimensions = [dim.text for dim in dimensions]
all_addresses = [address.text for address in addresses]

driver.quit()  # Fechar o navegador após a coleta dos dados

# Inserindo os dados no Supabase
for price, dim, address in zip(all_prices, all_dimensions, all_addresses):
    items = {
        "price": price,
        "dimension": dim,
        "address": address
    }

    try:
        # Inserir os dados na tabela do Supabase
        response = supabase.table("imoveis_usebio").insert(items).execute()
        print(f"Dados inseridos com sucesso: {items}")
    except Exception as e:
        print(f"Erro ao inserir os dados: {e}")
    continue