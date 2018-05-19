#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse, os, sys, json, time, mimetypes

class Cleaner(object):

  def __init__(self):
    mimetypes.init()
    start_time = time.time()
    self.home = os.environ['HOME']
    self.workdir = 'Downloads'
    self.cleandir = os.path.abspath(self.home+'/'+self.workdir)
    self.folders = ['Pictures', 'Documents', 'Music', 'Archives']
    self.filestoignore = ['.DS_Store', '.localized']
    self.types =  {
      'balls': [
        'application/zip',
        'application/gzip',
        'application/x-tar',
        'application/pkg',
        'application/x-apple-diskimage',
        'application/octet-stream',
      ],
      'video': [
        'video/mpeg',
        'video/mp4',
        'video/ogg',
        'video/quicktime',
        'video/webm',
        'video/x-ms-wmv',
        'video/x-flv',
        'video/3gpp',
        'video/3gpp2'
      ],
      'images': [
        'image/gif',
        'image/jpeg',
        'image/pjpeg',
        'image/png',
        'image/svg+xml',
        'image/tiff',
        'image/vnd.microsoft.icon',
        'image/vnd.wap.wbmp'
      ],
      'music': [
        'audio/basic',
        'audio/L24',
        'audio/mp4',
        'audio/aac',
        'audio/mpeg',
        'audio/ogg',
        'audio/vorbis',
        'audio/x-ms-wma',
        'audio/x-ms-wax',
        'audio/vnd.rn-realaudio',
        'audio/vnd.wave',
        'audio/webm'
      ],
      'docs': [
        'application/epub+zip',
        'text/plain',
        'application/atom+xml',
        'application/EDI-X12',
        'application/EDIFACT',
        'application/json',
        'application/javascript',
        'application/ogg',
        'application/pdf',
        'application/postscript',
        'application/soap+xml',
        'application/x-woff',
        'application/xhtml+xml',
        'application/xml-dtd',
        'application/xop+xml',
        'application/x-tex',
        'application/vnd.oasis.opendocument.spreadsheet',
        'application/vnd.oasis.opendocument.presentation',
        'application/vnd.oasis.opendocument.graphics',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.mozilla.xul+xml',
        'application/vnd.google-earth.kml+xml'
      ],
      'torrents': [
        'application/x-bittorrent'
      ]
    }
    parser = argparse.ArgumentParser(description="Download folder cleaner and recognizer", usage='''cleaner.py [-drfvmqaj]''')
    parser.add_argument('-d', action="store_true", dest="delete")
    parser.add_argument('-f', action="store_true", dest="force")
    parser.add_argument('-v', action="store_true", dest="verbose")
    parser.add_argument('-q', action="store_true", dest="quiet")
    parser.add_argument('-a', action="store_true", dest="all")
    parser.add_argument('-j', action="store_false", dest="json")
    self.results = parser.parse_args()
    if(self.results.json == True):
      self.defaultRecognize()
    print("--- %s seconds ---" % (time.time() - start_time))

  def CheckFolders(self):
    res = {}
    for wdirs in self.folders:
      working_path = os.path.join(self.home, wdirs)
      if os.path.isdir(working_path) == True:
        res[wdirs] =  working_path
        next
      else:
        print('Dir is not Exists, creating' + working_path)
        if(os.makedirs(working_path)):
          print('created' + working_path)
          res[wdirs] =  working_path
          next
    return res

  def gateringFiles(self):
    res = []
    for path,dirs,files in os.walk(self.cleandir):
      for f in files:
        if f not in self.filestoignore:
          file = os.path.join(path,f)
          fl = {}
          if os.path.isfile(file):
            fl['path'] = str(os.path.split(file))
            fl['abspath'] = str(os.path.abspath(file))
            fl['name']= str(os.path.splitext(os.path.split(file)[1])[0])
            fl['ext'] = str(os.path.splitext(file)[1])
            fl['mime'] = mimetypes.guess_type(os.path.abspath(file))[0]
            res.append(fl)
    return res

  def moveFiles(self, file, destfile):
    print('Now moving proccesing for file: '+file['name'])
    os.rename(file['abspath'], destfile)
    if os.path.isfile(destfile):
      res = { 'old': file, 'new': destfile }
    else:
      res = { 'err': { message: 'sorry error while move' } }
    return res

  def removeFile(self, file):
    res = {
      'file': file
    }
    if os.remove(file['abspath']):
      res = {
        'err': 0,
        'message': 'Removed sucessfully'
      }
    else:
      res = {
        'err': 1,
        'message': 'Error in remove file' + file['name']
      }
    return res

  def defaultRecognize(self):
    print('Default recognize files')
    filelist = self.gateringFiles()
    destdirs = self.CheckFolders()
    res = []
    print('Total files for replace or remove: '+str(len(filelist)))
    for file_ in filelist:
      if file_['mime'] in self.types['balls']:
        destfile = destdirs['Archives']+'/'+file_['name']+file_['ext']
        res.append(self.moveFiles(file_, destfile))
      elif file_['mime'] in self.types['docs']:
        destfile = destdirs['Documents']+'/'+file_['name']+file_['ext']
        res.append(self.moveFiles(file_, destfile))
      elif file_['mime'] in self.types['images']:
        destfile = destdirs['Pictures']+'/'+file_['name']+file_['ext']
        res.append(self.moveFiles(file_, destfile))
      elif file_['mime'] in self.types['music']:
        destfile = destdirs['Music']+'/'+file_['name']+file_['ext']
        res.append(self.moveFiles(file_, destfile))
      elif file_['mime'] in self.types['video']:
        destfile = destdirs['Video']+'/'+file_['name']+file_['ext']
        res.append(self.moveFiles(file_, destfile))
      if file_['mime'] in self.types['torrents']:
        res = self.removeFile(file_)
    print(json.dumps(res, sort_keys=True, indent=2))

if __name__ == '__main__':
  Cleaner()
