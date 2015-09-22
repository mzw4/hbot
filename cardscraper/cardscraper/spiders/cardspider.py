# -*- coding: utf-8 -*-
import urllib
import scrapy
from cardscraper.items import Card
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from urlparse import urljoin


class CardScraperSpider(scrapy.Spider):
    name = "cardspider"
    allowed_domains = ["hearthstone.gamepedia.com"]
    start_urls = [
        "http://hearthstone.gamepedia.com/Classic_card_list",
    ]

    # "http://hearthstone.gamepedia.com/Basic_card_list"
    # "http://hearthstone.gamepedia.com/Goblins_vs_Gnomes_card_list"
    # "http://hearthstone.gamepedia.com/Grand_Tournament_card_list"
    # "http://hearthstone.gamepedia.com/Naxxramas_card_list"
    # "http://hearthstone.gamepedia.com/Blackrock_Mountain_card_list"
    # "http://hearthstone.gamepedia.com/Promo_card_list"

    # '//div[@class="stdinfobox"]/div[@class="image"/img'

    # rules = (
    #     Rule(LinkExtractor(allow=('/*_card_list', )), callback='parse'),
    # )

    def parse(self, response):
        for sel in response.xpath('//tr'):
            print sel.xpath("td/a/@href").extract()

            cardlink = sel.xpath("td/a/@href").extract()
            if cardlink:
                url = urljoin(response.url, cardlink[0])
                yield scrapy.Request(url, callback=self.parse_card)
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)

    def parse_card(self, response):
        for sel in response.xpath('//div[@class="image"]'):
            print sel.xpath('a/img/@src').extract()


    # def parse_item(self, response):
    #   for sel in response.xpath('//ul/li'):
    #     movie = Movie()
    #     title = sel.xpath("i/a/text()").extract()

    #     if title:
    #       movie['title'] = title
    #       yield movie