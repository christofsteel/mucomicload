class Issue:
	def __init__(self, id, series_id, issue_number, cover_url = None, cover =
			None, title=None, local=False):
		self.id = id
		self.series_id = series_id
		self.issue_number = issue_number
		self.cover_url = cover_url
		self.cover = cover
		self.title = title
		self.local = local

class Series:
	def __init__(self, id, title, fav=False):
		self.id = id
		self.title = title
		self.fav = fav
		self.issues = []
