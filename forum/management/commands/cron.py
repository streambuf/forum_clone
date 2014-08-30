# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wen.settings'
from django.core.management.base import BaseCommand, CommandError
from forum.models import Topic, OldTopic, Help, Category, TwitterAccount
import xml.etree.cElementTree as ET
from datetime import datetime
import urllib
import urllib2
import twitter

def post_twitter(num, url, title):
	ac = TwitterAccount.objects.get(id=num)
	api = twitter.Api(consumer_key = ac.api_key,
					consumer_secret = ac.api_secret,
					access_token_key = ac.token,
					access_token_secret= ac.token_secret)
	mes = title + ' http://' + url
	api.PostUpdate(mes)
	return 1

class Command(BaseCommand):
 
	def handle(self, *args, **options):
		num = 1 # номер аккаунта для твита
		for i in range(1,5):
			catx = Topic.objects.filter(category_id = i)
			max_id = len(catx) - 1
			for j in range(3):
				old_id = Help.objects.get(id=i)
				old_id.number += 1
				old_id.save()
				if old_id.number > max_id:
					break;
 				t = catx[old_id.number]
				newtopic = OldTopic.objects.create(title = t.title, category = t.category,\
					content = t.content, dtime = t.dtime, user = t.user,\
					last_answer_dtime = t.last_answer_dtime, last_answer_username = t.last_answer_username,\
					count_answers = t.count_answers, slug = t.slug)
				newtopic.save()
				url = 'codingtalk.ru/' + newtopic.slug + '/'
				post_twitter(num, url, newtopic.title)
				params = {'key':'aac529c6d22797dbd8876b47f25f92b18d6c09f1','login':'hostdjango','search_id':'2170920','urls':url}
				url = 'http://site.yandex.ru/ping.xml?login=hostdjango&search_id=2170920&key=aac529c6d22797dbd8876b47f25f92b18d6c09f1&urls='
				req = urllib2.Request(url + urllib.urlencode(params), headers={'User-Agent':'Mozilla/5.0', 'Accept-Charset':'utf-8'})
				page = urllib2.urlopen(req).read()
				num += 1
				if i%2 == 0:
					break
		urlset = ET.Element("urlset")
		urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
	
		url = ET.SubElement(urlset, "url")
		loc = ET.SubElement(url, "loc")
		loc.text = "http://codingtalk.ru/"
		lastmod = ET.SubElement(url, "lastmod")
		lastmod.text = datetime.now().strftime("%Y-%m-%d")
		priority = ET.SubElement(url, "priority")
		priority.text = "1"
		changefreq = ET.SubElement(url, "changefreq")
		changefreq.text = "hourly"

		categories = Category.objects.all()
		for category in categories:
			url = ET.SubElement(urlset, "url")
			loc = ET.SubElement(url, "loc")
			loc.text = "http://codingtalk.ru/" + category.slug + '/'
			lastmod = ET.SubElement(url, "lastmod")
			lastmod.text = datetime.now().strftime("%Y-%m-%d")
			priority = ET.SubElement(url, "priority")
			priority.text = "0.8"
			changefreq = ET.SubElement(url, "changefreq")
			changefreq.text = "hourly"


		topics = OldTopic.objects.all().order_by("-id")
		for topic in topics:
			a_count = topic.count_answers
			last_page = a_count/50
			if a_count%50 != 0:
				last_page += 1
			i = 1
			while i <= int(last_page):
				if i ==1:
					page = "/"
				else:
					page = "/" + str(i) + '/' 
				doc = ET.SubElement(urlset, "url")
				loc = ET.SubElement(doc, "loc")
				loc.text = "http://codingtalk.ru/" + topic.slug + page
				i += 1

		tree = ET.ElementTree(urlset)
		tree.write("/var/www/wen/forum/media/sitemap.xml")
		
		params = {'key':'aac529c6d22797dbd8876b47f25f92b18d6c09f1','login':'hostdjango','search_id':'2170920','urls':'codingtalk.ru/sitemap.xml'}
		url = 'http://site.yandex.ru/ping.xml?login=hostdjango&search_id=2170920&key=aac529c6d22797dbd8876b47f25f92b18d6c09f1&urls='
		req = urllib2.Request(url + urllib.urlencode(params), headers={'User-Agent':'Mozilla/5.0', 'Accept-Charset':'utf-8'})
		page = urllib2.urlopen(req).read()

