import uasyncio
from machine import Pin, PWM
import time
import lcd
from button_handler import Btn
from ds1302 import DS1302
from settings.save_settings import Settings
import global_state

ds = DS1302(Pin(18), Pin(17), Pin(16))
settings = Settings.load()

lcd_pwm = PWM(Pin(lcd.BL))  # Hintergrundlicht
lcd_pwm.freq(1000)
lcd_pwm.duty_u16(65535)

LCD = lcd.LCD_1inch8()
LCD.show()



# --- DisplayMode Klassen ---
class DisplayMode:
    _position = 0

    def __init__(self, title):
        self.position = DisplayMode._position
        DisplayMode._position += 1
        self.title = title
        self.text_pos = self.position * 20

    def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
        LCD.fill_rect(0, self.text_pos, 160, 20, bg_color)
        LCD.text(self.title, 2, self.text_pos + 6, text_color)

    def update(self):
        if self.position == global_state.mode_switch:
            self.show_text(LCD.WHITE)
        else:
            self.show_text()

class TimeDisplaymode(DisplayMode):
    def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
        super().show_text(text_color, bg_color)
        text = "{:02}:{:02}:{:02}".format(ds.hour(), ds.minute(), ds.second())
        LCD.text(text, 70, self.text_pos + 6, text_color)

class OpenDisplaymode(DisplayMode):
    def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
        # Wenn Zeiten gleich, Text in Rot anzeigen
        if settings.open == settings.close:
            bg_color = LCD.RED
            
        super().show_text(text_color, bg_color)
        text = "{:02}:{:02}".format(settings.open[0], settings.open[1])
        LCD.text(text, 70, self.text_pos + 6, text_color)

class CloseDisplaymode(DisplayMode):
    def show_text(self, text_color=LCD.BLUE, bg_color=LCD.BLACK):
        # Wenn Zeiten gleich, Text in Rot anzeigen
        if settings.open == settings.close:
            bg_color = LCD.RED
            
        super().show_text(text_color, bg_color)
        text = "{:02}:{:02}".format(settings.close[0], settings.close[1])
        LCD.text(text, 70, self.text_pos + 6, text_color)

# --- Modi erstellen ---
time_mode = TimeDisplaymode("Time")
open_mode = OpenDisplaymode("Open")
close_mode = CloseDisplaymode("Close")
manual_mode = DisplayMode("Manual")
automatic_mode = DisplayMode("Automatic")

# --- Buttons ---
btn00 = Btn(pin=0)
btn01 = Btn(pin=1)
btn02 = Btn(pin=2)
btn03 = Btn(pin=3)
btn04 = Btn(pin=4)
btn05 = Btn(pin=5)

# --- Hilfsfunktionen ---

def mode(choice, _=None):
    if choice == "-":
        global_state.mode_switch = (global_state.mode_switch - 1) % 5
    elif choice == "+":
        global_state.mode_switch = (global_state.mode_switch + 1) % 5
    
    # Automatic-Modus blockieren, wenn Öffnungs- und Schließzeit gleich sind
    if settings.open == settings.close and global_state.mode_switch == 4:
        print("Automatik deaktiviert – Öffnungs- und Schließzeit sind gleich!")
        global_state.mode_switch = 2  # zurück zu open_mode

    print("mode =", global_state.mode_switch)
    

def change_time_unit(unit, change):
    if global_state.mode_switch == 0:
        value = getattr(ds, unit)()
        value = (value + change) % (24 if unit == "hour" else 60)
        getattr(ds, unit)(value)
    elif global_state.mode_switch == 1:
        index = 0 if unit == "hour" else 1
        settings.open[index] = (settings.open[index] + change) % (24 if index == 0 else 60)
    elif global_state.mode_switch == 2:
        index = 0 if unit == "hour" else 1
        settings.close[index] = (settings.close[index] + change) % (24 if index == 0 else 60)
    settings.save()

# --- Menü-Loop ---
async  def menu_loop():
    while True:
        time_mode.update()
        open_mode.update()
        close_mode.update()
        manual_mode.update()
        automatic_mode.update()

        btn04.activate(mode, "+", "")
        btn05.activate(mode, "-", "")

        if global_state.mode_switch in (0, 1, 2):
            btn01.activate(change_time_unit, "hour", +1)
            btn00.activate(change_time_unit, "hour", -1)
            btn03.activate(change_time_unit, "minute", +1)
            btn02.activate(change_time_unit, "minute", -1)

        LCD.show()
        await uasyncio.sleep(0.01)