from django.shortcuts import render

from articles.models import Article


# Create your views here.
def news(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, 'articles/news.html',
                  {"articles": articles})


def article(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, "articles/article.html",
                  {"art": article})