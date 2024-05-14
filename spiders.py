# -*- coding: utf-8 -*-
"""spiders

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MTfgSE_MkLCRF9fuMnb2jCurdknMa0c6
"""

!pip install scrapy

import scrapy
import csv
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class NewsDaySpider(scrapy.Spider):
    name = 'newsday_spider'
    start_urls = [
        'https://www.newsday.co.zw/category/4/business',
        'https://www.newsday.co.zw/category/9/opinion-and-analysis',
        'https://www.newsday.co.zw/category/5/sport',
        'https://www.newsday.co.zw/category/8/lifestyle-and-arts'
    ]

    def parse(self, response):
        category = response.css('div.brand-title h2 a.links::text').get()

        articles = response.css('div.card-body.pad-o.mt-3')

        for article in articles:
            title = article.css('a.text-dark div.sub-title.mt-3::text').get()
            link = article.css('a::attr(href)').get()
            content = article.css('div.mb-3.pt-2.top-article::text').get()

            scraped_info = {
                'category': category,
                'title': title,
                'link': link,
                'content': content
            }

            yield scraped_info

data = pd.read_csv('/content/scraped_newsday.csv')

data.head()

class FoxNewsSpider(scrapy.Spider):
    name = 'foxnews_spider'
    start_urls = ['https://www.foxnews.com/politics']  #

    def parse(self, response):
        for article in response.css('div.article'):
            title = article.css('h2.title::text').get().strip()
            url = article.css('a::attr(href)').get()
            description = article.css('p.description::text').get().strip()
            category = article.css('span.eyebrow::text').get().strip()  #

            yield {
                'Title': title,
                'URL': url,
                'Description': description,
                'Category': category
            }

class ABCSpider(scrapy.Spider):
    name = 'abcnews_spider'
    start_urls = [
        'https://www.newsday.co.zw/category/4/business',
        'https://www.newsday.co.zw/category/9/opinion-and-analysis',
        'https://www.newsday.co.zw/category/5/sport',
        'https://www.newsday.co.zw/category/8/lifestyle-and-arts'
    ]

    def parse(self, response):
        category = response.css('div.brand-title h2 a.links::text').get()

        articles = response.css('div.card-body.pad-o.mt-3')

        for article in articles:
            title = article.css('a.text-dark div.sub-title.mt-3::text').get()
            link = article.css('a::attr(href)').get()
            content = article.css('div.mb-3.pt-2.top-article::text').get()

            scraped_info = {
                'category': category,
                'title': title,
                'link': link,
                'content': content
            }

            yield scraped_info

df = pd.read_csv("/content/abcnews.csv")

import scrapy

class Telegraph(scrapy.Spider):
    name = "newyorktimes_spider"
    allowed_domains = ["nytimes.com"]
    start_urls = [
        "https://www.nytimes.com/"
    ]

    def parse(self, response):
        categories_to_scrap = ['politics', 'sports', 'business', 'arts']

        news_categories = response.css('header > div.css-1d8a290 > ul > li > a::text').getall()
        news_categories_urls = response.css('header > div.css-1d8a290 > ul > li > a::attr(href)').getall()

        for category, url in zip(news_categories, news_categories_urls):
            if category.lower() in categories_to_scrap:
                yield scrapy.Request(url, self.parse_articles, cb_kwargs=dict(category=category.lower()))


    def parse_articles(self, response, category):
        section_1 = response.css('ol > li > article > div > h2 > a::attr(href)').getall()
        section_2 = response.css('ol > li > div > div.css-1l4spti > a::attr(href)').getall()

        for url in section_1 + section_2:
            article_url = "https://www.nytimes.com" + url
            yield scrapy.Request(article_url, self.parse_story, cb_kwargs=dict(category=category))


    def parse_story(self, response, category):
        heading = response.css('header > div.css-1vkm6nb > h1::text').get()
        article = response.css('#story > section > div.css-1fanzo5  > div > p::text').getall()

        story = ' '.join([paragraph for paragraph in article])

        yield dict(url=response.url, category=category, heading=heading, article=article)

