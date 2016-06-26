import os,certifi
import sys
from utility import *
from bencode import decode

class Torrent():
	"""Python class which will handle a given torrent"""
	def __init__(self, file_address):
		self.file_address 		= file_address
		# torrent_file_undecoded 	= get_torrent_file(file_address)
		# self.torrent 			= decode(self.torrent_file_undecoded.read())
		self.torrent 			= get_torrent_file_decoded(file_address)
		self.announce 			= self.torrent['announce']
		self.left 				= get_total_length(self.torrent)
		self.info_hash 			= get_info_hash(self.torrent)
		self.peer_id 			= gen_peer_id()

	def connect_to_tracker(self):
		response = get_tracker_response(self.announce,self.info_hash,self.peer_id,self.left)
		print decode(response.content)


def main(args=None):
	if args is None:
		args = sys.argv[1:]
	file_dir = args[0]
	t = Torrent(file_dir)
	t.connect_to_tracker()	
	    
if __name__ == "__main__":
	os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
	main()
