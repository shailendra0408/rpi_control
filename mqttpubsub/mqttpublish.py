# this code is on the lowest level .Hadn't added any error handling. Need to improve this in future
# See this link and add other methods https://github.com/eclipse/paho.mqtt.python#single

import paho.mqtt.client as paho
import time
import paho.mqtt.publish as publish



def my_mqtt_publish(topic, payload):
    try:
	
        publish.single(topic, payload, hostname="broker.mqttdashboard.com")
        print "going to publish topic and i am in the other module"
        print "going to publish topic : {0} and payload {1}".format(topic,payload)
    except Exception as e:
        print e.args, e.message

