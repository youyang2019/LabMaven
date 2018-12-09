#!/usr/bin/python
# -*- coding: UTF-8 -*-.
import pymysql
from LoggerService import LoggerService

CacheDict = {}

#localLogger = LoggerService().getlog()

def main():
    #localLogger.info("This is the main function in ConfigService!")
    #CacheDict = { "b01f001r0001c00001" : { "ip": "127.0.0.1", "port" : "10001", "address": "40000", "length" : "1" } }

    #localLogger
    conn = pymysql.connect(host="localhost", user="root",password="1qaz!QAZ", db="ailab", port=3306)
    #print(conn)
    #localLogger.info(conn)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #localLogger.info(cursor)
    effect_row = cursor.execute("select * from c_define")
    #localLogger.info(effect_row)
    #rows=cursor.fetchall()
    #print(rows)

    hosts_mapping_dict={}

    for row in cursor.fetchall():
        #print(row["s_id"] + "m_t_ip :" + row["m_t_ip"])
        #print(row["s_id"] + "m_t_port :" + row["m_t_port"])
        #print(row["s_id"] + "m_t_address :" + str(row["m_t_address"]))
        #print(row["s_id"] + "m_t_lenght :" + str(row["m_t_lenght"]))
        if row["s_id"] not in hosts_mapping_dict:
            hosts_mapping_dict[row["s_id"]]={}
        hosts_mapping_dict[row["s_id"]]["m_t_ip"]=row["m_t_ip"]
        hosts_mapping_dict[row["s_id"]]["m_t_port"] = row["m_t_port"]
        hosts_mapping_dict[row["s_id"]]["m_t_address"] = row["m_t_address"]
        hosts_mapping_dict[row["s_id"]]["m_t_lenght"] = row["m_t_lenght"]

    #print(hosts_mapping_dict)
    CacheDict=hosts_mapping_dict

    return CacheDict

#main()