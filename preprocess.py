from underthesea import pos_tag

with open('scrapy_test/spiders/Output/newsContent.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        print(line)
        print(pos_tag(line))


