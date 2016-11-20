# -*-coding:utf-8-*-
import urllib2
import cookielib
import urllib

# 爬取研究生阶段的成绩
# 这个小爬虫主要学习了对于cookie的理解和使用
# cookie就是网站为了识别用户身份，进行session跟踪而存储在用户本地的数据（通常经过加密）
class getMyMasterGrade():
    def __init__(self):
        self.cookieFile = 'cookie.txt'
        self.loginUrl = "https://cas.scut.edu.cn/amserver/UI/Login"  # 登录界面的网址
        self.gradeUrl = "http://yjsjy.1yd3.cas.scut.edu.cn/ssfw/pygl/cjgl/cjcx.do"  # 成绩所在页面的网址
        self.username = "201520131506"
        self.password = "××××××"
        self.cookie = cookielib.MozillaCookieJar(self.cookieFile)  # 声明一个CookieJar实例来保存cookie
        # 构造一个cookie处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        # 通过handler来构建opener
        self.opener = urllib2.build_opener(self.cookieHandler)

    # 模拟登录，获得cookie，并返回登录界面的代码
    def login(self):
        # 通过浏览器审查获得需要的参数，通过POST方式进行提交
        postData = urllib.urlencode({"IDToken1": self.username, "IDToken2": self.password})
        request = urllib2.Request(url=self.loginUrl, data=postData)
        response = self.opener.open(request)
        content = response.read().decode('utf-8')
        return content

    # 根据cookie获取成绩页面
    def getGradePage(self):
        content = self.opener.open(self.gradeUrl)
        return content.read().decode('utf-8')

    # 打印cookie
    def printCookie(self):
        for item in self.cookie:
            print 'Name:'+item.name
            print 'value:'+item.value

if __name__ == '__main__':
    test = getMyMasterGrade()
    loginPage = test.login()
    gradePage = test.getGradePage()
    print gradePage