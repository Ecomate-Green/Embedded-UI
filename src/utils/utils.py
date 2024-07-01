# utils.py
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_exception(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {function.__name__}: {e}")
            show_popup("Error", "An unexpected error occurred.")
            raise e  # Re-raise the exception if needed
    return wrapper


def handle_error(context, exception):
    error_msg = f"{context}: {exception}"
    logger.error(error_msg, exc_info=True)
    show_popup("Error", error_msg)

def show_popup(title, message, size_hint=(0.8, 0.4)):
    popup = Popup(title=title, content=Label(text=message), size_hint=size_hint)
    popup.open()