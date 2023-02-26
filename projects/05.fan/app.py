from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']
    doc = {
        "nickname" : nickname_receive,
        "comment" : comment_receive
    }

    db.fan.insert_one(doc)
    return jsonify({'msg': '저장 완료'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find({},{'_id':False}))
    return jsonify({'result': all_comments})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)