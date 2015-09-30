from base64 import b64decode
from repo import Credentials, Repo

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
        except:
            pass

        self.file = repo.repo.contents(name, repo.branch_name)

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
        if newdata == self.data:
            print "[!] No change in file %s" % self.name
            return

        self.file.update("Updated file %s" % self.name,
                         newdata, self.repo.branch_name)
        self.file.refresh()
        self.unread = True

ds = None
if __name__=="__main__":
    cred = Credentials('simonvpe','******')
    repo = Repo('simonvpe','trj_modules','master', cred)
    ds = Datastore(repo, 'teststore3')

