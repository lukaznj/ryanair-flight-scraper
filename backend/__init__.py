import os
from dotenv import load_dotenv

from backend.mongo_service import MongoService

load_dotenv("../.env")

print("Connecting to", os.getenv("MONGO_DB_NAME") ,os.getenv("MONGO_URI"))

mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))

