import cv2
import math
import time

class EyeTracker:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        self.cap = cv2.VideoCapture(0)
        self.last_update_time = time.time()
        self.direction_text = ""
        self.text_display_start_time = None

    def get_frame_with_detections(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            
            roi_gray = gray[y:y + h, x:x + w]

            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) == 2:
                eye_1 = eyes[0]
                eye_2 = eyes[1]

                left_eye_center = (x + eye_1[0] + eye_1[2] // 2, y + eye_1[1] + eye_1[3] // 2)
                right_eye_center = (x + eye_2[0] + eye_2[2] // 2, y + eye_2[1] + eye_2[3] // 2)

                direction_vector = (right_eye_center[0] - left_eye_center[0], right_eye_center[1] - left_eye_center[1])

                angle = math.degrees(math.atan2(direction_vector[1], direction_vector[0]))

                if angle < -5:
                    new_direction_text = "Left"
                elif angle > 80:
                    new_direction_text = "Right"
                elif -80 <= angle <= 80:
                    if direction_vector[1] < 0:
                        new_direction_text = "Up"
                    else:
                        new_direction_text = "Down"
                else:
                    new_direction_text = ""

                if new_direction_text != self.direction_text or (time.time() - self.last_update_time > 2):
                    self.direction_text = new_direction_text
                    self.last_update_time = time.time()
                    self.text_display_start_time = time.time()

                    print("Eye Direction:", self.direction_text)

        if self.direction_text and (time.time() - self.text_display_start_time < 3):
            text_size, _ = cv2.getTextSize(f"You are looking: {self.direction_text}", cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = frame.shape[0] - 30

            padding = 3  
            bg_rect_top_left = (text_x - padding, text_y - text_size[1] - padding)
            bg_rect_bottom_right = (text_x + text_size[0] + padding, text_y + padding)

            #white background for the text
            cv2.rectangle(frame, bg_rect_top_left, bg_rect_bottom_right, (255, 255, 255), cv2.FILLED)

            # text for the direction on the frame
            cv2.putText(frame, f"You are looking: {self.direction_text}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def release(self):
        
        self.cap.release()
        cv2.destroyAllWindows()
