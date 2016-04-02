import RPi.GPIO as GPIO
import time

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

class LED(object):
    def __init__(self, pin1, pin2, pin3):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.outputValues = [False,False,False]
        self.state = 0
        self.setupPins()

    def setupPins(self):
        GPIO.setup(self.pin1,GPIO.OUT)
        GPIO.setup(self.pin2,GPIO.OUT)
        GPIO.setup(self.pin3,GPIO.OUT)

    def setOutputs(self, out1,out2,out3):
        self.outputValues = [out1,out2,out3]
        GPIO.output(self.pin1,out1)
        GPIO.output(self.pin2,out2)
        GPIO.output(self.pin3,out3)

    def getState(self):
        if(self.state==0):
            self.setOutputs(False,False,False)
        elif(self.state==1):
            self.setOutputs(True,False,False)
        elif(self.state==2):
            self.setOutputs(False,True,False)
        elif(self.state==3):
            self.setOutputs(False,False,True)
        elif(self.state==4):
            self.setOutputs(True,True,False)
        elif(self.state==5):
            self.setOutputs(True,False,True)
        elif(self.state==6):
            self.setOutputs(False,True,True)
        elif(self.state==7):
            self.setOutputs(True,True,True)

    def increment(self):
        self.state+=1
        if(self.state==8):
            self.state = 1
        self.getState()


class Button(object):
    def __init__(self, inputPin):
        self.inputPin = inputPin
        self.setupPin()

    def setupPin(self):
        GPIO.setup(self.inputPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getInput(self):
        return GPIO.input(self.inputPin)
