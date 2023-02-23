from pymongo import MongoClient
client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample

movie = db.movies.find_one({'title': '가버나움'})
titles = list(db.movies.find({'rating': movie['rating']}))

for title in titles:
    print(title['title'])

db.movies.update_one({'title': '가버나움'}, {'$set':{'rating' : 0}})