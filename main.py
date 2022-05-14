
import face_recognition
import cv2
from imutils import paths, resize
import numpy as np
import pickle
import os
import base64


saved_frames = []
is_motion = False
constants = {"threshold": 100, "frames_before_cops": 40}
saved_image = cv2.imread("data.png")  # To fill in as empty image

def upload_img(name, file):
    folder = os.path.join(os.getcwd(), "user_database", "images", name)
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    with open(os.path.join(folder, str(len(os.listdir()))+".jpg"), "wb") as file_write:
        file_write.write(file.file.read())

def create_encoding_dataset():
    images_dir = list(paths.list_images("user_database" + os.path.sep + "images"))
    enc_list = []
    names_list = []
    for image_path in images_dir:
        name = image_path.split(os.path.sep)[-2]
        rgb_image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image, model="hog")
        face_enc = face_recognition.face_encodings(rgb_image, face_locations)

        for enc in face_enc:
            enc_list.append(enc)
            names_list.append(name)

    enc_pickle = open("enc.pickle", "wb")
    enc_pickle.write(pickle.dumps({"encodings": enc_list, "names": names_list}))
    enc_pickle.close()


def recognize_faces(image_loaded):
    enc_pickle = open("enc.pickle", "rb")
    data = pickle.loads(enc_pickle.read())
    enc_pickle.close()

    rgb_image = cv2.cvtColor(image_loaded, cv2.COLOR_BGR2RGB)
    rgb_image = resize(rgb_image, width=750)

    face_locations = face_recognition.face_locations(rgb_image, model="hog")
    face_enc = face_recognition.face_encodings(rgb_image, face_locations)
    
    names = []

    for enc in face_enc:

        face_matches = face_recognition.compare_faces(data["encodings"], enc)
        name = ""
        
        name_matches = {}

        for (i, match) in enumerate(face_matches):
            if match:
                name = data["names"][i]
                name_matches[name] = name_matches.get(name, 0) + 1
        
        if not name_matches:
            continue

        name = max(name_matches, key=name_matches.get)

        names.append(name)
    
    return names

def compare_images(img1, img2):
    diff = cv2.absdiff(img1, img2)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(diff_gray, (21, 21), 0)
    thresh = cv2.threshold(blur, constants["threshold"], 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("rame", cv2.dilate(thresh, None, iterations=3))
    cv2.waitKey(100)
    return 255 in thresh

def display_image(img_file):

    image_loaded = cv2.imdecode(np.asarray(bytearray(img_file), dtype="uint8"), cv2.IMREAD_COLOR)
    cv2.imshow("frame", image_loaded)
    cv2.waitKey(1)

def process_data(image_file):

    global saved_image, saved_frames, is_motion

    image_loaded = cv2.imdecode(np.asarray(bytearray(image_file), dtype="uint8"), cv2.IMREAD_COLOR)

    compare_results = False

    try:
        compare_results = compare_images(image_loaded, saved_image)
    except:
        saved_image = image_loaded
        compare_results = False

    if compare_results:
        
        cv2.waitKey(100)
        is_motion = True
        
    if len(saved_frames) > 3:
        if not compare_images(image_loaded, saved_frames[-3]):
            is_motion = False

    saved_image = image_loaded
    

    if not is_motion:
        saved_frames = []
    else:
        saved_frames.append(image_loaded)
        if recognize_faces(image_loaded):
            saved_frames = []
            # is_motion = False
            # return is_motion
            is_motion = success()
    
    if len(saved_frames) > constants["frames_before_cops"]:
        # return alert()
        is_motion = alert()

    return is_motion

def is_constants():
    return constants != []

def in_motion():
    return is_motion

def alert():
    return "Call cops"

def success():
    return "Open door"

def return_saved_image():
    ret, buf = cv2.imencode(".jpg", saved_image)
    return base64.b64encode(buf)
    

