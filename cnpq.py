from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import sys
import csv

kernel_path = os.path.dirname(os.path.abspath(sys.argv[0]))
chromedriver_path = kernel_path.replace('.venv\\Lib\\site-packages', 'chromedriver.exe')

driver = webdriver.Chrome(service=Service(chromedriver_path))
driver.maximize_window()

with open('output.csv', 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    lines = list(csv_reader)
    inicio = int(lines[-1][0])

for id in range(inicio, 20000):
    try:
        url = f"https://dgp.cnpq.br/dgp/espelhogrupo/{id}"
        driver.get(url)

        driver.find_element(By.CSS_SELECTOR, "#identificacao").text
        nome = driver.find_element(By.CSS_SELECTOR, "#tituloImpressao").text.replace('Grupo de pesquisa\n', '')
        data = { "Nome": nome}

        items = driver.find_elements(By.CSS_SELECTOR, ".control-group")
        for item in items:
            key = item.find_element(By.CLASS_NAME, "control-label").text.replace(':','')
            value = item.find_element(By.CLASS_NAME, "controls").text
            data[key]= value

        row = []
        row.append(id)
        row.append(url)
        row.append(data['Nome'])
        row.append(data['Situação do grupo'])
        row.append(data['Data da Situação'])
        row.append(data['Data do último envio'])
        row.append(data['Contato do grupo'])
        row.append(data['Instituição do grupo'])

    except Exception as e:
        row = []
        row.append(id)
        row.append(url)
        row.append('')
        row.append('Não encontrado')
    finally:
        with open('output.csv', 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)