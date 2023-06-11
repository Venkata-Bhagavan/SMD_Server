import time
import threading
# from firebase import firebase
import firebase.firebase as fb

INSERTION_TIME = 2
HIGH_PRIORITY_TIME = 20
LOW_PRIORITY_TIME = 60
HIGH_ALERT_TIMER, LOW_ALERT_TIMER = HIGH_PRIORITY_TIME, LOW_PRIORITY_TIME

HIGH_ALERT_DATA = {}
LOW_ALERT_DATA = {}


def __start_high_alert_timer__():
    """This method needs to be called in a thread."""
    global HIGH_ALERT_TIMER
    HIGH_ALERT_TIMER = 0
    while HIGH_ALERT_TIMER < HIGH_PRIORITY_TIME:
        time.sleep(1)
        HIGH_ALERT_TIMER += 1


def __start_low_alert_timer__():
    """This method needs to be called in a thread."""
    global LOW_ALERT_TIMER
    LOW_ALERT_TIMER = 0
    while LOW_ALERT_TIMER < LOW_PRIORITY_TIME:
        time.sleep(1)
        LOW_ALERT_TIMER += 1


def send_high_alert(name, accuracy, image):
    def send_message():
        if len(HIGH_ALERT_DATA) > 0:
            max_pair = sorted(HIGH_ALERT_DATA.items(), key=lambda x: x[1][0])[0]
            # todo: send the message using firebase
            fb.send_message(name, accuracy, image)
            print("high alert triggerd")
            print(f"high alert --:{max_pair[0]} -- {max_pair[1][1]}")
            HIGH_ALERT_DATA.clear()
            pass
        else:
            print(f"high alert :{name} -- {accuracy}")

    global HIGH_ALERT_TIMER
    if HIGH_PRIORITY_TIME == HIGH_ALERT_TIMER:
        if len(HIGH_ALERT_DATA) == 0:
            HIGH_ALERT_DATA[name] = (1, accuracy, image)
        send_message()

        threading.Thread(target=__start_high_alert_timer__).start()
    elif HIGH_ALERT_TIMER >= HIGH_PRIORITY_TIME - INSERTION_TIME:
        count = 1 if HIGH_ALERT_DATA.get(name) is None else HIGH_ALERT_DATA.get(name)[0] + 1
        HIGH_ALERT_DATA[name] = (count, accuracy, image)


def send_low_alert(name, accuracy, image):
    # pass
    # print(f'low alert : {name} -- {accuracy}')
    #
    def send_message():
        if len(LOW_ALERT_DATA) > 0:
            max_pair = sorted(LOW_ALERT_DATA.items(), key=lambda x: x[1][0])[0]
            # todo: send the message using firebase
            fb.send_message(name, accuracy, image)
            print("low alert triggerd")
            print(f"high alert --:{max_pair[0]} -- {max_pair[1][1]}")
            LOW_ALERT_DATA.clear()
            pass
        else:
            print(f"high alert :{name} -- {accuracy}")

    global LOW_ALERT_TIMER
    if LOW_PRIORITY_TIME == LOW_ALERT_TIMER:
        if len(LOW_ALERT_DATA) == 0:
            LOW_ALERT_DATA[name] = (1, accuracy, image)
        send_message()

        threading.Thread(target=__start_low_alert_timer__).start()
    elif LOW_ALERT_TIMER >= LOW_PRIORITY_TIME - INSERTION_TIME:
        count = 1 if LOW_ALERT_DATA.get(name) is None else LOW_ALERT_DATA.get(name)[0] + 1
        LOW_ALERT_DATA[name] = (count, accuracy, image)
