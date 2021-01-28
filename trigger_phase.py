#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging,json,time
import config_setup as cf
import mqtt_service as mq

def trigger_phase(msg_i):

    if 'Phase' in msg_i :
        flag = 'trigger/phase'
        count_car(flag,msg_i)
    else:
        pass

def trigger_input(msg_i):

    for i in range(1,11):
        s_index = 'INP_'+str(i)
        if s_index in msg_i:
            flag='trigger/input'
            data_i={}
            data_i.update(msg_i)
        else:
            pass

    count_car(flag, data_i)

def trigger_group(msg_9):

    data={}

    for i in range(1, 25):
        s_index = 'G_' + str(i)
        if msg_9.keys() == s_index:
            data[i] = msg_9[s_index]
            flag = 'trigger/group'

        else:
            pass

def count_car(flag,data_i):
    if flag == 'trigger/input':
        logging.info('trigger/input')

        for j in range(1,11):
            s_index="INP_"+str(j)
            if s_index in data_i and data_i[s_index] != cf.inp_difs[s_index]:
                cf.inp_difs[s_index] = data_i[s_index]
                if data_i[s_index] == 3:
                    cf.counters['carCount_' + str(j)] += cf.weight[s_index]
                    #print(cf.counters['carCount_' + str(j)])
    if flag == 'trigger/phase':
        logging.info('trigger/phase')
        data_i = cf.phase_info

        if 'Phase' in data_i:
            msg={}
            phase = data_i['Phase']
            p_index = get_phase_send(phase)
            s_index = 'carCount_'+str(p_index)
            msg[s_index] = round(cf.counters[s_index])
            cf.counters[s_index]=0
            data_i = {cf.device_id: [{'ts': time.time(), 'values': msg}]}
            logging.debug(msg)

            if cf.MQTT_EN == '1':
                mq.mqttc.publish(cf.mqtt_pub_tele, json.dumps(data_i))
                if cf.PCB_VER == '5':
                    mq.mqtts.publish('cam_out',json.dumps(data_i))

def get_phase_send(ph):

    r_phase = ph -1
    if r_phase < 1:
        r_phase= cf.count_phase

    return r_phase









