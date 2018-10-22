# -*- coding: utf-8 -*-
import re
from copy import deepcopy

import scrapy
from ..items import AmazonItem


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com', 'amazon.cn']
    start_urls = [
        'https://www.amazon.cn/gp/search/other/ref=lp_665002051_sa_p_89?rh=n%3A2016116051%2Cn%3A%212016117051%2Cn%3A664978051%2Cn%3A665002051&bbn=665002051&pickerToList=lbr_brands_browse-bin&ie=UTF8&qid=1540199003']

    def parse(self, response):
        """提取每个品牌和列表页的url"""
        # print(response.text)
        lis = response.xpath('//ul[@class="s-see-all-indexbar-column"]//li')
        for li in lis:
            item = AmazonItem()
            item['brand'] = li.xpath('./span/a/@title').extract_first()
            item['brand_url'] = "https://www.amazon.cn" + li.xpath('./span/a/@href').extract_first()
            # print(item)
            yield scrapy.Request(url=item['brand_url'], callback=self.list_parse, meta={'item': deepcopy(item)})

    def list_parse(self, response):
        """处理品牌列表页"""
        item = response.meta['item']
        # print(item)
        lis = response.xpath('//ul[@id="s-results-list-atf"]/li')
        for li in lis:
            item['title'] = li.xpath('.//h2/@data-attribute').extract_first()
            item['sku_url'] = li.xpath(
                './/div[@class="a-section a-spacing-none a-inline-block s-position-relative"]/a/@href').extract_first()
            yield scrapy.Request(url=item['sku_url'], callback=self.detail_parse, meta={'item': deepcopy(item)})

        # 列表页进行翻页处理
        next_url = response.xpath('//span[@class="pagnRA"]/a/@href').extract_first()
        if next_url:
            next_url = "https://www.amazon.cn" + next_url
            # print(item)
            yield scrapy.Request(url=next_url, callback=self.list_parse, meta={'item': item})

    def detail_parse(self, response):
        """处理商品详情页"""
        item = response.meta['item']
        lis = response.xpath('//li[contains(@id, "_name_")]')
        for li in lis:
            sku_id =li.xpath('./@data-dp-url').extract_first()

            url = "https://www.amazon.cn" + sku_id
            # print(item['sku_url'])
            item['info'] = ''.join(i.strip() for i in (response.xpath('//span[@class="selection"]/text()').extract()))
            item['price'] = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
            print(response.url)
            print(url)
            print(item['info'])
            yield item
            # 对于选择方案的处理（如：选择不同颜色和不同内存不能算同一款手机）
            yield scrapy.Request(url=url, callback=self.detail_parse, meta={'item': deepcopy(item)})
