from   repo   import Credentials, Repo
from   data   import Datastore
from   plugin import Plugin
import json

from IPython.core.debugger import Tracer

# Fetch config from repository
config_login    = 'simonvpe'
config_repo     = 'trj'
config_branch   = 'master'
config_filename = 'config.json'

config_file = Datastore(
    Repo(
        config_login,
        config_repo,
        config_branch
    ),
    config_filename
)
config = json.loads(config_file.data)

# Repository for data is r/w and requires credentials
datastore = Datastore(
    Repo(
        config['data']['login'],
        config['data']['repo'],
        config['data']['branch'],
        Credentials(
            config['data']['username'],
            config['data']['password']
        )
    ),
    config['data']['file']
)

plugins = config['plugins'].keys()
args    = config['plugins'].values()

running = []

# Start plugins
for name,arg in zip(plugins, args):
    plug = Plugin(Repo(
        config['module']['login'],
        config['module']['repo'],
        config['module']['branch']
    ), name)
    plug.sync()
    running.append((name, plug.run_async(arg)))

# Join
data = json.loads(datastore.data)

for name, ret in running:
    val = ret.get()
    data[name] = val

datastore.data = json.dumps(data)
