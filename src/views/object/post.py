'''
User in DB:
    {'key': post_<id>,
    'prop':{
        'author': asdasd, 'title':xxx, 'tags':xxxx,
    }
    'content':{
        'raw': xxxx
        'html': xxxx
    }
'''
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
            'prop': {
                'author': self.author,
                'title': self.title,
                'tags': self.tags,
            },
            'content': {
                'pure': self.content,
                'html': self.content_html,
            }
        }
        db.put(item)

    @classmethod
    def get_post_info_by_key(cls, key: str):
        item = db.get(key)
        if not item:
            raise ValueError('No such key!')
        return cls(item, from_db=True)
