# -*- coding: utf-8 -*-
import keyword

import scrapy
import sys
import urllib

class GoogleItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    cited = scrapy.Field()
    authors = scrapy.Field()
    links = scrapy.Field()


class GoogleSpider(scrapy.Spider):
    name = 'google'
    allowed_domains = ['https://scholar.google.com/']
    start_urls = ['https://httpbin.org/get']
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    def __init__(self, keyword, number=10, sort_key=0):
        '''
        keyword: 研究领域或者关键字
        number: 论文数目上限
        sort_key: 默认0表示相关性，1表示时间倒序
        '''
        number = int(number)
        if keyword == '' or number <= 0:
            print('INPUT "keyword" or MAKE SURE "number" IS POSITIVE!')
            sys.exit(0)
        protocol = 'https'
        path = 'scholar'

        max_pn = number // 10 if number // 10 > 0 else 1

        for pn in range(max_pn):
            params = {}
            params['q'] = keyword
            params['start'] = pn * 10
            if sort_key == 1:
                params['scisbd'] = 1
            query_string = urllib.parse.urlencode(
                params, encoding='utf-8')
            url = '{}://{}/{}?{}'.format(protocol,
                                         self.allowed_domains[0], path, query_string)
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            proxy = "34.80.1.78:313538"
            proxies = ""
        if url.startswith("https://"):
            proxies = "https://" + "34.80.1.78:31353"
        elif url.startswith("https://"):
            proxies = "https://" + "34.80.1.78:31353"
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'proxies'})

            def parse(self, response):
                    print(response.text)
                    result_divs = response.xpath(
                        "//div[@id='gs_bdy']//div[@id='gs_res_ccl_mid']/div[@class='gs_r gs_or gs_scl']/div")
                    for div in result_divs:
                        item = GoogleItem()
                        links = []
                        pdf_key = div.xpath(
                            "./div[@class='gs_ggs gs_fl']//a/text()").extract()[0].strip()
                        pdf_link = div.xpath(
                            "./div[@class='gs_ggs gs_fl']//a/@href").extract()[0].strip()
                        links.append({pdf_key: pdf_link})

                        item['title'] = div.xpath(
                            "./div[@class='gs_ri']/h3/a/text()").extract()[0].strip()
                        link = div.xpath(
                            "./div[@class='gs_ri']/h3/a/@href").extract()[0].strip()
                        links.append({'google': link})

                        meta_info = div.xpath(
                            "./div[@class='gs_ri']/div[@class='gs_a']/text()").extract()[0].strip()
                        authors, conference, _ = meta_info.split('-')
                        item['authors'] = [x.strip() for x in authors.split(',')]
                        item['date'] = conference.split(',')[-1].strip()
                        if int(item['date']) < 2000:
                            break
                        item['cited'] = div.xpath(
                            "./div[@class='gs_ri']/div[@class='gs_fl']//a[2]").extract()[0].strip().split('：')[-1]

            def __init__(self, keyword, number=10, sort_key=0):
                    '''
                    keyword: 研究领域或者关键字
                    number: 论文数目上限
                    sort_key: 默认0表示相关性，1表示时间倒序
                    '''
                    number = int('number')
                    if keyword == '' or number <= 0:
                        print('INPUT "keyword" or MAKE SURE "number" IS POSITIVE!')
                        sys.exit(0)

                    protocol = 'https'
                    path = 'scholar'

                    max_pn = number // 10 if number // 10 > 0 else 1

                    for pn in range(max_pn):
                        params = {}
                        params['q'] = keyword
                        params['start'] = pn * 10
                        if sort_key == 1:
                            params['sci'] = 1
                        query_string = urllib.parse.urlencode(
                            params, encoding='utf-8')
                        url= '{}://{}/{}?{}'.format(protocol,
                                                     self.allowed_domains[0], path, query_string)
            self.start_urls.append(url)

            def start_requests(self):
                        for url in self.start_urls:
                            proxy = "34.80.1.78:313538"
                            proxies = ""
                        if url.startswith("https://"):
                            proxies = "https://" + "34.80.1.78:31353"
                        elif url.startswith("https://"):
                            proxies = "https://" + "34.80.1.78:31353"

            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': 'proxies'})

            def parse(self, response):
                    print(response.text)
                    result_divs = response.xpath(
                        "//div[@id='gs_bdy']//div[@id='gs_res_ccl_mid']/div[@class='gs_r gs_or gs_scl']/div")
                    for div in result_divs:
                        item = GoogleItem()
                        links = []
                        pdf_key = div.xpath(
                            "./div[@class='gs_ggs gs_fl']//a/text()").extract()[0].strip()
                        pdf_link = div.xpath(
                            "./div[@class='gs_ggs gs_fl']//a/@href").extract()[0].strip()
                        links.append({pdf_key: pdf_link})

                        item['title'] = div.xpath(
                            "./div[@class='gs_ri']/h3/a/text()").extract()[0].strip()
                        link = div.xpath(
                            "./div[@class='gs_ri']/h3/a/@href").extract()[0].strip()
                        links.append({'google': link})

                        meta_info = div.xpath(
                            "./div[@class='gs_ri']/div[@class='gs_a']/text()").extract()[0].strip()
                        authors, conference, _ = meta_info.split('-')
                        item['authors'] = [x.strip() for x in authors.split(',')]
                        item['date'] = conference.split(',')[-1].strip()
                        if int(item['date']) < 2000:
                            break
                        item['cited'] = div.xpath(
                            "./div[@class='gs_ri']/div[@class='gs_fl']//a[2]").extract()[0].strip().split('：')[-1]

                        item['links'] = links
                        yield item
                        item['links'] = links
                        yield item
# scrapy runspider -a keyword='mesenteric vasculitis' -a number=500 -a sort_key=0 -o google_papers.json google.py
