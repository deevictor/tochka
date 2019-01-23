from mathematician import simple_get

raw_html = simple_get('https://realpython.com/blog')
no_html = simple_get('https://realpython.com/blog/nope-not-gonna-find-it')
print(no_html)