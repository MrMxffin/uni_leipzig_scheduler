# scheduler.py
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
import telegram_notifier


def run_flask():
    from flask_app import app
    app.run(port=5000)  # Run the proxy service on port 5000


def schedule_task():
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()  # Start Flask in a separate thread
    import almaweb_client
    from os import getenv
    client = almaweb_client.AlmaWebClient(getenv('ALMAWEB_USERNAME'), getenv('ALMAWEB_PASSWORD'))
    formatted_schedule = client.get_schedule()
    if formatted_schedule:
        notifier = telegram_notifier.TelegramNotifier(getenv('TELEGRAM_BOT_TOKEN'), getenv('TELEGRAM_CHAT_ID'))
        notifier.notify(formatted_schedule)
    else:
        print("Failed to retrieve schedule")


def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(schedule_task, 'cron', day_of_week='tue', hour=17, minute=58, second=10)
    scheduler.start()
