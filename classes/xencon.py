__author__ = 'subadmin'

import XenAPI
from logger import logger


class xenviver:

    ses = ""
    templates = {}
    vm_run = {}
    vm_halt = {}
    log = ""
    ext_network = {}
    local_network = {}

    def __init__(self,host,username,password,ssl = False,log_file = '/tmp/xen_daemon.log'):
        tmp = logger(log_file)
        self.log = tmp.log
        url = 'http://%s/' % host
        if ssl:
            url = 'https://%s/' % host
        session = XenAPI.Session(url)
        try:
            session.xenapi.login_with_password(username, password)
            self.ses = session
        except Exception, e:
            self.log.error(str(e))
            raise
        self.log.info("Connection to host %s success" % url)
        self.__get_vm_list()
        self.__get_network_list()

    def get_vm_info(self,vm,params = "all"):
        try:
            record = self.vm_run[vm]
        except:
            record = self.vm_halt[vm]
        if params == "all":
            return record
        elif type(params) == list:
            ret_val = {}
            for param in params:
                ret_val.update({param: record[param]})
            return ret_val
        else:
            return record[params]

    def get_network_info(self,network,params = "all"):
        try:
            record = self.ext_network[network]
        except:
            record = self.local_network[network]
        if params == "all":
            return record
        elif type(params) == list:
            ret_val = {}
            for param in params:
                ret_val.update({param: record[param]})
            return ret_val
        else:
            return record[params]

    def local_network_destroy(self,network):
        try:
            self.ses.xenapi.network.destroy(self.ses.xenapi.network.get_by_uuid(network))
            del self.local_network[network]
            return True
        except:
            return False

    def local_network_create(self,name):
        network = {'other_config': {}, 'name_label': name,'MTU': '1500'}
        try:
            netw = self.ses.xenapi.network.create(network)
            uuid = self.ses.xenapi.network.get_uuid(netw)
            self.local_network.update({uuid: self.ses.xenapi.network.get_record(netw)})
            return uuid
        except:
            return False

    def __get_network_list(self):
        networks = self.ses.xenapi.network.get_all_records()
        self.log.info("Server has %d networks." % len(networks))
        for network in networks:
            record = networks[network]
            if record["PIFs"]:
                ty = "external"
                self.ext_network.update({record["uuid"]: record})
            else:
                ty = "local"
                self.local_network.update({record["uuid"]: record})
            self.log.debug("Found %s network with name_label = %s" % (ty,record["name_label"]))

    def __get_vm_list(self):
        vms = self.ses.xenapi.VM.get_all_records()
        self.log.info("Server has %d VM objects (this includes templates)." % (len(vms)))
        for vm in vms:
            record = vms[vm]
            if record["is_a_template"]:
                ty = "template"
                self.templates.update({record["uuid"]: record})
            else:
                ty = "vm"
                if record["power_state"] == "Running":
                    self.vm_run.update({record["uuid"]: record})
                else:
                    self.vm_halt.update({record["uuid"]: record})
            self.log.debug("Found %s with name_label = %s" % (ty,record["name_label"]))



    def __del__(self):
        self.ses.logout()
        del self.ses
