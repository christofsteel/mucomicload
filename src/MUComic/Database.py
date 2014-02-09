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
		conn = sqlite3.connect(db_path)
		c = conn.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS series(id integer primary key, title unique, fav integer);")
		c.execute("CREATE TABLE IF NOT EXISTS issues(id integer primary key, series_id integer, issue_number string, cover_url string, cover_img blob, local integer);")
		c.close()
		conn.commit()
		conn.close()

	def add_series(self, series):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute("INSERT OR IGNORE INTO series (id, title, fav) values (?,?,?)", (series.id, series.title, series.fav))
		c.close()
		conn.commit()
		conn.close()

	def add_issue(self, issue):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		print('DEBUG: Adding %s %s' % (issue.title, issue.issue_number))
		c.execute("INSERT OR IGNORE INTO issues (id,series_id,issue_number,cover_url, cover_img, local) values (?,?,?,?,?,?)", (issue.id, issue.series_id, issue.issue_number,issue.cover_url, issue.cover, issue.local))
		c.close()
		conn.commit()
		conn.close()
	
	def set_issue_cover(self, issue, image):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute("UPDATE issues set cover_img = ? where id = ?", (image,
			issue.id))
		c.close()
		conn.commit()
		conn.close()

	def update(self, api, v = 0):
		conn = sqlite3.connect(self.db_path)
		series = api.get_all_series()
		c = conn.cursor()
		for s in series:
			if v == 1:
				print(s[1])
			c.execute("INSERT OR IGNORE INTO series (id, title, fac) values (?,?,?);", (str(s[0], s[1], 0)))
			issues = api.get_series_by_id(s[0])
			for issue in issues:
				if v and v >= 2:
					print ("%s #%s" % (s[1], issue['issue_number']))
		c.close()
		conn.commit()
		conn.close()

	def search_series(self, term):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select id, title, fav from series where title LIKE ?', (termperc,))
		series = []
		for row in result:
			series.append(Series(*row))
		conn.close()
		return series

	def search(self, term):
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

	def get_issue_list(self, series_id):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		print("DEBUG: Get Issue List (%s)" % series_id)
		result = c.execute('select issues.id, series.id, issue_number, cover_url, cover_img, title, local from issues join series on issues.series_id == series.id where series_id == ? order by cast(issue_number as real)', (series_id,))
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
		result = c.execute('select issues.id, series_id, issue_number, cover_url, cover_img, title, local from issues join series on issues.series_id == series.id where issues.id == ?', (issue_id,)).fetchone()
		conn.close()
		return Issue(*result)

	def set_series_fav(self, id, fav):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute('update series set fav=? where id = ?', (fav, id))
		c.close()
		conn.commit()
		conn.close()

	def set_issue_local(self, issue_id, local):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute('update issues set local=? where id = ?', (local, issue_id))
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

	def get_series_list(self):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		result = c.execute('select * from series')
		series = [Series(*row) for row in result]
		c.close()
		conn.close()
		return series

