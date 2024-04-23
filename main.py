# main.py
from dotenv import load_dotenv
from scheduler import start_scheduler

load_dotenv()

if __name__ == "__main__":
    start_scheduler()