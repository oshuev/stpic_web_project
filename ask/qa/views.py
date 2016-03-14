from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from models import Answer
from models import Question

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

def main(request, *args, **kwargs):
    questions = Question.objects.all()
    questions = questions.order_by('-id')
    page = _pagination(request, questions)
    return render(request, 'qa/main.html', {
        'questions': page.object_list,
        'paginator': page.paginator,
        'page': page,
    })

def popular_questions(request, *args, **kwargs):
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
    question = get_object_or_404(Question, id=slug)
    answers = question.answer_set.all()
    return render(request, 'qa/question.html', {
            'question': question,
            'answers': answers,
        })