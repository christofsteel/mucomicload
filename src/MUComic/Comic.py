import zipfile

class Series:
	

class Comic:
	pass:

class MUComic:
	class Creators:
		def __init__(self, jsonobj=None):
			pass

	class AuthStr:
		def __init__(self, jsonobj=None):
			pass
	
	class Page:
		class Panels:
			def __init__(self, jsonobj=None):
				pass
		
		class CdnUrls:
			def __init__(self, jsonobj=None):
				if jsonobj == None or jsonobj == {}:
					self.base = None
					self.small_svg = None
					self.svg = None
					self.jpg = None
					self.jpg_75 = None
				else:
					self.loadJson(jsonobj)

			def loadJson(self, jsonobj):
				self.jpg_75 = jsonobj['jpg_75']['scalar']
			
		
		def __init__(self, jsonobj=None):
			if jsonobj == None:
				self.ad_url = None
				self.cdnUrls = MUComic.Page.CdnUrls()
				self.color_file = None
				self.id = None
				self.is_ad = None
				self.is_double = None
				self.order_nr = None
				self.panels = MUComic.Page.Panels()
			else:
				self.loadJson(jsonobj)

		def get_jpg_url(self):
			return self.cdnUrls.jpg_75

		def loadJson(self, jsonobj):
			self.ad_url = jsonobj['ad_url']
			self.cdnUrls = MUComic.Page.CdnUrls(jsonobj['cdnUrls'])
			self.color_file = jsonobj['color_file']
			self.id = jsonobj['id']
			self.is_ad = jsonobj['is_ad']
			self.is_double = jsonobj['is_double']
			self.order_nr = jsonobj['order_nr']
			self.panels = MUComic.Page.Panels(jsonobj['panels'])

	def __init__(self, jsonobj=None):
		if jsonobj == None:
			self.familyId = None
			self.publicationWeight = None
			self.seriesName = None
			self.viewCount = None
			self.releaseDate = None
			self.number = None
			self.seriesId = None
			self.isPreview = None
			self.viewsLastWeek = None
			self.readerDescription = None
			self.mainsite = None
			self.creators = MUComic.Creators()
			self.businessUnit = None
			self.publicationEndDate = None
			self.readsLastWeek = None
			self.teaserSpreads = None
			self.pages = []
			self.isFree = None
			self.description = None
			self.seriesEndYear = None
			self.thumbnail = None
			self.publicationStartDate = None
			self.readsThisWeek = None
			self.ratingCount = None
			self.viewsThisWeek = None
			self.hasFutureReleaseDate = None
			self.ratingAverage = None
			self.catalogId = None
			self.seriesTitle = None
			self.previewText = None
			self.authStr = MUComic.AuthStr()
			self.solicitText = None
			self.businessFamily = None
			self.seriesStartYear = None
			self.id = None
		else:
			self.loadJson(jsonobj)

	def loadJson(self, jsonobj):
			self.familyId = jsonobj['familyId']
			self.publicationWeight = jsonobj['publicationWeight']
			self.seriesName = jsonobj['seriesName']
			self.viewCount = jsonobj['viewCount']
			self.releaseDate = jsonobj['releaseDate']
			self.number = jsonobj['number']
			self.seriesId = jsonobj['seriesId']
			self.isPreview = jsonobj['isPreview']
			self.viewsLastWeek = jsonobj['viewsLastWeek']
			self.readerDescription = jsonobj['readerDescription']
			self.mainsite = jsonobj['mainsite']
			self.creators = MUComic.Creators(jsonobj['creators'])
			self.businessUnit = jsonobj['businessUnit']
			self.publicationEndDate = jsonobj['publicationEndDate']
			self.readsLastWeek = jsonobj['readsLastWeek']
			self.teaserSpreads = jsonobj['teaserSpreads']
			self.pages = [MUComic.Page(page) for page in jsonobj['pages']]
			self.isFree = jsonobj['isFree']
			self.description = jsonobj['description']
			self.seriesEndYear = jsonobj['seriesEndYear']
			self.thumbnail = jsonobj['thumbnail']
			self.publicationStartDate = jsonobj['publicationStartDate']
			self.readsThisWeek = jsonobj['readsThisWeek']
			self.ratingCount = jsonobj['ratingCount']
			self.viewsThisWeek = jsonobj['viewsThisWeek']
			self.hasFutureReleaseDate = jsonobj['hasFutureReleaseDate']
			self.ratingAverage = jsonobj['ratingAverage']
			self.catalogId = jsonobj['catalogId']
			self.seriesTitle = jsonobj['seriesTitle']
			self.previewText = jsonobj['previewText']
			self.authStr = MUComic.AuthStr(jsonobj['authStr'])
			self.solicitText = jsonobj['solicitText']
			self.businessFamily = jsonobj['businessFamily']
			self.seriesStartYear = jsonobj['seriesStartYear']
			self.id = jsonobj['id']

	def get_comic_jpg_urls(self):
		return [page.get_jpg_url() for page in self.pages if page.get_jpg_url() != None]

	def download(self, filename):
		if os.path.isdir(filename):
			filename = os.path.join(filename, self.get_name() + '.cbz')
		print('Downloading to %s' % filename)
		comiczip = zipfile.ZipFile(filename, mode='w')
		for k, url in enumerate(self.get_comic_jpg_urls()):
			#print('Page %02d' % k)
			image = urlopen(url).read()
			comiczip.writestr('img_%02d.jpg' % k, image)
		comiczip.close()

	def get_name(self):
		return '(%s) %s - %03d' % (self.seriesStartYear, self.seriesName, int(self.number))
