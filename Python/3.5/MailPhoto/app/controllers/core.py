""" Mailer Core controller 
"""
import os, json
from app import models as m
from app import mongo
from app import app
class Core:
  '''Mailer Core class
  '''
  def getIndex(skip):
    """ MailsPhoto найдет все записи в базе данных

    :param skip: пропуск
    :param type: int
    :returns: data (list): Список объектов
    """
    files = []
    if skip == None: skip = 0
    for file in mongo.db.files.find().sort('_id', -1).limit(50).skip(skip):
      files.append(file)
    count = mongo.db.files.count()
    data = { 
      'name': 'Mail reciever and publishing pictures',
      'files': files,
      'count': count,
      'skip': skip
    }
    return  data