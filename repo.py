import base64
from github3 import login, repository

class Credentials(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Repo(object):
    def __init__(self, login_str, repo, branch, credentials = None):
        self.login       = login_str
        self.repo_name   = repo
        self.branch_name = branch

        if credentials is not None:
            github = login(username=credentials.username,
                           password=credentials.password)

            self.repo = github.repository(self.login, self.repo_name)
        else:
            self.repo = repository(self.login, self.repo_name)

        

