import bencoder
import requests
import hashlib
from urllib.parse import urlparse

from os import listdir
from os.path import isfile, join


def send_request(name):
    f = open(name, 'rb')
    d = bencoder.decode(f.read())
    f.close()

    infos = bencoder.encode(d[b'info'])
    hasho = hashlib.sha1()
    hasho.update(infos)
    try:
        url = urlparse(d[b'announce'].decode('UTF-8'))
    except KeyError:
        #Error: announce key not found in .torrent file
        #print('{}.........Announce not found.'.format(name))
        return

    if not url.scheme == 'http':
        # Error: the tracker is not http
        # @todo: 
        # print('{}........Not http: {}'.format(name, url.scheme))
        return


    pl = {}
    pl['uploaded'] = 0
    pl['downloaded'] = 0
    pl['event'] = 'started'
    pl['peer_id'] = '12345asr987654321234'
    pl['info_hash'] = hasho.digest()
    pl['left'] = 0
    pl['port'] = 6881
    pl['compact'] = 1

    try:
        r = requests.get(url.geturl(), params=pl)
    except:
        #ignore
        print('{}.........Error'.format(name))
        #print(r.text)
        #r.raise_for_status()
        return

    try:
        bencoder.decode(r.content)
    except:
        print('{}..........Bencode not valid'.format(name))
        fname = d[b'info'][b'name'].decode('utf-8')
        with open('../res/out/{}.log'.format(fname), 'wb') as mfile:
            mfile.write(r.content)
        return
    #print('-------RESULT-------')
    #print(r.text)
    print('{}.......OK'.format(name))


mypath = '../res/torrent/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for fil in files:
    send_request(mypath+fil)
