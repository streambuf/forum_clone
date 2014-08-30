# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import  Http404, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.contrib.auth.models import User
from forum.models import Category, Topic, Answer, Help, OldTopic
from datetime import datetime, date
from django.utils import timezone, simplejson
from django.contrib import auth
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from pytils.translit import slugify
import urllib
import urllib2

def send_ping(request):
	params = {'key':'aac529c6d22797dbd8876b47f25f92b18d6c09f1','login':'hostdjango','search_id':'2170920','urls':'codingtalk.ru/sitemap.xml'}
	url = 'http://site.yandex.ru/ping.xml?login=hostdjango&search_id=2170920&key=aac529c6d22797dbd8876b47f25f92b18d6c09f1&urls='
	req = urllib2.Request(url + urllib.urlencode(params), headers={'User-Agent':'Mozilla/5.0', 'Accept-Charset':'utf-8'})
	page = urllib2.urlopen(req)
	return HttpResponse(page.read())

@csrf_exempt
def new_topic(request):
	if request.is_ajax():
		if request.method == 'POST':

			answer = request.POST.get('answer', None)
			answer = strip_tags(answer).lstrip()
			title = request.POST.get('title', None)
			title = strip_tags(title).lstrip()
			category_id = request.POST.get('category_id', None)

			if answer == '':
				resp = {"status": -1, 'error': "Сообщение не должно быть пустым"}
			elif title == '':
				resp = {"status": -1, 'error': "Заголовок не должен быть пустым"}
			elif Topic.objects.filter(slug = slugify(title)).exists():
			    resp = 	{"status": -1, 'error': "Тема с таким заголовком уже существует"}
			elif len(answer) > 2000 or len(title) > 120:
				resp = 	{"status": -1, 'error': "Превышена допустимая длина"}
			else:
				timezone.localtime(timezone.now())
				nowtime = datetime.now()
				newtopic = Topic.objects.create(title = title, category = Category.objects.get(id = category_id),\
				content = answer, dtime = nowtime, user = User.objects.get(id=request.user.id),\
				last_answer_dtime = nowtime, last_answer_username = request.user.username)
				newtopic.save()
				newtopic = OldTopic.objects.create(title = title, category = Category.objects.get(id = category_id),\
				content = answer, dtime = nowtime, user = User.objects.get(id=request.user.id),\
				last_answer_dtime = nowtime, last_answer_username = request.user.username, slug=slugify(title))
				newtopic.save()
				resp = {"status": 1}


		else:
			resp = {"status": -1, 'error': "Ошибка, повторите запрос позже."}
	else:
		resp = {"status": -2}
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')
@csrf_exempt
def replay(request):
	if request.is_ajax():
		if request.method == 'POST':
			ans = request.POST.get('ans', None)
			ans = strip_tags(ans).lstrip()
			url = request.POST.get('url', None)
			url = url.split('/')[1]

			if (ans == ''):
				resp = {"status": -1, 'error': "Сообщение не должно быть пустым"}
			elif len(ans) > 2000:
				resp = {"status": -1, 'error': "Ошибка"}
			elif (not Topic.objects.filter(slug = url).exists()):
				resp = {"status": -1, 'error': "Ошибка2"}
			else:
				topic = Topic.objects.get(slug = url)
				oldtopic = OldTopic.objects.get(slug = url)
				timezone.localtime(timezone.now())
				newans = Answer.objects.create(content = ans, dtime = datetime.now(),\
				user = User.objects.get(id=request.user.id), topic = topic)
				newans.save()
				topic.count_answers += 1
				oldtopic.count_answers += 1
				topic.save()
				oldtopic.save()
				resp = {"status": 1}


		else:
			resp = {"status": -1, 'error': "Ошибка, повторите запрос позже."}
	else:
		resp = {"status": -2}
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')

@csrf_exempt
def login_out(request):
	if request.is_ajax():
		if request.method == 'POST':
			username = request.POST.get('username', None)

			if User.objects.filter(username = username).exists():
				resp = {"status": 1, "user_exists": 1}
			else:
				resp = {"status": 1, "user_exists": 0}

		else:
			resp = {"status": -1, 'error': "Ошибка, повторите запрос позже."}
	else:
		resp = {"status": -2}
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')

@csrf_exempt
def login(request):
	if request.is_ajax():
		if request.method == 'POST':
			username = request.POST.get('username', None)
			password = request.POST.get('password', None)
			user = auth.authenticate(username=username, password=password)
			username_strip = strip_tags(username)
			if user is not None:
				auth.login(request, user)
				resp = {"status": 1, "username": username, "hello": "Авторизация прошла успешно!"}
			elif User.objects.filter(username = username).exists():
				resp = {"status": -1, 'error': "Это имя занято. Пароль не подходит."}
			elif len(username) > 29:
				resp = {"status": -2, 'error': "Имя пользователя должно быть меньше 30 символов"}
			elif len(password) > 19:
				resp = {"status": -3, 'error': "Пароль должен быть меньше 20 символов"}
			elif len(username) > len(username_strip):
				resp = {"status": -4, 'error': "Имя пользователя не должно содеражать служебных символов"}
			else:
				newuser = User.objects.create(username = username, email = 'new')
				newuser.set_password(password)
				newuser.save()
				user = auth.authenticate(username=username, password=password)
				if user is not None:
					auth.login(request, user)
					resp = {"status": 1, "username": username, "hello": "Поздравляем! Вы успешно зарегистрировались!"}
				else:
					resp = {"status": -1, 'error': "Произошла непредвиденная ошибка. Пожалуйста, попробуйте снова."}
		else:
			resp = {"status": -2, 'error': "Ошибка, повторите запрос позже."}
	else:
		resp = {"status": -3}
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')

def logout(request):
	auth.logout(request)
	return redirect("/")


def register(request):
	auth.logout(request)
	return redirect("/forum/")

def showurls(request):
	args = {}
	li = []
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
			url = "http://codingtalk.ru/" + topic.slug + page
			li.append(url)
			i += 1
	args['urls'] = li
	args['user'] = auth.get_user(request)
	return render_to_response('forum/showurls.html', args)

def sitemap_html(request):
	args = {}
	try:
		args['topics1'] = OldTopic.objects.filter(category__id=1).order_by("-id")
		args['topics2'] = OldTopic.objects.filter(category__id=2).order_by("-id")
		args['topics3'] = OldTopic.objects.filter(category__id=3).order_by("-id")
		args['topics4'] = OldTopic.objects.filter(category__id=4).order_by("-id")
		args['category'] = category
		args['user'] = auth.get_user(request)
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404
	except PageNotAnInteger:
		raise Http404
	return render_to_response('forum/sitemap.html', args, context_instance=RequestContext(request))


def category(request, slug, page_number=1):
	args = {}
	try:
		cat = Category.objects.get(slug = slug)
		topics_list = OldTopic.objects.filter(category=cat).order_by("-id")
		current_page = Paginator(topics_list, 50)
		pages = current_page.page(page_number)
		args['topics'] = pages
		args['category'] = cat
		args['user'] = auth.get_user(request)
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404
	except PageNotAnInteger:
		raise Http404
	return render_to_response('forum/index.html', args, context_instance=RequestContext(request))


def forum(request, page_number=1):
	args = {}
	# clean topics	
	'''topics = OldTopic.objects.all()
	for topic in topics:
		topic.delete()
	for i in range(1,5):
		h = Help.objects.get(id=i)
		h.number = 0
		h.save()'''
	try:
	    topics_list = OldTopic.objects.order_by("-id")
	    current_page = Paginator(topics_list, 50)
	    pages = current_page.page(page_number)
	    args['topics'] = pages
	    args['category'] = False
	    args['user'] = auth.get_user(request)
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404
	except PageNotAnInteger:
		raise Http404
	return render_to_response('forum/index.html', args, context_instance=RequestContext(request))



def topic(request, slug, page_number = 1):
	args = {}
	try:
		topic = Topic.objects.get(slug = slug)
		args['topic'] = topic
		answers_list = Answer.objects.filter(topic=topic)
		current_page = Paginator(answers_list, 50)
		pages = current_page.page(page_number)
		args['answers'] = pages
		a_count = topic.count_answers
		last_page = a_count/50
		if a_count%50 != 0:
			last_page += 1
		args['last_page'] = int(last_page)
		args['user'] = auth.get_user(request)
		args['last_topics'] = OldTopic.objects.filter(category=topic.category).order_by("-id")[:5]
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404
	except PageNotAnInteger:
		raise Http404

	return render_to_response('forum/topic.html', args)
