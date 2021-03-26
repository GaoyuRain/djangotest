from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from polls.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    # 对于 ListView， 自动生成的 context 变量是 question_list。为了覆盖这个行为，我们提供 context_object_name 属性，
    # 表示我们想使用 latest_question_list。作为一种替换方案，
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # 不指定会使用默认模版名：polls/question_detail.html
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     print(latest_question_list)
#     # template = loader.get_template('polls/index.html')
#     # output = ','.join(q.question_text for q in latest_question_list)
#     # return HttpResponse("Hello, world. You're at the polls index.")
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     # return HttpResponse(template.render(context))
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     print('question_id', question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     print("Question does not exist11111111")
#     #     raise Http404("问题不存在啊")
#     #
#     # # return HttpResponse("你正在查看的问题单号 %s." % question_id)
#     # return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "你没有选择任何选项！",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
