import time

import schedule

from run import run

if __name__ == "__main__":
    schedule.every(int(os.getenv("RUN_INTERVAL"))).minutes.do(run)
    # schedule.every(1).seconds.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
