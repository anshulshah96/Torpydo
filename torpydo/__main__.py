import os,certifi
import sys
from utility import *
from threading import Thread
from time import sleep, time
import signal

def handler(signum, frame):
	print "Exiting..."
	sys.exit(0)

class Torrent():
	"""Python class which will handle a given torrent"""
	def __init__(self, file_address):
		self.running			= False
		self.file_address 		= file_address
		self.torrent 			= get_torrent_file_decoded(file_address)
		self.announce 			= self.torrent['announce']
		self.left 				= get_total_length(self.torrent)
		self.info_hash 			= get_info_hash(self.torrent)
		self.peer_id 			= gen_peer_id()
		self.peer_list			= []		#list of (ip, port) of peers
		self.handshake_message 	= gen_handshake_mes(self.info_hash, self.peer_id)
		try:
			assert len(self.info_hash) == 20
			assert len(self.peer_id) == 20
		except Exception,msg:
			print msg
			sys.exit(0);

	def connect_to_tracker(self):
		while self.running:
			response = get_tracker_response(self.announce,self.info_hash,self.peer_id,self.left)
			print response
			# self.peers = []
			for peer in response['peers']:
				if peer not in self.peer_list:
					try:
						payload = self.handshake_to_peer(peer)
						hinfo_hash,hpeer_id = dec_handshake_mes(payload)
						if hinfo_hash != self.info_hash:
							raise Exception("info_hash does not match expected for ip: "+str(peer))
						else:
							print "new peer " + str(peer)
							self.peer_list.append(peer)
					except Exception,msg:
						print msg
			sleep(response['interval'])

	def run(self):
		if self.running == False:
			self.running = True
			self.connect_to_tracker()
			# self.tracker_loop = Thread(target = self.connect_to_tracker)
			# self.tracker_loop.start()

	def stop():
		if self.running:
			self.running = False
			self.tracker_loop.join()

	def handshake_to_peer(self,(ip,port)):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5.0)
		s.connect((ip, port))
		s.send(self.handshake_message)
		s.settimeout(1800.0)
		data = s.recv(len(self.handshake_message))
		s.close()
		return data

def main(args=None):
	if args is None:
		args = sys.argv[1:]
	file_dir = args[0]
	t = Torrent(file_dir)
	t.run()
	    
if __name__ == "__main__":
	signal.signal(signal.SIGINT, handler)
	os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
	main()
