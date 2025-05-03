import uasyncio
from menu import menu_loop, sleep_control_loop
from dcmotor import DCMotor
from button_handler import Btn
import global_state
from auto_loop import automatic_loop
from settings.save_settings import Settings
from machine import Pin, PWM
from ds1302 import DS1302
ds = DS1302(Pin(18), Pin(17), Pin(16))
settings = Settings.load()

# Motor und Steuerungsvariablen
frequency = 1000

pin1 = Pin(19, Pin.OUT)
pin2 = Pin(20, Pin.OUT)
enable = PWM(Pin(28))
enable.freq(frequency)
dc_motor = DCMotor(pin1, pin2, enable)

# Set min duty cycle (15000) and max duty cycle (65535)
# dc_motor = DCMotor(pin1, pin2, enable, 15000, 65535)


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
                    dc_motor.stop()
                    await uasyncio.sleep(0.1)
                    dc_motor.backwards(70)
                    print("Motor wird geöffnet mit Richtung 0")
                    motor_running = True
                    current_direction = 0

            elif btn00.value() == 1:
                if not motor_running or current_direction != 1:
                    dc_motor.stop()
                    await uasyncio.sleep(0.1)
                    dc_motor.forward(70)
                    print("Motor wird geöffnet mit Richtung 1")
                    motor_running = True
                    current_direction = 1

            elif btn00.value() == 0 and btn01.value() == 0 and motor_running:
                dc_motor.stop()
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
