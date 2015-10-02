from   repo        import Credentials, Repo
from   data        import Datastore
from   plugin      import Plugin
from   cached_uuid import UUID

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

class Model(object):
    def __init__(self, cfg_login, cfg_repo, cfg_branch, cfg_filename, cred=None):
        self.credentials = cred
        self.config = Datastore(
            Repo(
                cfg_login,
                cfg_repo,
                cfg_branch,
                cred
            ),
            cfg_filename
        )

        self.data_repo   = None
        self.plugin_repo = None
        self.uuid        = UUID().uuid()
        self.build(self.config)

    def build(self, config):
        cfg = json.loads(config.data)

        self.data_repo = Repo(
            cfg['data']['login'],
            cfg['data']['repo'],
            cfg['data']['branch'],
            self.credentials
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
plugins     = cfg['plugins'].keys()
args        = cfg['plugins'].values()

# Start plugins
running = []

for name,arg in zip(plugins, args):
    data_filename = os.path.join(model.uuid, name)
    data_file = Datastore(model.data_repo, data_filename)

    plug_filename = name + ".py"
    plug_file = Datastore(model.plugin_repo, plug_filename)
    plug = Plugin(plug_file, data_file, name)
    plug.sync()
    running.append((name, plug.run_async(arg)))

# Join
for name, ret in running:
    val = ret.get()
