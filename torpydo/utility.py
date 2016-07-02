import os,sys, requests
from hashlib import sha1
from random import choice
from bencode import encode,decode
from config import *
import socket
from struct import unpack

def decode_port(port):
	""" Given a big-endian encoded port, returns the numerical port. """

	return unpack(">H", port)[0]

def get_cuts(peer_str,n):
	# print peer_str
	peer_list = []
	i = n
	while(i <= len(peer_str)):
		peer_list.append(peer_str[(i-n):i])
		i += n
	return [(socket.inet_ntoa(p[:4]), decode_port(p[4:])) for p in peer_list]
	# return peer_list

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

def get_tracker_response(url,info_hash,peer_id,left,port=6882):
	payload = {'info_hash': info_hash, 'peer_id': peer_id, 'left': left, 'port':port,
				'uploaded':0, "compact" : 1}
	r = requests.get(url,params = payload)
	return parse_tracker_response(r)

def parse_tracker_response(res):
	res = decode(res.content)
	res['peers'] = get_cuts(res['peers'],6)
	return res

def gen_peer_id():
	'''Generates Peerid with random number of length 12'''
	rn = "-"+CLIENT_ID+CLIENT_VERSION+"-"
	while len(rn) != 20:
		rn = rn + choice("0123456789")
	return rn

def gen_handshake_mes(info_hash, peer_id):
	message =( chr(19) + "BitTorrent protocol" +
           8 * chr(0) + info_hash + peer_id )
	return message
def dec_handshake_mes(response):
	pstrlen = response[0]
	pstr = response[1:20]
	reserved = response[20:28]
	info_hash = response[28:48]
	peer_id = response[48:68]
	return (info_hash,peer_id)

def verify_peer(response,peer_id):
	if peer_id == response[48:68]:
		return True
	else:
		return False