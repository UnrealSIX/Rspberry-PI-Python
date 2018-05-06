#!\usr\bin\env python
#-*-coding: utf-8-*-
import socket
import time
import smtplib
import urllib
import json
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr

#检查网络连通性
def check_network():
    while True:
        try:
            result=urllib.urlopen('http://baidu.com').read()
            print result
            print "网络已联通!"
            break
        except Exception,e:
            print e
            print "网络未就位,5秒后重试"
            time.sleep(5)
    return True

def CPUtemp():
    file = open("/sys/class/thermal/thermal_zone0/temp")       
    temp = float(file.read()) / 1000        
    file.close()
    return ("  CPU温度 : %.2f" %temp)

#获取本级制定接口的ip地址
def get_ip_address():
    s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect(("1.1.1.1",80))
    ipaddr=s.getsockname()[0]
    s.close()
    
    response = urllib.urlopen('https://jsonip.com/')
    js = json.loads(response.read())
    IPS = '外网IP:'+ str(js['ip']) + '  内网IP:'+ str(ipaddr)
    return IPS

def sendEmail():
    ret=True
    ipaddr=get_ip_address()  + CPUtemp()
    try:
        msg=MIMEText(ipaddr,'plain','utf-8')
        msg['From']=formataddr(["用户名",'#自己邮箱#'])
        msg['To']=formataddr(["收件人",'#自己邮箱#'])
        msg['Subject']="树莓派IP"
        server=smtplib.SMTP_SSL("smtp.qq.com",465)
        server.login("#自己邮箱#","#自己秘钥#")#登录
        server.sendmail('#自己邮箱#',['#自己邮箱#',],msg.as_string())
        server.quit()
        print('邮件发送成功')
        ret=True
    except:
        ret=False
if  __name__ == '__main__' :
    check_network()
    sendEmail()
