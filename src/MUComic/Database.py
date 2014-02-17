import sqlite3
from MUComic.models import Issue, Series

"""
	Layout:
		Table Series:
			id | title | start | end | added | fav
		Table Issue:
			id | series_id | issue_number | cover_url 
"""
class DB:
	def __init__(self, db_path):
		self.db_path = db_path
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS series(id integer primary key, title string, start integer, end integer, added integer, fav integer);")
		c.execute("CREATE TABLE IF NOT EXISTS issues(id integer primary key, series_id integer, issue_number string, cover_url string);")
		c.close()
		conn.commit()
		conn.close()

	def add_series(self, series):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		for s in series:
			c.execute("INSERT OR IGNORE INTO series (id, title, start, end, added, fav) values (?,?,?,?,?,?)", 
				(s.id, s.title, s.start, s.end, s.added, s.fav))
		c.close()
		conn.commit()
		conn.close()

	def add_issues(self, issues):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		for issue in issues:
			c.execute("INSERT OR IGNORE INTO issues (id,series_id,issue_number,cover_url) values (?,?,?,?)", (issue.id, issue.series_id,
				issue.issue_number,issue.cover_url))
		c.close()
		conn.commit()
		conn.close()

	def add_issue(self, issue):
		print("This is depricated (add_issue)")
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute("INSERT OR IGNORE INTO issues (id,series_id,issue_number,cover_url) values (?,?,?,?)", (issue.id, issue.series_id,
				issue.issue_number,issue.cover_url))
		c.close()
		conn.commit()
		conn.close()
	
	def search_series(self, term):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select * from series where title LIKE ?', (termperc,))
		series = []
		for row in result:
			series.append(Series(*row))
		conn.close()
		return series

	def search(self, term):
		print("This function is depricated")
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select s.title, i.issue_number, i.id from series as s join issues as i on s.id == i.series_id where s.title LIKE ?',(termperc,)).fetchall()
		conn.close()
		return result

	def get_series(self, id):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		result = c.execute("select * from series where id == ?",
				(id,)).fetchone()
		conn.close()
		return Series(*result)

	def get_issue_list(self, series_id, limit=0):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		if limit:
			result = c.execute('select issues.id, series.id, issue_number, cover_url, title from issues join series on issues.series_id == series.id where series_id == ? order by cast(issue_number as real) limit ?', (series_id,limit))
		else:
			result = c.execute('select issues.id, series.id, issue_number, cover_url, title from issues join series on issues.series_id == series.id where series_id == ? order by cast(issue_number as real)', (series_id,))
		issues = [Issue(*row) for row in result]
		c.close()
		conn.close()
		return issues

	def get_issue_id(self, series_id, issue_nr):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		result = c.execute('select id from issues where series_id == ? and issue_number == ?', (series_id, str(issue_nr))).fetchone().id
		conn.close()
		return result
		
	def get_issue(self, issue_id):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		result = c.execute('select issues.id, series_id, issue_number, cover_url, title from issues join series on issues.series_id == series.id where issues.id == ?', (issue_id,)).fetchone()
		conn.close()
		return Issue(*result)

	def set_series_added(self, id, added):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute('update series set added=? where id = ?', (added, id))
		c.close()
		conn.commit()
		conn.close()

	def set_series_faved(self, id, fav):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute('update series set fav=? where id = ?', (fav, id))
		c.close()
		conn.commit()
		conn.close()

	def get_faved_series(self):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		result = c.execute('select * from series where fav = 1')
		series = [Series(*row) for row in result]
		c.close()
		conn.close()
		return series

	def get_added_series(self):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		result = c.execute('select * from series where added = 1')
		series = [Series(*row) for row in result]
		c.close()
		conn.close()
		return series

	def get_series_list(self, sortby=None):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		if sortby:
			print("Order in the court")
			result = c.execute('select * from series order by ?', (sortby,))
		else:
			result = c.execute('select * from series')
		series = [Series(*row) for row in result]
		c.close()
		conn.close()
		return series

