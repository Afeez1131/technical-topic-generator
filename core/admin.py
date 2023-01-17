from django.contrib import admin
from .models import Phrase, ArticleTopic, Counter

admin.site.register(Phrase)
admin.site.register(Counter)
admin.site.register(ArticleTopic)
