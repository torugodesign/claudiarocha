# Backup de conteúdo do site

`conteudo_site.json` — exportação (Django `dumpdata`) de: artigos do blog, colaboradores do carrossel e conteúdo editável do site.
Não inclui usuários, senhas, sessões, nem os arquivos de imagem/vídeo (pasta `media/` do servidor).

Gerado em 2026-11-13. Para restaurar: `python manage.py loaddata backup/conteudo_site.json`
