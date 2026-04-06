from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb+srv://jansivijila2004_db_user:PUSRt7r01m2u4pis@cluster0.m8eavcc.mongodb.net/?appName=Cluster0")
    db = client["security_db"]
    return db