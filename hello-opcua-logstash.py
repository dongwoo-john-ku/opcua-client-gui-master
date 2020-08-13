import sys
sys.path.insert(0, "..")
from opcua import Client
import logging
import logstash

host = 'localhost'
test_logger = logging.getLogger('ua-logger')
test_logger.setLevel(logging.INFO)
test_logger.addHandler(logstash.LogstashHandler(host, 5959, version=1))

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)
    #logger = logging.getLogger("KeepAlive")
    #logger.setLevel(logging.DEBUG)

    client = Client("opc.tcp://host.docker.internal:53530/OPCUA/SimulationServer")
    # client = Client("opc.tcp://SEOUL-DKU.apac.turck.info:53530/OPCUA/SimulationServer")
    # client = Client("opc.tcp://SEOUL-DKU.mshome.net:53530/OPCUA/SimulationServer")

    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        objects = client.get_objects_node()
        # Specific Node which I want to access
        # print("Object's children node are: ", objects.get_children()[2])
        # print(objects.get_children()[2])
        # print('')

        varList = objects.get_children()[2].get_children()

        for var in varList :
            tagName ='"tagName":' + '"' + str(var.get_browse_name()).split(":")[1][:-1] + '"'
            tagValue ='"tagValue":' + '"' + str(var.get_value()) + '"'
            # timestamp = (str(var.get_data_value()).split(",")[-1][1:-1]).split(':')
            # timestamp ='"' + timestamp[0] + '":"' + timestamp[1] +'"'
            logData = ([tagName, tagValue])
            logData = '{' + ", ".join(logData) +'}'
            test_logger.info(logData)

    finally:
        client.disconnect()