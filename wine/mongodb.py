from pymongo import MongoClient

client = MongoClient('mongodb+srv://(password)@wine-clurster.7vdta7y.mongodb.net/?retryWrites=true&w=majority')
db = client.wine_db
collection=db.wine_project
