# -*- coding: utf-8 -*-

"""
author: Alan
这是一个爬取百度贴吧的帖子，只要输入贴吧的代号，就能获得那个帖子所有楼层的文字信息，并且
可以选择是否只看楼主。
内部的运行顺序是这样的，先根据url获取网页的内容然后把编码转换成Unicode，
因为从服务器拉取到本地的网页是utf8编码的。
然后从编码后的网页中匹配也要用用Unicode的正则表达式
"""

# 爬取百度贴吧
import urllib2
import re

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
        
class BDTB:
    def __init__(self, baseUrl, seeLZ):
        '''
        初始化，baseUrl是基本的url，seeLZ为是否只看楼主的参数
        '''
        self.baseUrl = baseUrl
        self.seeLZ = seeLZ
        self.tool = Tools()
        self.file = None#文件写入对象，保存爬取的内容
        self.floor = 1# 楼层，初始化为1
        self.defaultTitle = u'百度贴吧'

    def getPage(self, pageNum):
        '''
        pageNum为想要获得的页码
        '''
        #构建URL
        if pageNum == 0:
            url = self.baseUrl + '?see_lz' + str(self.seeLZ)
        else:
            url = self.baseUrl + \
                  '?see_lz='+str(self.seeLZ)+\
                  '&pn='+str(pageNum)
        try:
            
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
#            print response.read().decode(u'utf-8')# 用于测试的打印
            return response.read().decode('utf-8')#把utf-8编码转化成Unicode字符串
        #unable to connect
        except urllib2.URLError, e:
            if hasattr(e, u'reason'):
                print u'连接百度贴吧失败，错误原因：', e.reason
                return None
        finally:
            response.close()
                
    def getTitle(self, page):
        '''
        获取帖子标题
        '''
        pattern = re.compile(u'<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
#            print result.group(1)# 用于测试
            return result.group(1).strip()
        else:
            return None
    
    def getPageNum(self, page):
        '''
        通过“共*页”的内容获取帖子的页数
        '''
        pattern = re.compile(u'<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
#            print result.group(1)
            return result.group(1).strip()
        else:
            return None

    # 根据页面内容获取每一楼的内容
    def getContent(self,page):
        pattern = re.compile(u'<div id="post_content_.*?>(.*?)</div>', re.S)
        result = re.findall(pattern, page)
        contents = []
        for item in result:
            #收尾加上换行符之后加入list中
            content = '\n'+self.tool.replace(item)+'\n' 
            contents.append(content.encode('utf-8'))# 要编码成utf8才能写入文件！！！
        return contents
        
    def setFileTitle(self, title):
        if title is not None:
            self.file =  open(title+'.txt', 'w+')
        else:
            self.file = open(self.defaultTitle + '.txt', 'w+')
            
    def writeData(self, contents):
        for item in contents:
            # 写入的时候不能用Unicode!!!
            floorLine = '\n-------------第'+ str(self.floor)+ '楼-------------'
            self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1
        self.file.flush()# 把数据从缓存写进文档
            
    def start(self):
        page = self.getPage(1)#先获取第一页
        pageNum = self.getPageNum(page)
        pageTitle = self.getTitle(page)
        self.setFileTitle(pageTitle)   
        if pageNum == None:
            print u'URL已经阵亡'
            return
        try:
            #这里的pageNum必须要转成int啊，不然Unicode不行啊！！
            print '总共有%d页' %(int(pageNum))
            for i in range(1, int(pageNum)+1):
                pageI = self.getPage(i)
                pageIContents = self.getContent(pageI)
                print '正在写入第%d页数据----' %(i)
                self.writeData(pageIContents)
        except IOError, e:
            print '写入异常'+e.message
        finally:
            print '写入任务完成'
            

if  __name__ == '__main__':      
    print u'请输入帖子代号' #3138733512
    baseURL = 'http://tieba.baidu.com/p/'\
               +str(raw_input('http://tieba.baidu.com/p/'))
    seeLZ = raw_input(u'是否只看楼主发的帖子，是请输入1，否请输入0\n')    
    bdtb = BDTB(baseURL, seeLZ)
    bdtb.start()    
    
#    page1 = bdtb.getPage(1)
#    title = bdtb.getTitle(page1)
#    print title
#    num = bdtb.getPageNum(page1)
#    print num
#    contents = bdtb.getContent(page1)
#    bdtb.setFileTitle(title)
#    bdtb.writeData(contents)
    


