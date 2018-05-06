# -*- coding:utf-8 -*-
import smbus
import time
 
address = 0x48 #设备地址 从40开始 基础设备占前三
A0 = 0x40 #光照传感器
A4 = 0X44 #设备4
A5 = 0x45 #设备5
 
acc = smbus.SMBus(1)
bcc = smbus.SMBus(1)

while True:
    acc.write_byte(address,A4)
    sun = acc.read_byte(address)
    bcc.write_byte(address,A5)
    mun = bcc.read_byte(address)
    #print (sun,mun) # sun 上 mun 下
    if sun < 189:
        print('下 ')
    else:
        if sun > 200:
            print('上')
    if mun < 170:
        print('左')
    else:
        if mun > 200:
            print('右')
    time.sleep(0.1)
