#!/usr/bin/env bash
export PATH=$PATH:/home/viktor/.virtualenvs/tochka/bin/
#scrapy runspider page_spider.py -o page.json
scrapy runspider article_spider.py -o article.json