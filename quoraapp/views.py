# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from quoraapp.forms import QuestionForm
from quoraapp.forms import AnswerForm
from quoraapp.forms import UpvoteForm
from quoraapp.models import Question
from quoraapp.models import Answer
from quoraapp.models import Upvote
# Create your views here.
class IndexView(View):
    pass

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

        return HttpResponse("The first view is at its place")


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

        return HttpResponse("The second view is at its place")


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
            if(upvote == 'on'):
                upvote = True
            else:
                upvote = False
            upvote_obj = Upvote(user=user, answer=answer, upvote=upvote)
            upvote_obj.save()

        return HttpResponse("The third view is at its place")


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