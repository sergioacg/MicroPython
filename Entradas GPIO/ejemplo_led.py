from machine import Pin
import utime

boton = Pin(2, Pin.IN, Pin.PULL_UP)
led = Pin(16, Pin.OUT)

while True:
    if not boton():
        led.on()
    else:
        led.off()