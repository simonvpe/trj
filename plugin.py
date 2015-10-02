import imp
from repo import Credentials, Repo
from data import Datastore
from multiprocessing.pool import ThreadPool

class Plugin(object):
    def __init__(self, plug_file, data_file, name):
        self.name      = name
        self.plug_file = plug_file
        self.data_file = data_file

    def sync(self):
        if not self.plug_file.check_update(): return False

        module = imp.new_module(self.name)
        exec self.plug_file.data in module.__dict__
        self.module = module
        return True

    def run(self, arg):
        if self.sync(): print "[*] Downloaded module %s" % self.name
        self.module.run(self.data_file, arg)
