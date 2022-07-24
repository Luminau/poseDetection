import cv2
import mediapipe as mp
import time


class PoseDetection():
    def __init__(self, static_image_mode=True,
                 model_complexity=1,
                 smooth_landmarks=False,
                 enable_segmentation=True,
                 smooth_segmentation=False,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.pTime = 0
        self.cTime = 0

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks,
                                      self.enable_segmentation, self.smooth_segmentation, self.min_detection_confidence,
                                      self.min_tracking_confidence)

    def detect_pose(self, image):
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        return results

    def draw_detected_pose(self, image, results):
        if results.pose_landmarks:
            image.flags.writeable = True
            # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style())
        return image

    def draw_fps(self, image):
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)
        return image

    def find_point(self, image, results):
        lm_list = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = image.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                # print(id, cx, cy)
        return lm_list


def main():
    detector = PoseDetection()
    cap = cv2.VideoCapture(0)
    while True:
        success, image = cap.read()
        res = detector.detect_pose(image)
        lm_list = detector.find_point(image, res)
        if len(lm_list) != 0:
            print(lm_list[0])
        image = detector.draw_detected_pose(image, res)
        image = detector.draw_fps(image)

        cv2.imshow("image", image)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
