from django import forms

class QuestionForm(forms.Form):
	question = forms.CharField(
		max_length=20000,
	)


class AnswerForm(forms.Form):
	answer = forms.CharField(
		max_length=20000,
	)


class UpvoteForm(forms.Form):
	upvote = forms.BooleanField()