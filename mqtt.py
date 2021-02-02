#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ast import literal_eval
import paho.mqtt.client as paho
import ssl, time, logging, redis
import apu_tcp_service as tcp
import config_setup as cf
import binascii, json

MQTT_HOST = "broker.react.net.my"
MQTT_PORT = 8883
MQTT_USERNAME = '2sa34dd5'
MQTT_PASS = '2sa34dd5'

MQTT_SUB_TOPIC = "raw/300"
# MQTT_SUB_TOPIC = "v1/gateway/telemetry"

logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        filename='service.log'
                        )

rconn = redis.Redis(host='localhost',port=6379, db=0)

def subs(client, userdata, message):
    data = message.payload.decode('utf-8')

    # data = binascii.a2b_hex(data)
    # jdata = json.loads(data)
    # for key in jdata.keys():
    #     if key == "BILIK-HAFIZ-IOT":
    #         print(jdata)
    # print('data',len(data))

    end = data[56:]
    
    junction_id = binascii.unhexlify(end[16:80]).decode('utf-8')
    junction_id = junction_id.replace('\u0000','')

    if (' ' in junction_id) == True:
        pass
    
    try:
        check_redis(junction_id)
            
        tcp.tcp_handle_byte(data)

    except Exception as msg:
        print("Caught error: %s",msg)
        logging.info("Caught error: %s" % msg)

def check_redis(junction_id):

    if rconn.get('phase_route_'+str(junction_id)) == None:
        rconn.set('phase_route_'+str(junction_id), str(cf.phase_route))
    if rconn.get('inp_data_'+str(junction_id)) == None:
        rconn.set('inp_data_'+str(junction_id), str(cf.inp_data))
    if rconn.get('phase_info_'+str(junction_id)) == None:
        rconn.set('phase_info_'+str(junction_id), str(cf.phase_info))
    if rconn.get('count_data_'+str(junction_id)) == None:
        rconn.set('count_data_'+str(junction_id), str(cf.count_data))
    if rconn.get('group_data_'+str(junction_id)) == None:
        rconn.set('group_data_'+str(junction_id), str(cf.group_data))
    if rconn.get('faults_'+str(junction_id)) == None:
        rconn.set('faults_'+str(junction_id), str(cf.faults))
    if rconn.get('inp_difs_'+str(junction_id)) == None:
        rconn.set('inp_difs_'+str(junction_id), str(cf.inp_difs))
    if rconn.get('weight_'+str(junction_id)) == None:
        rconn.set('weight_'+str(junction_id), str(cf.weight))
    if rconn.get('counters_'+str(junction_id)) == None:
        rconn.set('counters_'+str(junction_id), str(cf.counters))

def on_connect(client, userdata, flags, rc):
    print("MQTT Connected ")
    phase = rconn.keys('phase_*')
    for p in phase: rconn.delete(p)

    inp = rconn.keys('inp_data_*')
    for i in inp: rconn.delete(i)

    count = rconn.keys('count_data_*')
    for c in count: rconn.delete(c)

    group = rconn.keys('group_data_*')
    for g in group: rconn.delete(g)

    faults = rconn.keys('faults_*')
    for f in faults: rconn.delete(f)

    inp_difs = rconn.keys('inp_difs_*')
    for inp in inp_difs: rconn.delete(inp)

    weight = rconn.keys('weight_*')
    for w in weight: rconn.delete(w)

    counters = rconn.keys('counters_*')
    for cn in counters: rconn.delete(cn)


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