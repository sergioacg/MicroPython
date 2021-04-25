from machine import Pin, Timer

led = Pin(4, Pin.OUT)
led.value(0)

timer = Timer(-1)
timer.init(period = 1000, mode = Timer.PERIODIC, callback=lambda t:led.value(not led.value()))

