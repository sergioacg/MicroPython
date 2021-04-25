"""
Display 7 Segmentos usando MicroPython
by: Sergio Andres Castaño Giraldo
Referencia: https://controlautomaticoeducacion.com/
"""
from machine import Pin
import utime


def show(digito, display):
    """
        Muestra el digito en el display 7 segmentos
        
        llamado de la función:
        show(digito, display)
        
        Parametros de entrada:
        digito -> Digito a mostrar
        display -> Lista con los pines del display (Pin.OUT)
        
        by: Sergio Andres Castaño Giraldo
        https://controlautomaticoeducacion.com/
    """
    #Tupla con los números de un display 7 segmentos catodo común
    catodo = (int('3f',16),int('06',16),int('5b',16),int('4f',16),int('66',16),int('6d',16),int('7d',16),int('07',16),int('7f',16),int('67',16))
    
    bit = 1;    
    for i in range(7):
        if (catodo[digito]  & bit) == 0:
            display[i].off()
        else:
            display[i].on()
        bit = bit << 1
    

def main():
    
    #Configura los pines del display 7 segmentos
    display_pins = (19, 18, 13, 15, 14, 16, 17) #Raspberry Pi Pico
    #display_pins = (16, 5, 4, 0, 2, 14, 12) #NodeMCU8266
    display = list()
    for i in range(7):
        display.append( Pin( display_pins[i], Pin.OUT ) )

    
    #Inicia las variables
    contador = 0
    sentido = True
    
    
    while True:
        #Muestra el valor del contador en el display
        show(contador, display)
        
        #Verifica si incrementa o decrementa el contador
        if sentido:
            contador += 1
        else:
            contador -= 1
        
        #Si contador es nueve coloque el sentido del contador a decrementar
        if contador == 9:
            sentido = False
        
        #Si contador es cero coloque el sentido del contador a incrementar
        if contador == 0:
            sentido = True
        
        #Esperar por 1 segundo
        utime.sleep(1)
    

#Entry Point
if __name__ == '__main__':
    main()