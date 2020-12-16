import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from main import scrape_products
import config as cfg

sched = BlockingScheduler()

sched.add_job(scrape_products, 'interval', minutes=cfg.minutes, next_run_time=datetime.datetime.now())

print("clock started at: " + datetime.datetime.now().strftime("%H:%M:%S"))
sched.start()
