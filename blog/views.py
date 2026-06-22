from django.shortcuts import render, get_object_or_404
from .models import Artigo


def lista(request):
    artigos = Artigo.objects.filter(publicado=True)
    return render(request, 'blog/lista.html', {'artigos': artigos})


def detalhe(request, slug):
    artigo = get_object_or_404(Artigo, slug=slug, publicado=True)
    recentes = Artigo.objects.filter(publicado=True).exclude(pk=artigo.pk)[:3]
    return render(request, 'blog/detalhe.html', {'artigo': artigo, 'recentes': recentes})
