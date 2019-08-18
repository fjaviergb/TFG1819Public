import json
import time
import paho.mqtt.client as mqtt
import threading
import sys

def on_message (client, userdata, msg):
     global data_IOTA
     first_time()
     data_DICT=json.loads(msg.payload)
     if data_IOTA != {}:
         for key in data_DICT.keys():
             data_IOTA[key].append(data_DICT[key][0])
     if data_IOTA == {}:
         data_IOTA = data_DICT

def first_time():
    global first, bucle
    if first==True:
        bucle.start()
        first=False

def WAIT():
    global stop
    while stop==True:
        time.sleep(10)
        save_FILE()

def save_FILE():
    global data_IOTA
    file_name = str(time.time())
    path='/home/pi/Documents/FJavierGb/DATOSRPICTV/'+file_name+'.txt'
    db = open(path,'a+')
    db.write(str(data_IOTA))
    db.close()
    data_IOTA = {}

def on_connect(client, userdata, flags, rc):
    global MQTT_TOPIC, QOS
    client.subscribe(MQTT_TOPIC, qos=QOS)

def main():
    global stop, bucle, MQTT_TOPIC, QOS
    MQTT_BROKER ="localhost"
    MQTT_TOPIC = "RPICT3V1"
    QOS = 0
    CLEAN_SESSION = True
    client = mqtt.Client('Receptor',CLEAN_SESSION)
    try:
        bucle=threading.Thread(target=WAIT)
        client.on_message = on_message
        client.on_connect = on_connect
        client.connect(MQTT_BROKER, 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        stop = False
        bucle.join()
        print('Interrumpido')
        sys.exit()
data_IOTA = {}
first=True
stop=True
main()
