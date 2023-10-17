from machine import PWM, Pin, Timer
import lcd
import time


global mode

# time in seconds that we differ from system time
global delta_seconds

if __name__=='__main__':
    
    delta_seconds = 0
    
    
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
    

    mode = 1
    def mode_highlight(mode):
        pos = 0
        if mode == 1:
            pos = 0
        elif mode == 2:
            pos = 20
        elif mode == 3:
            pos = 40
        elif mode == 4:
            pos = 60
        elif mode == 5:
            pos = 80
        elif mode == 6:
            pos = 100
        #bg
        LCD.fill_rect(0,0,160,128,LCD.BLACK)
        #hightlight
        LCD.fill_rect(0,pos,160,20,LCD.RED)
        
    def limit_time(time,limit):
        if limit == 60 or 24:
            limit = limit-1
            
            if time < 0:
                time = limit
            if time > limit:
                time = 0
        else:
            print("wrong time typed at limit_time")
        return time
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
            print("btn 01")
            if mode < 6:
                mode += 1
                mode_highlight(mode)
                #print("mode: "+ str(mode))
            
        elif (btn_01.value() == False) and btn_01_prev_state == True:
            btn_01_prev_state = False

        elif (btn_02.value() == True) and btn_02_prev_state == False:
            btn_02_prev_state = True
            print("btn 02")
            if mode > 1:
                mode -= 1
                mode_highlight(mode)
               
                #print("mode: "+ str(mode))
        elif (btn_02.value() == False) and btn_02_prev_state == True:
            btn_02_prev_state = False
        
        # hour switch
        elif (btn_03.value() == True) and btn_03_prev_state == False:
            btn_03_prev_state = True
            print("btn 03")
            if mode == 1:
                momentary_hour += 1
                momentary_hour=limit_time(momentary_hour,24)
                LCD.fill_rect(0,0,160,20,LCD.RED)
                delta_seconds = delta_seconds + (60 * 60) # 1 hour
            elif mode == 2:
                open_hour += 1
                open_hour=limit_time(open_hour,24)
                LCD.fill_rect(0,20,160,20,LCD.RED)
            elif mode == 3:
                close_hour += 1
                close_hour=limit_time(close_hour,24)
                LCD.fill_rect(0,40,160,20,LCD.RED)

        elif (btn_03.value() == False) and btn_03_prev_state == True:
            btn_03_prev_state = False

        elif (btn_04.value() == True) and btn_04_prev_state == False:
            btn_04_prev_state = True
            print("btn 04")
            if mode == 1:
                momentary_hour -= 1
                momentary_hour=limit_time(momentary_hour,24)
                LCD.fill_rect(0,0,160,20,LCD.RED)
                delta_seconds = delta_seconds - (60 * 60) # 1 hour
            elif mode == 2:
                open_hour -= 1
                open_hour=limit_time(open_hour,24)
                LCD.fill_rect(0,20,160,20,LCD.RED)
            elif mode == 3:
                close_hour -= 1
                limit_time(close_hour,24)
                LCD.fill_rect(0,40,160,20,LCD.RED)
                    
        elif (btn_04.value() == False) and btn_04_prev_state == True:
            btn_04_prev_state = False

        elif (btn_05.value() == True) and btn_05_prev_state == False:
            btn_05_prev_state = True
            print("btn 05")
            if mode == 1:
                momentary_min += 1
                momentary_min = limit_time(momentary_min,60)
                LCD.fill_rect(0,0,160,20,LCD.RED)
                delta_seconds = delta_seconds + 60 # 1 minute
                
            elif mode == 2:
                open_min += 1
                open_min = limit_time(open_min,60)
                LCD.fill_rect(0,20,160,20,LCD.RED)
                
            elif mode == 3:
                close_min += 1
                close_min = limit_time(close_min,60)
                LCD.fill_rect(0,40,160,20,LCD.RED)
                
        elif (btn_05.value() == False) and btn_05_prev_state == True:
            btn_05_prev_state = False

        elif (btn_06.value() == True) and btn_06_prev_state == False:
            btn_06_prev_state = True
            print("btn 06")
            if mode == 1:
                momentary_min -= 1
                if momentary_min < 0:
                    momentary_min = 59
                if momentary_min > 59:
                    momentary_min = 0
                LCD.fill_rect(0,0,160,20,LCD.RED)
                delta_seconds = delta_seconds - 60 # 1 minute
            elif mode == 2:
                open_min -= 1
                open_min = limit_time(open_min,60)

                LCD.fill_rect(0,20,160,20,LCD.RED)
            elif mode == 3:
                close_min -= 1
                close_min = limit_time(close_min,60)
                LCD.fill_rect(0,40,160,20,LCD.RED)
                
        elif (btn_06.value() == False) and btn_06_prev_state == True:
            btn_06_prev_state = False
    
    def get_current_time_with_delta():
        current_time = time.time()
        
        (year, month, mday, hour, minute, second, *rest) = time.localtime(current_time + delta_seconds)
        
        return (hour, minute, second)
        
        
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
    
    
    
    while True:
        
        btn_handler()
        
        if mode == 1:
            LCD.fill_rect(0,0,160,20,LCD.RED)
            
            

        
        if mode == 5: #automatic
            (hour, minute, second) = get_current_time_with_delta()
            
            LCD.fill_rect(0,0,160,20,LCD.RED)
            LCD.text("Time:",2,6,LCD.WHITE)
            
            LCD.fill_rect(0,80,160,20,LCD.RED)
            LCD.text("Automatic",2,86,LCD.WHITE)
            LCD.text("{0:0=2d}".format(hour)+":"+"{0:0=2d}".format(minute)+":"+"{0:0=2d}".format(second),60,6,LCD.WHITE)
            
#             momentary_sec += 1
#             time.sleep(1)
#             if  momentary_sec == 60:
#                 momentary_sec = 0
#                 momentary_min += 1
#                 if momentary_min == 60:
#                     momentary_min = 0
#                     momentary_hour +=1
#                     if momentary_hour == 24:
#                         momentary_hour = 0
            if (momentary_hour == open_hour) and (momentary_min == open_min):
                LCD.fill_rect(0,100,160,20,LCD.BLUE)
                LCD.text("Status: Opens door",2,106,LCD.WHITE)
                
        display_text()
        LCD.show()
