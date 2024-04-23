# main.py

from dotenv import load_dotenv
from scheduler import start_scheduler


def main():
    """Entry point of the application."""
    load_dotenv()
    start_scheduler()


if __name__ == "__main__":
    main()
