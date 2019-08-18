import serial
import json
import time
import paho.mqtt.client as mqtt

def main():
    MQTT_BROKER = "localhost"
    MQTT_TOPIC = "RPICT3V1"
    QOS = 0
    client = mqtt.Client('Emisor',clean_session=True)
    client.connect(MQTT_BROKER, 1883, 60) #HOST + Puerto + KeepAlive;
    client.loop_start()
    ser = serial.Serial('/dev/ttyAMA0', 38400)
    try:
       while 1:
            line = ser.readline()
            line = line[:-2]
            Z=line.split(' ')
            if len(Z) > 15:
                DATA = {
                        'TIME': [time.time()],
                        'P1(W)': [Z[1]],
                        'S1(VA)': [Z[2]],
                        'Irms1(A)': [Z[3]],
                        'Vrms1(V)': [Z[4]],
                        'P.W1': [Z[5]],
                        'P2(W)': [Z[6]],
                        'S2(VA)': [Z[7]],
                        'Irms2(A)': [Z[8]],
                        'Vrms2(V)': [Z[9]],
                        'P.W2': [Z[10]],
                        'P3(W)': [Z[11]],
                        'S3(VA)': [Z[12]],
                        'Irms3(A)': [Z[13]],
                        'Vrms3(V)': [Z[14]],
                        'P.W3': [Z[15]],
                        }
                DATA_JSON = json.dumps(DATA)
            client.publish(MQTT_TOPIC, DATA_JSON, qos=QOS)
    except KeyboardInterrupt:
        ser.close()
main()