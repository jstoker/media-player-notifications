import dbus, asyncore
from socket import AF_INET, SOCK_STREAM

class server (asyncore.dispatcher):
	def __init__ (self):
		asyncore.dispatcher.__init__ (self)
		self.create_socket (AF_INET, SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('0.0.0.0', 19784))
		self.listen(1)
		print 'Server listening...'
	
	def handle_accept(self):
		sock, (host, port) = self.accept()
		sock.send(str(getSongInfo())+'\r\n')
		sock.close()
		return

def getSongInfo():
	bus = dbus.SessionBus()
	try:
		remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
		iface = dbus.Interface(remote_object, "org.exaile.Exaile")
	
		if iface.IsPlaying():
			title = iface.GetTrackAttr("title")
			album = iface.GetTrackAttr("album")
			artist = iface.GetTrackAttr("artist")
			pos = iface.CurrentPosition()
			length = iface.GetTrackAttr("__length")
			if length > 0:
				length = '%d:%02d' % (float(length) / 60, float(length) % 60)
			else:
				length = "0:00"
				
			return '%s\0%s\0%s\0%s\0%s' % (title, artist, album, pos, length)
		else:
			return 'NOTPLAYING'
	except dbus.exceptions.DBusException:
		return 'NOTRUNNING'

if __name__ == '__main__':
	server()
	asyncore.loop()
