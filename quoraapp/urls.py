from django.conf.urls import url, include
from quoraapp.views import QuestionView
from quoraapp.views import AnswerView
from quoraapp.views import UpvoteView
from quoraapp.views import UserQuestionsView
from quoraapp.views import UserAnswersView
from quoraapp.views import UserUpvotesView
from quoraapp.views import QuestionAnswersView
from quoraapp.views import HoursHighestVotesView
from quoraapp.views import EverHighestVotesView
from quoraapp.views import WhoUpvotedView

urlpatterns = [
	url(r'^question/$', QuestionView.as_view(), name='question'),
	url(r'^answer/(?P<pk>\d+)$', AnswerView.as_view(), name='answer'),
	url(r'^upvote/(?P<pk>\d+)$', UpvoteView.as_view(), name='upvote'),
	url(r'^userquestions/?', UserQuestionsView.as_view(), name='userquestions'),
	url(r'^useranswers/?', UserAnswersView.as_view(), name='useranswers'),
	url(r'^userupvotes/?', UserUpvotesView.as_view(), name='userupvotes'),
	url(r'^questionanswers/(?P<pk>\d+)$', QuestionAnswersView.as_view(), name='questionanswers'),
	url(r'^whoupvoted/(?P<pk>\d+)$', WhoUpvotedView.as_view(), name='whoupvoted'),
	url(r'^hourshighestvotes/?', HoursHighestVotesView.as_view(), name='hourshighestvotes'),
	url(r'^everhighestvotes/?', EverHighestVotesView.as_view(), name='everhighestvotes'),
 ]