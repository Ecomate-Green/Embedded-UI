from kivy.uix.screenmanager import Screen
import qrcode

class ScanScreen(Screen):
    def set_transaction_token(self, token):
        self.token = token

    def on_enter(self):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=4,
        )
        qr.add_data(self.token)
        qr.make(fit=True)
        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        # Save QR code image to a file
        qr_image_path = "assets/qrcodes/qrcode.png"
        qr_image.save(qr_image_path)
        # Set QR code image source in the Kivy Image widget
        self.ids.qr_code_image.source = qr_image_path
        self.ids.qr_code_image.reload()  # Ensure the image is reloaded
