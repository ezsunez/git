from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from .models import Article, Difficulty
import markdown

# Create your views here.
obj = Difficulty.objects.all()
context = {'difficulty': obj}

def welcome(request):
    return render(request,'blog/index.html',context)

# def detail(request, question_id,i):
#     return HttpResponse(f"You're looking at question {question_id},{i}." )
def detail(request,a_id):
    c=Article.objects.get(id=a_id)
    path=c.context
    with open(f'./blog/md/{path}', 'r', encoding='utf8') as f:
        line=f.readline()
        l=''
        while line:
            l+=line
            line = f.readline()
    out=markdown.markdown(l,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])
    context['artilcal']=out
    return render(request,'blog/details.html',context)

def frame(request):
    articals=Article.objects.all()
    context['articals']=articals
    context['id']=1
    return render(request,'blog/articale_frame.html',context)

