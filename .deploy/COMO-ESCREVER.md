# Como abastecer a fila de artigos (refil)

Este repositorio publica o blog da Brunna Rocha de forma automatica.
Todo dia, um processo roda `.deploy/publicar.py`, que pega os proximos 3 artigos
da fila em `.deploy/pauta.py` que ainda nao foram publicados e os coloca no ar.

## Quando abastecer

Quando `publicar.py` avisar `FILA_RESTANTE` baixa (3 ou menos) ou `NADA_A_PUBLICAR`,
e preciso escrever novos artigos e acrescenta-los ao final da lista `ARTICLES` em
`.deploy/pauta.py`.

## Regras de estilo (obrigatorias)

- Publico: pessoas leigas buscando informacao de nutricao confiavel.
- Tom: acolhedor, claro, profissional, em portugues do Brasil.
- NUNCA usar travessao longo. Usar virgula ou parenteses no lugar.
- Nao prometer cura, nao dar conduta medica, sempre reforcar que o conteudo e
  educativo e nao substitui consulta individualizada.
- Cada artigo entre 600 e 800 palavras aproximadamente.
- Tema tem que ser DIFERENTE de todos os artigos ja existentes (verifique os
  arquivos {slug}.html ja no repositorio antes de escolher o tema).

## Formato de cada item da lista ARTICLES

```python
{'slug':'slug-sem-acento-com-hifens','read':7,'cat':'bemestar','badge':'Frase curta',
 'title':'Titulo do artigo',
 'desc':'Meta description de 1 a 2 frases, com a palavra-chave.',
 'lead':'Paragrafo de abertura que engaja e apresenta o tema.',
 'body':[
   ('h2','Subtitulo de secao'),
   ('p','Paragrafo.'),
   ('quote','Frase de destaque.'),
   ('h3','Subtitulo menor'),
   ('p','Paragrafo.'),
   ('keybox','Titulo da caixa de dicas',['dica 1','dica 2','dica 3','dica 4','dica 5']),
   ('h2','Ultima secao, geralmente com chamada para acompanhamento'),
   ('p','Paragrafo final.'),
 ],
 'faq':[('Pergunta 1?','Resposta 1.'),
        ('Pergunta 2?','Resposta 2.'),
        ('Pergunta 3?','Resposta 3.')]},
```

- Nao inclua o campo `date`. Ele e preenchido automaticamente na hora de publicar.
- Estrutura recomendada do `body`: 1 lead + 2 a 3 blocos h2 (alguns com h3), 1 quote,
  1 keybox com 5 itens, 3 perguntas no faq.

## Categorias validas (`cat`)

- `saude` = Saude da Mulher
- `materno` = Materno-infantil
- `emagrecimento` = Emagrecimento
- `esportiva` = Nutricao Esportiva
- `bemestar` = Saude & Bem-estar

## O que NAO fazer

- Nao editar `publicar.py` para pular a verificacao de existencia.
- Nao alterar artigos ja publicados por aqui.
- Nao repetir tema ja coberto.
