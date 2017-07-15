# rpi home control - A small end-to-end DIY project (more information on my blog [LINK] (http://shail1501.blogspot.in/))
Home Automation using RPI. One of the best use cases of IOT(Internet of Things). This is one of the projects fro my wishlist. The main functionality of this project is that its a end-to-end solution which include following components

1. Hardware 
    1. RPI as a gateway hardware running a agent script which receive data from cloud using MQTT  / Push messages (yet to implememt)
    2. End nodes - If number of appliance which you want to control are all over the home, than your RPI will be a central gateway which receive commands and then distribute them to end-nodes using Bluetooth as a communication medium (This has not been implemented as of now)
2. Software  
    1. Web-application which allow user creation. Right now, it is done by Admin, but i want to release it as a web-application in which any one can login, set-up his appliaces, do the same in the RPI or download a configuration file on RPI and he is done. Also as of now, MQTT is done using a open broker which is not safe. Ceratin other features like encryption of data which is send to the MQTT broker, more error handling, more  MQTT features need to be implemented. Hive MQTT or Paho MQTT broker can also be installed on the own server. 
    2. Android application. Presently i am working on the API's so that we can develop a android application using the same. As of now, not much emphasis is given to security but yes that is one of the main features, that i need to implement. 

# Components used 
1. Hardware 
    1. RPI
    2. Ethernet for internet communication 
    3. 12 V controlled 230V rated  relay to control the AC appliance 
    4. Arduino Uno as end -sensor node
    5. HC-05 bluetooth module 

2. Web -application 
    1. Digital Ocean as server provider 
    2. Python 
    3. Flask - didn't used most the features, but it seems to be a good python framework to start with [LINK] (http://flask.pocoo.org/)
    4. Nginx 
    5. Jinja2 as a templating engine
    6. Mysql 
    7. MDL - Material design lite [LINK](https://getmdl.io/)
    

# future improvememts
Future aim is to provide
1. Web application, where some one can login and set-up his / her devices. 
2. Implement security features - Get the SSL certaificate install on the server.
3. Install the MQTT Broker on own server. 
4. Get the API's implementation done with security features 
5. Get OAuth implemented.
6. Get the multiple end-nodes connected to the gateway using bluetooth
7. Provide the gateway code as a package which can be installed. 

