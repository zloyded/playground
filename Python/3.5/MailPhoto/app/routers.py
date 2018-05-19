from flask import render_template, request
import jinja2,json
from app import app
from app.controllers import *

loader = jinja2.ChoiceLoader([ app.jinja_loader, jinja2.FileSystemLoader(['/app/templates/'])])
app.jinja_loader = loader

class Core:

  @app.route("/mailsphoto")
  @app.route("/mailsphoto/<int:skip>")  
  def getIndex(skip=None):
    """ MailsPhoto render template
      
      :Args:
        :url: /mailsphoto/(?skip:int)
      :params:
        :skip (int): Кол-во записей для пропуска (пагинация)
      :returns:
        Рендер странички с фотографиями
    """
    response = core.Core.getIndex(skip)
    return render_template('index.jinja2', data=response)

  @app.route("/api/v1/photos", methods=['GET'])
  @app.route("/api/v1/photos/<int:skip>", methods=['GET'])
  def getApi(skip=None):
    """ Mетод для API

      :returns: Список объектов Files 
        :list: 
    """
    response = core.Core.getIndex(skip)
    r = []
    for res in response['files']:
      del res['_id']
      r.append(res)
    return json.dumps(r)