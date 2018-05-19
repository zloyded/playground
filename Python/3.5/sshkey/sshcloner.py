#!/usr/bin/env python3 
import os, sys, json, netmiko, argparse,  subprocess, time
from getpass import getpass
from netmiko.linux.linux_ssh import LinuxSSH


class SshCloner(object):
  
  def __init__(self):
    parser = argparse.ArgumentParser(description="Put you id_ssh.pub into your authorized_keys at remotes servers", usage='''./sshcloner.py -s <servers list separate by ','> -k <id_rsa.pub location if not default>''')
    parser.add_argument('-s', dest="servers")
    parser.add_argument('-k', dest="pubkey")
    parser.add_argument('-u', dest="username")
    parser.add_argument('-p', dest="port") #TODO move to servers as additional parameter
    results = parser.parse_args()
    start_time = time.time()
    if results.servers != None:
      self.serverlist = results.servers
    elif results.servers == None:
      print(parser.parse_args(['-h']))
    
    if results.pubkey == None:
      self.publickeyfile = os.path.abspath(os.environ['HOME']+'/.ssh/id_rsa.pub')
    elif results.pubkey != None:
      self.publickeyfile = os.path.abspath(results.pubkey)
    
    if results.username != None:
      self.username = results.username
    elif results.username == None:
      print(parser.parse_args(['-h']))
    
    if results.port != None:
      self.port = results.port
    elif results.port == None:
      print(parser.parse_args(['-h']))
    res = self.existsCheck()
    print(json.dumps(res, sort_keys=True, indent=2))
    print("--- %s seconds ---" % (time.time() - start_time))

  def existsCheck(self):
    if not os.path.exists(self.publickeyfile):
      res = {'error': 1, 'message': 'File '+self.publickeyfile+'doesnt exists'}
    elif os.path.exists(self.publickeyfile):
      res = {'error': 0, 'message': 'File '+self.publickeyfile+' exists'}
    if res['error'] == 1:
      return res
    elif res['error'] == 0:
      res = self.readPublicKey(self.publickeyfile)
    return res

  def readPublicKey(self, pubkeyfile):
    # TODO: check file or key line or add attr for line-key
    with open(pubkeyfile, 'r') as k:
      pub_key = k.read()
    k.close()
    data = {
      "key": pub_key
    }
    res = self.listsServers(data)
    return res
  

  def listsServers(self, key):
    slist = self.serverlist.split(',')
    res = key
    res['servers'] = {}
    for server in slist:      
      p = subprocess.getoutput('host '+server).split(' ')[3]
      print('Enter password for ' + server + ' via ('+p+')')
      password = getpass()
      res['servers'].update({server: {'ip': p, 'port': self.port, 'username': self.username, 'password': password} })
      
    data = self.putKeys(res)
    return data

  def putKeys(self, serverList):
    res = []
    for server in serverList['servers']:
      s = serverList['servers'][server]
      key=serverList['key'].split("\n")[0]
      command = "echo '"+key+"' >> ~/.ssh/authorized_keys"
      try:
        ssh = LinuxSSH(**s)
        if ssh.send_command(command):
          res = {'error': 0, 'message': 'successfully added to '+ s['ip']}
      except TypeError as Err:
        res = Err
    return res

if __name__ == '__main__':
  SshCloner()