"""
Programa de Ejemplo Sensor de Temperatura de la Pico
by: Sergio Andrés Castaño Giraldo
https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import ADC
from utime import sleep


def main():    
    sensor_temp = ADC(4) #Sensor interno de temperatura
    factor_16 = 3.21 / (65535)
    
    while True:        
        voltaje = sensor_temp.read_u16() * factor_16
        temperatura = 27 - (voltaje - 0.706)/0.001721
        print('La temperatura es: ',temperatura)
        sleep(2)
        
    
if __name__ == '__main__':
    main()
