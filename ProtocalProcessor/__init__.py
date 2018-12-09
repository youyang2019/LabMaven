#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import json
import time
from threading import Thread
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

LOGGER = modbus_tk.utils.create_logger("console")

workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0, os.path.join(workpath, 'modules'))

# import multiprocessing
# import subprocess
# import threading
# from Processor.AlarmProcessor import funcA
# from multiprocessing.sharedctypes import
import CacheService
import ConfigService
from LoggerService import LoggerService
import pymysql

##############################################Variable########################################
CacheDict = {}
ConfigDict = {}
localLogger = LoggerService().getlog()

PYNAME = os.path.basename(__file__)
WORKPATH = os.path.dirname(os.path.realpath(__file__))

stop_flag_file = os.path.join(WORKPATH, "run", "stop_flag_file")
# ps_conf_fn=os.path.join(WORKPATH, "conf", "PotocalProcessor.conf")
ps_conf_fn = os.path.join(WORKPATH, "conf", "PotocalProcessor.json")

with open(ps_conf_fn, 'r') as cfp:
    ps_conf_dict = (json.load(cfp))
# print(json.dump(ps_conf_fn))
'''
The configpare don't have the capacity to load the whole configuration file by one op, so i chnange 
the configuration file to json format. 

print("[%s][%d][ps_conf_fn]" % (PYNAME, sys._getframe().f_lineno), ps_conf_fn)
'''

# stop_flag_file="C:\\Users\\sammyjeep\\PycharmProjects\\LabMaven\\ProtocalProcessor\\run\\stop_flag_file"
count = 0


##############################################Func########################################
def checkSingleDevice(deviceid, deviceinfo):
    # global count
    global ps_conf_dict
    count = 0
    threadId = deviceid
    global stop_flag_file
    localLogger.info("current device is [" + deviceid + ']:' + str(deviceinfo))

    MASTER = modbus_tcp.TcpMaster(host="127.0.0.1", port=12600)
    # localLogger.info("current device is [" + deviceId + '][m_t_ip]:' + str(type(deviceInfo["m_t_ip"])) )
    # localLogger.info("current device is [" + deviceId + '][m_t_port]:' + str(type(deviceInfo["m_t_port"])))
    MASTER = modbus_tcp.TcpMaster(host=deviceinfo["m_t_ip"], port=deviceinfo["m_t_port"])
    MASTER.set_timeout(5.0)

    # while not os.path.exists(stop_flag_file):
    # cursor = pymysql.connect(host=ps_conf_dict["mysql"]["host"], user=ps_conf_dict["mysql"]["user"],
    #                        password=ps_conf_dict["mysql"]["password"], db=ps_conf_dict["mysql"]["db"],
    #                        port=ps_conf_dict["mysql"]["port"]).cursor(cursor=pymysql.cursors.DictCursor)
    conn = pymysql.connect(host=ps_conf_dict["mysql"]["host"], user=ps_conf_dict["mysql"]["user"],
                           password=ps_conf_dict["mysql"]["password"], db=ps_conf_dict["mysql"]["db"],
                           port=ps_conf_dict["mysql"]["port"])


    cursor = conn.cursor()
    while True:
        if os.path.exists(stop_flag_file):
            break

        localLogger.info(count)
        # localLogger.info()
        localLogger.info("current device is [" + deviceid + ']:' + str(count))
        localLogger.info("current device is [" + deviceid + '][m_t_address]:' + str(deviceinfo["m_t_address"]))
        localLogger.info("current device is [" + deviceid + '][m_t_lenght]:' + str(deviceinfo["m_t_lenght"]))
        count = count + 1
        # value=MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1)
        LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, deviceinfo["m_t_address"], deviceinfo["m_t_lenght"]))
        current_value=MASTER.execute(1, cst.READ_HOLDING_REGISTERS, deviceinfo["m_t_address"], deviceinfo["m_t_lenght"])[0]

        rtn=cursor.execute("insert into e_data(s_id, input_time, value) VALUES(%s, %s, %s)", (deviceid, time.gmtime(time.time()), int(current_value)))
        conn.commit()

        #print(rtn)
        # LOGGER.info(MASTER.execute(1, cst.READ_HOLDING_REGISTERS, 4, 14))
        time.sleep(ps_conf_dict["common"]["checkInterval"])


##############################################Main########################################
localLogger.info('Potocal Stack main process start!')

localLogger.info('Potocal Stack main process start!')
# cp=ConfigParser()
# cp.read(ps_conf_fn)
# print(cp.items(cp.sections()))

localLogger.info('Fetching configuration start')
ConfigDict = ConfigService.main()
localLogger.info('Fetching configuration stoped')

localLogger.info('Fetching device start')
CacheDict = CacheService.main()
localLogger.info('Fetching device stoped')

localLogger.info(ConfigDict)
localLogger.info(CacheDict)
print(json.dumps(ConfigDict))
print(json.dumps(CacheDict))

checkThread = {}
for DeviceId in ConfigDict.keys():
    # checkSingleDevice(DeviceInfo)
    checkThread[DeviceId] = Thread(target=checkSingleDevice, args=(DeviceId, ConfigDict[DeviceId],))
    checkThread[DeviceId].start()
