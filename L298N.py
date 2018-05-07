#!/usr/bin/env python
# coding: 
# Autor:	kevin
# Date:		20160331
# Version:	1.0
#Thanks for origin Autor's Ingmar Stape 

# This module is designed to control two motors with a L298N H-Bridge

# Use this module by creating an instance of the class. To do so call the Init function, then command as desired, e.g.
# import L298NHBridge
# HBridge = L298NHBridge.L298NHBridge()
# HBridge.Init()
#编码：latin-1

#作者：凯文
#日期：20160331
#版本：1.0
#感谢源于作者的Ingmar Stape

#该模块设计用于通过L298N H桥控制两台电机

#通过创建类的实例来使用此模块。为此，请调用Init函数，然后根据需要执行命令，例如
#导入L298NHBridge
# H桥= L298NHBridge.L298NHBridge（）
# HBridge.Init（）




# Import the libraries the class needs
import RPi.GPIO as io
import time

class HBridge(object):

    def __init__(self, left_pin1, left_pin2, right_pin1, right_pin2, leftpwm_pin, rightpwm_pin):
        io.setmode(io.BCM)
        # Constant values
        # 常量值
        self.PWM_MAX = 100
        # Here we configure the GPIO settings for the left and right motors spinning direction. 
        # It defines the four GPIO pins used as input on the L298 H-Bridge to set the motor mode (forward, reverse and stopp).
        #这里我们配置左右电机旋转方向的GPIO设置。
        #它定义了L298 H桥上用作输入的四个GPIO引脚来设置电机模式（正向，反向和停止）。
        self.leftmotor_in1_pin = left_pin1
        self.leftmotor_in2_pin = left_pin2
        self.rightmotor_in1_pin = right_pin1
        self.rightmotor_in2_pin = right_pin2
        self.leftmotorpwm_pin = leftpwm_pin
        self.rightmotorpwm_pin = rightpwm_pin
        self.SetupGPIO()
        self.leftmotorpwm = io.PWM(self.leftmotorpwm_pin,100)
        self.rightmotorpwm = io.PWM(self.rightmotorpwm_pin,100)
        self.InitPWM()
        # Disable warning from GPIO
        #禁用GPIO的警告
        io.setwarnings(False)

    def SetupGPIO(self):
        io.setup(self.rightmotor_in1_pin, io.OUT)
        io.setup(self.rightmotor_in2_pin, io.OUT)
        io.setup(self.leftmotor_in1_pin, io.OUT)
        io.setup(self.leftmotor_in2_pin, io.OUT)
        io.setup(self.leftmotorpwm_pin, io.OUT)
        io.setup(self.rightmotorpwm_pin, io.OUT)

    def InitPWM(self): 
        # Here we configure the GPIO settings for the left and right motors spinning speed. 
        # It defines the two GPIO pins used as input on the L298 H-Bridge to set the motor speed with a PWM signal.
        #这里我们配置左右电机转速的GPIO设置。
        #它定义在L298 H桥上用作输入的两个GPIO引脚，用PWM信号设置电机速度。
        self.leftmotorpwm.start(0)
        self.leftmotorpwm.ChangeDutyCycle(0)
        self.rightmotorpwm.start(0)
        self.rightmotorpwm.ChangeDutyCycle(0)
    
    def resetMotorGPIO(self):
        io.output(self.leftmotor_in1_pin, False)
        io.output(self.leftmotor_in2_pin, False)
        io.output(self.rightmotor_in1_pin, False)
        io.output(self.rightmotor_in2_pin, False)

# setMotorMode()

# Sets the mode for the L298 H-Bridge which motor is in which mode.

# This is a short explanation for a better understanding:
# motor		-> which motor is selected left motor or right motor
# mode		-> mode explains what action should be performed by the H-Bridge

# setMotorMode(leftmotor, reverse)	-> The left motor is called by a function and set into reverse mode
# setMotorMode(rightmotor, stopp)	-> The right motor is called by a function and set into stopp mode
# setMotorMode（）

#设置电机处于哪种模式下的L298 H桥的模式。

#这是对更好理解的简短解释：
#电机 - >哪个电机选择了左电机或右电机
#模式- >模式说明了什么样的行动应该由H桥进行

# setMotorMode（leftmotor，反向） - >左马达由函数调用并设置成反向模式
# setMotorMode（rightmotor，STOPP） - >右马达由函数调用并设置成STOPP模式
    def setMotorMode(self, motor, mode):

	if motor == "leftmotor":
	    if mode == "reverse":
		io.output(self.leftmotor_in1_pin, True)
		io.output(self.leftmotor_in2_pin, False)
	    elif  mode == "forward":
		io.output(self.leftmotor_in1_pin, False)
		io.output(self.leftmotor_in2_pin, True)
	    else:
		io.output(self.leftmotor_in1_pin, False)
		io.output(self.leftmotor_in2_pin, False)
			
	elif motor == "rightmotor":
	    if mode == "reverse":
		io.output(self.rightmotor_in1_pin, False)
		io.output(self.rightmotor_in2_pin, True)		
	    elif  mode == "forward":
		io.output(self.rightmotor_in1_pin, True)
		io.output(self.rightmotor_in2_pin, False)		
	    else:
		io.output(self.rightmotor_in1_pin, False)
		io.output(self.rightmotor_in2_pin, False)
	else:
            self.resetMotorGPIO()

# SetMotorLeft(power)

# Sets the drive level for the left motor, from +1 (max) to -1 (min).

# This is a short explanation for a better understanding:
# SetMotorLeft(0)     -> left motor is stopped
# SetMotorLeft(0.75)  -> left motor moving forward at 75% power
# SetMotorLeft(-0.5)  -> left motor moving reverse at 50% power
# SetMotorLeft(1)     -> left motor moving forward at 100% power
# SetMotorLeft（功率）

#设置左侧电机的驱动级别，从+1（最大）到-1（最小）。

#这是对更好理解的简短解释：
# SetMotorLeft（0） - >左马达停止
# SetMotorLeft（0.75） - >左马达在75％的功率向前移动
# SetMotorLeft（-0.5） - >左马达移动反向，在50％的功率
# SetMotorLeft（1） - >左马达向前移动以100％功率
    def setMotorLeft(self, power):
	if power < 0:
	    # Reverse mode for the left motor
	    self.setMotorMode("leftmotor", "reverse")
	    pwm = -int(self.PWM_MAX * power)
	    if pwm > self.PWM_MAX:
		pwm = self.PWM_MAX
	elif power > 0:
	    # Forward mode for the left motor
	    self.setMotorMode("leftmotor", "forward")
	    pwm = int(self.PWM_MAX * power)
	    if pwm > self.PWM_MAX:
		pwm = self.PWM_MAX
	else:
	    # Stopp mode for the left motor
            #左电机的Stopp模式
	    self.setMotorMode("leftmotor", "stopp")
	    pwm = 0
#	print "SetMotorLeft", pwm
# 	打印“SetMotorLeft”，pwm
	self.leftmotorpwm.ChangeDutyCycle(pwm)

# SetMotorRight(power)

# Sets the drive level for the right motor, from +1 (max) to -1 (min).

# This is a short explanation for a better understanding:
# SetMotorRight(0)     -> right motor is stopped
# SetMotorRight(0.75)  -> right motor moving forward at 75% power
# SetMotorRight(-0.5)  -> right motor moving reverse at 50% power
# SetMotorRight(1)     -> right motor moving forward at 100% power
# SetMotorRight（功率）

#设置右电机的驱动级别，从+1（最大）到-1（最小）。

#这是对更好理解的简短解释：
# SetMotorRight（0） - >右马达停止
# SetMotorRight（0.75） - >右马达在75％的功率向前移动
# SetMotorRight（-0.5） - >右马达移动反向，在50％的功率
# SetMotorRight（1） - >右马达正向以100％功率移动


    def setMotorRight(self, power):
	if power < 0:
	    # Reverse mode for the right motor
	    #右侧电机的反向模式
	    self.setMotorMode("rightmotor", "reverse")
	    pwm = -int(self.PWM_MAX * power)
	    if pwm > self.PWM_MAX:
		pwm = self.PWM_MAX
	elif power > 0:
	    # Forward mode for the right motor
	     #右侧电机的正转模式
	    self.setMotorMode("rightmotor", "forward")
	    pwm = int(self.PWM_MAX * power)
	    if pwm > self.PWM_MAX:
	        pwm = self.PWM_MAX
	else:
	    # Stopp mode for the right motor
	    #右电机的Stopp模式
	    self.setMotorMode("rightmotor", "stopp")
	    pwm = 0
        #print "SetMotorRight", pwm
	    #打印“SetMotorRight”，pwm
	self.rightmotorpwm.ChangeDutyCycle(pwm)

# Program will clean up all GPIO settings and terminates
#程序将清除所有GPIO设置并终止
    def exit(self):
        self.resetMotorGPIO()
	io.cleanup()
