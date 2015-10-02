from base64 import b64decode
from repo import Credentials, Repo
from IPython.core.debugger import Tracer

class DatastoreReadonly(object):
    def __init__(self, repo, name):
        self.repo = repo
        self.name = name
        self.unread = True

class Datastore(object):
    def __init__(self, repo, name):
        self.repo   = repo
        self.name   = name
        self.unread = True

        try:
            self.file = repo.repo.create_file(name,
                                              "Created file %s" % name,
                                              "{}",
                                              repo.branch_name)
        except Exception, e:
            pass

        self.file = repo.repo.file_contents(name, repo.branch_name)

    def check_update(self):
        sha = self.file.sha[:]
        self.file.refresh()
        return (self.file.sha != sha) or self.unread

    def delete(self):
        self.file.delete("Deleted file %s" % self.name, repo.branch_name)
        self.file = None

    @property
    def data(self):
        self.unread = False
        return b64decode(self.file.content)
        
    @data.setter
    def data(self, newdata):
        if newdata == self.data: return

        self.file.update("Updated file %s" % self.name,
                         newdata, self.repo.branch_name)
        self.file.refresh()
        self.unread = True

