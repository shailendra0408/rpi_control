import mosquitto, os, urlparse

def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print "printing the payload: {0}".format(msg.payload)
    #print str(msg.payload)
    state = str(msg.payload)
    x= state.split(':')
    print "appliance is : {0} and state is : {1}".format (x[0],x[1])
    if state == "OFF":
        print "{0} is OFF".format(msg.topic)
    elif state == "ON":
        print "{0} is ON".format(msg.topic) 

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)

mqttc = mosquitto.Mosquitto()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe


url_str = os.environ.get('m11.cloudmqtt:10167', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)

mqttc.username_pw_set("wbjddnda", "oantKK07oLSg")
mqttc.connect(url.hostname, url.port)

data = mqttc.subscribe("appliance/state",0)


rc = 0
while rc == 0:
    rc = mqttc.loop()
print("rc: " + str(rc))
