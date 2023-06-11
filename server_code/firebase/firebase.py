import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
import datetime
import cv2

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


def notification_test():
    # need a name, accuracy, signed url.
    # The topic name can be optionally prefixed with "/topics/".
    topic = 'smd'
    # See documentation on defining a message payload.
    name = "unknown"
    accuracy = 90
    message = messaging.Message(
        data={
            "message": f"Found {'Unknown Object Movement' if name.lower() == 'unknown' else name + ' with ' + str(accuracy) + ' % accuracy'}.",
            "image": "https://storage.googleapis.com/smartmotiondetection123.appspot.com/smd/%3Cgoogle.cloud.firestore_v1.document.DocumentReference%20object%20at%200x000001A59EAD30D0%3E?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=firebase-adminsdk-2idt6%40smartmotiondetection123.iam.gserviceaccount.com%2F20230608%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230608T074824Z&X-Goog-Expires=604800&X-Goog-SignedHeaders=host&X-Goog-Signature=423ed6f89ed7703d0945aa690735c8310fa17d4684320c074fba1b71787accc880e8d4e8a8fb00f5d1f5189d5f96271560b75ed915cead88f884501a6366edf0b0206385acde44bf9c210a77e382ceb665ec3efbeb0fdf85d16f9be05c324399a18c7af9df1820e71e5330674dd9f955549f01edf9f74468affaf9dddddea9d2140979c20a1fe69dfb92b12f3a8029f62bfd72bec51899eeb498b1129efbaf7161250a7bca4921b01df17597035ff3987370a0160a3bed8354cf3bc40e8b64a78e8be713d8a8ae37a1e3fee2c5b8603353030a7d61cf90863180203254f09aed40b3423d70e9e8aac2d99ab116884bae68a28ef159e9b0a5450bef709cad398f"
        },
        topic=topic,
    )
    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


# notification_test()


def trigger_notification(payload: dict):
    # The topic name can be optionally prefixed with "/topics/".
    topic = 'smd'

    # See documentation on defining a message payload."
    name = payload.get("name")
    accuracy = payload.get("accuracy")
    message = messaging.Message(
        data={
            "message": f"Found {'Unknown Object Movement' if name.lower() == 'unknown' else name + ' with ' + str(accuracy) + ' % accuracy'}.",
            "image": payload.get("image"),
        },
        topic=topic,
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


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

    img_url = upload_image(image, f'smd/{doc_ref.id}')

    if img_url is not None:
        data = {
            'name': name,
            'accuracy': 0 if name.lower() == 'unknown' else accuracy,
            'image': img_url,
            'timestamp': firestore.SERVER_TIMESTAMP
        }
        # adding document to firestore.
        doc_ref.set(data)
        # triggering notification to devices with topic name "smd"
        trigger_notification(data)
        print("notification sent..")
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
