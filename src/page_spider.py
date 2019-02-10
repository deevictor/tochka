import scrapy


class PageSpider(scrapy.Spider):
    name = "page"
    start_urls = ['http://blog.theodo.fr/']

    def parse(self, response):
        for article_url in response.css('.entry-title a ::attr("href")').extract():
            yield response.follow(article_url, callback=self.parse_article)

    @staticmethod
    def replace_multiple(main_string, tobe_replaced, new_string):
        # Iterate over the strings to be replaced
        for elem in tobe_replaced:
            # Check if string is in the main string
            if elem in main_string:
                # Replace the string
                main_string = main_string.replace(elem, new_string)

        return main_string

    def parse_article(self, response):
        content = response.xpath(".//div[@class='entry-content']/descendant::text()").extract()
        # content = self.replace_multiple(content, ["\r", "\n", "\t"], "")
        # content.replace("\r", "")
        yield {'article': ''.join(content)}

