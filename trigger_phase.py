#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging,json,time, redis, ssl
import config_setup as cf
import paho.mqtt.client as paho
import mqtt_service as mq
from ast import literal_eval
rconn = redis.Redis(host='my-redis',port=6379,db=0)

MQTT_HOST = "broker.react.net.my"
MQTT_PORT = 8883
MQTT_USERNAME = '2sa34dd5'
MQTT_PASS = '2sa34dd5'

def trigger_phase(msg_i,junction):

    if 'Phase' in msg_i :
        flag = 'trigger/phase'+str(junction)
        count_car(flag,msg_i,junction)
    else:
        pass

def trigger_input(msg_i,junction):

    for i in range(1,11):
        s_index = 'INP_'+str(i)
        if s_index in msg_i:
            flag='trigger/input'+str(junction)
            data_i={}
            data_i.update(msg_i)
        else:
            pass

    count_car(flag, data_i,junction)

def trigger_group(msg_9,junction):

    data={}

    for i in range(1, 25):
        s_index = 'G_' + str(i)
        if msg_9.keys() == s_index:
            data[i] = msg_9[s_index]
            flag = 'trigger/group'+str(junction)

        else:
            pass

def count_car(flag,data_i,junction):
    inp_difs = literal_eval(rconn.get('inp_difs_'+str(junction)).decode('utf-8'))
    counters = literal_eval(rconn.get('counters_'+str(junction)).decode('utf-8'))
    weight = literal_eval(rconn.get('weight_'+str(junction)).decode('utf-8'))
    phase_info = literal_eval(rconn.get('phase_info_'+str(junction)).decode('utf-8'))
    if flag == 'trigger/input'+str(junction):
        logging.info('trigger/input'+str(junction))
        
        for j in range(1,11):
            s_index="INP_"+str(j)
            # if s_index in data_i and data_i[s_index] != cf.inp_difs[s_index]:
            if s_index in data_i and data_i[s_index] != inp_difs[s_index]:
                # cf.inp_difs[s_index] = data_i[s_index]
                inp_difs.update({s_index:data_i[s_index]})
                rconn.set('inp_difs_'+str(junction),str(inp_difs))
                if data_i[s_index] == 3:
                    # cf.counters['carCount_' + str(j)] += cf.weight[s_index]
                    # counters['carCount_' + str(j)] = counters['carCount_' + str(j)] + weight[s_index]
                    counters.update({
                        'carCount_'+str(j):counters['carCount_' + str(j)] + weight[s_index]
                        })
                    rconn.set('counters_'+str(junction),str(counters))
                    #print(cf.counters['carCount_' + str(j)])

    if flag == 'trigger/phase'+str(junction):
        logging.info('trigger/phase'+str(junction))
        # data_i = cf.phase_info
        data_i = phase_info

        if 'Phase' in data_i:
            msg={}
            phase = data_i['Phase']
            p_index = get_phase_send(phase,junction)
            s_index = 'carCount_'+str(p_index)
            msg[s_index] = round(counters[s_index])
            # cf.counters[s_index]=0
            counters.update({s_index:0})
            rconn.set('counters_'+str(junction),str(counters))
            # data_i = {cf.device_id: [{'ts': time.time(), 'values': msg}]}
            data_i = {junction: [{'ts': time.time(), 'values': msg}]}
            # print(data_i)
            logging.debug(msg)

            if cf.MQTT_EN == '1':
                mqttc.publish(cf.mqtt_pub_tele, json.dumps(data_i))
                if cf.PCB_VER == '5':
                    mq.mqtts.publish('cam_out',json.dumps(data_i))

def get_phase_send(ph,junction):

    r_phase = ph -1
    if r_phase < 1:
        r_phase= cf.count_phase
        cursor = cf.mydb.cursor()
        sql = 'SELECT phasecount FROM Junction WHERE serial LIKE "%'+str(junction)+'%" '
        cursor.execute(sql)
        rows = cursor.fetchone()
        # print(junction,' phase count ====> ',rows[0])
        cursor.close()
        if rows[0] is not None:
            r_phase = rows[0]
        
        # print('this ------> ',r_phase)

    return r_phase


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








