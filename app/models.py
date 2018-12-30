from flask import json
from flask_login import UserMixin
from app import FLASK_LOGIN
import os


@FLASK_LOGIN.user_loader
def load_user(id):
    return User(id)

class User(UserMixin):

    phash = ''
    uname = ''

    def __init__(self, id):
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        with open(os.path.join(SITE_ROOT, 'files/users.json')) as f:
            USER_INFO = json.load(f)

        self.uname = id
        if id in USER_INFO:
            self.phash = USER_INFO[id]['phash']
        else:
            self.phash = None

    def get_id(self):
        return self.uname
