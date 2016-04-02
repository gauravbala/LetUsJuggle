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

    def setupPin(self):
        GPIO.setup(self.inputPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getInput(self):
        return GPIO.input(self.inputPin)

firstLed = LED(26,19,13)
secondLed = LED(6,5,22)
thirdLed = LED(27,17,4)
fourthLed = LED(24,23,18)
leds = [firstLed,secondLed,thirdLed,fourthLed]
for led in leds:
    led.setupPins()
firstButton = Button(21)
secondButton = Button(20)
thirdButton = Button(16)
fourthButton = Button(12)
ledButtons = [firstButton,secondButton,thirdButton,fourthButton]
for button in ledButtons:
    button.setupPin()
commitButton = Button(25)
commitButton.setupPin()

def returnStates():
    states = []
    for led in leds:
        if(led.state == 0):
            #one led is off
            return False
        states.append(led.state)
    return states

while(True):
    try:
        for button in ledButtons:
            if(button.getInput()==False):
                if(button == firstButton):
                    firstLed.increment()
                elif(button == secondButton):
                    secondLed.increment()
                elif(button == thirdButton):
                    thirdLed.increment()
                elif(button == fourthButton):
                    fourthLed.increment()
                time.sleep(0.2)

        for led in leds:
            led.getState()
            
        if(commitButton.getInput()==False):
            if(returnStates()!= False):
                for led in leds:
                    led.state=0
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        GPIO.cleanup()





