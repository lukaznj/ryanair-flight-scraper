import os
import time

import schedule
from dotenv import load_dotenv

from backend import mongo_service
from mongo_service import MongoService
from run import run

if __name__ == "__main__":
    # schedule.every(int(os.getenv("RUN_INTERVAL"))).minutes.do(run, mongo_service)
    schedule.every(30).seconds.do(run, mongo_service)
    while True:
        schedule.run_pending()
        time.sleep(1)