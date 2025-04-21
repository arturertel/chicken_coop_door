import uasyncio
from menu import menu_loop, sleep_control_loop
from new_motor import MotorDriver
from button_handler import Btn
import global_state
from automatic_loop import automatic_loop
from settings.save_settings import Settings
from machine import Pin
from ds1302 import DS1302
ds = DS1302(Pin(18), Pin(17), Pin(16))
settings = Settings.load()

# Motor und Steuerungsvariablen
motor = MotorDriver(pwm_pin=19, dir_pin=28, en_pin=20)
motor_running = False
current_direction = None

# Buttons initialisieren
btn00 = Btn(pin=0)  # z.B. Rückwärts
btn01 = Btn(pin=1)  # z.B. Vorwärts

async def motor_loop():
    global motor_running, current_direction
    while True:
        if global_state.mode_switch == 3:  # Manueller Modus
            # print("Manueller Modus aktiv")
            if btn01.value() == 1:
                if not motor_running or current_direction != 0:
                    motor.stop()
                    await uasyncio.sleep(0.1)
                    motor.start(0, 13000, 40000)
                    print("Motor wird geöffnet mit Richtung 0")
                    motor_running = True
                    current_direction = 0

            elif btn00.value() == 1:
                if not motor_running or current_direction != 1:
                    motor.stop()
                    await uasyncio.sleep(0.1)
                    motor.start(1, 13000, 30000)
                    print("Motor wird geöffnet mit Richtung 1")
                    motor_running = True
                    current_direction = 1

            elif btn00.value() == 0 and btn01.value() == 0 and motor_running:
                motor.stop()
                motor_running = False
                current_direction = None

        await uasyncio.sleep(0.01)

async def main():
    await uasyncio.gather(
        menu_loop(),
        motor_loop(),
        automatic_loop(),
        sleep_control_loop()
    )

uasyncio.run(main())

