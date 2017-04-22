import mosquitto, os, urlparse
import time

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish


url_str = os.environ.get('m11.cloudmqtt:10167', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)


def my_mqtt_publish(topic, payload):
    mqttc.username_pw_set("wbjddnda", "oantKK07oLSg")
    mqttc.connect(url.hostname, url.port)
    mqttc.publish(topic, payload)
    print "going to publish topic : {0} and payload {1}".format(topic,payload)





