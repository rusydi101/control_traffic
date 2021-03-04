#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, signal
import mysql.connector
#cannot have import logging in this file or any calling logging.info
CONFIGINI = 'config_file.ini'

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


try:
    mydb = mysql.connector.connect(host='localhost',user='root',password='#traffiC$', database='traffic')
except Exception as e:
    print('mysql error',e)

# instantiate
config = ConfigParser()

# parse existing file
config.read(CONFIGINI)

# #[setup]
FUNCTION1 = config.get('setup', 'function1')
PCB_VER = config.get('setup', 'pcb_ver')

# #[services]
TCP_EN = config.get('service', 'tcp_en')
MQTT_EN = config.get('service', 'mqtt_en')
MBUS_EN = config.get('service', 'mbus_en')
DEBUG_EN = config.get('service', 'debug_en')
#
if FUNCTION1 == 'slight':
    TCP_EN = '0'
    MQTT_EN = '1'
    config.set('service', 'tcp_en', TCP_EN)
    config.set('service', 'mqtt_en' ,MQTT_EN)
    with open('config_file.ini', 'w') as configfile:
        config.write(configfile)

elif FUNCTION1 == 'tlight':
    TCP_EN = '1'
    MQTT_EN = '1'
    config.set('service', 'tcp_en', TCP_EN)
    config.set('service', 'mqtt_en' ,MQTT_EN)
    with open('config_file.ini', 'w') as configfile:
        config.write(configfile)

elif FUNCTION1 == 'modbus':
    TCP_EN = '0'
    MQTT_EN = '1'
    MBUS_EN = '1'
    config.set('service', 'tcp_en', TCP_EN)
    config.set('service', 'mqtt_en', MQTT_EN)
    config.set('service', 'mbus_en' ,MBUS_EN)
    with open('config_file.ini', 'w') as configfile:
        config.write(configfile)

#[service]
WIFI_EN = config.get('service', 'wifi_en')
# if WIFI_EN == 'True':
#     os.system('sudo rfkill unblock wlan')
# else:
#     os.system('sudo rfkill unblock wlan')

BLE_EN = config.get('service', 'ble_en')
# if BLE_EN == 'True':
#     os.system('sudo rfkill unblock bluetooth')
# else:
#     os.system('sudo rfkill block bluetooth')



# read values from a section [attributes]
device_id = config.get('attributes', 'device_id')
tl_ver = config.get('attributes', 'tl_ver')
latitude = config.get('attributes', 'latitude')
longitude = config.get('attributes', 'longitude')
description = config.get('attributes', 'description')
commision = config.get('attributes', 'commision')
category = config.get('attributes', 'category')
apu_ver = config.get('attributes', 'apu_ver')
make = config.get('attributes', 'make')
model = config.get('attributes', 'model')
sim_id = config.get('attributes', 'sim_id')
installer = config.get('attributes', 'installer')
client = config.get('attributes', 'client')

#[alarm]
alarm_enabled = config.get('alarm', 'alarm_enabled')
root = config.get('alarm', 'alarm_enabled')
state = config.get('alarm', 'alarm_enabled')
route = config.get('alarm', 'alarm_enabled')
card_alert = config.get('alarm', 'alarm_enabled')
apu_alert = config.get('alarm', 'alarm_enabled')
camfail_alert = config.get('alarm', 'alarm_enabled')
rdoor_alert = config.get('alarm', 'alarm_enabled')
misc1_alert = config.get('alarm', 'alarm_enabled')
misc2_alert = config.get('alarm', 'alarm_enabled')

#[telemetry]
tele_enabled = config.get('telemetry', 'tele_enabled')
tele_source = config.get('telemetry', 'tele_source')
apu_ip = config.get('telemetry', 'apu_ip')
apu_port = config.get('telemetry', 'apu_port')
mqtt_broker = config.get('telemetry', 'mqtt_broker')
mqtt_port = config.get('telemetry', 'mqtt_port')
mqtt_user = config.get('telemetry', 'mqtt_user')
mqtt_pass = config.get('telemetry', 'mqtt_pass')
mqtt_pub_tele = config.get('telemetry', 'mqtt_pub_tele')
mqtt_pub_alarm = config.get('telemetry', 'mqtt_pub_alarm')
mqtt_pub_modbus = config.get('telemetry', 'mqtt_pub_modbus')
mqtt_pub_heartbeat = config.get('telemetry', 'mqtt_pub_heartbeat')
mqtt_sub_300 = config.get('telemetry', 'mqtt_sub_300')
qos_val = config.get('telemetry', 'qos_val')

#CAMERA AI 
mqtt_sub_vsens = config.get('telemetry', 'mqtt_sub_vsens')
mqtt_sub_direction = config.get('telemetry', 'mqtt_sub_direction')
mqtt_sub_vehicle = config.get('telemetry', 'mqtt_sub_vehicle')
mqtt_sub_summary = config.get('telemetry', 'mqtt_sub_summary')


#[phase]
count_phase = config.get('phase', 'count')
group_1 = config.get('phase', 'group_1')
group_2 = config.get('phase', 'group_2')
group_3 = config.get('phase', 'group_3')
group_4 = config.get('phase', 'group_4')
group_5 = config.get('phase', 'group_5')
group_6 = config.get('phase', 'group_6')
group_7 = config.get('phase', 'group_7')
group_8 = config.get('phase', 'group_8')
group_9 = config.get('phase', 'group_9')
group_10 = config.get('phase', 'group_10')

#[route]
route_1 = config.get('route', 'route_1')
route_2 = config.get('route', 'route_2')
route_3 = config.get('route', 'route_3')
route_4 = config.get('route', 'route_4')
route_5 = config.get('route', 'route_5')
route_6 = config.get('route', 'route_6')
route_7 = config.get('route', 'route_7')
route_8 = config.get('route', 'route_8')
route_9 = config.get('route', 'route_9')
route_10 = config.get('route', 'route_10')

#[detection]
dect_source = config.get('detection', 'dect_source')


#naming for route
phase_route = ['',route_1,route_2,route_3,route_4,route_5,route_6,route_7,route_8,route_9,route_10]
#logging.debug(route_10)

inp_data = {
    "INP_1": 0, "INP_2": 0, "INP_3": 0, "INP_4": 0, "INP_5": 0, "INP_6": 0, "INP_7": 0, "INP_8": 0, "INP_9": 0,"INP_10": 0,
    "INF_11": 0, "INF_12": 0, "INF_13": 0, "INF_14": 0, "INF_15": 0, "INF_16": 0, "INF_17": 0, "INF_18": 0,"INF_19": 0, "INF_20": 0,
    "PED_21": 0, "PED_22": 0, "PED_23": 0, "PED_24": 0,
}

phase_data = {"Phase": 0, "Time": 0, "Mode": 'N/A', "Gap": 0, "Max": 0, "Min": 0, "RunErr": 0, "Actual": 0,"Route":""}

phase_info = phase_data

count_data = {
    "CNT_TYPE_1": 0, "CNT_VAL_1": 0, "CNT_TYPE_2": 0, "CNT_VAL_2": 0, "CNT_TYPE_3": 0, "CNT_VAL_3": 0,
    "CNT_TYPE_4": 0, "CNT_VAL_4": 0,
    "CNT_TYPE_5": 0, "CNT_VAL_5": 0, "CNT_TYPE_6": 0, "CNT_VAL_6": 0, "CNT_TYPE_7": 0, "CNT_VAL_7": 0,
    "CNT_TYPE_8": 0, "CNT_VAL_8": 0,
    "CNT_TYPE_9": 0, "CNT_VAL_9": 0, "CNT_TYPE_10": 0, "CNT_VAL_10": 0, "CNT_TYPE_11": 0, "CNT_VAL_11": 0,
    "CNT_TYPE_12": 0, "CNT_VAL_12": 0,
    "CNT_TYPE_13": 0, "CNT_VAL_13": 0, "CNT_TYPE_14": 0, "CNT_VAL_14": 0,
}

group_data = {
    "G_1": -1, "G_2": -1, "G_3": -1, "G_4": -1, "G_5": -1, "G_6": -1, "G_7": -1, "G_8": -1,
    "G_9": -1, "G_10": -1, "G_11": -1, "G_12": -1, "G_13": -1, "G_14": -1, "G_15": -1, "G_16": -1,
    "G_17": -1, "G_18": -1, "G_19": -1, "G_20": -1, "G_21": -1, "G_22": -1, "G_23": -1, "G_24": -1,
}

faults = [0]*48

mqtt_sub_cmnd = 'remote/'+ str(device_id) + '/cmnd'
mqtt_pub_lwt = "stat/" + device_id + '/LWT'  # Last Will and Testament

qos_value = int(qos_val)

inp_difs = {"INP_1": 3, "INP_2": 3, "INP_3": 3, "INP_4": 3, "INP_5": 3, "INP_6": 3, "INP_7": 3, "INP_8": 3,
            "INP_9": 3,
            "INP_10": 3}
weight = {"INP_1": 3.0, "INP_2": 3.0, "INP_3": 3.0, "INP_4": 3.0, "INP_5": 3.0, "INP_6": 3.0, "INP_7": 3.0,
          "INP_8": 3.0, "INP_9": 3.0, "INP_10": 3.0}
counters = {"carCount_1": 0, "carCount_2": 0, "carCount_3": 0, "carCount_4": 0, "carCount_5": 0,
            "carCount_6": 0, "carCount_7": 0, "carCount_8": 0, "carCount_9": 0, "carCount_10": 0}

# save to a file
# with open('test_update.ini', 'w') as configfile:
#     config.write(configfile)