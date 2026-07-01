from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from blog.models import Artigo
from core.models import ConteudoSite

# Mapa completo de campos editáveis por seção
SECOES = {
    'hero': {
        'label': 'Hero',
        'campos': [
            {'chave': 'hero_video', 'label': 'Vídeo de fundo', 'tipo': 'video'},
            {'chave': 'hero_logo',  'label': 'Logo',           'tipo': 'imagem'},
        ],
    },
    'sobre': {
        'label': 'Sobre',
        'campos': [
            {'chave': 'sobre_titulo',           'label': 'Título principal',       'tipo': 'titulo'},
            {'chave': 'sobre_p1',               'label': 'Parágrafo 1',            'tipo': 'texto'},
            {'chave': 'sobre_p2',               'label': 'Parágrafo 2',            'tipo': 'texto'},
            {'chave': 'sobre_p3',               'label': 'Parágrafo 3',            'tipo': 'texto'},
            {'chave': 'sobre_credencial_num',   'label': 'Número (ex: 35)',        'tipo': 'titulo'},
            {'chave': 'sobre_credencial_label', 'label': 'Label (ex: anos de atuação)', 'tipo': 'titulo'},
            {'chave': 'sobre_imagem',           'label': 'Foto da Cláudia',        'tipo': 'imagem'},
        ],
    },
    'atuacao': {
        'label': 'Atuação',
        'campos': [
            {'chave': 'atuacao_titulo',      'label': 'Título',              'tipo': 'titulo'},
            {'chave': 'atuacao_intro',       'label': 'Texto introdutório',  'tipo': 'texto'},
            {'chave': 'atuacao_c1_titulo',   'label': 'Card 1 — Título',     'tipo': 'titulo'},
            {'chave': 'atuacao_c1_desc',     'label': 'Card 1 — Descrição',  'tipo': 'texto'},
            {'chave': 'atuacao_c2_titulo',   'label': 'Card 2 — Título',     'tipo': 'titulo'},
            {'chave': 'atuacao_c2_desc',     'label': 'Card 2 — Descrição',  'tipo': 'texto'},
            {'chave': 'atuacao_c3_titulo',   'label': 'Card 3 — Título',     'tipo': 'titulo'},
            {'chave': 'atuacao_c3_desc',     'label': 'Card 3 — Descrição',  'tipo': 'texto'},
            {'chave': 'atuacao_c4_titulo',   'label': 'Card 4 — Título',     'tipo': 'titulo'},
            {'chave': 'atuacao_c4_desc',     'label': 'Card 4 — Descrição',  'tipo': 'texto'},
        ],
    },
    'equipe': {
        'label': 'Capital Humano',
        'campos': (
            [
                {'chave': 'equipe_titulo', 'label': 'Título', 'tipo': 'titulo'},
                {'chave': 'equipe_texto',  'label': 'Texto',  'tipo': 'texto'},
            ] + [
                item
                for i in range(1, 51)
                for item in [
                    {'tipo': 'grupo', 'label': f'Colaborador {i}'},
                    {'chave': f'eq_foto_{i:02d}', 'label': 'Foto',  'tipo': 'imagem'},
                    {'chave': f'eq_nome_{i:02d}', 'label': 'Nome',  'tipo': 'titulo'},
                ]
            ]
        ),
    },
    'estrutura': {
        'label': 'Nossa Estrutura',
        'campos': (
            [
                {'chave': 'estrutura_titulo', 'label': 'Título',         'tipo': 'titulo'},
                {'chave': 'estrutura_texto',  'label': 'Texto de apoio', 'tipo': 'texto'},
            ] + [
                item
                for i in range(1, 11)
                for item in [
                    {'tipo': 'grupo', 'label': f'Foto {i}'},
                    {'chave': f'est_foto_{i:02d}', 'label': 'Imagem', 'tipo': 'imagem'},
                ]
            ]
        ),
    },
    'diferenciais': {
        'label': 'Diferenciais',
        'campos': [
            {'chave': 'dif_titulo',       'label': 'Título',              'tipo': 'titulo'},
            {'chave': 'dif_texto',        'label': 'Texto',               'tipo': 'texto'},
            {'chave': 'dif_i1_titulo',    'label': 'Item 1 — Título',     'tipo': 'titulo'},
            {'chave': 'dif_i1_desc',      'label': 'Item 1 — Descrição',  'tipo': 'texto'},
            {'chave': 'dif_i2_titulo',    'label': 'Item 2 — Título',     'tipo': 'titulo'},
            {'chave': 'dif_i2_desc',      'label': 'Item 2 — Descrição',  'tipo': 'texto'},
            {'chave': 'dif_i3_titulo',    'label': 'Item 3 — Título',     'tipo': 'titulo'},
            {'chave': 'dif_i3_desc',      'label': 'Item 3 — Descrição',  'tipo': 'texto'},
        ],
    },
    'contato': {
        'label': 'Contato',
        'campos': [
            {'chave': 'contato_titulo',   'label': 'Título',              'tipo': 'titulo'},
            {'chave': 'contato_endereco', 'label': 'Endereço',            'tipo': 'titulo'},
            {'chave': 'contato_telefone', 'label': 'Telefone',            'tipo': 'titulo'},
            {'chave': 'contato_email',    'label': 'E-mail',              'tipo': 'titulo'},
        ],
    },
}


def _carregar_conteudo():
    """Retorna dict {chave: objeto ConteudoSite} para uso no template."""
    return {c.chave: c for c in ConteudoSite.objects.all()}


_EQUIPE = [
    ('adriana',       'Adriana'),
    ('concei-o',      'Conceição'),
    ('f-tima',        'Fátima'),
    ('gabrielle',     'Gabrielle'),
    ('j-lia',         'Júlia'),
    ('karine',        'Karine'),
    ('la-s',          'Laís'),
    ('larissa',       'Larissa'),
    ('lidiane',       'Lidiane'),
    ('lilian',        'Lilian'),
    ('lucas',         'Lucas'),
    ('luis-henrique', 'Luis Henrique'),
    ('luiza',         'Luiza'),
    ('maira',         'Maira'),
    ('patr-cia',      'Patrícia'),
    ('roberval',      'Roberval'),
    ('tarik',         'Tarik'),
    ('valkiria',      'Valkiria'),
]

def home(request):
    artigos_recentes = Artigo.objects.filter(publicado=True)[:4]
    c = _carregar_conteudo()

    # Colaboradores: lê do painel (eq_foto_01..50 + eq_nome_01..50)
    # Fallback: lista estática _EQUIPE com arquivos em static/img/equipe/
    equipe_membros = []
    for i in range(1, 51):
        foto_obj = c.get(f'eq_foto_{i:02d}')
        nome_obj = c.get(f'eq_nome_{i:02d}')
        if foto_obj and foto_obj.imagem:
            equipe_membros.append({
                'url':  foto_obj.imagem.url,
                'nome': nome_obj.titulo if nome_obj else '',
                'tipo': 'media',
            })
    if not equipe_membros:
        equipe_membros = [{'slug': s, 'nome': n, 'tipo': 'static'} for s, n in _EQUIPE]

    # Fotos do escritório: lê do painel (est_foto_01..10)
    # Fallback: hardcoded no template
    estrutura_fotos = []
    for i in range(1, 11):
        foto_obj = c.get(f'est_foto_{i:02d}')
        if foto_obj and foto_obj.imagem:
            estrutura_fotos.append(foto_obj.imagem.url)

    return render(request, 'index.html', {
        'artigos_recentes': artigos_recentes,
        'c': c,
        'equipe_membros':   equipe_membros,
        'estrutura_fotos':  estrutura_fotos,
    })


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

_ICONES = {
    'hero':         '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><polygon points="10 8 16 11 10 14 10 8" fill="currentColor" stroke="none"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    'sobre':        '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="7" r="4"/><path d="M1 21v-2a7 7 0 0 1 14 0v2"/><line x1="17" y1="8" x2="23" y2="8"/><line x1="17" y1="12" x2="23" y2="12"/><line x1="17" y1="16" x2="21" y2="16"/></svg>',
    'atuacao':      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="17"/><line x1="9.5" y1="14.5" x2="14.5" y2="14.5"/></svg>',
    'equipe':       '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    'estrutura':    '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>',
    'diferenciais': '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>',
    'contato':      '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
}

_DESC = {
    'hero':         'Vídeo de fundo do cabeçalho',
    'sobre':        'Foto, textos e credenciais',
    'atuacao':      'Títulos e descrições dos 4 cards',
    'equipe':       'Foto e texto da equipe',
    'estrutura':    'Carrossel de fotos do escritório',
    'diferenciais': 'Pontos fortes do escritório',
    'contato':      'Endereço, telefone e e-mail',
}

@login_required(login_url='/painel/login/')
def painel_dashboard(request):
    secoes_site = [(slug, info, _ICONES[slug], _DESC[slug]) for slug, info in SECOES.items()]
    ctx = {
        'artigos_recentes':  Artigo.objects.order_by('-criado_em')[:5],
        'total_artigos':     Artigo.objects.count(),
        'total_publicados':  Artigo.objects.filter(publicado=True).count(),
        'total_rascunhos':   Artigo.objects.filter(publicado=False).count(),
        'secoes_site':       secoes_site,
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
            try:
                artigo.imagem_capa.delete(save=False)
            except OSError:
                pass
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


# ── CONTEÚDO DO SITE ────────────────────────────────────

@login_required(login_url='/painel/login/')
def painel_conteudo(request):
    return redirect('painel_conteudo_secao', secao='hero')


@login_required(login_url='/painel/login/')
def painel_conteudo_secao(request, secao):
    if secao not in SECOES:
        return redirect('painel_conteudo_secao', secao='hero')

    campos  = SECOES[secao]['campos']
    chaves  = [f['chave'] for f in campos if f.get('chave')]
    objetos = {c.chave: c for c in ConteudoSite.objects.filter(chave__in=chaves)}

    if request.method == 'POST':
        # Upload em lote para colaboradores
        if secao == 'equipe' and request.FILES.getlist('eq_fotos_batch'):
            fotos = request.FILES.getlist('eq_fotos_batch')
            if len(fotos) > 50:
                messages.error(request, f'Máximo de 50 fotos (você enviou {len(fotos)}).')
                return redirect('painel_conteudo_secao', secao=secao)
            for i in range(1, 51):
                chave_foto = f'eq_foto_{i:02d}'
                chave_nome = f'eq_nome_{i:02d}'
                obj_foto, _ = ConteudoSite.objects.get_or_create(chave=chave_foto, defaults={'secao': secao})
                obj_nome, _ = ConteudoSite.objects.get_or_create(chave=chave_nome, defaults={'secao': secao})
                if i <= len(fotos):
                    f = fotos[i - 1]
                    if obj_foto.imagem:
                        obj_foto.imagem.delete(save=False)
                    obj_foto.imagem = f
                    obj_foto.secao  = secao
                    obj_foto.save()
                    # nome = filename sem extensão
                    import os
                    nome = os.path.splitext(f.name)[0]
                    obj_nome.titulo = nome
                    obj_nome.secao  = secao
                    obj_nome.save()
                else:
                    if obj_foto.imagem:
                        obj_foto.imagem.delete(save=False)
                    obj_foto.imagem = None
                    obj_foto.secao  = secao
                    obj_foto.save()
                    obj_nome.titulo = ''
                    obj_nome.secao  = secao
                    obj_nome.save()
            # salva título e texto
            for campo in campos:
                chave = campo.get('chave')
                if not chave or campo['tipo'] not in ('titulo', 'texto'):
                    continue
                if chave in ('equipe_titulo', 'equipe_texto'):
                    obj, _ = ConteudoSite.objects.get_or_create(chave=chave, defaults={'secao': secao})
                    if campo['tipo'] == 'titulo':
                        obj.titulo = request.POST.get(chave, '')
                    else:
                        obj.texto = request.POST.get(chave, '')
                    obj.secao = secao
                    obj.save()
            messages.success(request, f'{len(fotos)} colaborador{"es" if len(fotos) != 1 else ""} salvo{"s" if len(fotos) != 1 else ""}.')
            return redirect('painel_conteudo_secao', secao=secao)

        # Upload em lote para o escritório
        if secao == 'estrutura' and request.FILES.getlist('est_fotos_batch'):
            fotos = request.FILES.getlist('est_fotos_batch')
            if len(fotos) < 5 or len(fotos) > 10:
                messages.error(request, f'Selecione entre 5 e 10 fotos (você enviou {len(fotos)}).')
                return redirect('painel_conteudo_secao', secao=secao)
            # Apaga slots anteriores e salva os novos
            for i in range(1, 11):
                chave = f'est_foto_{i:02d}'
                obj, _ = ConteudoSite.objects.get_or_create(chave=chave, defaults={'secao': secao})
                if obj.imagem:
                    try:
                        obj.imagem.delete(save=False)
                    except OSError:
                        pass
                if i <= len(fotos):
                    obj.imagem = fotos[i - 1]
                else:
                    obj.imagem = None
                obj.secao = secao
                obj.save()
            # Salva título e texto normalmente
            for campo in campos:
                chave = campo.get('chave')
                if not chave or campo['tipo'] not in ('titulo', 'texto'):
                    continue
                obj, _ = ConteudoSite.objects.get_or_create(chave=chave, defaults={'secao': secao})
                if campo['tipo'] == 'titulo':
                    obj.titulo = request.POST.get(chave, '')
                else:
                    obj.texto = request.POST.get(chave, '')
                obj.secao = secao
                obj.save()
            messages.success(request, f'{len(fotos)} fotos salvas com sucesso.')
            return redirect('painel_conteudo_secao', secao=secao)

        for campo in campos:
            chave = campo.get('chave')
            if not chave:
                continue
            obj, _ = ConteudoSite.objects.get_or_create(chave=chave, defaults={'secao': secao})
            obj.secao = secao

            if campo['tipo'] == 'titulo':
                obj.titulo = request.POST.get(chave, '')
            elif campo['tipo'] == 'texto':
                obj.texto = request.POST.get(chave, '')
            elif campo['tipo'] == 'imagem':
                if f'remover_{chave}' in request.POST:
                    try:
                        obj.imagem.delete(save=False)
                    except OSError:
                        pass
                    obj.imagem = None
                if request.FILES.get(chave):
                    obj.imagem = request.FILES[chave]
            elif campo['tipo'] == 'video':
                if f'remover_{chave}' in request.POST:
                    try:
                        obj.video.delete(save=False)
                    except OSError:
                        pass
                    obj.video = None
                if request.FILES.get(chave):
                    obj.video = request.FILES[chave]

            obj.save()

        messages.success(request, 'Conteúdo salvo com sucesso.')
        return redirect('painel_conteudo_secao', secao=secao)

    # Enriquece cada campo com seus valores atuais
    campos_ctx = []
    for campo in campos:
        if not campo.get('chave'):
            # campo tipo 'grupo' — apenas separador visual, sem valor
            campos_ctx.append(campo)
            continue
        obj = objetos.get(campo['chave'])
        campos_ctx.append({
            **campo,
            'valor_titulo': obj.titulo if obj else '',
            'valor_texto':  obj.texto  if obj else '',
            'imagem_url':   obj.imagem.url if obj and obj.imagem else '',
            'video_url':    obj.video.url  if obj and obj.video  else '',
        })

    fotos_escritorio = []
    if secao == 'estrutura':
        for i in range(1, 11):
            obj = objetos.get(f'est_foto_{i:02d}')
            if obj and obj.imagem:
                fotos_escritorio.append(obj.imagem.url)

    colaboradores_atuais = []
    if secao == 'equipe':
        for i in range(1, 51):
            obj_foto = objetos.get(f'eq_foto_{i:02d}')
            obj_nome = objetos.get(f'eq_nome_{i:02d}')
            if obj_foto and obj_foto.imagem:
                colaboradores_atuais.append({
                    'url':  obj_foto.imagem.url,
                    'nome': obj_nome.titulo if obj_nome else '',
                })

    ctx = {
        'secao':               secao,
        'secao_label':         SECOES[secao]['label'],
        'secoes':              SECOES,
        'campos':              campos_ctx,
        'fotos_escritorio':    fotos_escritorio,
        'colaboradores_atuais': colaboradores_atuais,
    }
    return render(request, 'painel/conteudo.html', ctx)
