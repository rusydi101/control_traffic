#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging,signal,os
import socket,json,time,ssl, binascii
import config_setup as cf
import decode_apu as de
import paho.mqtt.client as paho

MQTT_HOST = "broker.react.net.my"
MQTT_PORT = 8883
MQTT_USERNAME = '2sa34dd5'
MQTT_PASS = '2sa34dd5'

sdata = b'\x01\x02\xd7\xb4\xcc\xac'  # as specify by Yang
s = socket.socket()
s.settimeout(5)

def conn():

    try:
        s.connect((cf.apu_ip, int(cf.apu_port)))  # port 2000 as specify by Yang
        logging.info(s)
    except Exception as msg:
        logging.info("Caught exception socket.error: %s" % msg)
    except socket.error as msg:
        logging.info("Socket Error: %s" % msg)
    except TypeError as msg:
        logging.info("Type Error: %s" % msg)

def req_data():
    try:
        s.send(sdata)
        rdata = s.recv(300)
        if len(rdata) == 300:
            tcp_handle_byte(rdata)
            # send_raw(rdata)
        else:
            logging.info("Data Error")
    except:
        logging.info("TCP comm error")
        # os.kill(os.getpid(), signal.SIGINT)


def tcp_handle_byte(byte_payload):
    
    header = byte_payload[0:56]
    device_id = header[22:30]
    # print(device_id)
    end = byte_payload[56:]
    
    junction_id = binascii.unhexlify(end[16:80]).decode('utf-8')
    junction_id = junction_id.replace('\u0000','')
    # print('deviceid',device_id,' junctionid',junction_id)
    data = binascii.a2b_hex(end)
    # if junction_id == 'BILIK-HAFIZ-CPU':
    func_list=[de.group_info,de.input_info,de.phase_info,de.fault_info,de.count_info]
    for i in func_list:
        publish_telemetry(i, data, junction_id)
    
    # get_pb = de.pb_info(data)
    # publish_other('v1/gateway/sms',get_pb, junction_id)

def send_raw(byte_payload):
    try:
        mq.client.publish('raw/300', byte_payload)
    except:
        pass

def publish_telemetry(func, pub_string, junction_id):
    pubmsg=func(pub_string)
    if pubmsg != None:
        data = {junction_id: [{'ts': time.time(), 'values': pubmsg}]}
        # print(data)
        if cf.MQTT_EN=='1':
            try:
                mqttc.publish(cf.mqtt_pub_tele, json.dumps(data))
                print(data)
                # mqttc.loop_start()
            except:
                logging.info('Failed to publish to broker')

def publish_other(topics, pub_str, junction_id):
    # print(pub_str)
    if pub_str != None:
        data = {junction_id: [{'ts': time.time(), 'values': pub_str}]}
        try:
            mqttc.publish(topics, json.dumps(data))
        except:
            logging.info('Failed to publish to broker')
            dlog.store(data,topics)

def on_connect(client, userdata, flags, rc):
    logging.info('Success connect to broker')

mqttc = paho.Client()
logging.info("Connecting to broker")
mqttc.tls_set(None,None,None, cert_reqs=ssl.CERT_NONE, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
mqttc.tls_insecure_set(True)
# mqttc.tls_insecure_set(True)
mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASS)
mqttc.connect(MQTT_HOST, MQTT_PORT, 60)

# Assign event callbacks
mqttc.on_connect = on_connect
