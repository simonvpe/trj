from repo   import Credentials, Repo
from data   import Datastore
from plugin import Plugin
import json

config = {
    'username': 'simonvpe',
    'password': '******',
    'module' : {
        'login': 'simonvpe',
        'repo': 'trj_modules',
        'branch': 'master'
    },
    'data' : {
        'login': 'simonvpe',
        'repo': 'trj_modules',
        'branch': 'master',
        'file': 'datastore_file'
    },
    'plugins': {
        'helloworld.py' : {
            'number' : 12
        }
    }
}

cred    = Credentials(config['username'],
                      config['password'])

repo_module = Repo(config['module']['login'],
                   config['module']['repo'],
                   config['module']['branch'])

repo_data   = Repo(config['data']['login'],
                   config['data']['repo'],
                   config['data']['branch'],
                   cred)

datastore = Datastore(repo_data, config['data']['file'])

plugins = config['plugins'].keys()
args    = config['plugins'].values()

running = []

# Start plugins
for name,arg in zip(plugins, args):
    plug = Plugin(repo_module, name)
    plug.sync()
    running.append((name, plug.run_async(arg)))

# Join
data = {}
for name, ret in running:
    val = ret.get()
    data[name] = val

datastore.data = json.dumps(data)
