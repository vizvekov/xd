__author__ = 'subadmin'

import logging

class logger:

    log = logging

    def __init__(self,file = "/tmp/xen_daemon.log"):
        self.log.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = self.log.INFO, filename = file)
