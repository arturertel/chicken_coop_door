import uasyncio
from machine import Pin, PWM

class MotorDriver:
    def __init__(self, pwm_pin, dir_pin, en_pin, pwm_freq=20000):
        self.dir = Pin(dir_pin, Pin.OUT)
        self.en = Pin(en_pin, Pin.OUT)
        self.pwm = PWM(Pin(pwm_pin))
        self.pwm.freq(pwm_freq)

        self.running = False
        self._motor_task = None
        self.stop()

    async def _run_motor(self, direction, start_pwm, max_pwm, ramp_step, ramp_delay):
        # print(f"Motorstart: Richtung={direction}, Start bei {start_pwm}, Ziel={max_pwm}")

        self.dir.value(direction)
        self.en.value(0)
        self.running = True

        current_pwm = start_pwm
        self.pwm.duty_u16(current_pwm)

        # Sanftes Hochfahren
        while current_pwm < max_pwm and self.running:
            current_pwm += ramp_step
            if current_pwm > max_pwm:
                current_pwm = max_pwm
            self.pwm.duty_u16(current_pwm)
            await uasyncio.sleep(ramp_delay)

        print("Motor läuft mit PWM:", max_pwm)

        # PWM halten mit leichtem Flackern
        hold_low = max_pwm - 1000 if max_pwm >= 1000 else max_pwm
        hold_high = max_pwm

        while self.running:
            self.pwm.duty_u16(hold_low)
            await uasyncio.sleep(0.02)
            self.pwm.duty_u16(hold_high)
            await uasyncio.sleep(0.02)

    def start(self, direction=0, start_pwm=13000, max_pwm=65535, ramp_step=1024, ramp_delay=0.05):
        if self._motor_task is None or self._motor_task.done():
            self._motor_task = uasyncio.create_task(
                self._run_motor(direction, start_pwm, max_pwm, ramp_step, ramp_delay)
            )

    def stop(self):
        self.running = False
        self.pwm.duty_u16(0)
        self.en.value(1)
        print("Motor gestoppt.")


            
