from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient

application = app = Flask(__name__)
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
        "comment" : comment_receive,
        "use_yn" : 'y'
    }

    db.fan.insert_one(doc)
    return jsonify({'msg': '저장 완료'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_comments = list(db.fan.find())
    return jsonify({'result': dumps(all_comments)})

@app.route("/api/complete", methods=["POST"])
def complete_post():
    print(request)
    id_receive = request.form['id_give']
    print(id_receive)
    db.fan.update_one({'_id':ObjectId(id_receive)},{"$set":{'use_yn':'n'}})
    return jsonify({'msg': '완료처리 되었습니다'})

@app.route("/api/uncomplete", methods=["POST"])
def uncomplete_post():
    print(request)
    id_receive = request.form['id_give']
    print(id_receive)
    db.fan.update_one({'_id':ObjectId(id_receive)},{"$set":{'use_yn':'y'}})
    return jsonify({'msg': '회수처리 되었습니다'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)