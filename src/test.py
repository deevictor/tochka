from mathematician import simple_get, get_html
import scrapy

# def get_names():
#
#     url = 'http://www.fabpedigree.com/james/mathmen.htm'
#     raw_html = simple_get(url)
#     if raw_html:
#         html = get_html(raw_html)
#         names = set()
#         for li in html.select('li'):
#             for name in li.text.split('\n'):
#                 if len(name) > 0:
#                     names.add(name.strip())
#         return list(names)
#
#     raise Exception('Error retrieving contents at {}'.format(url))
#
#
# for name in get_names():
#     print(name)


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').extract_first()}

        for next_page in response.css('div.prev-post >a'):
            yield response.follow(next_page, self.parse)

