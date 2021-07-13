import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_news(url):
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    article = []
    for paragraph in doc.find_all(class_='post__description')[0].findAll('p'):
        article.append(paragraph.text)
    news = '\n'.join(article)
    return news

response = requests.get('https://www.jornaldacidadeonline.com.br/')

doc = BeautifulSoup(response.text, 'html.parser')

rows = []

for item in doc.find_all(class_='widget__data'):
    row = {}
    row['tag'] = item.find(class_ = 'widget__tag').text
    row['date'] = item.find(class_ = 'widget__date').text
    row['title'] = item.find(class_ = 'widget__title').text
    row['link'] = item.find(class_ = 'widget__title')['href']
    rows.append(row)

df = pd.DataFrame(rows)

df['text'] = df.link.apply(scrape_news)

pd.read_csv('jornaldacidade.csv').append(df).drop_duplicates().to_csv('jornaldacidade.csv')
