from django.db import models
from django.contrib.auth.models import User
from pytils.translit import slugify

# Create your models here.


class Category(models.Model):
	content = models.CharField(max_length=80)
	slug = models.CharField(max_length=80)
	def __unicode__(self):  
		return self.content
		
		
class Topic(models.Model):
	title = models.CharField(max_length=120)
	content = models.TextField()
	count_answers = models.IntegerField(default='0')
	dtime = models.DateTimeField(null = True)
	user = models.ForeignKey(User, related_name='topics', null = True)
	category = models.ForeignKey(Category, related_name='topics')
	last_answer_username = models.CharField(max_length=100)
	last_answer_dtime = models.DateTimeField(null = True)
	slug = models.SlugField(max_length=120)
	def __unicode__(self):  
		return self.title
	def save(self, **kwargs):
		self.slug=slugify(self.title)
		super(Topic, self).save()	
		
		
class Answer(models.Model):
	content = models.TextField()
	dtime = models.DateTimeField()
	user = models.ForeignKey(User, related_name='answers')
	topic = models.ForeignKey(Topic, related_name='answers')
	def __unicode__(self):  
		return self.content				


class OldTopic(models.Model):
        title = models.CharField(max_length=120)
        content = models.TextField()
        count_answers = models.IntegerField(default='0')
        dtime = models.DateTimeField(null = True)
        user = models.ForeignKey(User, related_name='oldtopics', null = True)
        category = models.ForeignKey(Category, related_name='oldtopics')
        last_answer_username = models.CharField(max_length=100)
        last_answer_dtime = models.DateTimeField(null = True)
        slug = models.CharField(max_length=120)
        def __unicode__(self):
                return self.title


class Help(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    number = models.IntegerField(default='0')
    def __unicode__(self):
        return self.name
