import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
import time
from pymongo import MongoClient
import speedtest
# To login into mongo container shell
# docker exec -it mongodb bash
# mongosh
# use network
# db.bandwidth.find()
# db.bandwidth.deleteMany({})
client = MongoClient('mongodb://0.0.0.0:27017/')
networkDB = client.network
bandwidthTable = networkDB.bandwidth
speed_test = speedtest.Speedtest()
counter = 0


def bytes_to_mb(bytes):
    KB = 1024  # One Kilobyte is 1024 bytes
    MB = KB * 1024  # One MB is 1024 KB
    return int(bytes/MB)


try:
    while (counter < 1800):
        download_speed = bytes_to_mb(speed_test.download())
        upload_speed = bytes_to_mb(speed_test.upload())
        utc_now = pytz.utc.localize(
            datetime.utcnow()).strftime("%Y-%m-%d:%H-%M-%S")
        bandwidth = {
            "downloadSpeed": download_speed,
            "uploadSpeed":  upload_speed,
            "created_at": datetime.utcnow(),
        }
        print(bandwidth)
        result = bandwidthTable.insert_one(bandwidth)
        counter += 30
        time.sleep(30)
except Exception as e:
    print(e)
