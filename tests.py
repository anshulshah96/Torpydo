from torpydo import *
	
def send_recv_handshake(handshake, host, port):
	""" Sends a handshake, returns the data we get back. """

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	s.send(handshake)

	data = s.recv(len(handshake))
	s.close()

	return data

if __name__ == "__main__":
	print "Test started\n"

	# torrent = get_torrent_file_decoded(sys.argv[1])
	# print(torrent)
	# print(get_info_hash(torrent))
	# print(gen_peer_id())
	# print(get_total_length(torrent))
	# print(gen_handshake_mes(self.info_hash, self.peer_id))
	torrent = Torrent(sys.argv[1])
	print send_recv_handshake( gen_handshake_mes(torrent.info_hash, torrent.peer_id), '122.168.167.201', 46337 )
