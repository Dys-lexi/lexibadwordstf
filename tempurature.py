import requests
import threading
import time
temp = {"temp":0,"lastupdate":0} , 500
lock = threading.Lock()

def tempreading():
    re = requests.get("https://allusive.me/temp/",timeout = 30)
    if re.ok:
        return {"temp":float(f"{float(re.text):.2f}"),"lastupdate":int(time.time())} ,200
    else:
        return None

def tempreadingloop():
    global temp
    while True:
        try:
            output = tempreading()
            with lock:
                temp = output or temp
                # print(temp)
        except:
            pass
        time.sleep(60)   
def recalltemp():
    global temp
    with lock:
        return temp
threading.Thread(target=tempreadingloop, daemon=True).start()