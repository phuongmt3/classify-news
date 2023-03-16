import random
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "NewsCrawler"

    start_urls = ['https://vietnamnet.vn/tin-tuc-24h']
    pageLimit = 100
    cnt = 0

    def parse(self, response):
        if self.cnt >= self.pageLimit:
            return

        contents = response.css('.main-content ::text')
        category = response.css('.bread-crumb-detail  a::attr(title)').get()
        keywords = response.css('meta[name*=keywords]::attr(content)').get()
        title = response.css('title::text').get().strip()
        if contents and response.css('.bread-crumb-detail  a::attr(title)').get() \
                and category != 'Video' and category != 'Premium':
            self.cnt += 1
            if 50 < random.randint(0, 100) <= 80:
                ftest = open('scrapy_test/spiders/Output/testSet.txt', 'a+', encoding='utf-8')
                ftestans = open('scrapy_test/spiders/Output/testAns.txt', 'a+', encoding='utf-8')
                ftest.write(title + ' ' + response.css('meta[name*=description]::attr(content)').get().strip() + ' ')
                for p in contents:
                    ftest.write(p.get().strip().replace('\n', ' ') + ' ')
                ftest.write('\n')
                ftestans.write(getSubjectName(category, keywords, title) + '\n')
                ftest.close()
                ftestans.close()

            else:
                ftrain = open('scrapy_test/spiders/Output/trainSet.txt', 'a+', encoding='utf-8')
                ftrain.write(getSubjectName(category, keywords, title) + '  ')
                ftrain.write(title + ' ' + response.css('meta[name*=description]::attr(content)').get().strip() + ' ')
                for p in contents:
                    ftrain.write(p.get().strip().replace('\n', ' ') + ' ')
                ftrain.write('\n')
                ftrain.close()

            yield {
                'URL': response.url,
                'Title': title,
                'Category': category,
                'Keywords': keywords,
                'Publish date': response.css('.bread-crumb-detail__time p::text').get(),
                'Cnt': self.cnt
            }

        for nextUrl in response.css('.main-v1 a::attr(href), .main-content a::attr(href)').getall():
            if self.cnt >= self.pageLimit:
                return
            yield response.follow(nextUrl, callback=self.parse)


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


