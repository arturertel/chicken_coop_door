import uasyncio
from ds1302 import DS1302
from dcmotor import DCMotor
from settings.save_settings import Settings
import global_state  # enthält mode_switch
from machine import Pin, PWM

ds = DS1302(Pin(18), Pin(17), Pin(16))

frequency = 1000

pin1 = Pin(19, Pin.OUT)
pin2 = Pin(20, Pin.OUT)
enable = PWM(Pin(28))
enable.freq(1000)  # z. B. 1000 Hz

dc_motor = DCMotor(pin1, pin2, enable)

# Set min duty cycle (15000) and max duty cycle (65535)
# dc_motor = DCMotor(pin1, pin2, enable, 15000, 65535)

already_opened = False
already_closed = False


async def automatic_loop():
    global already_opened, already_closed

    while True:
        if global_state.mode_switch == 4:  # Automatikmodus aktiviert
            settings = Settings.load()

            hour = ds.hour()  # Die aktuelle Stunde
            minute = ds.minute()  # Die aktuelle Minute

            print("AUTOMATIC LOOP läuft, mode =", global_state.mode_switch)
            print("Uhrzeit:", hour, ":", minute)
            print("Open-Zeit:", settings.open)
            print("Close-Zeit:", settings.close)

            # Wenn es die Öffnungszeit ist und noch nicht geöffnet wurde
            if [hour, minute] == settings.open and not already_opened:
                print("Automatik: Öffnen der Tür")
                # Motor starten, Richtung 1 für Öffnen
                uasyncio.create_task(run_motor(1))
                already_opened = True
                already_closed = False  # Status für Schließen zurücksetzen

            # Wenn es die Schließzeit ist und noch nicht geschlossen wurde
            elif [hour, minute] == settings.close and not already_closed:
                print("Automatik: Schließen der Tür")
                # Motor starten, Richtung 0 für Schließen
                uasyncio.create_task(run_motor(0))
                already_closed = True
                already_opened = False  # Status für Öffnen zurücksetzen

        # 1 Sekunde warten, bevor die Schleife wiederholt wird
        await uasyncio.sleep(1)


async def run_motor(direction):
    dc_motor.stop()
    await uasyncio.sleep(1)  # Kurze Pause, bevor der Motor startet
    if direction == 1:
        print('Forward with speed: 50%')
        dc_motor.forward(70)
    elif direction == 0:
        print('Backwards with speed: 50%')
        dc_motor.backwards(70)
