from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from main import scrape_products

sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(scrape_products, 'interval', minutes=2)
print("clock started :)")
sched.start()