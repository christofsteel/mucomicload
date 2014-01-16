import sqlite3

"""
	Layout:
		Table Series:
			id | title
		Table Issue:
			id | series_id | issue_number
"""
class DB():
	def __init__(self, db_path):
		self.conn = sqlite3.connect(db_path)
	
	def init(self):
		c = self.conn.cursor()
		c.execute("CREATE TABLE series(id integer primary key, title unique);")
		c.execute("CREATE TABLE issues(id integer primary key, series_id \
				integer, issue_number);")
		c.close()

	def update(self, api, v = 0):
		series = api.get_all_series()
		c = self.conn.cursor()
		for s in series:
			if v == 1:
				print(s[1])
			c.execute("INSERT OR IGNORE INTO series (id, title) values (" + str(s[0]) + ",\"" + s[1] + "\");")
			issues = api.get_series_by_id(s[0])
			for issue in issues:
				if v >= 2:
					print ("%s #%s" % (s[1], issue['issue_number']))
				c.execute("INSERT OR IGNORE INTO issues (id,series_id,issue_number) values (?,?,?)",(issue['digital_id'], s[0], issue['issue_number']))
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
		result = c.execute('select s.title, i.issue_number, i.id from series as s join issues as i on s.id == i.series_id where s.title LIKE ?', (termperc,))
		rresult = []
		for row in result:
			rresult.append(row)
		return rresult

	def get_title(self, id):
		c = self.conn.cursor()
		result = c.execute("select title from series where id == ?", (id,))
		rresult = []
		for row in result:
			rresult.append(row)
		return rresult

	def get_issue_list(self, series_id):
		c = self.conn.cursor()
		result = c.execute('select issue_number, id from issues where series_id == ?',
				(series_id,))
		rresult = []
		for row in result:
			rresult.append(row)
		return rresult

	def get_issue_id(self, series_id, issue_nr):
		c = self.conn.cursor()
		result = c.execute('select id from issues where series_id == ? and issue_number == ?', (series_id, str(issue_nr))).fetchone()[0]
		return result
		
	


