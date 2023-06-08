import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import datetime
import cv2

import threading
import time

# Use a service account.
# path = "firebase-adminsdk-2idt6-de6f4a615e.json"
path = "C:/Users/venkat/PycharmProjects/Sem_4_Project/server_code/firebase/firebase-adminsdk-2idt6-de6f4a615e.json"
cred = credentials.Certificate(path)

firebaseConfig = {
    "apiKey": "AIzaSyDbo04FjEP36YLRUyOnw-os1deZDDbKgSs",
    "authDomain": "smartmotiondetection123.firebaseapp.com",
    "databaseURL": "https://smartmotiondetection123-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "smartmotiondetection123",
    "storageBucket": "smartmotiondetection123.appspot.com",
    "messagingSenderId": "327758864559",
    "appId": "1:327758864559:web:71aa5350ee9cb0cdc4b45a",
    "measurementId": "G-THZDV6150G"
}
# Initialize firebase
app = firebase_admin.initialize_app(cred)
# getting firestore reference
db = firestore.client()
# reference for the firebase cloud storage
bucket = storage.bucket("smartmotiondetection123.appspot.com")


def image_url(name, image):
    # client = storage.Client()
    # bucket = client.get_bucket('smartmotiondetection123.appspot.com')
    blob = bucket.blob('testfile.txt')
    blob.upload_from_string('this is test content!')
    return True


def upload_image(mat_image, destination_path):
    _, buffer = cv2.imencode('.jpg', mat_image)
    image_bytes = buffer.tobytes()

    # Upload file to Cloud Storage
    blob = bucket.blob(destination_path)
    # blob.upload_from_filename(file_path)
    blob.upload_from_string(image_bytes, content_type='image/jpeg')

    # todo: change the signed url to public url.
    # Generate a signed URL for downloading the file
    download_url = blob.generate_signed_url(
        version='v4',
        expiration=datetime.timedelta(days=7),  # Set the URL to expire in 15 minutes
        method='GET')

    # download_url = blob.public_url

    return download_url


def send_message(name, accuracy, image):
    doc_ref = db.collection('smd').document()

    # doc_ref.id this will give the id of the document.
    # todo: upload the image and get its path
    if image_url(doc_ref.id, image):
        doc_ref.set({
            'name': name,
            'accuracy': accuracy,
            'image': upload_image(image,f'smd/{doc_ref}'),
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    print(doc_ref.id)


# send_message(90, "test", None)

# url = upload_image(cv2.imread('test1.PNG'), 'res/img3.jpg')

# print('Image uploaded successfully. Download URL:', url)


#
# # inserting data (create) we also have add() --> don't require doc name, update()
# doc_ref = db.collection(u'users').document(u'alovelace')
# # doc_ref.delete()
# # doc_ref.set({
# #     u'first': u'Venkata Bhagavan',
# #     u'last': u'Devarapalli',
# #     u'born': 2000,
# #     'timestamp':firestore.SERVER_TIMESTAMP
# # })
#
# # docs = db.collection("users").get()
# # for doc in docs:
# #     # doc = doc_ref.get()
# #     if doc.exists:
# #         print(f'{doc.id} ==> {doc.to_dict()}')
#
#
# # Create an Event for notifying main thread.
# callback_done = threading.Event()
#
# # Create a callback on_snapshot function to capture changes
# def on_snapshot(doc_snapshot, changes, read_time):
#     for doc in doc_snapshot:
#         print(f'Received document snapshot: {doc.id}-->{doc.to_dict()}')
#         print(f'read time : {read_time}')
#         print(f'changes : {changes}')
#     callback_done.set()
#
# # doc_ref = db.collection(u'cities').document(u'SF')
#
# # Watch the document
# doc_watch = doc_ref.on_snapshot(on_snapshot)
#
# callback_done.wait() # this method will stop main thread until it fetch for one time.
#
# # while True:
# #     if input().lower() in ['stop', 's', 'quit', 'q']:
# #         # doc_watch.unsubscribe()
# #
# #         break
