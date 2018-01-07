import paho.mqtt.client as paho
import time
 
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))
 
client = paho.Client()
client.on_publish = on_publish
client.connect("broker.mqttdashboard.com", 1883)
client.loop_start()



def my_mqtt_publish(topic, payload):
    try:
        (rc, mid) = client.publish(topic, payload, qos=2)
        time.sleep(1)
        print "going to publish topic and i am in the other module"
        print "going to publish topic : {0} and payload {1}".format(topic,payload)
    except Exception as e:
        print e.args, e.message

#while True:
 #   temperature = 23 
  #  (rc, mid) = client.publish(, str(temperature), qos=1)
   # time.sleep(1)
