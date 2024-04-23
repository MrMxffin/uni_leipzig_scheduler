# scheduler.py

import threading
from apscheduler.schedulers.blocking import BlockingScheduler
import telegram_notifier


def run_flask():
    """Start the Flask server."""
    from flask_app import app
    app.run(port=5000)


def schedule_task():
    """Schedule the task."""
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    try:
        import almaweb_client
        from os import getenv
        client = almaweb_client.AlmaWebClient(getenv('ALMAWEB_USERNAME'), getenv('ALMAWEB_PASSWORD'))
        formatted_schedule = client.get_schedule()
        if formatted_schedule:
            notifier = telegram_notifier.TelegramNotifier(getenv('TELEGRAM_BOT_TOKEN'), getenv('TELEGRAM_CHAT_ID'))
            notifier.notify(formatted_schedule)
        else:
            print("Failed to retrieve schedule")
    except Exception as e:
        print(f"Error in scheduling task: {e}")


def start_scheduler():
    """Start the scheduler."""
    scheduler = BlockingScheduler()
    scheduler.add_job(schedule_task, 'cron', day_of_week='sun', hour=12, minute=0, second=0)
    scheduler.start()
