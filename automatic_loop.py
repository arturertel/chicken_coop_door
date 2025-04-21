import uasyncio
from ds1302 import DS1302
from new_motor import MotorDriver
from settings.save_settings import Settings
import global_state  # enthält mode_switch
from machine import Pin
ds = DS1302(Pin(18), Pin(17), Pin(16))
motor = MotorDriver(pwm_pin=19, dir_pin=28, en_pin=20)

already_opened = False
already_closed = False
last_checked_day = -1  # zum Tageswechsel erkennen

async def automatic_loop():
    global already_opened, already_closed, last_checked_day

    while True:
        if global_state.mode_switch == 4:  # Automatikmodus aktiviert
            settings = Settings.load()

            hour = ds.hour()  # Die aktuelle Stunde
            minute = ds.minute()  # Die aktuelle Minute
            day = ds.day()  # Der aktuelle Tag des Monats
            
            print("AUTOMATIC LOOP läuft, mode =", global_state.mode_switch)

            print("Uhrzeit:", ds.hour(), ":", ds.minute())
            print("Open-Zeit:", settings.open)
            print("Close-Zeit:", settings.close)
            
            # Prüfen, ob ein neuer Tag ist
            if day != last_checked_day:
                already_opened = False
                already_closed = False
                last_checked_day = day
                print("Neuer Tag – Status zurückgesetzt")

            # Wenn es die Öffnungszeit ist und noch nicht geöffnet wurde
            if [hour, minute] == settings.open and not already_opened:
                print("Automatik: Öffnen der Tür")
                uasyncio.create_task(run_motor(1))  # Motor starten, Richtung 0
                already_opened = True

            # Wenn es die Schließzeit ist und noch nicht geschlossen wurde
            elif [hour, minute] == settings.close and not already_closed:
                print("Automatik: Schließen der Tür")
                uasyncio.create_task(run_motor(0))  # Motor starten, Richtung 1
                already_closed = True

        await uasyncio.sleep(1)  # 1 Sekunde warten, bevor die Schleife wiederholt wird

async def run_motor(direction):
    motor.stop()
    await uasyncio.sleep(1)  # Kurze Pause, bevor der Motor startet
    motor.start(direction=direction, max_pwm=30000)  # Motor starten

