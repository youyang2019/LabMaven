#!/usr/bin/python
import json

#config_dict={ "slave_no" : "10",  "slave_ip" : "127.0.0.1", "slave_port" : "1100" }
config_str='{"slaves":[{"slave_no":"10","slave_ip":"127.0.0.1","slave_port":"1100"},{"slave_no":"10","slave_ip":"127.0.0.1","slave_port":"1100"},{"slave_no":"11","slave_ip":"127.0.0.1","slave_port":"1101"}]}'
#config_dict={ "slave_no" : "10",  "slave_ip" : "127.0.0.1", "slave_port" : "1100" }

config_dict=json.loads(config_str)

#config_dict["slave_no"]="1"
#config_dict["slave_ip"]="127.0.0.1"
#config_dict["slave_port"]="1100"

config_dict_str=json.dumps(config_dict, sort_keys=True, indent=4, separators=(',', ': '))
#print json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': '))

print(config_dict_str)
print(type(config_dict_str))
