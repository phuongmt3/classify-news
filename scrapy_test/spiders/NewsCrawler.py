import random
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "NewsCrawler"

    pageLimit = 60
    cnt = 0

    def start_requests(self):
        urls = []
        for i in range(10):
            urls.append('https://vietnamnet.vn/phap-luat-page' + str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseBig)

    def parseBig(self, response):
        for nextUrl in response.css('.vnn-title a::attr(href)').getall():
            if self.cnt >= self.pageLimit:
                return
            yield response.follow(nextUrl, callback=self.parse)

    def parse(self, response):
        if self.cnt >= self.pageLimit:
            return

        contents = response.css('.main-content ::text')
        category = response.css('.bread-crumb-detail  a::attr(title)').getall()
        keywords = response.css('meta[name*=keywords]::attr(content)').get()
        title = response.css('title::text').get().strip()
        if contents and response.css('.bread-crumb-detail  a::attr(title)').get() \
                and category[0] == 'Pháp luật':
            self.cnt += 1
            ftrain = open('spiders/Output/KH.txt', 'a+', encoding='utf-8')
            # ftrain.write(getSubjectName(category[1], keywords, title) + '\t')
            ftrain.write('__PL__\t')
            ftrain.write(title + ' ' + response.css('meta[name*=description]::attr(content)').get().strip() + ' ')
            for p in contents:
                ftrain.write(p.get().strip().replace('\n', ' ') + ' ')
            ftrain.write('\n')
            ftrain.close()

            yield {
                'URL': response.url,
                'Title': title,
                'Category': category[1],
                'Keywords': keywords,
                'Publish date': response.css('.bread-crumb-detail__time p::text').get(),
                'Cnt': self.cnt
            }


def getSubjectName(category, keywords, title):
    switcher = {
        'Giáo dục': '__giao-duc__', 'Thời sự': '__thoi-su__', 'Kinh Doanh': '__kinh-doanh__',
        'Thế giới': '__the-gioi__', 'Giải trí': '__giai-tri__', 'Đời sống': '__doi-song__',
        'Pháp luật': '__phap-luat__', 'Thể thao': '__the-thao__',
        'Thông tin và Truyền thông': '__thong-tin-truyen-thong__',
        'Ô tô - Xe máy': '__oto-xe-may__', 'Bất động sản': '__bat-dong-san__', 'Bạn đọc': '__ban-doc__',
        'Du lịch': '__du-lich__', 'Sức khỏe': '__suc-khoe__', 'Dân tộc - Tôn giáo': '__dan-toc-ton-giao__',
        'Thị trường - tiêu dùng': '__thi-truong-tieu-dung__', 'Tư liệu': '__tu-lieu__'
    }
    if category not in switcher.keys():
        with open('scrapy_test/spiders/Output/unlabeledTrainSet.txt', 'a+', encoding='utf-8') as f:
            f.write(title + '\n')
    return switcher.get(category, '__' + category + keywords + '__')


