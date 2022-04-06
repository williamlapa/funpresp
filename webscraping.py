import requests
from bs4 import BeautifulSoup

resposta = requests.get('https://www.funpresp.com.br/fique-por-dentro/cotas/')

soup = BeautifulSoup(resposta.text, 'html.parser')

for i in soup.find_all('a'):
    # Testa se a palavra Historico está nos hiperlinks do excel obtidos na página e atribui variável link:
    if 'Historico' in i.get('href'):
      link = i.get('href')