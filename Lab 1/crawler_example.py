import requests
from bs4 import BeautifulSoup



response = requests.get("https://vnexpress.net/the-thao")
soup = BeautifulSoup(response.content, "html.parser")
print(soup)

titles = soup.findAll('h3', class_='title-news')
print(titles)

links = [link.find('a').attrs["href"] for link in titles]
print(links)

for link in links:
    news = requests.get(link)
    print(news)
    
    soup = BeautifulSoup(news.content, "html.parser")
    print(soup)
    
    title = soup.find("h1", class_="title-detail")
    print("Tiêu đề: " +title.text)

    abstract = soup.find("p", class_="description")
    print("Mô tả: " +abstract.text)
    
    body = soup.find("p", class_="Normal")
    print("Nội dung: " +body.text)