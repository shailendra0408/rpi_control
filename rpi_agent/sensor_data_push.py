import requests
import random
import time

while 1:
    try:
        mylist=[22.3,24.5,22.74,27.98,18.03,22.00,21.09,24.89,26.76,21.54]
        sensor_value = random.choice(mylist)
        url = 'http://127.0.0.1:8000/rpi/apitest/v1.0/task_sensor_data?data={0}'.format(sensor_value)
        res = requests.post(url)
        print res.text
        time.sleep(60)
    except requests.ConnectionError:
        print "Server is not up"
        time.sleep(60)
        #@todo - Send mail or message to the Admin
