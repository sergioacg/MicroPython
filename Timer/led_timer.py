from machine import Pin, Timer

led = Pin(25, Pin.OUT)
led.value(0)

timer = Timer()
timer.init(period = 500, mode = Timer.PERIODIC, callback=lambda t:led.value(not led.value()))

