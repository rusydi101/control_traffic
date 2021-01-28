#!/usr/bin/python3
# -*- coding: utf-8 -*-

import paho.mqtt.client as paho
import ssl, time, logging
import apu_tcp_service as tcp
import binascii, json

MQTT_HOST = "broker.react.net.my"
MQTT_PORT = 8883
MQTT_USERNAME = '2sa34dd5'
MQTT_PASS = '2sa34dd5'

MQTT_SUB_TOPIC = "raw/300"

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        filename='service.log'
                        )

def subs(client, userdata, message):
    data = message.payload.decode('utf-8')

    # data = binascii.a2b_hex(data)
    # jdata = json.loads(data)
    # for key in jdata.keys():
    #     if key == "JKR-SEL-006":
    #         print(jdata)
    # print('data',len(data))
    try:
        tcp.tcp_handle_byte(data)
    except Exception as msg:
        print("Caught error: %s",msg)
        logging.info("Caught error: %s" % msg)
    


def on_connect(client, userdata, flags, rc):
    print("MQTT Connected ")
    mqttc.subscribe(MQTT_SUB_TOPIC, qos=2)


mqttc = paho.Client()
print("Connecting to broker")
mqttc.tls_set(None,None,None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
mqttc.tls_insecure_set(True)
# mqttc.tls_insecure_set(True)
mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASS)
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

# Assign event callbacks
mqttc.on_connect = on_connect

mqttc.message_callback_add(MQTT_SUB_TOPIC, subs)
while True:
    ##start loop to process received messages
    try:
        mqttc.loop_start()
    except Exception as e:
        print(e)
    # wait to allow publish and logging and exit
    time.sleep(1)