from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mars", methods=["POST"])
def mars_post():
    # name
    # address
    # size
    name_give = request.form['name_give']
    address_give = request.form['address_give']
    size_give = request.form['size_give']
    print(name_give, address_give, size_give)

    user = db.humens.insert_one({
        'name':name_give,
        'address' : address_give,
        'size' : size_give
        })

    return jsonify({'msg':'저장완료'})

@app.route("/mars", methods=["GET"])
def mars_get():
    mars_data = list(db.humens.find({},{'_id':False}))
    return jsonify({'results' : mars_data})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)