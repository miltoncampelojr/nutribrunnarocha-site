#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publicador diario autonomo do blog da Brunna Rocha.

Uso:
    python3 .deploy/publicar.py [N]     # publica os proximos N (padrao 3) artigos
                                        # da fila (pauta.py) que ainda nao existem no repo.

Estado = existencia do arquivo {slug}.html na raiz do repo.
Assim o script e idempotente: rodar de novo nao republica o que ja foi.
Nao faz git: quem clona/commita/faz push e o processo que chama este script.
"""
import sys, os, html, json, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # raiz do repositorio
sys.path.insert(0, HERE)
from pauta import ARTICLES, CATS  # noqa: E402

TEMPLATE = 'tireoide-peso-hipotireoidismo.html'
MONTHS = {'01':'jan','02':'fev','03':'mar','04':'abr','05':'mai','06':'jun',
          '07':'jul','08':'ago','09':'set','10':'out','11':'nov','12':'dez'}

def today_br():
    # data de hoje no fuso de Brasilia, sem depender de tz do servidor
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%Y-%m-%d')
    except Exception:
        return (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).strftime('%Y-%m-%d')

def br_date(d):
    y, m, dd = d.split('-'); return f"{int(dd)} {MONTHS[m]} {y}"

def esc(s): return html.escape(s, quote=True)
def j(o): return json.dumps(o, ensure_ascii=False, separators=(',', ':'))

def load_template():
    tpl = open(os.path.join(ROOT, TEMPLATE), encoding='utf-8').read()
    header = tpl[tpl.index('<header class="site-header">'):tpl.index('</header>')+len('</header>')]
    tail = tpl[tpl.index('<section class="landing-index"'):]
    return header, tail

def build_article(a, header, tail):
    catlabel, catkw = CATS[a['cat']]; slug = a['slug']
    url = f"https://nutribrunnarocha.com.br/{slug}.html"
    title = a['title']; desc = a['desc']; d = a['date']
    blog_ld = {"@context":"https://schema.org","@type":"BlogPosting","headline":title,"description":desc,"inLanguage":"pt-BR","image":"https://nutribrunnarocha.com.br/brunna-hero-v3.jpg","datePublished":d,"dateModified":d,"author":{"@type":"Person","name":"Brunna Rocha","jobTitle":"Nutricionista","honorificSuffix":"CRN 26103232/P"},"publisher":{"@type":"Organization","name":"Brunna Rocha · Nutricionista"},"mainEntityOfPage":url,"articleSection":catlabel}
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a['faq']]}
    bc_ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Início","item":"https://nutribrunnarocha.com.br/"},{"@type":"ListItem","position":2,"name":"Blog","item":"https://nutribrunnarocha.com.br/blog.html"},{"@type":"ListItem","position":3,"name":catlabel,"item":url}]}
    parts = []
    for item in a['body']:
        t = item[0]
        if t == 'h2': parts.append(f"<h2>{esc(item[1])}</h2>")
        elif t == 'h3': parts.append(f"<h3>{esc(item[1])}</h3>")
        elif t == 'p': parts.append(f"<p>{esc(item[1])}</p>")
        elif t == 'quote': parts.append(f"<blockquote>{esc(item[1])}</blockquote>")
        elif t == 'keybox':
            lis = ''.join(f"<li>{esc(x)}</li>" for x in item[2])
            parts.append(f'<div class="key-box">\n<h4>{esc(item[1])}</h4>\n<ul>\n{lis}\n</ul>\n</div>')
    body_html = '\n'.join(parts)
    faq_items = ''.join(f'<div class="faq-item"><button>{esc(q)}<span class="pm">+</span></button><div class="a"><p>{esc(ans)}</p></div></div>' for q,ans in a['faq'])
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} | Brunna Rocha</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Brunna Rocha">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="BR-ES"><meta name="geo.placename" content="Vitória">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{esc(title)} | Brunna Rocha"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="https://nutribrunnarocha.com.br/brunna-hero-v3.jpg">
<meta property="og:site_name" content="Brunna Rocha · Nutricionista">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)} | Brunna Rocha"><meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="https://nutribrunnarocha.com.br/brunna-hero-v3.jpg">
<meta name="theme-color" content="#2F193B">
<link rel="icon" href="favicon-32-v2.png" sizes="32x32">
<link rel="apple-touch-icon" href="favicon-180-v2.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">
{j(blog_ld)}
</script>
<script type="application/ld+json">
{j(faq_ld)}
</script>
<script type="application/ld+json">
{j(bc_ld)}
</script>
</head>
<body>
{header}
<article>
  <div class="article-hero">
    <div class="container">
      <div class="crumb" style="color:rgba(255,255,255,.7)"><a href="index.html#inicio" style="color:var(--lav)">Início</a> › <a href="blog.html" style="color:var(--lav)">Blog</a> › {esc(catlabel)}</div>
      <span class="cat">{esc(catlabel)}</span>
      <h1>{esc(title)}</h1>
      <div class="meta">Por Brunna Rocha · Nutricionista · <time datetime="{d}">{br_date(d)}</time> · {a['read']} min de leitura</div>
    </div>
  </div>
  <div class="article-body">

<p>{esc(a['lead'])}</p>

{body_html}

    <h2>Perguntas frequentes</h2>
    <div class="faq">{faq_items}</div>
    <div class="key-box" style="text-align:center;margin-top:44px">
      <h4>Quer um plano feito para você?</h4>
      <p>Este conteúdo é educativo e não substitui uma consulta individualizada. Agende o seu atendimento e receba orientação personalizada.</p>
      <a class="btn btn-primary" href="https://wa.me/5527992497622?text=Ol%C3%A1%2C%20Brunna!%20Gostaria%20de%20agendar%20uma%20consulta%20de%20nutri%C3%A7%C3%A3o." target="_blank" rel="noopener">Agendar com a Brunna</a>
    </div>
    <p style="margin-top:30px"><a href="blog.html" style="color:var(--plum);font-weight:600">← Voltar para o blog</a></p>
  </div>
</article>
{tail}'''

def build_card(a):
    catlabel, catkw = CATS[a['cat']]; slug = a['slug']; d = a['date']; cat = a['cat']
    badge = a['badge']; title = a['title']; desc = a['desc']; rd = a['read']
    search = (title.lower()+' '+desc.lower()+' '+catkw)
    return ('<a class="post-card blog-item reveal" href="'+slug+'.html" data-cat="'+cat+'" data-search="'+esc(search)+'">'
            '<div class="post-thumb"><span class="cat">'+esc(catlabel)+'</span><span class="mk">'+esc(badge)+'</span></div>'
            '<div class="post-body"><div class="meta"><time datetime="'+d+'">'+br_date(d)+'</time> · '+str(rd)+' min de leitura · '+esc(catlabel)+'</div>'
            '<h3>'+esc(title)+'</h3><p>'+esc(desc)+'</p></div></a>')

def sm_url(a):
    return '<url><loc>https://nutribrunnarocha.com.br/'+a['slug']+'.html</loc><lastmod>'+a['date']+'</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>'

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    date = today_br()
    # proximos N que ainda nao existem no repo
    pend = [a for a in ARTICLES if not os.path.exists(os.path.join(ROOT, a['slug']+'.html'))]
    batch = pend[:n]
    if not batch:
        print('NADA_A_PUBLICAR: a fila (pauta.py) esta esgotada. Refil necessario (ver .deploy/COMO-ESCREVER.md).')
        return 2
    for a in batch:
        a['date'] = date
    header, tail = load_template()
    for a in batch:
        open(os.path.join(ROOT, a['slug']+'.html'), 'w', encoding='utf-8').write(build_article(a, header, tail))
    # cards no blog (mais novo primeiro, logo apos a ancora)
    cards = '\n      '.join(build_card(a) for a in batch)
    blog_path = os.path.join(ROOT, 'blog.html')
    blog = open(blog_path, encoding='utf-8').read()
    anchor = '<div class="grid grid-3 mt-4" id="blogGrid">'
    if anchor not in blog:
        print('ERRO: ancora do blogGrid nao encontrada em blog.html'); return 1
    blog = blog.replace(anchor, anchor+'\n      '+cards, 1)
    open(blog_path, 'w', encoding='utf-8').write(blog)
    # sitemap
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    urls = '\n'.join(sm_url(a) for a in batch)
    sm = sm.replace('</urlset>', urls+'\n</urlset>', 1)
    open(sm_path, 'w', encoding='utf-8').write(sm)
    restantes = len(pend) - len(batch)
    print('PUBLICADOS %d em %s:' % (len(batch), date))
    for a in batch:
        print('  - %s.html  [%s]  %s' % (a['slug'], a['cat'], a['title']))
    print('FILA_RESTANTE: %d artigos ainda nao publicados.' % restantes)
    if restantes <= 3:
        print('AVISO: fila baixa. Em breve sera preciso refil (ver .deploy/COMO-ESCREVER.md).')
    return 0

if __name__ == '__main__':
    sys.exit(main())
