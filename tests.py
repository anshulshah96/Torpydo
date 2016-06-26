from torpydo import *

if __name__ == "__main__":
	print "Test started\n"

	torrent = get_torrent_file_decoded(sys.argv[1])
	print(torrent)
	print(get_info_hash(torrent))
	print(gen_peer_id())
	print(get_total_length(torrent))
