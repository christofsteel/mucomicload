from MUComic.models import Issue, Series
from urllib.request import urlopen

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
						id = json['id'],
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

	def getCover(self, issue):
		try:
			url = urlopen(issue.cover_url)
			data = url.read()
			self.db.set_issue_cover(issue, data)
			return data
		except:
			print("Could not download cover for \"%s #%s\"" % (issue.title,
				issue.issue_number))
			return None
