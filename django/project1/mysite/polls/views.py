from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})	
	

def vote(request, question_id):
    # 모델을 받아오고, 존재하지 않으면 404페이지를 띄운다.
    question = get_object_or_404(Question, pk=question_id)
    try:
        # post로 넘어온 choice 값으로 선택된 choice를 얻는다.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 예외가 발생했을 시에 question모델과 에러 메시지를 템플릿에 전달한다.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # choice를 잘 얻어왔다면 투표 수를 1 증가시키고, 결과창으로 이동시킨다.
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))	

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})		