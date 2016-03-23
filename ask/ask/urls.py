from django.conf.urls import patterns, include, url
from django.contrib import admin
from qa.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', main, name='main'),
    url(r'^login/$', login_user, name='login'),
    url(r'^signup/$', signup_user, name='signup'),
    url(r'^question/(?P<slug>\d+)/$', question, name='question'),
    url(r'^ask/$', question_add, name='question-add'),
    url(r'^answer/$', answer, name='answer'),
    url(r'^popular/$', popular_questions, name='popular-questions'),
    url(r'^new/$', test),

    url(r'^admin/$', include(admin.site.urls)),
)