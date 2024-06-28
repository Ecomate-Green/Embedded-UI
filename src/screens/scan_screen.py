from kivy.uix.screenmanager import Screen
import qrcode
import os
from dotenv import load_dotenv

load_dotenv()

class ScanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = None
        self.qr_image_path = os.environ.get("QRCODE")
        

    def set_transaction_token(self, token):
        self.token = token
        self.generate_qr_code(token)  # Generate QR code when setting the token

    def on_pre_enter(self, *args):
        # Set QR code image source in the Kivy Image widget before entering the screen
        if self.token:
            self.ids.qr_code_image.source = self.qr_image_path
            self.ids.qr_code_image.reload()  # Ensure the image is reloaded

        
    def generate_qr_code(self, data):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        # Save QR code image to a file
        qr_image.save(self.qr_image_path)