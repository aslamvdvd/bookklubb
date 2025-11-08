from django.contrib import admin
from .models import ContentItem, Book, Article, Movie, TVShow, Dataset, Lecture, WebResource

admin.site.register(ContentItem)
admin.site.register(Book)
admin.site.register(Article)
admin.site.register(Movie)
admin.site.register(TVShow)
admin.site.register(Dataset)
admin.site.register(Lecture)
admin.site.register(WebResource)
