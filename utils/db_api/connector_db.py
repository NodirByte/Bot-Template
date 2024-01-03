import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
from django import setup
setup()
from asgiref.sync import sync_to_async

"""You can write code here ..."""