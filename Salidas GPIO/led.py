from machine import Pin
import utime


def main():
    led = Pin(14, Pin.OUT)
    while True:
        led.value(1)
        utime.sleep_ms( 1000 )
        led.value(0)
        utime.sleep_ms( 1000 )
        

if __name__ == '__main__':
    main()