from machine import PWM, Pin, Timer
import lcd
import time


global mode

# time in seconds that we differ from system time
global delta_seconds

if __name__=='__main__':
    
    delta_seconds = 0
    
    pwm = PWM(Pin(lcd.BL))
    pwm.freq(1000)
    pwm.duty_u16(65535)#max 65535
    
    LCD = lcd.LCD_1inch8()
    LCD.show()

    
    btn_01 = Pin(00, Pin.IN, Pin.PULL_DOWN)
    btn_01_prev_state = btn_01.value()
    btn_02 = Pin(01, Pin.IN, Pin.PULL_DOWN)
    btn_02_prev_state = btn_02.value()

    btn_03 = Pin(02, Pin.IN, Pin.PULL_DOWN)
    btn_03_prev_state = btn_03.value()
    btn_04 = Pin(03, Pin.IN, Pin.PULL_DOWN)
    btn_04_prev_state = btn_04.value()
    
    btn_05 = Pin(04, Pin.IN, Pin.PULL_DOWN)
    btn_05_prev_state = btn_05.value()
    btn_06 = Pin(05, Pin.IN, Pin.PULL_DOWN)
    btn_06_prev_state = btn_06.value()
    
    
    momentary_hour = 0
    momentary_min = 0
    momentary_sec = 0
    
    open_hour = 6
    open_min = 30
    
    close_hour = 20
    close_min = 0
    

    mode = 0

    standby_timer = Timer(-1)
    
    def go_on_standby(timer):
        print("standby")
        for fade in range(65535, 0, -1):
            pwm.duty_u16(fade)#max 65535

    def menu(mode):
        def display_text():

            (hour, minute, second) = get_current_time_with_delta()
            LCD.text("Time:",2,6,LCD.WHITE)
            LCD.text("{0:0=2d}".format(hour)+":"+"{0:0=2d}".format(minute)+":"+"{0:0=2d}".format(second),60,6,LCD.WHITE)
        
            LCD.text("Open:",2,26,LCD.WHITE)
            LCD.text("{0:0=2d}".format(open_hour)+":"+"{0:0=2d}".format(open_min),60,26,LCD.WHITE)

            LCD.text("Close:",2,46,LCD.WHITE)
            LCD.text("{0:0=2d}".format(close_hour)+":"+"{0:0=2d}".format(close_min),60,46,LCD.WHITE)

            LCD.text("Manual",2,66,LCD.WHITE)
        
            LCD.text("Automatic",2,86,LCD.WHITE)

            

        #bg
        LCD.fill_rect(0,0,160,128,LCD.BLACK)     
        #hightlight
        pos = mode * 20
        LCD.fill_rect(0,pos,160,20,LCD.RED)
  
        display_text()
    
    def btn_handler():
        global mode
        global btn_01_prev_state
        global btn_02_prev_state
        global btn_03_prev_state
        global btn_04_prev_state
        global btn_05_prev_state
        global btn_06_prev_state
        
        global momentary_hour
        global momentary_min
        
        global open_hour
        global open_min
        
        global close_hour
        global close_min
        
        global delta_seconds

        
        # mode switch
        if (btn_01.value() == True) and btn_01_prev_state == False:
            btn_01_prev_state = True
            pwm.duty_u16(65535)#max 65535
            mode = mode + 1
            mode = mode % 5
            menu(mode)
            print("mode= ",mode)
            
        elif (btn_01.value() == False) and btn_01_prev_state == True:
            btn_01_prev_state = False
            standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=go_on_standby)

        elif (btn_02.value() == True) and btn_02_prev_state == False:
            btn_02_prev_state = True
            pwm.duty_u16(65535)#max 65535
            mode = mode - 1
            mode = mode % 5
            menu(mode)
            print("mode= ",mode)

        elif (btn_02.value() == False) and btn_02_prev_state == True:
            btn_02_prev_state = False
        
            standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=go_on_standby)
        # hour switch
        elif (btn_03.value() == True) and btn_03_prev_state == False:
            btn_03_prev_state = True
            pwm.duty_u16(65535)#max 65535
            if mode == 0:
                momentary_hour = momentary_hour + 1
                momentary_hour = momentary_hour & 24
                delta_seconds = delta_seconds + (60 * 60) # 1 hour
            elif mode == 1:
                open_hour = open_hour + 1
                open_hour = open_hour % 24
            elif mode == 2:
                close_hour = close_hour + 1
                close_hour = close_hour % 24
            

        elif (btn_03.value() == False) and btn_03_prev_state == True:
            btn_03_prev_state = False
            standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=go_on_standby)

        elif (btn_04.value() == True) and btn_04_prev_state == False:
            btn_04_prev_state = True
            pwm.duty_u16(65535)#max 65535
            if mode == 0:
                momentary_hour = momentary_hour - 1
                momentary_hour = momentary_hour & 24
                delta_seconds = delta_seconds - (60 * 60) # 1 hour
            elif mode == 1:
                open_hour = open_hour - 1
                open_hour = open_hour % 24
            elif mode == 2:
                close_hour = close_hour -1
                close_hour = close_hour % 24
                    
        elif (btn_04.value() == False) and btn_04_prev_state == True:
            btn_04_prev_state = False
            standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=go_on_standby)

        elif (btn_05.value() == True) and btn_05_prev_state == False:
            btn_05_prev_state = True
            pwm.duty_u16(65535)#max 65535
            if mode == 0:
                momentary_min = momentary_min +1
                momentary_min = momentary_min % 60
                delta_seconds = delta_seconds + 60 # 1 minute
                
            elif mode == 1:
                open_min = open_min + 1
                open_min = open_min % 60
                
            elif mode == 2:
                close_min = close_min + 1
                close_min = close_min % 60
                
        elif (btn_05.value() == False) and btn_05_prev_state == True:
            btn_05_prev_state = False
            standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=go_on_standby)

        elif (btn_06.value() == True) and btn_06_prev_state == False:
            btn_06_prev_state = True
            pwm.duty_u16(65535)#max 65535
            if mode == 0:
                momentary_min = momentary_min - 1
                momentary_min = momentary_min % 60

                delta_seconds = delta_seconds - 60 # 1 minute
            elif mode == 1:
                open_min = open_min - 1
                open_min = open_min % 60

            elif mode == 2:
                close_min = close_min -1
                close_mion = close_min % 60
                
        elif (btn_06.value() == False) and btn_06_prev_state == True:
            btn_06_prev_state = False
    
            standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=go_on_standby)
    def get_current_time_with_delta():
        current_time = time.time()
        
        (year, month, mday, hour, minute, second, *rest) = time.localtime(current_time + delta_seconds)
        
        return (hour, minute, second)
        
        

    
    
    
    while True:
        
        btn_handler()
        
        if mode == 4:
            # automatic
            # compare the time
            if (momentary_hour == open_hour) and (momentary_min == open_min):
                print("Opens door")
            if (momentary_hour == close_hour) and (momentary_min == close_min):
                print("Closes the door")
        

        menu(mode)
        LCD.show()
