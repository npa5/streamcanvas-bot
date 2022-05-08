from canvas import config,image,place,selfdestruct
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
    
    if settings["self_destruct"] == True:
        selfdestruct.check(settings["channel"], settings["self_destruct_users"])
