import requests
import threading
import time
temp = "pants" , 500
lock = threading.Lock()

def tempreading():
    re = requests.get("https://allusive.me/temp/",timeout = 30)
    if re.ok:
        return f"{float(re.text):.2f}",200
    else:
        return "idk",500

def tempreadingloop():
    global temp
    while True:
        output = tempreading()
        with lock:
            temp = output
        time.sleep(300)
def recalltemp():
    global temp
    with lock:
        return temp
threading.Thread(target=tempreadingloop, daemon=True).start()