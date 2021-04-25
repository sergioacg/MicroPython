"""
Programa de Ejemplo de PWM
Control de Giro y Velocidad de un motor DC con Puente H

by: Sergio Andrés Castaño Giraldo
Sitio web: https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import Pin, PWM, ADC
from utime import sleep_ms

def main():
    #Placa -> Raspberry Pi Pico = True, ESP8266 = False  
    placa= True
    
    frequency = 10000  #10Khz
    sentido = True #Sentido derecha
    
    if placa:
        potenciometro = ADC(26) #Raspberry Pi Pico ADC0
        r_pwm = PWM(Pin(16)) #PWM derecha
        r_pwm.freq(frequency)
        l_pwm = PWM(Pin(17)) #PWM izquierda
        l_pwm.freq(frequency)
        boton = Pin(15, Pin.IN, Pin.PULL_UP)
    else:
        potenciometro = ADC(0)  #NodeMCU8266v3 ADC0
        r_pwm = PWM(Pin(4), frequency) #PWM derecha
        l_pwm = PWM(Pin(5), frequency) #PWM izquierda
        boton = Pin(2, Pin.IN, Pin.PULL_UP)
    
    while True:
        #Pregunta por el boton
        if not boton():
            sleep_ms(200) #Anti-Rebote
            while not boton():
                pass
            sleep_ms(200) #Anti-Rebote
            sentido = not sentido
        
        
        #Aplica el PWM al motor
        if placa:
            velocidad = potenciometro.read_u16();
            if sentido:
                r_pwm.duty_u16(velocidad)
                l_pwm.duty_u16(0)
            else:
                r_pwm.duty_u16(0)
                l_pwm.duty_u16(velocidad)
        else:
            velocidad = potenciometro.read();
            if sentido:
                r_pwm.duty(velocidad)
                l_pwm.duty(0)
            else:
                r_pwm.duty(0)
                l_pwm.duty(velocidad)
            
        sleep_ms(5)
    

if __name__ == '__main__':
    main()