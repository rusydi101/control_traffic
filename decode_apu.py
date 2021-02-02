#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, json, redis
import config_setup as cf
import trigger_phase as t
import mqtt_service as mq
from ast import literal_eval

rconn = redis.Redis(host='localhost',port=6379, db=0)

def group_info(temp):

    data=temp[41:53]
    junction=temp[8:39].decode('utf-8').replace('\x00','')
    # print(len(temp))
    # print(len(data))
    get_redis = literal_eval(rconn.get('group_data_'+str(junction)).decode('utf-8'))
    # print('get_redis',get_redis)
    valueObj = {}
    values1 = {
        "G_1" : data[0]  & 0x0F,"G_2" : data[0]  >> 4,"G_3" : data[1]  & 0x0F,"G_4" : data[1]  >> 4,
        "G_5" : data[2]  & 0x0F,"G_6" : data[2]  >> 4,"G_7" : data[3]  & 0x0F,"G_8" : data[3]  >> 4,
        "G_9" : data[4]  & 0x0F,"G_10": data[4]  >> 4,"G_11": data[5]  & 0x0F,"G_12": data[5]  >> 4,
        "G_13": data[6]  & 0x0F,"G_14": data[6]  >> 4,"G_15": data[7]  & 0x0F,"G_16": data[7]  >> 4,
        "G_17": data[8]  & 0x0F,"G_18": data[8]  >> 4,"G_19": data[9]  & 0x0F,"G_20": data[9]  >> 4,
        "G_21": data[10] & 0x0F,"G_22": data[10] >> 4,"G_23": data[11] & 0x0F,"G_24": data[11] >> 4,
    }

    # for values in cf.group_data:
    #     if cf.group_data[values] != values1[values]:
    #         cf.group_data[values]=values1[values]
    #         valueObj[values] = values1[values]

    for key, value in get_redis.items():
        if value != values1[key]:
            get_redis.update({key:values1[key]})
            rconn.set('group_data_'+str(junction),str(get_redis))
            valueObj[key] = values1[key]
    

    if valueObj != {}:
        logging.debug(valueObj)

        t.trigger_group(valueObj,junction)
        return valueObj

def count_info(temp):

    data=temp[53:81]
    junction=temp[8:39].decode('utf-8').replace('\x00','')
    get_redis = literal_eval(rconn.get('count_data_'+str(junction)).decode('utf-8'))
    valueObj={}

    values1 = {
        "CNT_TYPE_1" :data[0],"CNT_VAL_1"  :data[1],
        "CNT_TYPE_2" :data[2],"CNT_VAL_2"  :data[3],
        "CNT_TYPE_3" :data[4],"CNT_VAL_3"  :data[5],
        "CNT_TYPE_4" :data[6],"CNT_VAL_4"  :data[7],
        "CNT_TYPE_5" :data[8],"CNT_VAL_5"  :data[9],
        "CNT_TYPE_6" :data[10],"CNT_VAL_6"  :data[11],
        "CNT_TYPE_7" :data[12],"CNT_VAL_7"  :data[13],
        "CNT_TYPE_8" :data[14],"CNT_VAL_8"  :data[15],
        "CNT_TYPE_9" :data[16],"CNT_VAL_9"  :data[17],
        "CNT_TYPE_10":data[18],"CNT_VAL_10" :data[19],
        "CNT_TYPE_11":data[20],"CNT_VAL_11" :data[21],
        "CNT_TYPE_12":data[22],"CNT_VAL_12" :data[23],
        "CNT_TYPE_13":data[24],"CNT_VAL_13" :data[25],
        "CNT_TYPE_14":data[26],"CNT_VAL_14" :data[27],
    }

    # for values in cf.count_data:
    #     if cf.count_data[values] != values1[values]:
    #         cf.count_data[values]=values1[values]
    #         valueObj[values] = values1[values]
    
    for key, value in get_redis.items():
        if value != values1[key]:
            get_redis.update({key:values1[key]})
            rconn.set('count_data_'+str(junction),str(get_redis))
            valueObj[key] = values1[key]

    if valueObj != {}:
        logging.debug(valueObj)
        return valueObj

def phase_info(temp):
    data = temp[88:96]
    junction=temp[8:39].decode('utf-8').replace('\x00','')
    
    p_info = literal_eval(rconn.get('phase_info_'+str(junction)).decode('utf-8'))
    p_route = literal_eval(rconn.get('phase_route_'+str(junction)).decode('utf-8'))

    phase = data[0]
    timing = data[1]
    mode = "MP"
    if data[2]== 0x00:
        mode = "VA"
    max = data[3]
    min = data[4]
    err = data[5]
    gap = data[6]
    act = data[7]
    # route = cf.phase_route[phase]
    route = p_route[phase]

    valuei = {
        "Phase"   : phase,
        "Time"    : timing,
        "Mode"    : mode,
        "Max"     : max,
        "Min"     : min,
        "RunErr"  : err,
        "Gap"     : gap,
        "Actual"  : act,
        "Route"   : route
    }


    valueObj = {}

    if p_info["Phase"] != valuei["Phase"]:
        p_info.update({"Phase":valuei["Phase"]})
        valueObj["Phase"] = valuei["Phase"]

        p_info.update({"Time":valuei["Time"]})
        valueObj["Time"] = valuei["Time"]

        p_info.update({"Mode":valuei["Mode"]})
        valueObj["Mode"] = valuei["Mode"]

        p_info.update({"Max":valuei["Max"]})
        valueObj["Max"] = valuei["Max"]

        p_info.update({"Min":valuei["Min"]})
        valueObj["Min"] = valuei["Min"]

        p_info.update({"RunErr":valuei["RunErr"]})
        valueObj["RunErr"] = valuei["RunErr"]

    if p_info["Mode"] != valuei["Mode"]:
        p_info.update({"Mode":valuei["Mode"]})
        valueObj["Mode"] = valuei["Mode"]

    if p_info["Gap"] != valuei["Gap"]:
        p_info.update({"Gap":valuei["Gap"]})
        valueObj["Gap"] = valuei["Gap"]

    if p_info["Actual"] != valuei["Actual"]:
        p_info.update({"Actual":valuei["Actual"]})
        valueObj["Actual"] = valuei["Actual"]

    if str(p_info["Route"]) != valuei["Route"]:
        p_info.update({"Route":valuei["Route"]})
        valueObj["Route"] = valuei["Route"]


    # if cf.phase_data["Phase"] != valuei["Phase"]:
    #     cf.phase_data["Phase"] = valuei["Phase"]
    #     valueObj["Phase"] = valuei["Phase"]

    #     cf.phase_data["Time"] = valuei["Time"]
    #     valueObj["Time"] = valuei["Time"]
        
    #     cf.phase_data["Mode"] = valuei["Mode"]
    #     valueObj["Mode"] = valuei["Mode"]
        
    #     cf.phase_data["Max"]= valuei["Max"]
    #     valueObj["Max"] = valuei["Max"]
        
    #     cf.phase_data["Min"] = valuei["Min"]
    #     valueObj["Min"] = valuei["Min"]
        
    #     cf.phase_data["RunErr"] = valuei["RunErr"]
    #     valueObj["RunErr"] = valuei["RunErr"]

    # if cf.phase_data["Mode"] != valuei["Mode"] :
    #     cf.phase_data["Mode"] = valuei["Mode"]
    #     valueObj["Mode"] = valuei["Mode"]

    # if cf.phase_data["Gap"] != valuei["Gap"] :
    #     cf.phase_data["Gap"] = valuei["Gap"]
    #     valueObj["Gap"] = valuei["Gap"]

    # if cf.phase_data["Actual"] != valuei["Actual"] :
    #     cf.phase_data["Actual"] = valuei["Actual"]
    #     valueObj["Actual"] = valuei["Actual"]

    # if cf.phase_data["Route"] != valuei["Route"] :
    #     cf.phase_data["Route"] = valuei["Route"]
    #     valueObj["Route"] = valuei["Route"]
    
    # cf.phase_info = valuei
    rconn.set('phase_info_'+str(junction),str(p_info))
    #print(c.phase_info)

    if valueObj != {}:
        logging.debug(valueObj)
        if cf.PCB_VER == '5':
            mq.client.publish('cam/out', json.dumps(valuei))
        if cf.PCB_VER == '6':
            mq.client.publish('cam/out', json.dumps(valuei))

        t.trigger_phase(valueObj,junction)
        return valueObj

def input_info(temp):

    inps = temp[106:112]
    junction=temp[8:39].decode('utf-8').replace('\x00','')
    get_redis = literal_eval(rconn.get('inp_data_'+str(junction)).decode('utf-8'))
    k=[0]*24

    # detect
    k[0] = 1 if inps[0] & 0x01 == 0x01 else  3
    k[1] = 1 if inps[0] & 0x02 == 0x02 else  3
    k[2] = 1 if inps[0] & 0x04 == 0x04 else  3
    k[3] = 1 if inps[0] & 0x08 == 0x08 else  3
    k[4] = 1 if inps[0] & 0x10 == 0x10 else  3
    k[5] = 1 if inps[0] & 0x20 == 0x20 else  3
    k[6] = 1 if inps[0] & 0x40 == 0x40 else  3
    k[7] = 1 if inps[0] & 0x80 == 0x80 else  3
    k[8] = 1 if inps[1] & 0x01 == 0x01 else  3
    k[9] = 1 if inps[1] & 0x02 == 0x02 else  3

    # fault
    k[10] = 2 if inps[2] & 0x01 == 0x01 else  3
    k[11] = 2 if inps[2] & 0x02 == 0x02 else  3
    k[12] = 2 if inps[2] & 0x04 == 0x04 else  3
    k[13] = 2 if inps[2] & 0x08 == 0x08 else  3
    k[14] = 2 if inps[2] & 0x10 == 0x10 else  3
    k[15] = 2 if inps[2] & 0x20 == 0x20 else  3
    k[16] = 2 if inps[2] & 0x40 == 0x40 else  3
    k[17] = 2 if inps[2] & 0x80 == 0x80 else  3
    k[18] = 2 if inps[3] & 0x01 == 0x01 else  3
    k[19] = 2 if inps[3] & 0x02 == 0x02 else  3

    # pedestrian
    k[20] = 1 if inps[4] & 0x01 == 0x01 else  3
    k[21] = 1 if inps[4] & 0x02 == 0x02 else  3
    k[22] = 1 if inps[4] & 0x04 == 0x04 else  3
    k[23] = 1 if inps[4] & 0x08 == 0x08 else  3

    valueObj = {}
    values1 = {
        "INP_1": k[0],"INP_2": k[1],"INP_3": k[2],"INP_4": k[3],"INP_5": k[4],"INP_6": k[5],"INP_7": k[6],"INP_8": k[7],"INP_9": k[8],"INP_10": k[9],
        "INF_11": k[10],"INF_12": k[11],"INF_13": k[12],"INF_14": k[13],"INF_15": k[14],"INF_16": k[15],"INF_17": k[16],"INF_18": k[17],"INF_19": k[18],"INF_20": k[19],
        "PED_21": k[20],"PED_22": k[21],"PED_23": k[22],"PED_24": k[23],
    }

    # for values in cf.inp_data:
    #     if cf.inp_data[values] != values1[values]:
    #         cf.inp_data[values]=values1[values]
    #         valueObj[values] = values1[values]

    for key, value in get_redis.items():
        if value != values1[key]:
            get_redis.update({key:values1[key]})
            rconn.set('inp_data_'+str(junction),str(get_redis))
            valueObj[key] = values1[key]

    if valueObj != {}:
        logging.debug(valueObj)
        t.trigger_input(valueObj,junction)
        return valueObj

def fault_info(temp):

    data5=temp[120:169]
    junction=temp[8:39].decode('utf-8').replace('\x00','')
    get_redis = literal_eval(rconn.get('faults_'+str(junction)).decode('utf-8'))
    cardFault = {}
    groupFault = {}

    # logging.infos out the numbers 0,1,2,3,4,5,6,7
    for i in range(8):

        ptr = i * 6

        # if cf.faults[ptr] != data5[ptr]:
        #     cf.faults[ptr] = data5[ptr]
        if get_redis[ptr] != data5[ptr]:
            get_redis[ptr] = data5[ptr]
            rconn.set('faults_'+str(junction),str(get_redis))
            if data5[ptr] & 0x0f == 0x00:
                cardFault["CFAULT_" + str(i + 1)] = 0
            elif data5[ptr] & 0x0f == 0x01:
                cardFault["CFAULT_" + str(i + 1)] = 1
            elif data5[ptr] & 0x0f == 0x02:
                cardFault["CFAULT_" + str(i + 1)] = 2
            elif data5[ptr] & 0x0f == 0x03:
                cardFault["CFAULT_" + str(i + 1)] = 3

        grp = i * 2 + 1

        # if cf.faults[ptr + 4] != data5[ptr + 4]:
            # cf.faults[ptr + 4] = data5[ptr + 4]
        if get_redis[ptr + 4] != data5[ptr + 4]:
            get_redis[ptr + 4] = data5[ptr + 4]
            rconn.set('faults_'+str(junction),str(get_redis))
            # Group 1 - RED
            if data5[ptr + 4] & 0x01 == 0x01:
                groupFault["GFAULT_R_" + str(grp)] = 2
            elif data5[ptr + 4] & 0x10 == 0x10:
                groupFault["GFAULT_R_" + str(grp)] = 3
            else:
                groupFault["GFAULT_R_" + str(grp)] = 1

            # Group 2 - YELLOW
            if data5[ptr + 4] & 0x02 == 0x02:
                groupFault["GFAULT_Y_" + str(grp)] = 2
            elif data5[ptr + 4] & 0x20 == 0x20:
                groupFault["GFAULT_Y_" + str(grp)] = 3
            else:
                groupFault["GFAULT_Y_" + str(grp)] = 1

            # Group 3 - GREEN
            if data5[ptr + 4] & 0x04 == 0x04:
                groupFault["GFAULT_G_" + str(grp)] = 2
            elif data5[ptr + 4] & 0x40 == 0x40:
                groupFault["GFAULT_G_" + str(grp)] = 3
            else:
                groupFault["GFAULT_G_" + str(grp)] = 1

        grp = i * 2 + 2

        # if cf.faults[ptr + 5] != data5[ptr + 5]:
        #     cf.faults[ptr + 5] = data5[ptr + 5]
        if get_redis[ptr + 5] != data5[ptr + 5]:
            get_redis[ptr + 5] = data5[ptr + 5]
            rconn.set('faults_'+str(junction),str(get_redis))
            # Group 1 - RED
            if data5[ptr + 5] & 0x01 == 0x01:
                groupFault["GFAULT_R_" + str(grp)] = 2
            elif data5[ptr + 5] & 0x10 == 0x10:
                groupFault["GFAULT_R_" + str(grp)] = 3
            else:
                groupFault["GFAULT_R_" + str(grp)] = 1

            # Group 2 - YELLOW
            if data5[ptr + 5] & 0x02 == 0x02:
                groupFault["GFAULT_Y_" + str(grp)] = 2
            elif data5[ptr + 5] & 0x20 == 0x20:
                groupFault["GFAULT_Y_" + str(grp)] = 3
            else:
                groupFault["GFAULT_Y_" + str(grp)] = 1

            # Group 3 - GREEN
            if data5[ptr + 5] & 0x04 == 0x04:
                groupFault["GFAULT_G_" + str(grp)] = 2
            elif data5[ptr + 5] & 0x40 == 0x40:
                groupFault["GFAULT_G_" + str(grp)] = 3
            else:
                groupFault["GFAULT_G_" + str(grp)] = 1

    if cardFault != {}:
        # logging.debug(cardFault)
        return cardFault

    if groupFault != {}:
        # logging.debug(groupFault)
        return groupFault
