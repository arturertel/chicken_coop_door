from machine import PWM, Pin, Timer
import lcd
import time

class Btn:
    def __init__(self, pin):
        self.pin = pin
        self.btn = Pin(self.pin, Pin.IN, Pin.PULL_DOWN)
        self.btn_prev_state = False
        self.value = self.btn.value

    def activate(self, other, parameter_1, parameter_2):
        if self.btn.value() == True and self.btn_prev_state == False:
            # button press
            self.btn_prev_state = True
            # call the other function, the brackets are for starting the function
            other(parameter_1, parameter_2)
            print("btn", self.pin)

        elif (self.btn.value() == False) and self.btn_prev_state == True:
            # button release
            self.btn_prev_state = False
            
            


        
