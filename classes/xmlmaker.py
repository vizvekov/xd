__author__ = 'subadmin'

from xml.dom.minidom import getDOMImplementation

class xmlmaker:

    def __init__(self, name):
        impl = getDOMImplementation()
        self.newdoc = impl.createDocument(None, name, None)
