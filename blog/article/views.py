from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import ArticleForm
from django.contrib import messages
from .models import Article
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):

    return render(request, template_name = "index.html")


def about(request):

    return render(request, template_name = "about.html")

@login_required(login_url="user:login")
def dashboard(request):

    articles = Article.objects.filter(author=request.user)
    
    context = {
        "articles":  articles
    }
    
    return render(request, template_name = "dashboard.html", context=context)


def detail(request, id):

  #  article = Article.objects.filter(id = id).first()

    article = get_object_or_404(Article,id = id)

    return render(request, template_name = "detail.html", context={"article":article})


@login_required(login_url="user:login")
def addarticle(request):

    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request,"Article created successfully.")
        return redirect("article:dashboard")

    return render(request, template_name = "addarticle.html", context={"form":form})


@login_required(login_url="user:login")
def updateArticle(request, id):

    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request, "Article updated successfully.")
        return redirect("article:dashboard")

    return render(request, template_name="update.html", context={"form":form})

@login_required(login_url="user:login")
def deleteArticle(request, id):

    article = get_object_or_404(Article, id = id)
    article.delete()
    
    messages.info(request, "Article deleted successfully.")

    return redirect("article:dashboard")



