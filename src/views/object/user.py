'''
User in DB:
    {'key': user_<username>, 
    'name': asdasd, 'passwd':xxx, 'uuid':xxxx, 
    'prop':{
        register_time: xxxx
        last_login_time: xxxx
    }
'''
from utils import db


class User:
    def __init__(self, info: dict):
        self.name = info.get('name')
        self.passwd = info.get('passwd')

    @classmethod
    def get_by_name(cls, username):
        ret = db.get(f'user_{username}')
        if ret:
            return cls(ret)
        else:
            raise ValueError('没有这个用户')

    @staticmethod
    def create_user(info):
        key = 'user_%s' % info.get('username')
        if not db.get(key):
            db.put(info, key=key)
        else:
            raise ValueError('该用户已存在')

    @staticmethod
    def check_login_valid(info):
        key = 'user_%s' % info.get('username')
        user_info = db.get(key)
        if info.get('password') == user_info.get('password'):
            return True
        else:
            return False
