import time
import importlib
import schedule
import sys
from core.sender import send_payload
from core.config import TASKS

def load_function(path):
    module_name, func_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, func_name)

def schedule_task(task):
    func = load_function(task["handler"])
    def job():
        payload = func()
        send_payload(task["webhook"], payload)

    # Явный вывод в stdout
    sys.stdout.write(f"📌 Scheduled {task['name']} every {task['interval']} seconds\n")
    sys.stdout.flush()

    job()
    schedule.every(task["interval"]).seconds.do(job)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    for task in TASKS:
        schedule_task(task)
    sys.stdout.write("🚀 Scheduler started\n")
    sys.stdout.flush()
    run_scheduler()
