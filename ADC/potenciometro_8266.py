"""
Programa de Ejemplo lectura ADC
by: Sergio Andrés Castaño Giraldo
https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import ADC
from utime import sleep


def main():
    #potenciometro = ADC(26) #Raspberry Pi Pico ADC0
    potenciometro = ADC(0)  #NodeMCU8266v3 ADC0
    
    factor_10 = 3.3 / (1023)
    #factor_12 = 3.3 / (4095)
    factor_16 = 3.3 / (65535)

    while True:
        bits = potenciometro.read();
        bits_16 = potenciometro.read_u16();
        
        volts_10 = bits * factor_10
        #volts_12 = bits * factor_12
        volts_16 = bits_16 * factor_16
        
        print('\nValor en 10 bits: {}, y en volts: {}'.format(bits, volts_10))
        print('Valor en 16 bits: {}, y en volts: {}'.format(bits_16, volts_16))
        sleep(1)
        
        
if __name__ == '__main__':
    main()
