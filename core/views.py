from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from blog.models import Artigo


def home(request):
    artigos_recentes = Artigo.objects.filter(publicado=True)[:4]
    return render(request, 'index.html', {'artigos_recentes': artigos_recentes})


# ── AUTENTICAÇÃO DO PAINEL ───────────────────────────────

def painel_login(request):
    if request.user.is_authenticated:
        return redirect('painel_dashboard')
    erro = False
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', 'painel_dashboard'))
        erro = True
    return render(request, 'painel/login.html', {'erro': erro})


@require_POST
def painel_logout(request):
    logout(request)
    return redirect('painel_login')


# ── PAINEL ──────────────────────────────────────────────

@login_required(login_url='/painel/login/')
def painel_dashboard(request):
    ctx = {
        'artigos_recentes':  Artigo.objects.order_by('-criado_em')[:5],
        'total_artigos':     Artigo.objects.count(),
        'total_publicados':  Artigo.objects.filter(publicado=True).count(),
        'total_rascunhos':   Artigo.objects.filter(publicado=False).count(),
    }
    return render(request, 'painel/dashboard.html', ctx)


@login_required(login_url='/painel/login/')
def painel_artigos(request):
    artigos = Artigo.objects.order_by('-criado_em')
    return render(request, 'painel/artigos.html', {'artigos': artigos})


@login_required(login_url='/painel/login/')
def painel_artigo_novo(request):
    if request.method == 'POST':
        artigo = Artigo(
            titulo    = request.POST['titulo'],
            resumo    = request.POST['resumo'],
            conteudo  = request.POST['conteudo'],
            publicado = 'publicado' in request.POST,
        )
        if request.FILES.get('imagem_capa'):
            artigo.imagem_capa = request.FILES['imagem_capa']
        artigo.save()
        messages.success(request, 'Artigo criado com sucesso.')
        return redirect('painel_artigo_editar', pk=artigo.pk)
    return render(request, 'painel/artigo_form.html', {'artigo': None})


@login_required(login_url='/painel/login/')
def painel_artigo_editar(request, pk):
    artigo = get_object_or_404(Artigo, pk=pk)
    if request.method == 'POST':
        artigo.titulo    = request.POST['titulo']
        artigo.resumo    = request.POST['resumo']
        artigo.conteudo  = request.POST['conteudo']
        artigo.publicado = 'publicado' in request.POST
        if 'remover_imagem' in request.POST:
            artigo.imagem_capa.delete(save=False)
            artigo.imagem_capa = None
        if request.FILES.get('imagem_capa'):
            artigo.imagem_capa = request.FILES['imagem_capa']
        artigo.save()
        messages.success(request, 'Alterações salvas.')
        return redirect('painel_artigo_editar', pk=artigo.pk)
    return render(request, 'painel/artigo_form.html', {'artigo': artigo})


@login_required(login_url='/painel/login/')
def painel_artigo_publicar(request, pk):
    if request.method == 'POST':
        artigo = get_object_or_404(Artigo, pk=pk)
        artigo.publicado = not artigo.publicado
        artigo.save()
        status = 'publicado' if artigo.publicado else 'movido para rascunho'
        messages.success(request, f'Artigo {status}.')
    return redirect('painel_artigos')


@login_required(login_url='/painel/login/')
def painel_artigo_deletar(request, pk):
    if request.method == 'POST':
        artigo = get_object_or_404(Artigo, pk=pk)
        artigo.delete()
        messages.success(request, 'Artigo deletado.')
    return redirect('painel_artigos')
