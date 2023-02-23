from pymongo import MongoClient
client = MongoClient('mongodb+srv://yungsu2391:1234@sample.9vspvll.mongodb.net/?retryWrites=true&w=majority')
db = client.sample

user = db.humens.delete_one({'name':'yongso'})

print(user)