from machine import Pin, PWM
from utime import sleep_ms

frequency = 50
led = PWM(Pin(14))
led.freq(frequency)

while True:
  #for duty_cycle in range(0, 1024):
    #led.duty_ns(1500000)
    #sleep_ms(5)
    for pulso in range(500000,2500000,1000):
        led.duty_ns(pulso)
        sleep_ms(1)