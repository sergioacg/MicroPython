"""
Programa de Ejemplo lectura ADC
by: Sergio Andrés Castaño Giraldo
https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import ADC
from utime import sleep


def main():
    # True: Raspberry Pi Pico
    # False: NodeMCU ESP8266
    placa = False
    
    if placa:
        potenciometro = ADC(26) #Raspberry Pi Pico ADC0
    else:
        potenciometro = ADC(0)  #NodeMCU8266v3 ADC0
        factor_10 = 3.3 / (1023) #Se puede leer con read()
    
    factor_16 = 3.3 / (65535)
    

    while True:
        
        if not placa: #NodeMCU ESP8266
            bits = potenciometro.read();
            volts_10 = bits * factor_10
            print('\nValor en 10 bits: {}, y en volts: {}'.format(bits, volts_10))
            
        bits_16 = potenciometro.read_u16();
        volts_16 = bits_16 * factor_16
        
        
        print('Valor en 16 bits: {}, y en volts: {}'.format(bits_16, volts_16))
        sleep(1)
        
        
if __name__ == '__main__':
    main()
