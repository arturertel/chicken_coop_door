from machine import PWM, Pin, Timer
import lcd
import time

global mode_switch
# time in seconds that we differ from system time
global delta_seconds
global lcd_awake
if __name__ == '__main__':
    delta_seconds = 0

    pwm = PWM(Pin(lcd.BL))
    pwm.freq(1000)
    pwm.duty_u16(65535)  # max 65535

    LCD = lcd.LCD_1inch8()
    LCD.show()

    momentary_hour = 0
    momentary_min = 0
    momentary_sec = 0

    open_hour = 6
    open_min = 30

    close_hour = 20
    close_min = 0

    mode_switch = 3

    standby_timer = Timer(-1)


    class Btn:
        def __init__(self, pin):
            self.pin = pin
            self.btn_prev_state = False
            self.btn = Pin(self.pin, Pin.IN, Pin.PULL_DOWN)
            self.value = self.btn.value
            global lcd_awake
            lcd_awake = True

        def activate(self, other):
            global lcd_awake
            self.value = self.btn.value()

            if self.btn.value() == True and self.btn_prev_state == False:
                self.btn_prev_state = True
                if not lcd_awake:
                    lcd_awake = True
                    lcd_wake_up()

                    pass
                else:
                    # call function
                    other()
            elif (self.btn.value() == False) and self.btn_prev_state == True:
                self.btn_prev_state = False
                standby_timer.init(mode=Timer.ONE_SHOT, period=10000, callback=lcd_fall_asleep)


    class DisplayMode:
        def __init__(self, title, position):
            self.title = title
            self.position = position
            self.text_pos = self.position * 20

        def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
            LCD.fill_rect(0, self.text_pos, 160, 20, bg_color)
            LCD.text(self.title, 2, self.text_pos + 6, text_color)

        def update(self):

            # highlight active mode
            if self.position == mode_switch:
                self.show_text(LCD.WHITE)
            else:
                self.show_text()


    class TimeDisplaymode(DisplayMode):
        def __init__(self, title, position):
            super().__init__(title, position)

        def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
            LCD.fill_rect(0, self.text_pos, 160, 20, bg_color)
            LCD.text(self.title, 2, self.text_pos + 6, text_color)
            self.hour, self.minute, self.second = get_current_time_with_delta()

            LCD.text(
                "{0:0=2d}".format(self.hour) + ":" + "{0:0=2d}".format(self.minute) + ":" + "{0:0=2d}".format(
                    self.second),
                70, self.text_pos + 6, text_color)


    class OpenDisplaymode(DisplayMode):
        def __init__(self, title, position):
            super().__init__(title, position)

        def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
            LCD.fill_rect(0, self.text_pos, 160, 20, bg_color)
            LCD.text(self.title, 2, self.text_pos + 6, text_color)
            LCD.text("{0:0=2d}".format(open_hour) + ":" + "{0:0=2d}".format(open_min), 70, self.text_pos + 6,
                     text_color)


    class CloseDisplaymode(DisplayMode):
        def __init__(self, title, position):
            super().__init__(title, position)

        def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
            LCD.fill_rect(0, self.text_pos, 160, 20, bg_color)
            LCD.text(self.title, 2, self.text_pos + 6, text_color)
            LCD.text("{0:0=2d}".format(close_hour) + ":" + "{0:0=2d}".format(close_min), 70, self.text_pos + 6,
                     text_color)


    # lcd standby functions
    def lcd_fall_asleep(time):
        global lcd_awake
        lcd_awake = False
        print("lcd goes to sleep")
        for fade in range(65535, 0, -1):
            pwm.duty_u16(fade)  # max 65535


    def lcd_wake_up():
        print("lcd is awake")
        pwm.duty_u16(65535)  # max 65535


    # button functions
    def plus_mode():
        global mode_switch
        mode_switch = mode_switch + 1
        mode_switch = mode_switch % 5
        return mode_switch


    def minus_mode():
        global mode_switch
        mode_switch = mode_switch - 1
        mode_switch = mode_switch % 5
        print("mode= ", mode_switch)
        return mode_switch


    def plus_hour():
        global momentary_hour
        global open_hour
        global close_hour
        global delta_seconds

        if mode_switch == 0:
            momentary_hour = momentary_hour + 1
            momentary_hour = momentary_hour & 24
            delta_seconds = delta_seconds + (60 * 60)  # 1 hour
        elif mode_switch == 1:
            open_hour = open_hour + 1
            open_hour = open_hour % 24
        elif mode_switch == 2:
            close_hour = close_hour + 1
            close_hour = close_hour % 24


    def minus_hour():
        global momentary_hour
        global open_hour
        global close_hour
        global delta_seconds

        if mode_switch == 0:
            momentary_hour = momentary_hour - 1
            momentary_hour = momentary_hour & 24
            delta_seconds = delta_seconds - (60 * 60)  # 1 hour
        elif mode_switch == 1:
            open_hour = open_hour - 1
            open_hour = open_hour % 24
        elif mode_switch == 2:
            close_hour = close_hour - 1
            close_hour = close_hour % 24


    def plus_min():
        global momentary_min
        global open_min
        global close_min
        global delta_seconds
        if mode_switch == 0:
            momentary_min = momentary_min + 1
            momentary_min = momentary_min % 60
            delta_seconds = delta_seconds + 60  # 1 minute

        elif mode_switch == 1:
            open_min = open_min + 1
            open_min = open_min % 60

        elif mode_switch == 2:
            close_min = close_min + 1
            close_min = close_min % 60


    def minus_min():
        global momentary_min
        global open_min
        global close_min
        global delta_seconds
        if mode_switch == 0:
            momentary_min = momentary_min - 1
            momentary_min = momentary_min % 60
            delta_seconds = delta_seconds + 60  # 1 minute

        elif mode_switch == 1:
            open_min = open_min - 1
            open_min = open_min % 60

        elif mode_switch == 2:
            close_min = close_min - 1
            close_min = close_min % 60


    def door_up():
        print("door_up_function")
        if limit_switch_open.value() == False:
            print("Door goes up")
            

    def door_down():
        print("door_down_function")
        if limit_switch_close.value() == False:
            print("Door goes down")


    # Create Buttons
    btn_01 = Btn(0)
    btn_02 = Btn(1)

    btn_03 = Btn(2)
    btn_04 = Btn(3)

    btn_05 = Btn(4)
    btn_06 = Btn(5)
    
    limit_switch_open = Btn(22)
    limit_switch_close= Btn(26)


    def get_current_time_with_delta():
        current_time = time.time()

        (year, month, mday, hour, minute, second, *rest) = time.localtime(current_time + delta_seconds)

        return hour, minute, second


    # create different modes
    time_mode = TimeDisplaymode(title="Time", position=0)
    open_mode = OpenDisplaymode(title="Open", position=1)
    close_mode = CloseDisplaymode(title="Close", position=2)
    manual_mode = DisplayMode(title="Manual", position=3)
    automatic_mode = DisplayMode(title="Automatic", position=4)

    while True:

        time_mode.update()
        open_mode.update()
        close_mode.update()
        manual_mode.update()
        automatic_mode.update()

        # change mode
        btn_01.activate(plus_mode)
        btn_02.activate(minus_mode)

        if mode_switch == 0:
            # change hour
            btn_03.activate(plus_hour)
            btn_04.activate(minus_hour)
            # change minute
            btn_05.activate(plus_min)
            btn_06.activate(minus_min)

        if mode_switch == 1:
            # change hour
            btn_03.activate(plus_hour)
            btn_04.activate(minus_hour)
            # change minute
            btn_05.activate(plus_min)
            btn_06.activate(minus_min)

        if mode_switch == 2:
            # change hour
            btn_03.activate(plus_hour)
            btn_04.activate(minus_hour)
            # change minute
            btn_05.activate(plus_min)
            btn_06.activate(minus_min)


        if mode_switch == 3:
            # manual
            # if the limit switch 01 is not active:
            btn_04.activate(door_up)
            btn_06.activate(door_up)
            # if the limit switch 02 is not active:
            btn_03.activate(door_down)
            btn_05.activate(door_down)

        if mode_switch == 4:
            # this function must be checked again
            # automatic
            # compare the time
            if momentary_hour == open_hour and momentary_min == open_min:
                btn_03.activate(door_up)
            if (momentary_hour == close_hour) and (momentary_min == close_min):
                btn_04.activate(door_down)

        LCD.show()
