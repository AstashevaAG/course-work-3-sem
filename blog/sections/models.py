# models.py
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Section(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    section = models.ForeignKey(Section, related_name='articles', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='comment_users', on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.content[:10]}..."