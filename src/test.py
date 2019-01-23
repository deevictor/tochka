from mathematician import simple_get, get_html

raw_html = simple_get('https://realpython.com/blog')
no_html = simple_get('https://realpython.com/blog/nope-not-gonna-find-it')


raw_html = open('contrived.html').read()
html = get_html(raw_html)
print(html.select('p'))

for p in html.select('p'):
    if p['id'] == 'walrus':
        print(p)
