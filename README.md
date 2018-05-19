# PLAYGROUND
## PYTHON 3
 - [PDF to TXT](#pdf-to-txt)
 - [Downloads Cleaner](#downloads-cleaner)
 - [MailPhotos](#mailphotos)
 - [SSHCloner](#sshcloner).

### PDF to TXT 
Just for know how lobrary works.
Save input PDF file to txt with Page wrapp or without
#### Example
```bash
pdf.py -i /path/to/pdf.pdf -o /path/to/out.txt -w
```
### Downloads Cleaner
Finding all files like torrents and images
Remove torrent files, images and gifs put in to ~/Prictures folder.
Long name files as <data-name>.png move to ~/Pictures/Screenshots folder.
PDF files move to ~/Documents/PDF folder.
Berofe script start work, he will create needed folders, check you permissions, script will not do it.
#### Example
Just run ```./cleaner```
After i`ll add some functional for find and clean up home dir. 
 - only JSON out,
 - add advanced types
 - attrs for not move or not delete files like torrent
 - advances destination folder

### MailPhotos 
just IMAP client, go to my dog@mail, get from imap-folder all mail, 
parse for IMAGES put in to mongo. Backend-side: (admin) remove some photos. All photo gedding from http://club-photo.ru

Generate html docs:

```bash
  make html
```

### SSHCloner
Get Your ssh public key and put em to servers in list
for example:
```bash
./sshcloner.py -s server.com, example.com -u username -p <port number(only one for all servers)> -k </path/to/pubkey.file>
```
