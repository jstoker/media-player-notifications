import xchat, sys, socket, threading
__module_name__ = "Now Playing (from network)" 
__module_version__ = "1.0"
__module_description__ = "Network now playing script"

remote = ('192.168.0.7', 19784)

class remoteSongInfo (threading.Thread):
	def __init__ (self, callback, *args, **kwargs):
		threading.Thread.__init__ (self)
		self.callback = callback
		self.args = args
		self.kwargs = kwargs

	def run (self):
		self.sock = socket.socket()
		self.sock.connect(remote)
		songInfo = self.sock.recv(8192)

		return self.callback(songInfo.strip().split('\0'), self.args, self.kwargs)

def getSongInfo(callback, userdata):
	thread = remoteSongInfo(callback, userdata)
	thread.start()

def callback (songInfo, userdata):
	if songInfo[0] == 'ERROR':
		if songInfo[1] == 'NOTPLAYING':
			xchat.prnt("Remote music player is not playing")
		elif songInfo[1] == 'NOTRUNNING':
			xchat.prnt("Remote music player is not running")
	else:
		if not userdata:
			xchat.command("me is listening to %s by %s - %s (%s/%s)" % tuple(songInfo))
		else:
			xchat.command("me is listening to \x0303%s\x03 by \x0303%s\x03 - \x0303%s\x03 (\x0305%s\x03/\x0305%s\x03)" % tuple(songInfo))

def printSong(word, word_eol, userdata):
	songInfo = getSongInfo(callback, (userdata,))
	return xchat.EAT_ALL

xchat.prnt("Network Now Playing script initialized")
xchat.prnt("Use /np to announce the currently played song")
xchat.hook_command("np", printSong)
