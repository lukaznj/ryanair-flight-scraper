import os
import sys

from dotenv import load_dotenv
from backend.mongo_service import MongoService

load_dotenv()

mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))
