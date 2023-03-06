import scrapy


class QuotesSpider(scrapy.Spider):
    name = "NewsCrawler"

    start_urls = ['https://vietnamnet.vn/tin-tuc-24h']
    pageLimit = 100
    cnt = 0

    def parse(self, response):
        if self.cnt >= self.pageLimit:
            return
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
                'Cnt': self.cnt
            }

        for nextUrl in response.css('.main-v1 a::attr(href), .main-content a::attr(href)').getall():
            if self.cnt >= self.pageLimit:
                return
            yield response.follow(nextUrl, callback=self.parse)


