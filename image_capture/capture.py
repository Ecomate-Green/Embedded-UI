# image_capture.py
import cv2
import requests

class ImageCapture:
    def __init__(self, device_index=0):
        self.capture = cv2.VideoCapture(device_index)

    def read_frame(self):
        ret, frame = self.capture.read()
        return ret, frame

    def send_image_to_server(self, image, url, token):
        resized_image = cv2.resize(image, (256, 256))
        _, img_encoded = cv2.imencode('.jpg', resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])  # High compression
        # Check file size in bytes
        # print(len(img_encoded.tobytes()))

        # # If you want to send the token as bearer
        # headers = {'Authorization': f'Bearer {token}'}
        # response = requests.post(url, files={"file": img_encoded.tobytes()}, headers=headers)

        payload = {"file": img_encoded.tobytes(), "machine_token": token}
        response = requests.post(url, files=payload)
        return response

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()

    def show_frame(self, frame):
        cv2.imshow("Webcam Feed", frame)
        cv2.waitKey(1)  # Required to show the image window
