#Samplecode
import time
import logging
import serial 
import codecs
import sys
import binascii

i = 0 

def openBTSerialData(port, speed):
    BTSerData = serial.Serial(port, speed)
    BTData = BTSerData.readline()
    print(BTData)
    time.sleep(1)
    return BTData 

def print_hex(packet):

    size = len(packet)
    for i in range(size):
        sys.stdout.write("{0} ".format(hex(packet[i])))
    print ("\r\n")
    print(" ---- ")
    return



while i < 10:
    data = openBTSerialData("/dev/tty.Bluetooth-Incoming-Port", 9600)
    data = data.rstrip()
    print_hex(data)
    if data[0] == 0x02:
        print("valid start of the string")
    else:
        print("unvalidated data, capture again")

    print  ("Data at byte 18 in hex format is ",(hex(data[18])))
    print  ("Data at byte 18 in binary format is ",(bin(data[18])))
    print  ("bit at 0th position of byte 18 is ")
    
    if (data[18]) & 0x40:
        print ("Testing")
        print ("Not Set")
        print ("data at bit 26 i.e. thickness is", dec(data[25]))
    else:
        print ("Set")
        print ("data at bit 26 i.e. thickness is", hex(data[25]))

    #printing complete packets
    stringsize = len(data)
    print ("length of the packet is", stringsize)

    for i in range(stringsize):
        print (hex(data[i]))
        i = i+1


    
    




#while i < 6:
#    i = i+1
#    print (i)
#    if i == 6: 
#        print ("done receiving data as per allowed number,exiting") 
#    BTSer = serial.Serial("/dev/tty.Bluetooth-Incoming-Port", 9600)
#    x = BTSer.readline()
#    print(x) 
#    y = "This is serial data"
#    print (y)




