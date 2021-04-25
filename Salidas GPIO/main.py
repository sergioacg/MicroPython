from machine import Pin
import utime


def main():
    led = Pin(5, Pin.OUT)
    while True:
        #Prende y apaga por 1 segundo
        led.value(1)
        utime.sleep(1)
        led.value(0)
        utime.sleep(1)
        
        #Prende y Apaga por medio segundo
        led.on()
        utime.sleep_ms(500)
        led.off()
        utime.sleep_ms(500)
        

if __name__ == '__main__':
    main()