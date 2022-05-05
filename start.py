import canvas.config as config
import canvas.log as log
import canvas.image as image
import canvas.account as account
import canvas.place as place
import threading
import datetime
import time

if __name__ == "__main__":
    conf = config.load()
    settings = conf["settings"]
    if settings["mode"] != "void":
        img = image.load(settings["image"])
    else:
        img = None
    accounts = conf["accounts"]["accounts"]
    placet = {}
    token = {}
    
    for i in range(len(accounts)):
        placet[i] = threading.Thread(target=place.loop, args=(accounts[i],img,settings))
        placet[i].start()
        time.sleep(conf["settings"]["offset"])
