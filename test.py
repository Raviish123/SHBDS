import re
import numpy as np
import time
import cv2
import requests

vid = cv2.VideoCapture(0)

ret, frame = vid.read()
time.sleep(3)
ret, frame = vid.read()


while (True):
    ret, frame = vid.read()
    img = cv2.imencode('.jpg', frame)[1].tobytes()
    res = requests.post("http://192.168.0.122:8000/", files = {"file": img})
    print(res.text)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break



