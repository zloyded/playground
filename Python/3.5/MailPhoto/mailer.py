# -*- coding: utf-8 -*-
"""Mail downloader
    :platform: Unix, Mac, Windows
    :synopsis: A useful mailer 
.. moduleauthor:: zloyded <me@zloz.ru>
"""
from flask import request
from app import app
import sys,os,yaml, imaplib, getpass, email, re, email.header, datetime, wget, pymongo
from pymongo import MongoClient


EMAIL_ACCOUNT   = app.config['COMMON']['email']
EMAIL_FOLDER    = app.config['COMMON']['email_folder']
EMAIL_PASSWORD  = app.config['MAILER']['email_pass']
DOWN_PATH       = app.config['COMMON']['downloaded']

client = MongoClient('localhost', 27017)
db = client.Mailer

class Mailer:
    """ Class Mailer
    .. module:: Mailer
        :class: Mailer
    """
    def __init__(self):
        """
        ..Class: Mailer
            :func: __init__
            Runner
        """
        self.run()
    def process_mailbox(self, M):
        ''' Process emails parse and getting images, putting into DB 
            
            :param M: imaplib instance.
            :type M: instance.
            :returns: img (list): array of files
        '''
        rv, data = M.search(None, "(ALL)")
        if rv != 'OK':
            print("No messages found!")
            return 1
        imgs = []
        for num in data[0].split():
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
                return 1
            sys.stdout.write('.')
            msg = email.message_from_bytes(data[0][1])
            hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
            pattern = re.compile('https?:\/\/.*\.(?:png|jpg)')
            res = pattern.findall(str(msg), 2)
            for r in res:
                
                image = r.replace('small','photo')
                if image.find('http://club.foto.ru/images/banner') == -1:
                    filename = os.path.split(image)[1]
                    if self.chekFiles(filename) == True:
                        next
                    else:
                        fl = self.downloadFile(image)
                        jsondata = self.mkDbNode(filename)

        sys.stdout.write('\n')
        return imgs

    def chekFiles(self, filename):
        '''Check existing file and update/ insert db
        
           Args:
            file (str): Filename
           Returns:
            bool(True/False)::

                True -- File exists. lookup db and insert entrie if not exists!
                False -- File not exists. 

        '''
        if os.path.isfile(os.path.join(os.path.abspath(DOWN_PATH) , filename)):
            sys.stdout.flush()
            fdb = db.files
            fdbf = fdb.find_one({'name': filename})
            if fdbf is None:            
                self.mkDbNode(filename)
            elif 'url' not in fdbf:
                self.updDbNode(fdbf,filename)
            return True
        
        return False

    def updDbNode(self, fdbf, filename):
        '''Update node if url is not in results

            :param fdbf: File DB object.
            :type fdbf: obj.
            :param filename: Filename for update.
            :type filename: str.
            :returns: int -- the return code
        '''
        fdbf['url'] = 'http://club.foto.ru/gallery/photos/photo.php?photo_id='+filename
        if fdb.update_one({'_id': fdbf['_id']}, {'$set': fdbf}):
            return fdbf
        return 0

    def downloadFile(self, file):
        '''Download a file

            :param file: url to file.
            :type file: url.
            :returns: int -- return code.
        '''
        w = wget.download(file, os.path.abspath(DOWN_PATH))
        if w:
            return w
        return 0

    def mkDbNode(self, filename):
        '''Inser DB object

            :param filename: Filename for insert.
            :type filename: str.
            :returns: 
                int or object  The return code:: 

                    0 -- not inserted, or already exists.
                    object({ 'name': 'name', 'url':'url', 'path': 'path to file' }) -- inserted obj
        '''
        fdb = db.files
        fl = {
            'name': filename,
            'path': os.path.abspath(DOWN_PATH),
            'url': 'http://club.foto.ru/gallery/photos/photo.php?photo_id='+filename
        }
        fdbf = fdb.insert_one(fl).inserted_id
        if fdbf:
            return fdbf
        return 0

    def run(self):
        '''Mailer runner.
            Start proccessing.
            Connect to Imap-server, provide password and login.
            
            :returns: none.
        '''
        M = imaplib.IMAP4_SSL('imap.yandex.ru')
        try:
            rv, data = M.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        except imaplib.IMAP4.error:
            print("LOGIN FAILED!!!")
            sys.exit(1)
        rv, data = M.select(EMAIL_FOLDER)
        if rv == 'OK':
            images = self.process_mailbox(M)
            M.close()
        else:
            print("ERROR: Unable to open mailbox ", rv)
        M.logout()

if __name__ == '__main__':
    Mailer()
