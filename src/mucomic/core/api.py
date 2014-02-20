from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import json


class Api:
	alphabet_url = 'http://api.marvel.com/browse/alphabet?type=comic_series&byType=digital-comics&byZone=marvel_site_zone&limit=10000'
	login_url = 'https://secure.marvel.com/user/login?referer=http%3A%2F%2Fmarvel.com'
	issue_url = 'https://reader.marvel.com/issue/id/%s'
	issues_url = 'http://api.marvel.com/browse/comics?byType=comic_series&byId=%s&isDigital=1&limit=10000'
	series_url = 'http://api.marvel.com/browse/series?startsWith=%s&offset=0&byType=digital-comics&byZone=marvel_site_zone&limit=10000'

	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/31.0.1650.63 Safari/537.36'

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.cookiejar = CookieJar()
		self.opener = build_opener(HTTPCookieProcessor(self.cookiejar))
		self._connected = False

	def connect(self):
		print('logging in with username %s' % self.username)
		self.firstpass = self.opener.open(self.login_url)
		loginData = {'login': self.username, 'password': self.password}
		loginRequest = Request(self.login_url, data=urlencode(loginData).encode('UTF-8'), headers={'User-Agent': self.user_agent}, origin_req_host='https://secure.marvel.com')
		response = self.opener.open(loginRequest)
		self._connected = True
		return response

	def get_alphabet(self):
		response = self.opener.open(self.alphabet_url).read()
		jsonresponse = json.loads(str(response, 'UTF-8'))
		return jsonresponse['data']['results']

	def get_issue_by_id(self, id):
		if not self._connected:
			self.connect()
		response = self.opener.open(self.issue_url % str(id)).read()
		jsonresponse = json.loads(str(response, 'UTF-8'))
		return jsonresponse

	def get_series_by_id(self, id):
		response = self.opener.open(self.issues_url % id).read()
		jsonresponse = json.loads(str(response, 'UTF-8'))
		return jsonresponse['data']['results']

	def get_series_starts_with(self, char):
		response = self.opener.open(self.series_url % char).read()
		jsonresponse = json.loads(str(response, 'UTF-8'))
		return jsonresponse['data']['results']

	def get_all_series(self):
		series = []
		for char in self.get_alphabet():
			series += self.get_series_starts_with(char)
		return series
