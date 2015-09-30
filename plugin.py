import imp
from repo import Credentials, Repo
from data import Datastore
from multiprocessing.pool import ThreadPool

class Plugin(object):
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name
        self.datastore = Datastore(repo, name)

    def sync(self):
        if not self.datastore.check_update():
            print "[*] File is unchanged, not downloading"
            return False

        print "[*] Detected change of file"
        module = imp.new_module(self.name)
        exec self.datastore.data in module.__dict__
        self.module = module
        print "[*] File downloaded"
        return True

    def run_async(self, args=None):
        pool = ThreadPool(processes=1)
        return pool.apply_async(self.module.run, (args,))

if __name__ == "__main__":
    import threading

    cred = Credentials('simonvpe','******')
    repo = Repo('simonvpe','trj_modules','master')
    plug = Plugin(repo, 'helloworld.py')
    plug.sync()

    ret = plug.run_async()
    print ret.get()
