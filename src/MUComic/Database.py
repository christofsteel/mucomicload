import sqlite3
from MUComic.models import Issue, Series

"""
	Layout:
		Table Series:
			id | title | fav
		Table Issue:
			id | series_id | issue_number | cover_url | cover_img | local	
"""
class DB:
	def __init__(self, db_path):
		self.db_path = db_path
		self.conn = sqlite3.connect(db_path)
		c = self.conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS series(id integer primary key, title unique, fav integer);")
		c.execute("CREATE TABLE IF NOT EXISTS issues(id integer primary key, series_id integer, issue_number string, cover_url string, cover_img blob, local integer);")
		c.close()

	def add_series(self, series):
		c = self.conn.cursor()
		c.execute("INSERT OR IGNORE INTO series (id, title, fav) values (?,?,?)", (series.id, series.title, series.fav))
		c.close()
		self.conn.commit()

	def add_issue(self, issue):
		c = self.conn.cursor()
		print('%s %s' % (issue.title, issue.issue_number))
		c.execute("INSERT OR IGNORE INTO issues (id,series_id,issue_number,cover_url, local) values (?,?,?,?,?)", (issue.id, issue.series_id, issue.issue_number, issue.cover_url, issue.local))
		c.close()
		self.conn.commit()
	
	def set_issue_cover(self, issue, image):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute("UPDATE issues set cover_img = ? where id = ?", (image,
			issue.id))
		c.close()
		conn.commit()
		conn.close()

	def update(self, api, v = 0):
		series = api.get_all_series()
		c = self.conn.cursor()
		for s in series:
			if v == 1:
				print(s[1])
			c.execute("INSERT OR IGNORE INTO series (id, title, fac) values (?,?,?);", (str(s[0], s[1], 0)))
			issues = api.get_series_by_id(s[0])
			for issue in issues:
				if v and v >= 2:
					print ("%s #%s" % (s[1], issue['issue_number']))
		c.close()
		self.conn.commit()

	def search_series(self, term):
		c = self.conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select id, title, fav from series where title LIKE ?', (termperc,))
		series = []
		for row in result:
			series.append(Series(*row))
		return series

	def search(self, term):
		c = self.conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select s.title, i.issue_number, i.id from series as s join issues as i on s.id == i.series_id where s.title LIKE ?',(termperc,)).fetchall()
		return result

	def get_series(self, id):
		c = self.conn.cursor()
		result = c.execute("select * from series where id == ?",
				(id,)).fetchone()
		return Series(*result)

	def get_issue_list(self, series_id):
		c = self.conn.cursor()
		result = c.execute('select issues.id, series.id, issue_number, cover_url, cover_img, title, local from issues join series on issues.series_id == series.id where series_id == ? order by cast(issue_number as real)', (series_id,))
		issues = [Issue(*row) for row in result]
		c.close()
		return issues

	def get_issue_id(self, series_id, issue_nr):
		c = self.conn.cursor()
		result = c.execute('select id from issues where series_id == ? and issue_number == ?', (series_id, str(issue_nr))).fetchone().id
		return result
		
	def get_issue(self, issue_id):
		c = self.conn.cursor()
		result = c.execute('select issues.id, series_id, issue_number, cover_url, cover_img, title, local from issues join series on issues.series_id == series.id where issues.id == ?', (issue_id,)).fetchone()
		return Issue(*result)

	def set_series_fav(self, id, fav):
		c = self.conn.cursor()
		c.execute('update series set fav=? where id = ?', (fav, id))
		c.close()
		self.conn.commit()

	def set_issue_local(self, issue_id, local):
		c = self.conn.cursor()
		c.execute('update issues set local=? where id = ?', (local, issue_id))
		c.close()
		self.conn.commit()

	def get_faved_series(self):
		c = self.conn.cursor()
		result = c.execute('select * from series where fav = 1')
		series = [Series(*row) for row in result]
		c.close()
		return series

	def get_series_list(self):
		c = self.conn.cursor()
		result = c.execute('select * from series')
		series = [Series(*row) for row in result]
		c.close()
		return series

