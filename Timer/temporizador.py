"""
Programa de Ejemplo de PWM
Control de Giro y Velocidad de un motor DC con Puente H

by: Sergio Andrés Castaño Giraldo
controlautomaticoeducacion.com
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

import machine
import utime

contador = 0

def handle_timer(timer):
    global contador, lampara
    contador += 1
    lampara.value(not lampara.value())
    
    

def main():
    global contador, lampara
    boton = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
    lampara = machine.Pin(4, machine.Pin.OUT)
    led = machine.Pin(5, machine.Pin.OUT)
    tim = machine.Timer(-1)
    tim.init(period=50, mode=machine.Timer.PERIODIC, callback=handle_timer)
    tiempo = 500
    while True:
        led.on()
        utime.sleep(3)
        led.off()
        utime.sleep(3)


if __name__ == '__main__':
    main()
