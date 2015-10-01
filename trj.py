from   repo   import Credentials, Repo
from   data   import Datastore
from   plugin import Plugin
import json

from IPython.core.debugger import Tracer

username = 'simonvpe'
password = 'Elobari1'

# Fetch config from repository
config_login    = 'simonvpe'
config_repo     = 'trj'
config_branch   = 'master'
config_filename = 'config.json'

class Model(object):
    def __init__(self, cfg_login, cfg_repo, cfg_branch, cfg_filename, cred=None):
        self.credentials = cred
        self.config      = Datastore(Repo(cfg_login, cfg_repo, cfg_branch, cred), cfg_filename)
        self.data_store  = None
        self.plugin_repo = None

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
            cfg['data']['file']
        )

        self.plugin_repo = Repo(
            cfg['module']['login'],
            cfg['module']['repo'],
            cfg['module']['branch'],
            self.credentials
        )
            
credentials = Credentials(username, password)
model       = Model(config_login, config_repo, config_branch, config_filename, credentials)

cfg         = json.loads(model.config.data)
plugin_repo = model.plugin_repo
plugins     = cfg['plugins'].keys()
args        = cfg['plugins'].values()

running = []

# Start plugins
for name,arg in zip(plugins, args):
    plug = Plugin(plugin_repo, name)
    plug.sync()
    running.append((name, plug.run_async(arg)))


#running = load_plugins(model)

# Join
d = json.loads(model.data_store.data)

for name, ret in running:
    val = ret.get()
    d[name] = val

model.data_store.data = json.dumps(d, indent=4)
