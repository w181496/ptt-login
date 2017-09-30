#!/usr/bin/env python
#coding=utf-8

import telnetlib
import sys
import time
import codecs

host = 'ptt.cc'
delay = 1.5
log = codecs.open('log.txt', 'w', 'utf-8')

def login(host, user ,password) :
    global telnet
    telnet = telnetlib.Telnet(host)
    time.sleep(delay - 0.9)
    content = telnet.read_very_eager().decode('big5','ignore')
    if u"系統過載" in content :
        output(u"[ERROR] 系統超載，晚點再來~", "red")
        sys.exit(0)
        

    if u"請輸入代號" in content:
        output(u"輸入帳號中...", "gray")
        telnet.write(user + "\r\n" )
        time.sleep(delay - 0.9)
        output(u"輸入密碼中...", "gray")
        telnet.write(password + "\r\n")
        time.sleep(delay - 0.2)
        content = telnet.read_very_eager().decode('big5','ignore')
        if u"密碼不對" in content:
           output(u"[ERROR] 密碼錯誤或帳號不存在!", "red")
           sys.exit()
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您想刪除其他重複登入" in content:
           output(u"刪除重複登入的連線...", "blue")
           telnet.write("y\r\n")
           time.sleep(10)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"請按任意鍵繼續" in content:
           telnet.write("\r\n" )
           time.sleep(delay - 0.2)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您要刪除以上錯誤嘗試" in content:
           output(u"刪除以上錯誤嘗試...", "blue")
           telnet.write("y\r\n")
           time.sleep(5)
           content = telnet.read_very_eager().decode('big5','ignore')
        output(u"登入成功!", "green")
        
        telnet.write("T\r\nQ\r\n" + user + "\r\n")
        time.sleep(delay)
        content = telnet.read_very_eager().decode('big5','ignore')
        idx = content.find(u'登入次數')
        idx2 = content.find(u' 次')
        output(content[idx-1:idx2+2], "yellow")   # 登入次數
        log.write(user + " " + password + " " + content[idx - 1 : idx2 + 2] + "\r\n")
        
    else:
        output(u"[ERROR] 伺服器沒有回應", "red")

def disconnect() :
     output(u"登出中...", "gray")
     telnet.write("qqqqqqqqqg\r\ny\r\n" )
     time.sleep(delay - 0.2)
     #content = telnet.read_very_eager().decode('big5','ignore')
     output(u"登出成功!", "green")
     telnet.close()

def setdelay() :
    str = u'Input delay: '
#output('test','green')
    delay = input(str.encode('big5'))  # Windows

def output(msg, color='Normal') :
    if color == 'Normal' :
        print '\033[0;37;40m%s' % msg
    if color == 'red' :
        print '\033[1;31;40m%s\033[0m' % msg
    if color == 'green' :
        print '\033[1;32;40m%s\033[0m' % msg
    if color == 'blue' :
        print '\033[1;34;40m%s\033[0m' % msg
    if color == 'yellow' :
        print '\033[1;33;40m%s\033[0m' % msg
    if color == 'gray' :
        print '\033[1;30;40m%s\033[0m' % msg
    
def main():
    setdelay()
    file = open('acc.txt', 'r')
    while True:
        line = file.readline().split()
        if not line: break
        output(line[0])
        user = line[0]
        password = line[1]
        login(host, user, password)
        disconnect()
    file.close()
    log.close()
if __name__=="__main__" :
   main()
