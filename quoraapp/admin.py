# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from quoraapp.models import Question
from quoraapp.models import Answer
from quoraapp.models import Upvote
# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Upvote)