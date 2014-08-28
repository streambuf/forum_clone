# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'wen.settings'
from django.core.management.base import BaseCommand, CommandError
from forum.models import Topic, OldTopic, Help, Category
import xml.etree.cElementTree as ET
from datetime import datetime

class Command(BaseCommand):
 
	def handle(self, *args, **options):
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
		

