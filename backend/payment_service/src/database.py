# backend/payment_service/src/database.py
from pymongo import MongoClient
import os

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://52.12.70.97:27017")
client = MongoClient(MONGODB_URI)
db = client.payment_app

def get_payment_collection():
    return db.payments
