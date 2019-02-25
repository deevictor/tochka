import scrapy


class BlogSpider(scrapy.Spider):
    name = "blog"
    start_urls = ['http://blog.theodo.fr/']

    def parse(self, response):
        for article_url in response.css('.entry-title a ::attr("href")').extract():
            yield response.follow(article_url, callback=self.parse_article)
        older_posts = response.css('.nav-previous a ::attr("href")').extract_first()
        if older_posts is not None:
            yield response.follow(older_posts, callback=self.parse)

    def parse_article(self, response):
        content = response.xpath(".//div[@class='entry-content']/descendant::text()").extract()
        yield {'article': ''.join(content)}


result = [
    [row1, row2, row3], [row8, row9, row10]
]

data = [
    2, -10, 3, 15, 7, -1, -6, 10, 7, -4, 2, 9, 1, 0, -5, 0, 9, -2, -5, 1, 10
]