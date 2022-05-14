import cv2
import requests
import base64
import numpy as np

while (True):
    res = requests.get("http://192.168.0.122:8000/")
    #img = cv2.imencode('.png', frame)[1].tobytes()
    res = res.text
    jpg = base64.b64decode(res)
    jpg = np.frombuffer(jpg, dtype=np.uint8)
    img = cv2.imdecode(jpg, flags=1)
    cv2.imshow("frame", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break