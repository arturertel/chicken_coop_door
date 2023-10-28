from machine import Pin, PWM
from time import sleep    


pwm = PWM(Pin(16))
duty_step = 129  # Step size for changing the duty cycle
direction = Pin(28, Pin.OUT)

#Set PWM frequency
frequency = 5000
pwm.freq (frequency)
try:
    while True:
        if direction.value() == 0:
            direction.value(1)
        else:
            direction.value(0)
        print(direction.value())   
      # Increase the duty cycle gradually
        for duty_cycle in range(0, 65536, duty_step):
            pwm.duty_u16(duty_cycle)
            sleep(0.005)
        
      # Decrease the duty cycle gradually
        for duty_cycle in range(65536, 0, -duty_step):
            pwm.duty_u16(duty_cycle)
            sleep(0.005)

except KeyboardInterrupt:
    print("Keyboard interrupt")
    pwm.duty_u16(0)
    print(pwm)
    pwm.deinit()

