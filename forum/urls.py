from django.conf.urls import patterns, url
from forum import views


urlpatterns = patterns('',
	url(r'^$', views.forum, name='forum'),
	url(r'^send/ping/$', views.send_ping, name='send_ping'),
	url(r'^login/$', views.login, name='login'),
	url(r'^login_out/$', views.login_out, name='login_out'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^replay/$', views.replay, name='replay'),
	url(r'^sitemap-html/$', views.sitemap_html, name='sitemap_html'),
	url(r'^show/allurls/$', views.showurls, name='showurls'),
	url(r'^new_topic/$', views.new_topic, name='new_topic'),
	url(r'^page/(?P<page_number>\d+)/$', views.forum, name='forum'),
    url(r'^category/(?P<slug>.*)/(?P<page_number>\d+)/$', views.category, name='category'),
    url(r'^category/(?P<slug>.*)/$', views.category, name='category'),
    url(r'^(?P<slug>.*)/(?P<page_number>\d+)/$', views.topic, name='topic'),
    url(r'^(?P<slug>.*)/$', views.topic, name='topic'),
)
