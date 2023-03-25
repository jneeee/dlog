'''
Post in DB:
    {'key': post_<id>, # id: random long int
    'prop':{
        'author': <username>,
        'title': xxx,
        'tags': [xx,],
        'create_time': ,
    }
    'content':{
        'raw': xxxx # the markdown file
        'html': xxxx
    }
'''
import time
import markdown
from random import randint

from utils import db, async_exc

class Post:

    def __init__(self, forms, author_name=None, from_db=False) -> None:
        if from_db:
            # key in forms means the data is from db
            self.prop = forms.get('prop')
            self.key = forms.get('key')
            self.content = forms.get('content')
        else:
            # the form is from web post
            self.key = f'post_{randint(0, 100000000000)}'
            self.prop = {
                'tags': [i.strip() for i in forms.get('tags').split(',')],
                'title': forms.get('title'),
                'author': author_name,
                'create_time': time.ctime(time.time()),
            }
            self.content = {
                'raw': forms.get('content'),
                'html': markdown.markdown(forms.get('content')),
            }

    @async_exc
    def save(self):
        item = {
            'key': self.key,
            'type': 'post',
            'prop': self.prop,
            'content': self.content,
        }
        db.put(item)

    @classmethod
    def get_post_inst_by_key(cls, key: str):
        item = db.get(key)
        if not item:
            raise ValueError('No such key!')
        return cls(item, from_db=True)

    @staticmethod
    @async_exc
    def delete_post_by_key(key: str):
        item = db.delete(key)

    @staticmethod
    def fetch_posts(limit=10, last=None):
        '''Get posts list
        
        :return: [] if have no posts, else [{posts.__dict__}, ]
        '''
        filte = {'key?pfx': 'post_'}
        res = db.fetch(filte, limit=limit, last=last)
        items = []
        if res.count:
            items = sorted(
                res.items, 
                key=lambda i: i.get('prop', {}).get('create_time'),
                reverse=True,
            )
        return items

    @staticmethod
    def fetch_by_tag(tag, limit=1000, last=None):
        '''Get posts list(filter by tag)

        :return: [] if have no posts, else [{posts.__dict__}, ]
        '''
        filte = {'prop.tags?contains': tag}
        res = db.fetch(filte, limit=limit, last=last)
        items = []
        if res.count:
            items = sorted(
                res.items, 
                key=lambda i: i.get('prop', {}).get('create_time'),
                reverse=True,
            )
        return items
