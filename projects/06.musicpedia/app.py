from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver


client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/music", methods=["POST"])
def music_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    # https://beomi.github.io/gb-crawling/posts/2017-02-27-HowToMakeWebCrawler-With-Selenium.html
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)
    driver = webdriver.Chrome('/Users/yungsu2391naver.com/Downloads/chromedriver_mac64/chromedriver')
    driver.get(url_receive)
    driver.implicitly_wait(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    ogtitle = soup.select_one('span.title').text.replace('곡명', '')
    ogdesc = soup.select_one('#content > div.end_section.section_lyrics > div > p').text
    ogimage = soup.select_one('#content > div.summary_section > div > div.summary_thumb > img')['src']
    # # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.

    doc = {
        'title' : ogtitle,
        'desc' : ogdesc,
        'image' : ogimage,
        'comment' : comment_receive,
        'star': star_receive
    }

    db.musics.insert_one(doc)

    return jsonify({'msg':'저장완료'})

# 데코레이터라고 불림
@app.route("/music", methods=["GET"])
def music_get():
    result = list(db.musics.find({},{'_id': False}))
    print(result)
    return jsonify({
        'result':result
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
