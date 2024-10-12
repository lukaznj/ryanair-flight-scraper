import os
import time

import schedule
from dotenv import load_dotenv

from mongo_service import MongoService
from run import run

load_dotenv()
mongo_service = MongoService(os.getenv("MONGO_URI"), os.getenv("MONGO_DB_NAME"))

if __name__ == "__main__":
    schedule.every(int(os.getenv("RUN_INTERVAL"))).minutes.do(run, mongo_service)
    # schedule.every(30).seconds.do(run, mongo_service)
    while True:
        schedule.run_pending()
        time.sleep(1)
