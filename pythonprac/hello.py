import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20210829',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 코딩 시작

trs = soup.select('#old_content > table > tbody > tr')
# 제목 : old_content > table > tbody > tr:nth-child(2) > td.title > div > a
# 평점 : old_content > table > tbody > tr:nth-child(2) > td.point 
# 순위 : old_content > table > tbody > tr:nth-child(9) > td:nth-child(1) > img

for tr in trs:
    title = tr.select_one('td.title > div > a')
    if title is not None:
        title = tr.select_one('td.title > div > a').text
        rating = tr.select_one('td.point').text
        ranking = tr.select_one('td:nth-child(1) > img')['alt']
        doc = {
            'title': title, 
            'rating': rating, 
            'ranking': ranking
        }
        db.movies.insert_one(doc)