"""
Programa de Ejemplo de PWM
Control de Giro y Velocidad de un motor DC con Puente H

by: Sergio Andrés Castaño Giraldo
controlautomaticoeducacion.com
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

import machine
import utime


def encoder_handler(pin):
    global paso
    paso += 1
    
    

def main():
    global paso
    paso = 0
    
    #Placa -> Raspberry Pi Pico = True, ESP8266 = False  
    placa= True
    
    
    frequency = 10000  #10Khz
    sentido = True #Sentido derecha
    
    if placa:
        potenciometro = machine.ADC(26) #Raspberry Pi Pico ADC0
        r_pwm = machine.PWM(machine.Pin(16)) #PWM derecha
        r_pwm.freq(frequency)
        l_pwm = machine.PWM(machine.Pin(17)) #PWM izquierda
        l_pwm.freq(frequency)
        boton = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
        encoder = machine.Pin(14, machine.Pin.IN)
        encoder.irq(trigger=machine.Pin.IRQ_FALLING, handler=encoder_handler)
    else:
        potenciometro = machine.ADC(0)  #NodeMCU8266v3 ADC0
        r_pwm = machine.PWM(machine.Pin(4), frequency) #PWM derecha
        l_pwm = machine.PWM(machine.Pin(5), frequency) #PWM izquierda
        boton = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
        encoder = machine.Pin(14, machine.Pin.IN)
        encoder.irq(trigger=machine.Pin.IRQ_FALLING, handler=encoder_handler)
        
    timer_start = utime.ticks_ms()

    while True:
        #Pregunta por el boton
        if not boton():
            utime.sleep_ms(200) #Anti-Rebote
            while not boton():
                pass
            utime.sleep_ms(200) #Anti-Rebote
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
        
         
        # Usando únicamnete Retardo       
        utime.sleep_ms(1000)
        state = machine.disable_irq()
        rpm = paso * 60 / 2
        paso = 0
        print(rpm, 'RPM')
        machine.enable_irq(state)
             
        """    
        timer_elapsed = utime.ticks_diff(utime.ticks_ms(), timer_start)
        if timer_elapsed >= 1000:
            #Calculo de las RPM (2 aspas)
            state = machine.disable_irq()
            rpm = paso * 60 / 2
            paso = 0
            machine.enable_irq(state)
            timer_start = utime.ticks_ms()
            print(rpm, 'RPM')
        """         

if __name__ == '__main__':
    main()