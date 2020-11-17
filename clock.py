#from datetime import timedelta
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from main import scrape_products
import config as cfg

sched = BlockingScheduler()

sched.add_job(scrape_products, 'interval', minutes=cfg.minutes, next_run_time=datetime.datetime.now())

print("clock started at: " + datetime.datetime.now().strftime("%H:%M:%S"))
sched.start()

# TOOD: add prev_run var to output table
# if the new rows are the same as prev_run = 1 rows, then delete prev_run = 1 rows, and call newly added lines prev_run = 1