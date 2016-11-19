
# -*- coding:utf-8 -*-
import urllib2
import re
import numpy as np
import time

class QSBK:
    '''
    这是一个爬取糗事百科段子的爬虫
    '''
    def __init__(self):
        self.pageIndex = 1  # 默认第一页
        self.baseUrl = 'http://www.qiushibaike.com/hot/page/'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-agent': self.user_agent}
        self.file = None  # 文件对象，用于存储爬去的段子

    def getPage(self, pageIndex):
        '''
        :param self:
        :param pageIndex:页码编号
        :return: 页码的代码内容
        '''
        url = self.baseUrl + str(pageIndex)
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')  # 转化成Unicode
            return content
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "连接糗事百科失败，原因：", e.reason
                return None


    def onePageStories(self, pageContent):
        '''
        :param self:
        :param pageContent:某一个网页的页面代码
        :return: 返回一整页的段子们，过滤掉带图片的
        '''
        pageStories = [] # 存储一页的段子们
        pattern = re.compile('<div.*?<h2>(.*?)</h2>.*?<span>(.*?)</span>.*?number">(.*?)</i>.*?number">(.*?)</i>', re.S)
        items = re.findall(pattern, pageContent)
        for item in items:
            returnItem = []  # 存储处理后的每条段子，包括id，content，votes，comments
            returnItem.append(item[0])
            returnItem.append(item[1].replace("<br/>", '\n'))  # 过滤掉换行符
            returnItem.append(item[2])
            returnItem.append(item[3])
            pageStories.append(returnItem)
        return pageStories  # 返回每一页的段子们

    # 获得点赞排行前n的段子
    def getTopNStroies(self, n, stories):

        retStories = []
        voteNum = []
        if n > len(stories):
            print "超过总的段子数，将返回全部段子"
            return stories
        else:
            for story in stories:
                voteNum.append(int(story[2]))
            indexOfTopN = np.array(voteNum).argsort()[-n:]  # 获得topN元素的下标
            retStories = np.array(stories)[indexOfTopN]
            return retStories.tolist()


    # 传入段子组成的列表，存储到文件中
    def saveStoriesToFile(self, stories):
        # 用时间(精确到分钟)构造文件名
        fileName = time.strftime("%Y%m%d%H", time.localtime(time.time()))
        try:
            self.file = open(fileName+'.txt', 'w+')
            for story in stories:
                self.file.write('ID:' + story[0].encode('utf-8') + '\n')
                self.file.write(story[1].encode('utf-8')+ '\n')
                self.file.write('\n'+ '\n')
        finally:
            if self.file:
                self.file.flush()
                self.file.close()



# 爬取nPage页段子,并保存最受欢迎的topN个
def run(nPage, topN):
    qiushibaike = QSBK()
    stories = []
    for i in range(1, nPage + 1):
        pageContent = qiushibaike.getPage(i)
        pageStories = qiushibaike.onePageStories(pageContent)
        stories += pageStories

        time.sleep(2)  # 猜测由于频繁访问报下面的错，所以休眠
        # 连接糗事百科失败，原因： Service Temporarily Unavailable

    topNStories = qiushibaike.getTopNStroies(topN, stories)
    qiushibaike.saveStoriesToFile(topNStories)
    # for item in topNStories:
    #     print "id:", item[0]
    #     print item[1]
    # print "总的段子数量", len(stories)
    # print "最受欢迎的段子数", len(topNStories)

# 测试代码
if __name__ == "__main__":
    run(5, 10)





