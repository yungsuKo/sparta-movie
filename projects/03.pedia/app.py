from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']
    
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']

    doc = {
        'title' : ogtitle,
        'desc' : ogdesc,
        'image' : ogimage,
        'comment' : comment_receive,
        'star': star_receive
    }

    db.movies.insert_one(doc)

    return jsonify({'msg':'저장완료'})

@app.route("/movie", methods=["GET"])
def movie_get():
    result = list(db.movies.find({},{'_id': False}))
    print(result)
    return jsonify({
        'result':result
    })

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
