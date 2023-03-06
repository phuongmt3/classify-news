import scrapy


class QuotesSpider(scrapy.Spider):
    name = "NewsCrawler"

    start_urls = ['https://vietnamnet.vn/tin-tuc-24h']
    frontierLimit = 100
    pageLimit = 10000
    frontier = []
    addedUrls = []  # upgrade to hash table
    cnt = 0

    def errorHandler(self, failure):
        yield scrapy.Request(self.frontier.pop(0), callback=self.parse, dont_filter=True)

    def parse(self, response):
        if len(self.addedUrls):
            with open('scrapy_test/spiders/Output/newsContent.txt', 'a+', encoding='utf-8') as f:
                contents = response.css('.main-content ::text')
                if contents and response.css('.bread-crumb-detail  a::attr(title)').get():
                    self.cnt += 1
                    f.write(str(self.cnt) + '-- ')
                    f.write(response.css('title::text').get() + '\n' +
                            response.css('meta[name*=description]::attr(content)').get() + '\n')
                    for p in contents:
                        f.write(p.get().strip() + ' ')
                    f.write('\n')

                yield {
                    'URL': response.url,
                    'Category': response.css('.bread-crumb-detail  a::attr(title)').get(),
                    'Keywords': response.css('meta[name*=keywords]::attr(content)').get(),
                    'Publish date': response.css('.bread-crumb-detail__time p::text').get(),
                    #'Frontier size': len(self.frontier),
                    'Added url size': len(self.addedUrls),
                    'Cnt': self.cnt#,
                    #'Frontier': self.frontier
                }

        nextPages = response.css('.main-v1 a::attr(href), .main-content a::attr(href)').getall()
        for url in nextPages:
            if len(self.frontier) > self.frontierLimit:
                break

            if url[-5:] == '.html' and response.urljoin(url) not in self.addedUrls:
                self.frontier.append(response.urljoin(url))
                self.addedUrls.append(response.urljoin(url))

        if self.cnt == self.pageLimit or len(self.frontier) == 0:
            return
        yield scrapy.Request(self.frontier.pop(0), callback=self.parse, dont_filter=True, errback=self.errorHandler)
