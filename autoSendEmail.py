# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email import encoders
from email.header import Header
import smtplib, time

class autoSendEmail:
    def __init__(self):
        self.smtp_server = "smtp.qq.com"  # 使用qq转发需要用到，可以在QQ邮箱设置中查看并开通此转发功能
        self.smtp_port = 465  # smtp默认的端口是25
        # self.recever = ["985575418@qq.com"]  #接受者可以是多个，放在列表中
        self.recever = ["*********@qq.com"]
        self.sender = "*********@qq.com"
        self.password = "****************"  # 该密码是配置qq邮箱的SMTP功能的授权码
        self.msg = "Coco, good day!"  # 默认文本信息

    # 格式化邮件地址
    def _format_addr(self, s):
        name, address = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), address))

    # 读取当天要发送的文件构造需要发送的信息
    def getMsgFromFile(self):
        fileName = time.strftime("%Y%m%d%H", time.localtime(time.time()))
        with open(fileName + '.txt', 'r') as f:
            self.msg += f.read()

    def createMIMEText(self):
        mimeText = MIMEText(self.msg, 'plain', 'utf-8')
        mimeText['From'] = self._format_addr(u'Alan <%s>' % self.sender)
        mimeText['To'] = self._format_addr(u'Coco <%s>' % self.recever[0])
        mimeText['Subject'] = Header(u'每天都想逗你笑', 'utf-8').encode()
        return  mimeText

    def sendEmail(self, mimeText):
        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.set_debuglevel(1) # 打印出和SMTP服务器交互的信息
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.recever, mimeText.as_string())
        print 'send email successfully!'
        server.quit()


if __name__ == '__main__':
    import qiushibaike
    # 先爬取糗事百科5页的段子,取前十个保存
    npage = 5
    topN = 10
    qiushibaike.run(npage, topN)
    autoEmail = autoSendEmail()
    autoEmail.msg += '''\n这是一个从糗事百科自动百科自动爬取的精选段子
                        每天从%d条段子中选择点赞最多的%d条呈现在你眼前
                        希望你开心，快乐
                                       Alan
                                       %s\n\n''' % (npage*20, topN, time.strftime("%Y%m%d%H%M", time.localtime(time.time())))
    autoEmail.getMsgFromFile()
    mimeText = autoEmail.createMIMEText()
    autoEmail.sendEmail(mimeText)









