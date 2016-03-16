from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotModified
from django.views.decorators.http import require_GET, require_POST
from django.core.urlresolvers import reverse
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

@require_GET
def question(request, slug):
    slug=int(slug)
    question = get_object_or_404(Question, id=slug)
    answers = question.answer_set.all()
    form = AnswerForm(initial={'question': str(slug)})
    return render(request, 'qa/question.html', {
            'question': question,
            'answers': answers,
            'form': form,
        })

def question_add(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
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
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save()
        return HttpResponseRedirect(reverse('question', args=[answer.question.id]))
    else:
        return HttpResponseNotModified()
