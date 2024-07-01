import cv2
import requests
import logging
from dotenv import load_dotenv
import os
from src.utils import handle_error

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageCapture:
    def __init__(self, device_index=1):
        device = os.getenv("DEVICE")
        api_preference = cv2.CAP_V4L2 if device == "rasp" else cv2.CAP_DSHOW

        self.capture = self._initialize_capture(device_index, api_preference)
        if not self.capture:
            logger.error("Failed to initialize the video capture device.")
            raise Exception("Could not open video device, check your .env or the camera device index")

    def _initialize_capture(self, device_index, api_preference):
        capture = cv2.VideoCapture(device_index, api_preference)
        if capture.isOpened():
            logger.info(f"Using camera at index {device_index}")
            return capture
        else:
            logger.warning(f"Camera not found at index {device_index}, attempting to open the default camera.")
            capture = cv2.VideoCapture(0, api_preference)
            if capture.isOpened():
                logger.info("Using default camera at index 0")
                return capture
            else:
                logger.error("Default camera could not be opened.")
                return None
            
        
    def get_camera_index(self):
        # Attempt to open the USB camera (usually at index 1)
        usb_camera_index = 1
        cap = cv2.VideoCapture(usb_camera_index)

        if cap.isOpened():
            print(f"Using USB camera at index {usb_camera_index}")
            return usb_camera_index
        else:
            print(f"USB camera not found, falling back to laptop camera at index 0")
            return 0  # Default to laptop camera

    def read_frame(self):
        if not self.capture:
            logger.error("Capture device is not initialized.")
            return False, None
        ret, frame = self.capture.read()
        if not ret:
            logger.error("Failed to read frame from capture device.")
        return ret, frame

    def send_image_to_server(self, image, url, token, api_key):
        try:
            resized_image = cv2.resize(image, (256, 256))
            _, img_encoded = cv2.imencode('.jpg', resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # High compression
            # Check file size in bytes
            # print(len(img_encoded.tobytes()))

            # # If you want to send the token as bearer
            # headers = {'Authorization': f'Bearer {token}'}
            # response = requests.post(url, files={"file": img_encoded.tobytes()}, headers=headers)

            params = { 
                "machine_token": token, 
                "api_key": api_key
            }
            files = {
                'image': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')
            }
            response = requests.post(url, params=params, files=files)
            response.raise_for_status()  # Raise an error for bad responses
            logger.info("Image successfully sent to server.")
            return response
        except requests.RequestException as req_err:
            logger.error(f"Request error occurred while sending the image: {req_err}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending the image: {e}")
        return None

    def release(self):
        if self.capture:
            self.capture.release()
            cv2.destroyAllWindows()
            logger.info("Capture device released and all windows destroyed.")

    def show_frame(self, frame):
        if frame is not None:
            cv2.imshow("Webcam Feed", frame)
            cv2.waitKey(1)
        else:
            logger.error("Cannot show frame because it is None.")