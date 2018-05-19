""" Files mongo Model

  :returns: (obj) Mongo document.
"""
from mongoengine import *

class Files(Document):
  """ Class Files set Files model

    :name: name of file.
    :path: file to path.
    :url: url to club-photo.ru.
  """
  name = StringField(required=True) # caller number: for incoming-phone number for out 3 digit ext num
  path = StringField(required=True) # destionation numbers
  url = StringField(required=True) # Call date

