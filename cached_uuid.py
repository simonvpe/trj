from appdirs import user_cache_dir
import uuid, os

class UUID(object):
    def __init__(self):
        appname   = "testapp"
        appauthor = "testauthor"
        self.dir  = user_cache_dir(appname, appauthor)

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

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
