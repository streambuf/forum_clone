from django.contrib import admin
from forum.models import TwitterAccount, Topic, OldTopic, Answer, Category, Help

admin.site.register(Topic)
admin.site.register(OldTopic)
admin.site.register(Answer)
admin.site.register(Category)
admin.site.register(Help)
admin.site.register(TwitterAccount)

