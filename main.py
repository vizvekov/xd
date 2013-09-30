__author__ = 'subadmin'

from classes.server import Server
from classes.xencon import xenviver
import json

xen = xenviver(host="176.9.72.4", username="root", password="1784554782", log_file="C:/logs/xe.log")

server = Server()
server.start()

run = True

while run:

    if server.last_msg != "":
        print(server.last_msg)
        try:
            req = dict(json.loads(server.last_msg))
        except:
            server._closeConnection()
            server.last_msg = ""
        if req['variable'] == "vif_get":
            for ln in xen.local_network:
                server._send("%s\n\r" % json.dumps(xen.local_network[ln]['name_label']))
            server.last_msg = ""
            server._closeConnection()
    elif server.last_msg == "quit":
        server.stop()
        run = False
        server.last_msg = ""
        continue