from django.shortcuts import render
from pymongo import MongoClient
# Create your views here.

# client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000')
client = MongoClient()
db = client.neurall

people = db.people

people.insert_one({"name": "Seny", "age":24})
people.insert_one( {"name": "Toutou", "age": 24, "comp": ["Python", "Java"]} )

for person in people.find():
    print(person)
