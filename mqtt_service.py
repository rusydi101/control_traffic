#!/usr/bin/python3
# -*- coding: utf-8 -*-


import logging,time,json
import paho.mqtt.client as mqtt
import ssl,sqlite3

import config_setup as cf
import decode_apu as de
# import rcommand as ct
import apu_tcp_service as tcp
# import datalog as dlog

from ast import literal_eval

mqttc = mqtt.Client()
if cf.PCB_VER == '5':
    client = mqtt.Client()
    logging.info(client)

if cf.PCB_VER == '6':
    client = mqtt.Client()
    logging.info(client)

def on_connect(mqttc, obj, flags, rc):
    logging.info("rc: " + str(rc))
    logging.info('MQTT service connected to broker REACT')

    ############################################################################

    mqttc.publish(cf.mqtt_pub_lwt, 'on-line' ,qos=cf.qos_value,retain=True) #online status

    ############################################################################

    mqttc.subscribe(cf.mqtt_sub_300, qos=cf.qos_value)  #for callback to activate
    mqttc.subscribe(cf.mqtt_sub_cmnd, qos=cf.qos_value)  # for callback to activate


# The callback for when the client receives a CONNACK response from the server.
# topic: cam/in
# {"cam1" : 0,"cam2" : 0,"cam3" : 0,"cam4" : 0,"cam5" : 0,"fault1" : 0,"fault2" : 0,"fault3" : 0,"fault4" : 0,"fault5" : 0}
def on_connects(client, obj, flags, rc):
    print("Connected with result code "+str(rc))
    logging.info('MQTT service connected to broker LOCAL')
    client.subscribe('cam/in', qos=cf.qos_value)  # for callback to activate

def on_connects_Camera(client, obj, flags, rc):
    print("Connected with result code "+str(rc))
    logging.info('MQTT service connected to broker LOCAL')
    client.subscribe('smart_traffic/cyberjaya/vsens', qos=cf.qos_value)  # for callback to activate


# The callback for when a PUBLISH message is received from the server.
def on_messages(client, obj, msg):
    logging.info(msg)
    print(msg.topic+" "+str(msg.payload))

def on_message(mqttc, obj, msg):
    #logging.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    pass

def on_publish(mqttc, obj, mid):
    pass
    #logging.debug("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    #pass
    logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, msg):
    #pass
    logging.info(msg)

def on_handle_byte(mqttc, obj, msg):
    func_list=[de.group_info,de.input_info,de.phase_info,de.fault_info,de.count_info]
    for i in func_list:
        tcp.publish_telemetry(i, msg.payload)

def on_handle_cmnd(mqttc, obj, msg):
    logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    some_string = str(msg.payload.decode("utf-8", "ignore"))
    ct.process_cmnd(some_string)

def on_handle_cam_all(client, obj, msg):
    logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    print(msg.payload)

    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("data Received type",type(m_decode))
    print("data Received",m_decode)
    print("Converting from Json to Object")
    m_in=json.loads(m_decode) #decode json data
    print(type(m_in))
    ct.process_cam_all(m_in)


def on_handle_Camera_AI_direction(client, obj, msg):
    logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    x = msg.payload
    try:
        publish_camera('v1/gateway/camera/direction',x)
    except:
        pass
def on_handle_Camera_AI_vehicle_type(client, obj, msg):
    logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    x = msg.payload
    try:
        publish_camera('v1/gateway/camera/vehicle_type',x)
    except:
        pass
def on_handle_Camera_AI_summary(client, obj, msg):
    logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    x = msg.payload
    try:
        publish_camera('v1/gateway/camera/summary',x)
    except:
        pass
def on_handle_Camera_AI(client, obj, msg):
    logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    # print(msg.payload)
    x = msg.payload
    try:
        my_new_string_value = x.decode("utf-8")
        result = literal_eval(my_new_string_value)
        print(result)
        for keys,values in result.items():
            # print(keys)
            if keys == 'detection':
                arrdetect = values
                # for i in range(len(arrdetect)):
                #     carexist = arrdetect[i]
                    # print('Car detection line ',(i+1),' :',carexist)
            if keys == 'camIP':
                camip = values
                print('Cam IP: ',values)

        try:
            updatesql(arrdetect,camip)
            # time.sleep(1)
        except Exception as e:
            # print('updatesql')
            print(e)
    except Exception as e:
        print('literal eval')
        print(e)


#update sqlite
def updatesql(detection,camip):
    import sqlite3
    from pymemcache.client import base
    
    conn = sqlite3.connect('./web/config/db.sqlite3')
    curs = conn.cursor()
    curs.execute('SELECT * FROM camera WHERE name != "disable" ')
    arr_do = []
    for cam in curs.fetchall():
        if cam[1] == camip:
            cam_id = cam[0]
            name = cam[1]
            #clientele.set(name, 1) #set watchdogCam reset 1
            curs2 = conn.cursor()
            curs2.execute('SELECT * FROM camera_lane WHERE camera_id ='+str(cam_id))
            for cl in curs2.fetchall():
                arr_do.append(cl[2])

    print(len(arr_do),arr_do)
    print(len(detection),detection)
    jdata = {}
    arrtemp = {}
    if len(arr_do) == len(detection):
        for arr in range(len(arr_do)):
            do_col = arr_do[arr]
            mqtt_detection = detection[arr]
            # print(do_col,' = ',mqtt_detection)
            
            # print('len arrtemp: ',len(arrtemp))
            chkupdate = 0
            for keys,values in jdata.items():
                if keys == do_col and values == 1:
                    chkupdate = 1

            if len (arrtemp) == 0 and mqtt_detection == 0 or mqtt_detection == 1:
                chkupdate = 0
            if chkupdate == 1:
                pass
            else:
                jdata.update({do_col:mqtt_detection})
            arrtemp.update({do_col:mqtt_detection})
            # if mqtt_detection == 1:
            #     jdata.update({do_col:mqtt_detection})
            # print('Update output_do memcache',do_col,' detection ',mqtt_detection)
        print(jdata)
        ct.process_cam_ai(jdata)
    else:
        print('Data length not same')
    # topic=msg.topic
    # m_decode=str(msg.payload.decode("utf-8","ignore"))
    # print("data Received type",type(m_decode))
    # print("data Received",m_decode)
    # print("Converting from Json to Object")
    # m_in=json.loads(m_decode) #decode json data
    # print(type(m_in))
    

    

# def on_handle_cam_count(client, obj, msg):
#     logging.info(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
#     print(msg.payload)
#     topic=msg.topic
#     m_decode=str(msg.payload.decode("utf-8","ignore"))
#     print("data Received type",type(m_decode))
#     print("data Received",m_decode)
#     print("Converting from Json to Object")
#     m_in=json.loads(m_decode) #decode json data
#     print(type(m_in))
#     publish_other(cf.mqtt_pub_tele, m_in)

def publish_other(topics, pub_str):
    if pub_str != None:
        data = {cf.device_id: [{'ts': time.time(), 'values': pub_str}]}
        try:
            mqttc.publish(topics, json.dumps(data))
        except:
            logging.info('Failed to publish to broker')
            dlog.store(data,topics)

def publish_other1(topics, pub_str,id_str,model):

    if pub_str != None:
        data = {cf.device_id: [{'ts': time.time(), 'values' : pub_str, 'mbus_id':id_str, 'model':model }]}
        try:
            mqttc.publish(topics, json.dumps(data))
        except:
            logging.info('Failed to publish to broker')
            dlog.store(data, topics)


def publish_camera(topics, pub_str):
    if pub_str != None:
        data = {cf.device_id: [{'ts': time.time(), 'values': pub_str}]}
        try:
            mqttc.publish(topics, json.dumps(data))
        except:
            logging.info('Failed to publish to broker')
            dlog.store(data,topics)


def heartbeat():
    from uptime import uptime

    temp= uptime()

    if cf.MQTT_EN == '1':
        try:
            publish_other(cf.mqtt_pub_heartbeat, temp)
            logging.info("Heartbeat. System uptime (sec): " + str(temp))
        except:
            logging.info("Problem publish heartbeat data")

def mqtt_init():

    mqttc.tls_set('/etc/ssl/certs/ca-certificates.crt')

    mqttc.will_set(cf.mqtt_pub_lwt, 'off-line', qos= cf.qos_value, retain=True) #Put call to will_set before client.connect.
    mqttc.username_pw_set(cf.mqtt_user, cf.mqtt_pass)
    try:
        mqttc.connect(cf.mqtt_broker, int(cf.mqtt_port),60)   #client.connect
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_publish = on_publish
        mqttc.on_subscribe = on_subscribe

        # Uncomment to enable debug messages
        #mqttc.on_log = on_log

        #########################################################
        mqttc.message_callback_add(cf.mqtt_sub_300, on_handle_byte)
        mqttc.message_callback_add(cf.mqtt_sub_cmnd, on_handle_cmnd)
    except Exception as e:
        print('Error mqtt',e)
        logging.info("Error mqtt",e)


    if cf.PCB_VER == '5':
        client.connect('localhost',1883,60) #connect to local broker
        client.on_message = on_messages
        client.on_connect = on_connects
        client.message_callback_add('cam/in', on_handle_cam_all)  #topic cam/in

    if cf.PCB_VER == '6':
        client.connect('localhost',1883,60) #connect to local broker
        client.on_message = on_messages
        client.on_connect = on_connects_Camera
        client.message_callback_add('smart_traffic/cyberjaya/vsens', on_handle_Camera_AI) 
        client.message_callback_add('smart_traffic/cyberjaya/direction', on_handle_Camera_AI_direction)
        client.message_callback_add('smart_traffic/cyberjaya/vehicle_type', on_handle_Camera_AI_vehicle_type)
        client.message_callback_add('smart_traffic/cyberjaya/summary', on_handle_Camera_AI_summary)
        # print('try connect to camera ai')
        #to be tested
        # client.message_callback_add('cam/count', on_handle_cam_count)  # topic cam/in

    #########################################################
    #mqttc.subscribe("$SYS/#", 0)

