import pymongo as pm

url = "mongodb+srv://eLibraryAccount:elibacc@cluster0.l3kpj.mongodb.net/"
client = pm.MongoClient(url)

db = client["eLibrary"]
collection = db["users"]