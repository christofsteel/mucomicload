from MUComic.models import Issue, Series
import os.path
from urllib.request import urlopen
import zipfile

class Connector:
	def __init__(self, db, api):
		self.db = db
		self.api = api

	def updateSeries(self):
		jsonseries = self.api.get_all_series()
		series = [
					Series(
						id = json['id'],
						title = json['title']
						)
						for json in jsonseries
					]
		for s in series:
			self.db.add_series(s)

	def getIssues(self, series):
		issues = self.db.get_issue_list(series.id)
		return issues

	def get_series(self, series_id):
		series = self.db.get_series(series_id)
		return series

	def get_faved_series(self):
		series = self.db.get_faved_series()
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
							"https://i.annihil.us/u/prod/marvel%s/portrait_xlarge.jpg" % json['image_url']
						)
						for json in jsonissues
					]
		for issue in issues:
			self.db.add_issue(issue)
		return issues

	def downloadIssue(self, issue):
		print("start Downloading")
		pages = self.api.get_issue_by_id(issue.id)['pages']
		links = [page['cdnUrls']['jpg_75']['scalar'] for page in pages if page['cdnUrls']
				!= {}]
		if not os.path.isdir(issue.cbzpath):
			os.makedirs(issue.cbzpath)
		filename = issue.cbzfile
		comiczip = zipfile.ZipFile(filename, mode='w')
		for k, url in enumerate(links):
			print("page %s" % k)
			image = urlopen(url).read()
			comiczip.writestr('img_%02d.jpg' % k, image)
		comiczip.close()
		print('"%s" Downloaded' % issue.cbzpath)
