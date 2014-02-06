import sqlite3
from collections import namedtuple


"""
	Layout:
		Table Series:
			id | title | fav
		Table Issue:
			id | series_id | issue_number | cover_link | cover_img | local	
"""
class DB:
	def namedtuple_factory(self, cursor, row):
		"""
		Usage:
		con.row_factory = namedtuple_factory
		"""
		fields = [col[0] for col in cursor.description]
		Row = namedtuple("Row", fields)
		return Row(*row)

	def __init__(self, db_path):
		self.conn = sqlite3.connect(db_path)
		self.conn.row_factory = self.namedtuple_factory
	
	def init_db(self):
		c = self.conn.cursor()
		c.execute("CREATE TABLE series(id integer primary key, title unique, fav integer);")
		c.execute("CREATE TABLE issues(id integer primary key, series_id \
				integer, issue_number string, local integer);")
		c.close()

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
				c.execute("INSERT OR IGNORE INTO issues (id,series_id,issue_number,local) values (?,?,?,?)",(issue['digital_id'], s[0], issue['issue_number'], 0))
		c.close()
		self.conn.commit()

	def search_series(self, term):
		c = self.conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select title, id from series where title LIKE ?', (termperc,))
		rresult = []
		for row in result:
			rresult.append(row)
		return rresult

	def search(self, term):
		c = self.conn.cursor()
		termperc = "%" + term + "%"
		result = c.execute('select s.title, i.issue_number, i.id from series as s join issues as i on s.id == i.series_id where s.title LIKE ?',(termperc,)).fetchall()
		return result

	def get_series(self, id):
		c = self.conn.cursor()
		result = c.execute("select * from series where id == ?",
				(id,)).fetchone()
		return result

	def get_issue_list(self, series_id):
		c = self.conn.cursor()
		result = c.execute('select issue_number, issues.id, local, series.title from issues join series on issues.series_id == series.id where series_id == ? order by cast(issue_number as real)', (series_id,)).fetchall()
		return result

	def get_issue_id(self, series_id, issue_nr):
		c = self.conn.cursor()
		result = c.execute('select id from issues where series_id == ? and issue_number == ?', (series_id, str(issue_nr))).fetchone().id
		return result
		
	def get_issue(self, issue_id):
		c = self.conn.cursor()
		result = c.execute('select * from issues where id == ?',
				(issue_id,)).fetchone()
		return result

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
		result = c.execute('select * from series where fav = 1').fetchall()
		c.close()
		return result

	def get_series_list(self):
		c = self.conn.cursor()
		result = c.execute('select * from series').fetchall()
		c.close()
		return result

