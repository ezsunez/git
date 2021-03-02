from django.shortcuts import render, HttpResponse,redirect
from firstapp.models import Article, Profile
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
# Create your views here.
def first(request):
    html = "Django Response"
    return HttpResponse(html)

def second(request):
    first_artical=Article.objects.all().first()
    artical_lst=Article.objects.filter(~Q(headline__contains=first_artical.headline))
    hmap={}
    hmap['current_article']=first_artical
    hmap['articles']=artical_lst
    return render(request,'test.html',hmap)

def three(request):
    hmap={}
    articles=Article.objects.all()
    hmap['articles']=articles
    article_name=request.GET.get('name')
    if article_name:
        current_article=Article.objects.get(headline=article_name)
    elif len(articles)>0:
        current_article = articles[0]
    hmap['current_article'] = current_article
    return render(request, 'test.html', hmap)

def index_register (request):
    if request.method == "GET":
        form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user=form.save()
            p=Profile(user=user)
            p.nickname=form.data['nickname']
            p.save()
            return redirect(to="login")
    content = {}
    content['form'] = form
    content['status']='register'
    return render(request, 'index.html', content)

def index_login(request):
    content = {}
    content['correct'] = 't'
    if request.method == "GET":
        form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid(),form.error_messages)
        if form.is_valid():
            login(request,form.get_user())
            return HttpResponse("Login Success")
            content['correct']='t'
        else:
            content['correct'] = 'r'

    content['form']=form
    content['status'] = 'login'
    return render(request,'index.html',content)