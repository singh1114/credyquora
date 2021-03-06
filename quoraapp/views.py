# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic.edit import FormView

from quoraapp.forms import QuestionForm
from quoraapp.forms import AnswerForm
from quoraapp.forms import UpvoteForm
from quoraapp.models import Question
from quoraapp.models import Answer
from quoraapp.models import Upvote
# Create your views here

class QuestionView(LoginRequiredMixin, FormView):
    template_name = 'quoraapp/question.html'
    form_class = QuestionForm

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST)

        if form.is_valid():
            question = request.POST['question']
            question_obj = Question(user=user, question=question)
            question_obj.save()

        return HttpResponse("Done")


class AnswerView(LoginRequiredMixin, FormView):
    template_name = 'quoraapp/answer.html'
    form_class = AnswerForm

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        question = Question.objects.get(pk=pk)        

        return render(request, 'quoraapp/answer.html', context={
            'question': question,
            'form': self.form_class,
        })


    def post(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs['pk']
        question = Question.objects.get(pk=pk)
        form = self.form_class(request.POST)

        if form.is_valid():
            answer = request.POST['answer']
            answer_obj = Answer(user=user, question=question, answer=answer)
            answer_obj.save()

        return HttpResponse("Done")


class UpvoteView(LoginRequiredMixin, FormView):
    template_name = 'quoraapp/upvote.html'
    form_class = UpvoteForm

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        answer = Answer.objects.get(pk=pk)        

        return render(request, 'quoraapp/upvote.html', context={
            'answer': answer,
            'form': self.form_class,
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs['pk']
        answer = Answer.objects.get(pk=pk)
        form = self.form_class(request.POST)

        if form.is_valid():
            upvote = request.POST['upvote']
            if(answer.user != user):
                print answer.user
                print user
                date = timezone.now()
                if(upvote == 'on'):
                    upvote = True
                else:
                    upvote = False
                upvote_obj = Upvote(user=user, answer=answer, upvote=upvote, date=date)
                upvote_obj.save()
                return HttpResponse("Done")
            else:
                return HttpResponse("You can't upvote your own answer")


class UserQuestionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        questions = Question.objects.filter(user=user)

        return render(request, 'quoraapp/user_questions.html', context={
            'questions': questions,
        })


class UserAnswersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        answers = Answer.objects.filter(user=user)
        context_obj = []
        for answer in answers:
            question_pk = answer.question.pk
            question = Question.objects.get(pk=question_pk)
            temp_obj = {}
            temp_obj['question'] = question.question
            temp_obj['answer'] = answer.answer
            context_obj.append(temp_obj)

        return render(request, 'quoraapp/user_answers.html', context={
            'context_obj': context_obj,
        })


class UserUpvotesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        upvotes = Upvote.objects.filter(user=user, upvote=True)
        context_obj = []
        for upvote in upvotes:
            answer_pk = upvote.answer.pk
            answer = Answer.objects.get(pk=answer_pk)
            temp_obj = {}
            temp_obj['answer'] = answer.answer
            temp_obj['upvote'] = upvote.upvote
            context_obj.append(temp_obj)

        return render(request, 'quoraapp/user_upvotes.html', context={
            'context_obj': context_obj,
        })


class QuestionAnswersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs['pk']
        question = Question.objects.get(pk=pk)
        answers = Answer.objects.filter(question=question)
        return render(request, 'quoraapp/question_answers.html', context={
            'question': question,
            'answers': answers
        })


class WhoUpvotedView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        pk = self.kwargs['pk']
        context_obj = {}
        question = Question.objects.get(pk=pk)
        context_obj['question'] = question.question
        answer_obj = {}
        answer_list = []
        answers = Answer.objects.filter(question=question)
        for answer in answers:
            answer_obj['answer'] = answer.answer
            upvotes = Upvote.objects.filter(answer=answer)
            upvote_usernames = []
            upvote_obj = {}
            for upvote in upvotes:
                user = upvote.user
                username = User.objects.get(username=user.username).username
                upvote_obj['username'] = username
                upvote_usernames.append(upvote_obj)
            answer_obj['upvote_user'] = upvote_usernames
            answer_list.append(answer_obj.copy())
            print answer_list
        context_obj['ansup'] = answer_list

        return render(request, 'quoraapp/who_upvoted.html', context={
            'context_obj': context_obj
        })


class HoursHighestVotesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        questions = Question.objects.all()
        last_hour_date_time = datetime.now() - timedelta(hours = 1)
        now_time = datetime.now()
        highest_question_pk = None
        max_upvotes = 0
        for question in questions:
            total_upvotes = 0
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                upvotes = Upvote.objects.filter(answer=answer, date__gte=last_hour_date_time, date__lt=now_time)
                total_upvotes += len(upvotes)
            if(total_upvotes > max_upvotes):
                max_upvotes = total_upvotes
                highest_question_pk = question.pk

                question = Question.objects.get(pk=highest_question_pk).question

        return render(request, 'quoraapp/hourshighestvotes.html', context={
            'max_votes': max_upvotes,
            'question': question
        })


class EverHighestVotesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        questions = Question.objects.all()
        highest_question_pk = None
        max_upvotes = 0
        for question in questions:
            total_upvotes = 0
            answers = Answer.objects.filter(question=question)
            for answer in answers:
                upvotes = Upvote.objects.filter(answer=answer)
                total_upvotes += len(upvotes)
            if(total_upvotes > max_upvotes):
                max_upvotes = total_upvotes
                highest_question_pk = question.pk

                question = Question.objects.get(pk=highest_question_pk).question

        return render(request, 'quoraapp/everhighestvotes.html', context={
            'max_votes': max_upvotes,
            'question': question
        })