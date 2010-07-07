import socket, threading

remote = ('192.168.0.7', 19784)

class remoteSongInfo (threading.Thread):
	def __init__ (self, callback):
		threading.Thread.__init__ (self)
		self.callback = callback

	def run (self):
		self.sock = socket.socket()
		self.sock.connect(remote)
		songInfo = self.sock.recv(8192)

		return self.callback(songInfo.strip().split('\0'))
.
def getSongInfo(callback):
	thread = remoteSongInfo(callback)
	thread.start()

def callback (songInfo):
	if songInfo[0] == 'ERROR':
		if songInfo[1] == 'NOTPLAYING':
			print("Remote music player is not playing")
		elif songInfo[1] == 'NOTRUNNING':
			print("Remote music player is not running")
	else:
		print("Listening to %s by %s - %s (%s/%s)" % tuple(songInfo))

def printSong():
	songInfo = getSongInfo(callback)

printSong()
