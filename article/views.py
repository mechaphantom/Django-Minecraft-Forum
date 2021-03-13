from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm, contactformemail
from django.contrib import messages
from .models import Article, Comment, User, Profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
import os.path
from os import path
# Create your views here.

@require_http_methods(['POST'])
def LikeView(request, id):
    post = get_object_or_404(Article, id=id)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    messages.success(request,"Bu gönderiyi beğendiniz!")
    return redirect("article:detail", id)

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "articles.html", {"articles" : articles})

    articles = Article.objects.all()
    return render(request, "articles.html", {"articles":articles})

def index(request):
    return render(request, "index.html")

def games(request):
    return render(request, "games.html")

def shop(request):
    return render(request, "shop.html")

def contact(request):
    if request.method == "GET":
        form = contactformemail()
    else:
        form=contactformemail(request.POST)
        if form.is_valid():
            frommail = form.cleaned_data['frommail']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            send_mail(subject,message,frommail,['spikecowboy123@gmail.com',frommail])
    return render(request, "contact.html", {'form':form})
    #return render(request, "contact.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Gönderiniz Başarıyla Paylaşıldı!")
        return redirect("index")

    return render(request, "addarticle.html", {"form":form})

def detail(request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    
    def get_context_data(self, *args, **kwargs):
        context = super(detail, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Article, id=self.kwargs['id'])
        total_likes = stuff.total_likes()
        
        liked= False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context
    
    return render(request, "detail.html", {"article" : article, "comments" : comments})

@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Gönderiniz Başarıyla Güncellendi!")
        return redirect("article:dashboard")

    return render(request, "update.html",{"form" : form})

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.warning(request,"Gönderi Silindi!")
    return redirect("article:dashboard")

def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    
    return redirect(reverse("article:detail", kwargs={"id":id}))


