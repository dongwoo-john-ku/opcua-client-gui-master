import sys
sys.path.insert(0, "..")
import time
import logging
import configparser
import logstash
from opcua import Client

config = configparser.ConfigParser()
config.read('./communication.conf')
end_point = config.get('MAIN', 'opcua_server_endpoint')
logging_interval = config.get('MAIN', 'logging_interval')
logstash_host = config.get('MAIN', 'logstash_host')
logstash_port = int(config.get('MAIN', 'logstash_port'))

opc_nodeid = config.get('MAIN', 'opc_nodeid')
opc_timeout = int(config.get('MAIN', 'opc_timeout'))

# config = config['MAIN']
# print(config['opcua_server_endpoint'])

test_logger = logging.getLogger('ua-logger')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(logstash.LogstashHandler(logstash_host, logstash_port, version=1))

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)
    client = Client(url=end_point)

    while True:
        try:
            client.connect()
        except:
            print('connection failed')
        else:
            # client.load_type_definitions()  # load definition of server specific structures/extension objects
            varList = client.get_node(opc_nodeid).get_children()

            for var in varList :
                tagName ='"tagName":' + '"' + str(var.get_browse_name()).split(":")[1][:-1] + '"'
                tagValue ='"tagValue":' + '"' + str(var.get_value()) + '"'
                # timestamp = (str(var.get_data_value()).split(",")[-1][1:-1]).split(':')
                # timestamp ='"' + timestamp[0] + '":"' + timestamp[1] +'"'
                logData = ([tagName, tagValue])
                logData = '{' + ", ".join(logData) +'}'
                test_logger.info(logData)

            client.disconnect()
            time.sleep(int(logging_interval) / 1000)

