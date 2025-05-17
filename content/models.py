from django.db import models
from django.conf import settings # For User ForeignKey

class ContentItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='uploaded_content_items'
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    source_url = models.URLField(max_length=2000, blank=True, null=True)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

class Book(ContentItem):
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    publication_year = models.PositiveIntegerField(blank=True, null=True)
    # cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

class Article(ContentItem):
    authors = models.CharField(max_length=500, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    source_name = models.CharField(max_length=255, blank=True)
    article_type = models.CharField(max_length=50, blank=True)

class Movie(ContentItem):
    director = models.CharField(max_length=255)
    release_year = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)

class TVShow(ContentItem):
    creator = models.CharField(max_length=255, blank=True)
    start_year = models.PositiveIntegerField(blank=True, null=True)
    end_year = models.PositiveIntegerField(blank=True, null=True)

class Dataset(ContentItem):
    version = models.CharField(max_length=50, blank=True)
    format = models.CharField(max_length=50, blank=True)

class Lecture(ContentItem):
    speaker = models.CharField(max_length=255)
    event_name = models.CharField(max_length=255, blank=True)
    lecture_date = models.DateField(blank=True, null=True)

class WebResource(ContentItem):
    resource_type = models.CharField(max_length=100, blank=True, help_text="E.g., Website, Report, Forum Thread")
