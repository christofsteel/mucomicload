from mucomic import paths
from urllib.request import urlopen
import os.path
import hashlib

class Issue:
	def __init__(self, id, series_id, issue_number, cover_url = None, title=None):
		self.id = id
		self.downloading = False
		self.series_id = series_id
		self.issue_number = issue_number
		self.safe_nr = self._safe_nr(issue_number)
		self.cover_url = cover_url
		h = hashlib.new('sha256')
		h.update(bytes(self.cover_url, 'utf-8'))
		self.coverFile = os.path.join(paths.coverfolder,h.hexdigest())
		self.title = title

	def __eq__(self, other):
		return self.id == other.id

	def _safe_nr(self,nr):
		if type(nr) is int:
			return '%03d' % nr
		elif type(nr) is float:
			return self._safe_nr(str(nr))
		elif type(nr) is str:
			if '.' in nr:
				split = [int(i) for i in nr.split('.')]
				split[0] = "%03d" % split[0]
				return ".".join([str(s) for s in split])
			else:
				return self._safe_nr(int(nr))
		else:
			print("Unrecognized issue number: %s" % nr)
			return str(nr)

	def cover(self):
		try:
			file = open(self.coverFile, 'rb')
			data = file.read()
			file.close()
			return data
		except:
			return None

	def hasCover(self):
		return os.path.isfile(self.coverFile)

	def getCover(self):
		try:
			url = urlopen(self.cover_url)
			data = url.read()
			h = hashlib.new('sha256')
			h.update(bytes(self.cover_url, 'utf-8'))
			file = open(self.coverFile, 'wb')
			file.write(data)
			file.close()
			url.close()
			return data
		except:
			print("Could not download cover for \"%s #%s\"" % (self.title,
				self.issue_number))
			return None


class Series:
	def __init__(self, id, title, start, end, added=False, fav=False):
		self.id = id
		self.title = title
		self.start = start
		if end == 'present':
			self.end = None
		elif not end is None:
			self.end = end
		else:
			self.end = start
		if self.start:
			self.formatedseries = "(%s) %s" % (self.start, self.title)
		self.added = added
		self.fav = fav
	
	def __eq__(self, other):
		return self.id == other.id
