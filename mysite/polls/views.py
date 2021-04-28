from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from polls.forms import LoginForm

from polls.models import Choice, Question




# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list' 

#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')[:20]


# class DetailView(generic.DetailView):
#     template_name = 'polls/detail.html'
#     model = Question


# class ResultsView(generic.DetailView):
#     template_name = 'polls/result.html'
#     model = Question



def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list, 
        'is_logged': request.user.is_authenticated
        }
    
    return render(request, 'polls/index.html', context)


@login_required(login_url='polls:login')
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST['choice'])
    except KeyError:
        return render(
            request, 
            'polls/detail.html', 
            {'question': question})
    else:
        selected_choice.votes =  F('votes') + 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, 
                username=form.data['username'], 
                password=form.data['password']
                )
            if user is not None and user.is_active:
                login(request, user)
            return HttpResponseRedirect(reverse('polls:index', args=()))
    form = LoginForm()
    return render(request, 'polls/login.html', {'form':form})


def user_logout(request):
    logout(request)
    print('request. user', type(request.user))
    return HttpResponseRedirect(reverse('polls:index', args=()))    
