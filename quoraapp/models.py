# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
   	Question = models.CharField(
   		max_length=2000,
	)

class Answer(models.Model):
	answertext = models.CharField(
        max_length=2000,
    )
	upvotes = models.BooleanField()

class AnswerUser(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	answer = models.ForeignKey(
		Answer,
		on_delete=models.CASCADE
	)


