import os
from bs4 import BeautifulSoup
import urllib
import urllib2
import MySQLdb
import twitter

db = MySQLdb.connect(host='localhost', user='root', passwd='dm89gm', db='wen_db')
cursor = db.cursor()
cursor.execute("SELECT * FROM forum_twitteraccount")
accounts = cursor.fetchall()


#url = 'http://bash.im/random'
url = 'http://citaty.info/random/10'
req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0"})
conn = urllib2.urlopen(req)
s = conn.read()
soup = BeautifulSoup(s)
n = 0
for text in soup.findAll('div', attrs={'class': 'field-item even last'}):
	if text.find('p') != None:
		text = ''.join([e for e in text.recursiveChildGenerator() if isinstance(e, unicode)])
		separators = ['?', '!', '.', ';', ',', ' ']
		i = 0
		while len(text) > 140:
			text = ''.join(text.split(separators[i], 1)[0])
			i += 1
			if i > len(separators) - 1:
				break
		if len(text) > 140:
			text = 'jk'
		ac = accounts[n]
		api = twitter.Api(consumer_key = ac[3],
					consumer_secret = ac[4],
					access_token_key = ac[5],
					access_token_secret= ac[6])
		api.PostUpdate(text)
		n += 1
		if n > 7:
			break

