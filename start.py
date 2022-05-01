import canvas.config as config
import canvas.log as log
import canvas.image as image
import canvas.place as place
import threading
import datetime
import time

if __name__ == "__main__":
    conf = config.load()
    img = image.load(conf["settings"]["image"])
    size = image.size(conf["settings"]["image"])
    start = conf["settings"]["start"]
    accounts = conf["accounts"]["accounts"]
    placet = {}
    completeIn = int(size[0]*size[1]*conf["settings"]["delay"]/len(conf["accounts"]["accounts"]))
    log.info(f"Starting threads all threads, job will be done in about {datetime.timedelta(seconds =completeIn)} hours.")
    
    for acc in accounts:
        placet[acc] = threading.Thread(target=place.loop, args=(acc,img,size,start))
        placet[acc].start()
        time.sleep(conf["settings"]["offset"])
