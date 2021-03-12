import requests
from bs4 import BeautifulSoup
import json



class Insert (object):
    def __init__(self, tilte, abstract, body):
        self.tilte = tilte
        self.abstract = abstract
        self.body = body



response = requests.get("https://vnexpress.net/the-thao")
soup = BeautifulSoup(response.content, "html.parser")
# print(soup)

titles = soup.findAll('h3', class_='title-news')
# print(titles)

links = [link.find('a').attrs["href"] for link in titles]
# print(links)

last_j = []

for link in links:
    news = requests.get(link)
    # print(news)

    soup = BeautifulSoup(news.content, "html.parser")
    #print(soup)

    tilte = soup.find("h1", class_="title-detail")
    #print("Tiêu đề: " +tilte.text)

    abstract = soup.find("p", class_="description")
    #print("Mô tả: " +abstract.text)

    body = soup.find("p", class_="Normal")
    #print("Nội dung: " +body.text)

    #dùng thuộc tính dict
    insert = Insert(tilte.text,abstract.text,body.text)
    last_j.append(insert.__dict__)

# Lưu dữ liệu vào file
with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(last_j, file)
