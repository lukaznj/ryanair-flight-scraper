import os
from dotenv import load_dotenv

from backend import MongoService

load_dotenv()

mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))
