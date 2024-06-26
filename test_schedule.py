import schedule
import time

def job():
    print("Hello, world!")

schedule.every(1).minute.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)