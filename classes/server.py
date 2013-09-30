__author__ = 'adminko'

import jsonSocket
import threading
import socket
from logger import logger


class Server(threading.Thread, jsonSocket.JsonServer):

    last_msg = ""

    def __init__(self, address='127.0.0.1', port=5489):
        threading.Thread.__init__(self)
        jsonSocket.JsonServer.__init__(self, address, port)
        self._isAlive = False
        tmp = logger('C:\logs\dx.log')
        self.logger =tmp.log

    def __pm(self, msg):
        self.last_msg = msg


    def run(self):
        while self._isAlive:
            try:
                self.acceptConnection()
            except socket.timeout as e:
                self.logger.debug("socket.timeout: %s" % e)
                continue
            except Exception as e:
                self.logger.exception(e)
                continue

            while self._isAlive:
                try:
                    self._send("Hi\n\r")
                    msg = "\r"
                    while msg[len(msg)-1] != "\n" or len(msg) == 0:
                        msg += self._read(1)
                    self.__pm(msg)
                    break
                except socket.timeout as e:
                    self.logger.debug("socket.timeout: %s" % e)
                    continue
                except Exception as e:
                    self.logger.exception(e)
                    self._closeConnection()
                    break

    def start(self):
        self._isAlive = True
        super(Server, self).start()

    def stop(self):
        self._isAlive = False
