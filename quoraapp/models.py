# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.

class Question(models.Model):
	user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
   	question = models.CharField(
   		max_length=20000,
	)

class Answer(models.Model):
	
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	question = models.ForeignKey(
		Question,
		on_delete=models.CASCADE,
	)
	answer = models.CharField(
		max_length=20000,
	)


class Upvote(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	answer = models.ForeignKey(
		Answer,
		on_delete=models.CASCADE
	)
	upvote = models.BooleanField()
	date = models.DateTimeField()