import cv2
import requests

class ImageCapture:
    def __init__(self, device_index=1):
        # Attempt to open the specified device index
        self.capture = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)

        # Check if the device is opened successfully
        if not self.capture.isOpened():
            print(f"USB camera not found at index {device_index}, falling back to the default camera.")
            # Attempt to open the default camera
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            # Raise an exception if the default camera also fails to open
            if not self.capture.isOpened():
                raise Exception("Could not open video device")
        
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
        ret, frame = self.capture.read()
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
            return response
        except Exception as e:
            print(f"An error occurred while sending the image: {e}")
            return None

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def show_frame(self, frame):
        cv2.imshow("Webcam Feed", frame)
        cv2.waitKey(1)  # Required to show the image window
