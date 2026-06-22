# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Site institucional para **Cláudia Rocha Advocacia — Direito do Trabalho** (Araraquara/SP), migrado de um site estático (`C:\Projeto_Site`) para Django com blog e painel de gestão.

## Commands

```powershell
# Rodar o servidor de desenvolvimento (PowerShell — && não funciona no PS 5.1)
cd C:\claudia_rocha
python manage.py runserver

# Aplicar migrações
python manage.py migrate

# Criar superusuário (sem TTY — usar shell)
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin','','claudia@2026')"

# Popular o banco com artigos de exemplo
python seed_blog.py

# Coletar estáticos (produção)
python manage.py collectstatic --noinput
```

> **PowerShell**: use `;` em vez de `&&` para encadear comandos. O shell Bash também está disponível via ferramenta Bash.

## Architecture

### Apps Django

| App    | Responsabilidade |
|--------|-----------------|
| `core` | View `home`, modelos de conteúdo editável (`ConteudoSite`), e todas as views do painel customizado (`/painel/`) |
| `blog` | Model `Artigo`, views públicas (`/blog/`), URLs do blog |

### URL map

| Prefixo | Destino |
|---------|---------|
| `/` | `core.views.home` → `templates/index.html` |
| `/blog/` | `blog.urls` → lista e detalhe de artigos |
| `/painel/` | Views em `core/views.py` — painel customizado (requer login) |
| `/admin/` | Django admin nativo (usado apenas para login/logout) |

### Painel customizado (`/painel/`)

Não usa o Django admin — é um conjunto de views próprias em `core/views.py` decoradas com `@login_required(login_url='/admin/login/')`. O login redireciona para o Django admin's `/admin/login/` e depois volta ao painel.

Rotas do painel:
- `GET /painel/` — dashboard com contadores
- `GET/POST /painel/artigos/` — listagem com toggle de publicação inline
- `GET/POST /painel/artigos/novo/` — criar artigo
- `GET/POST /painel/artigos/<pk>/editar/` — editar artigo
- `POST /painel/artigos/<pk>/publicar/` — toggle publicado/rascunho
- `POST /painel/artigos/<pk>/deletar/` — deletar

### Templates

```
templates/
  index.html              ← one-page site (home)
  blog/
    lista.html            ← listagem editorial do blog
    detalhe.html          ← artigo completo
  painel/
    base.html             ← layout com sidebar fixa (todo CSS inline)
    dashboard.html        ← visão geral com stats cards
    artigos.html          ← tabela com toggle de publicação
    artigo_form.html      ← formulário criar/editar (two-column layout)
  admin/
    base_site.html        ← override do branding do Django admin
```

Templates ficam em `templates/` na raiz (não dentro dos apps). `APP_DIRS = True` permite que o Django admin encontre os seus próprios templates.

### Static files

```
static/
  css/style.css           ← estilos do site público
  js/script.js            ← nav scroll, reveal, menu mobile
  fonts/gilroy-font/      ← arquivos .ttf da Gilroy (fonte local)
  admin/css/custom.css    ← tema aplicado ao Django admin nativo
  video/                  ← vídeo do hero (se existir)
```

Fontes Gilroy são referenciadas com caminho absoluto `/static/fonts/gilroy-font/...` — não relativo.

### Models

**`blog.Artigo`** — `titulo`, `slug` (auto-gerado), `resumo`, `conteudo`, `imagem_capa` (upload → `media/blog/`), `publicado`, `criado_em`, `atualizado_em`.

**`core.ConteudoSite`** — modelo para textos/imagens editáveis por seção (`hero`, `sobre`, `atuacao`, `diferenciais`, `contato`). Ainda não está integrado às views — foi criado para uso futuro.

### Brand tokens (CSS variables em `static/css/style.css`)

| Variável | Hex | Uso |
|----------|-----|-----|
| `--grafite` | `#232425` | Fundo principal / footer |
| `--teal` | `#353C3D` | Seção Atuação |
| `--vinho` | `#432A35` | Diferenciais / CTA / accent do painel |
| `--pedra` | `#C0BFBF` | Textos secundários |
| `--off-white` | `#E0E0DE` | Seção Sobre |

Tipografia: `Gilroy` (local, weight 600) para títulos; `Cormorant Garamond` (Google Fonts, italic) para `<em>` em títulos específicos; `Inter` (Google Fonts) para corpo.

## Pending

- Integrar `ConteudoSite` às views para conteúdo editável sem deploy
- Integrar formulário de contato (EmailJS / Formspree)
- Substituir Inter por Gilroy no corpo de texto
- SEO: meta description, Open Graph, schema markup
- Favicon com símbolo CR
- Configurar `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS` para produção
