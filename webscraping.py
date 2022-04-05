import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}

resposta = requests.get('https://www.funpresp.com.br/fique-por-dentro/cotas/', headers=headers)

soup = BeautifulSoup(resposta.text, 'html.parser')

#print(soup.prettify())

links = soup.find_all('a')

for link in soup.find_all('a'):
    print(link.get('href'))
    link.get('href').split('.')

pass
