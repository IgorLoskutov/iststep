import datetime

from django.db import models
from django.test import Client
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    

    def was_published_recently(self):
        now = timezone.now()
        return  now - datetime.timedelta(days=2) <= self.pub_date <= now 


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chice_text = models.CharField(max_length=80)
    votes = models.IntegerField(default=0)
      