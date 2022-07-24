import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import cv2

interpreter = tf.lite.Interpreter(model_path="lite-model_movenet_singlepose_lightning_tflite_float16_4.tflite")
interpreter.allocate_tensors()

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()

    # reshape image
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192, 192)
    input_image = tf.cast(img, dtype=tf.uint8)

    # setup input and output
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # make perdiction
    interpreter.set_tensor(input_details[0]['index'], np.array(input_image))
    interpreter.invoke()
    keypoints_with_score = interpreter.get_tensor(output_details[0]['index'])



    left_shoulder = keypoints_with_score[0][0][5]
    left_shoulder = np.array(left_shoulder[:2]*[480,640]).astype(int)
    print(left_shoulder)

    cv2.imshow("moveNet LT", frame)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        exit()

cap.release()
cv2.destroyAllWindows()
