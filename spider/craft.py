from pymongo import MongoClient

MongoConn = MongoClient(host="119.29.184.167", port=27017)['yangqh']
collection = MongoConn['init']

print (collection.find()[1])