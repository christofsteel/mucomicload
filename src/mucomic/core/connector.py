from mucomic.core.models import Issue, Series
from mucomic.core import DB, Api
from mucomic import paths

import shutil
import os.path
from urllib.request import urlopen
import zipfile
import re

class Connector:
	def __init__(self, config):
		self.config = config
		self.db = DB(paths.dbfile)
		self.api = Api(self.config['MUComicLoad']['username'], self.config['MUComicLoad']['password'])

	def updateSeries(self):
		jsonseries = self.api.get_all_series()
		reg = "(?P<title>.*) \((?P<start>[^ ]*)(?: - (?P<end>[^ ]*))?\)"
		parser = re.compile(reg)
		series = []
		for json in jsonseries:
			id = json['id']
			parsedTitle = parser.match(json['title'])
			if parsedTitle:
				title = parsedTitle.group('title')
				start = parsedTitle.group('start')
				end = parsedTitle.group('end')
			else:
				print("Could not parse Title %s" % json['title'])
				title = json['title']
				start = None
				end = None
			series.append(Series(id, title, start, end))
		self.db.add_series(series)

	def getIssues(self, series):
		issues = self.db.get_issue_list(series.id)
		return issues

	def get_series(self, series_id):
		series = self.db.get_series(series_id)
		return series

	def get_added_series(self):
		series = self.db.get_added_series()
		return series

	def updateIssues(self, series):
		jsonissues = self.api.get_series_by_id(series.id)
		issues = [
					Issue(
						id = json['digital_id'],
						series_id = series.id,
						title = series.title,
						issue_number = json['issue_number'],
						cover_url =
							"https://i.annihil.us/u/prod/marvel%s/portrait_incredible.jpg" % json['image_url']
						)
						for json in jsonissues
					]
		self.db.add_issues(issues)
		return issues

	def downloadIssue(self, issue):
		if not os.path.isdir(self.cbzpath(issue)):
			os.makedirs(self.cbzpath(issue))
		filename = "%s_" % self.cbzfile(issue)
		comiczip = zipfile.ZipFile(filename, mode='w')
		pages = self.api.get_issue_by_id(issue.id)['pages']
		links = [page['cdnUrls']['jpg_75']['scalar'] for page in pages if page['cdnUrls']
				!= {}]
		for k, url in enumerate(links):
			image = urlopen(url).read()
			comiczip.writestr('img_%02d.jpg' % k, image)
		comiczip.close()
		shutil.move(filename, self.cbzfile(issue))

	def getFirstCover(self, series):
		maybeFirst = self.db.get_issue_list(series.id, 1)
		if maybeFirst:
			firstIssue = maybeFirst[0]
			return firstIssue.cover()
		else:
			return None

	def updateConfig(self):
		with open(paths.configfile, 'w') as config:
			self.config.write(config)
		self.api = Api(self.config['MUComicLoad']['username'], self.config['MUComicLoad']['password'])

	def cbzpath(self, issue):
		series = self.get_series(issue.series_id)
		safetitle = re.sub('[^\w\-_\.\(\) ]', '',series.formatedseries)
		return os.path.join(self.config['MUComicLoad']['downloaddir'],
				safetitle) 

	def cbzfile(self, issue):
		series = self.get_series(issue.series_id)
		safetitle = re.sub('[^\w\-_\.\(\) ]', '',series.formatedseries)
		return os.path.join(self.config['MUComicLoad']['downloaddir'], safetitle, 
			'%s %s (%s).cbz' % (safetitle, issue.safe_nr, issue.id))

	def issueHasTemp(self, issue):
		return os.path.isfile("%s_" % self.cbzfile(issue))

	def issueHasLocal(self, issue):
		return os.path.isfile(self.cbzfile(issue))
