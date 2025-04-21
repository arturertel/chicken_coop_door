from machine import Pin, PWM
import time

class MotorDriver:
    def __init__(self, pwm_pin, dir_pin, en_pin, pwm_freq=20000):
        """Initialisierung des Motors und Pins"""
        self.dir = Pin(dir_pin, Pin.OUT)  # Richtungspin
        self.en = Pin(en_pin, Pin.OUT)    # Enable-Pin (motor an/aus)
        self.pwm = PWM(Pin(pwm_pin))      # PWM Pin für Geschwindigkeit
        self.pwm.freq(pwm_freq)           # PWM Frequenz (20 kHz empfohlen)

        self.stop()  # Initial motor stop (not running)

    def start(self, direction=0, target_duty=60000, kickstart_duty=65535, kickstart_time=0.2, ramp_step=1024, ramp_delay=0.01):
        """Startet den Motor mit Kickstart und Rampenregelung"""
        print("Motorstart mit Kickstart und Rampe auf", target_duty)

        # Richtung setzen
        self.dir.value(direction)
        self.en.value(0)  # Motor aktivieren (LOW für Aktivierung)

        # Kickstart: voller Anlauf mit max. Leistung für 200ms
        self.pwm.duty_u16(kickstart_duty)
        time.sleep(kickstart_time)

        # Rampenregelung: Motorleistung verringern bis zum Zielwert
        for duty in range(kickstart_duty, target_duty, -ramp_step):
            self.pwm.duty_u16(duty)
            time.sleep(ramp_delay)

        # Ziel-PWM Wert setzen, um den Motor mit konstanter Geschwindigkeit laufen zu lassen
        self.pwm.duty_u16(target_duty)

    def stop(self):
        """Stoppt den Motor sofort und schaltet den Brake Mode ein"""
        self.pwm.duty_u16(0)  # Setzt PWM auf 0 (Brake Mode)
        self.en.value(1)  # Motor deaktivieren (HIGH für Deaktivierung)
        # print("Motor gestoppt.")

    def set_speed(self, duty_u16):
        """Setzt die Geschwindigkeit des Motors direkt (ohne Rampen)"""
        self.pwm.duty_u16(duty_u16)

    def set_direction(self, direction):
        """Setzt die Richtung des Motors"""
        self.dir.value(direction)

    def toggle_direction(self):
        """Wechselt die Richtung des Motors"""
        self.dir.toggle()
