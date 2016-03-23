from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotModified
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from models import Answer
from models import Question
from forms import *


def _pagination(request, qs):
    limit = request.GET.get('limit', 10);
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, limit)
    paginator.baseurl = '/?page='
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def main(request):
    questions = Question.objects.all()
    questions = questions.order_by('-id')
    page = _pagination(request, questions)
    return render(request, 'qa/main.html', {
        'questions': page.object_list,
        'paginator': page.paginator,
        'page': page,
    })


def popular_questions(request):
    questions = Question.objects.all()
    questions = questions.order_by('-rating')
    page = _pagination(request, questions)
    return render(request, 'qa/popular_questions.html', {
        'questions': page.object_list,
        'paginator': page.paginator,
        'page': page,
    })


def question(request, slug):
    slug=int(slug)
    question = get_object_or_404(Question, id=slug)
    answers = question.answer_set.all()
    form = AnswerForm(request.user, initial={'question': str(slug)})
    return render(request, 'qa/question.html', {
            'question': question,
            'answers': answers,
            'form': form,
        })


def question_add(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated():
            return HttpResponseRedirect('/login/')
        form = AskForm(request.user, request.POST)
        if form.is_valid():
            # form._user = user
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/question_add.html', {
        'form': form,
        })


@require_POST
def answer(request):
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect('/login/')
    form = AnswerForm(request.user, request.POST)
    # form._user = user
    if form.is_valid():
        post = form.save()
        # url = answer.question.get_url()
        # return HttpResponseRedirect(url)
        return HttpResponseRedirect(reverse('question', args=[post.question.id]))
    else:
        return HttpResponseNotModified()


def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'qa/signup.html', {
        'form': form,
        })


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'qa/login.html', {
        'form': form,
        })
