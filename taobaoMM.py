# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 12:55:52 2016

@author: Alan

这是一个爬取淘宝mm的爬虫
"""

# 爬取百度贴吧
import urllib2
import re
import os

class Tools:
    '''
    替换多余标签或者内容的工具类
    '''
    # 移除img标签
    removeImg = re.compile(u'<img.*?>| {7}') 
    # 移除超链接标签
    removeAddr = re.compile(u'<a.*?>')
    #把换行的标签换为\n
    replaceLine = re.compile(u'<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile(u'<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile(u'<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile(u'<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile(u'<.*?>')
    def replace(self, x):
        x = re.sub(self.removeImg, u'', x)# remove
        x = re.sub(self.removeAddr, u'', x )
        x = re.sub(self.replaceLine, u'\n', x)
        x = re.sub(self.replaceTD, u'\t', x)
        x = re.sub(self.replacePara, u'\n  ', x)
        x = re.sub(self.replaceBR, u'\n', x)
        x = re.sub(self.removeExtraTag, u'', x)
        return x.strip()# 删除前后的空格

class MMSpyder:
    def __init__(self):
        self.baseUrl = 'https://mm.taobao.com/json/request_top_list.htm'
        self.tool = Tools()

    # 根据URL获取某一页信息
    def getPageByUrl(self, inputUrl):
        try:
            request = urllib2.Request(inputUrl)
            response = urllib2.urlopen(request)
            #通过浏览器的工具可以查看到该网页使用gbk编码的，现在解码成Unicode
            return response.read().decode('gbk')
        except urllib2.URLError, e:
            if hasattr(e, 'reason'):
                print "url错误:", e.reason
                return None
        
    # 根据pageIndex获取某一页的信息，pageIndex从1开始
    def getPageByIndex(self, pageIndex):
        url = self.baseUrl + '?page=' + str(pageIndex)
        return self.getPageByUrl(url)
    
    
    # 获取mm的基本信息，包括详情URL，头像URL，姓名，年龄，地址,简介
    # 其中item[0]就是详情URL，有各种信息和本人的大量图片
    # 每人的信息组成一个列表，然后再组合成一个总的列表返回
    def getBasicInfo(self, page):
        pattern = re.compile('<div class="list-item".*?"personal-info".*?<a href="(.*?)".*?<img src="(.*?)".*?\<a class="lady-name"".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>', re.S)
        result = re.findall(pattern, page)#以列表形式返回全部能匹配的字串
        contents = []
#        print result[0][0]
        for item in result:
            contents.append([item[0], item[1], item[2], item[3], item[4], item[5]])
        return contents
        
    #获取个人的描述 
    def getDescription(self, page):
        pattern = re.compile('<div class="list-item".*?<p class="description">(.*?)</p>', re.S)
        result = re.findall(pattern, page)
        result = [x.strip() for x in result]        
        return result         
    
    # 保存头像
    def saveIcon(self, iconUrl, name):
        iconUrlSplit = iconUrl.split('.')
        fTail = iconUrlSplit.pop()# 获得文件的后缀
        fileName = unicode(name + '/icon.' + fTail)
        response = urllib2.urlopen(iconUrl)
        f = open(fileName, 'wb')#以二进制模式写入
        print u"正在保存的头像为：", fileName        
        f.write(response.read())     
        f.close()
           
    # 根据名字保存mm描述信息        
    def saveDescription(self, name, contents, index):
        fileName = unicode(name + '/desc.txt')
        f = open(fileName, 'w+')
        f.write(contents[index].encode('utf-8'))        
        f.close()
        
    # 在taobaomm文件夹下面创建以名字命名的文件夹
    def mkdir(self, name):
        path = unicode(name)      
        #返回True or False
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            return True
        else:
            print u'路径已经存在！'
            return False
    
    # 保存一页mm的信息
    def savaOnePageMM(self, pageIndex):
        page = self.getPageByIndex(pageIndex)
        contents = self.getBasicInfo(page)
        descContents = self.getDescription()
        # 每一个item是一个人的信息    
        for index in range(len(contents)):
            item = contents[index]
            personName = item[2]
            iconURL = item[1]
            self.mkdir(personName)
            print '现在保存', personName, '的信息'
            print '保存头像'
            self.saveIcon(iconURL, personName)
            print '保存描述'
            self.saveDescription(personName, descContents, index)
            
        
         
if __name__ == '__main__':
    taobaomm = MMSpyder()
    taobaomm.savaOnePageMM(1)