import os,sys, requests
from hashlib import sha1
from random import choice
from bencode import encode,decode
from config import *

def print_detail(torrent):
	print "comment: "+torrent['comment']
	print "Announce URL: "+torrent['announce']
	for fl in torrent["info"]["files"]:
	    print "%r - %d bytes" % ("/".join(fl["path"]), fl["length"])

def get_info_hash(torrent):
	return sha1(encode(torrent['info'])).digest()

def get_torrent_file(file_address):
	if os.path.exists(file_address):
	    fh 		= open(file_address,'rb')
	    return fh

def get_torrent_file_decoded(file_address):
	if os.path.exists(file_address):
	    fh 		= open(file_address,'rb')
	    return decode(fh.read())
   	else:
   		print "File Does Not exists"

def get_total_length(torrent):
	length = 0
	for fl in torrent["info"]["files"]:
		length += fl["length"]
	return length

def get_tracker_response(url,info_hash,peer_id,left,port=6881):
	payload = {'info_hash': info_hash, 'peer_id': peer_id, 'left': left, 'port':port,
				'uploaded':0, "compact" : 1}
	r = requests.get(url,params = payload)
	return r


def gen_peer_id():
	'''Generates Peerid with random number of length 12'''
	rn = "-"+CLIENT_ID+CLIENT_VERSION+"-"
	while len(rn) != 20:
		rn = rn + choice("0123456789")
	return rn