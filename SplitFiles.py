def getSubjectName(category):
    switcher = {
        '__giao-duc__': '__CTXH__', '__thoi-su__': '__CTXH__', '__kinh-doanh__': '__KD__',
        '__the-gioi__': '__TG__', '__giai-tri__': '__VH__', '__doi-song__': '__DS__',
        '__phap-luat__': '__PL__', '__the-thao__': '__TT__',
        '__thong-tin-truyen-thong__': '__VT__',
        '__oto-xe-may__': '__XE__', '__bat-dong-san__': '__KD__', '__ban-doc__': '__DS__',
        '__du-lich__': '__CTXH__', '__suc-khoe__': '__SK__',
        '__thi-truong-tieu-dung__': '__KD__', '__tu-lieu__': '__CTXH__'
    }
    return switcher.get(category, '__' + category + '__')


# thay labels in Output
trainFile = open('scrapy_test/spiders/Output/trainSet.txt', 'r', encoding='utf-8')
testAns = open('scrapy_test/spiders/Output/testAns.txt', 'r', encoding='utf-8')
testFile = open('scrapy_test/spiders/Output/testSet.txt', 'r', encoding='utf-8')
outTrain = open('scrapy_test/spiders/Output/_trainSet.txt', 'w', encoding='utf-8')

labels = []
for line in trainFile.readlines():
    category, text = line.split("  ", 1)
    outTrain.write(getSubjectName(category) + '\t' + text)
for line in testAns.readlines():
    labels.append(getSubjectName(line.strip()))
curid = 0
for line in testFile.readlines():
    outTrain.write(labels[curid] + '\t' + line)
    curid += 1
