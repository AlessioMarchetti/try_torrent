import bencoder
import requests
import hashlib
from urllib.parse import urlparse

# only in debug phase
from os import listdir
from os.path import isfile, join


def send_request(name):
    """
    send the request for the peer list to the tracker specified by the name
        .torrent file.
    """

    # get the text of the .torrent file
    with open(name, 'rb') as f:
        d = bencoder.decode(f.read())

    # calculate the sha1sum of the info dictionary
    # (info_hash parameter in the request)
    infos = bencoder.encode(d[b'info'])
    hasho = hashlib.sha1()
    hasho.update(infos)
    sha1sum = hasho.digest()

    # get the tracker url
    try:
        url = urlparse(d[b'announce'].decode('UTF-8'))
    except KeyError:
        # Error: announce key not found in .torrent file
        # print('{}.........Announce not found.'.format(name))
        return

    def http_request(url, sha1sum):
        # initialize the dictionary with the params to send to the tracker
        pl = {}
        pl['uploaded'] = 0
        pl['downloaded'] = 0
        pl['event'] = 'started'
        pl['peer_id'] = '12345asr987654321234'
        pl['info_hash'] = sha1sum
        pl['left'] = 0
        pl['port'] = 6881
        pl['compact'] = 1

        # send the HTTP GET request
        r = requests.get(url.geturl(), params=pl)
        return r

    # check the protocol
    if url.scheme == 'http':
        try:
            r = http_request(url, sha1sum)
        except:
            #ignore
            print('{}.........Error'.format(name))
            #print(r.text)
            #r.raise_for_status()
            return None
    elif url.scheme == 'udp':
        # todo: implement udp
        return
    else:
        # Error: the tracker is not http or udp
        # print('{}........Not http: {}'.format(name, url.scheme))
        return

    # try to decode the return
    try:
        bencoder.decode(r.content)
    except:
        print('{}..........Bencode not valid'.format(name))
        fname = d[b'info'][b'name'].decode('utf-8')
        with open('../res/out/{}.log'.format(fname), 'wb') as mfile:
            mfile.write(r.content)
        return

    # for debug only
    print('{}.......OK'.format(name))


mypath = '../res/torrent/'
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for fil in files:
    send_request(mypath+fil)
