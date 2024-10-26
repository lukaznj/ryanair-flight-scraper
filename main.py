import time
import os
import schedule

from backend.run import run

if __name__ == "__main__":
    run()

    schedule.every(int(os.getenv("SCRAPE_INTERVAL"))).minutes.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
