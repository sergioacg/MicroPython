"""
Programa de Ejemplo de Motor Paso a Paso Unipolar
by: Sergio Andrés Castaño Giraldo
https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import Pin
import utime


def envia_pasos(paso, tipo, bobinas):
    bit = 1;
    for i in range(4):
        if (tipo[paso]  & bit) == 0:
            bobinas[i].off()
        else:
            bobinas[i].on()
        bit = bit << 1
        

def main():
    #Define los pines de los 4 botones Raspberry Pi PICO
    boton_horario = Pin(19, Pin.IN, Pin.PULL_UP)
    boton_antihorario = Pin(18, Pin.IN, Pin.PULL_UP)
    boton_velocidad = Pin(17, Pin.IN, Pin.PULL_UP)
    boton_pasos = Pin(16, Pin.IN, Pin.PULL_UP)
    
    #Define los pines del Motor PaP
    motor_pins = (13, 12, 11, 10)
    
    """
    #Define los pines de los 4 botones NodeMCU8266
    boton_horario = Pin(5, Pin.IN, Pin.PULL_UP)
    boton_antihorario = Pin(4, Pin.IN, Pin.PULL_UP)
    boton_velocidad = Pin(0, Pin.IN, Pin.PULL_UP)
    boton_pasos = Pin(2, Pin.IN, Pin.PULL_UP)
    
    #Define los pines del Motor PaP
    motor_pins = (14, 12, 13, 15)
    """
  
    #Configura las GPIO como Salidas
    bobinas = list()
    for i in motor_pins:
        bobinas.append( Pin(i, Pin.OUT) )
        
    #Configura las secuencia de los pasos
    
    #Secuencia a 1 paso
    un_paso  = ( int('1000',2),
                 int('0100',2),
                 int('0010',2),
                 int('0001',2) )
    #Secuencia a 2 pasos
    dos_pasos = ( int('1100',2),
                  int('0110',2),
                  int('0011',2),
                  int('1001',2) )
    #Secuencia a 1/2 paso
    medio_paso = ( int('1000',2),
                   int('1100',2),
                   int('0100',2),
                   int('0110',2),
                   int('0010',2),
                   int('0011',2),
                   int('0001',2),
                   int('1001',2) )
    
    #variables del programa
    sentido = True #True -> Horario, False -> Anti-Horario
    velocidad = (5, 10, 30, 100, 500) #Velocidades
    configuracion = 1 #Selecciona los pasos
    contador_pasos = 0 #cuenta del paso actual
    contador_velocidad = 0
    cantidad_pasos = 3
    
    while True:
        
        #Giro en Sentido Horario
        if not boton_horario.value():
            utime.sleep_ms(100) #Anti-Rebote
            print('Sentido horario')            
            sentido = True
            contador_pasos = -1
         
        #Giro en Sentido AntiHorario
        if not boton_antihorario.value():            
            utime.sleep_ms(100) #Anti-Rebote
            print('Sentido antihorario')
            sentido = False
            contador_pasos = cantidad_pasos
            
        #Cambio de la secuencia de pasos
        if not boton_pasos(): #Recordar que los objetos pin son invocables.
            utime.sleep_ms(100) #Anti-Rebote
            print('Cambio de secuencia de pasos')
                        #esperar hasta soltar el boton
            while boton_pasos.value() == 0:
                pass
            utime.sleep_ms(100) #Anti-Rebote
            configuracion += 1
            if configuracion > 3:
                configuracion = 1
                
            if configuracion != 3 and contador_pasos > 3:
                contador_pasos = contador_pasos - 4

        
        #Cambio de la velocidad del motor
        if boton_velocidad.value() == 0:
            print('Cambio de velocidad')
            utime.sleep_ms(100) #Anti-Rebote
            #esperar hasta soltar el boton
            while boton_velocidad.value() == 0:
                pass
            utime.sleep_ms(100) #Anti-Rebote
            contador_velocidad += 1
            if contador_velocidad > 4:
                contador_velocidad = 0
                
        #************************************#
        #*****  Logica de los Contadores ****#
        #************************************#
        if sentido:
            contador_pasos += 1
            if contador_pasos > cantidad_pasos:
                contador_pasos = 0
        else:
            contador_pasos -= 1
            if contador_pasos < 0:
                contador_pasos = cantidad_pasos
                
        #************************************#
        #*****  Logica de los Contadores ****#
        #************************************#
        if configuracion == 1:
            envia_pasos(contador_pasos, un_paso, bobinas)
            cantidad_pasos = 3
        elif configuracion == 2:
            envia_pasos(contador_pasos, dos_pasos, bobinas)
            cantidad_pasos = 3
        else:
            envia_pasos(contador_pasos, medio_paso, bobinas)
            cantidad_pasos = 7
            
        # Velocidad
        utime.sleep_ms(velocidad[contador_velocidad])
        

#Entry Point
if __name__ == '__main__':
    main()