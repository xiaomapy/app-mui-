import os
import time
import hashlib
import requests

from uuid import uuid4
from settings import CREATE_QR_URL
from settings import DEVICE_CODE_PATH
from settings import M_DB


def create_device_id(count=1):
    device_list = []
    for i in range(count):
        device_id = "%s,%s" % (time.time(), uuid4())
        device_md5 = hashlib.md5(device_id.encode("utf8"))

        qr_code = device_md5.hexdigest()
        url = "%s,%s" % (CREATE_QR_URL, qr_code)

        res = requests.get(url)
        code_file = os.path.join(DEVICE_CODE_PATH, "%s" % qr_code + ".jpg")

        with open(code_file,"wb") as f:
            f.write(res.content)

        device_list.append({"device_id":qr_code})

        time.sleep(0.11)

    M_DB.devices.insert_many(device_list)

create_device_id(5)