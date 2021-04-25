"""
Display 7 Segmentos usando MicroPython
Importación de nuestro propio módulo display7seg

by: Sergio Andres Castaño Giraldo
Referencia: https://controlautomaticoeducacion.com/
"""

from machine import Pin
import utime
import display7seg



def main():
    #Configura los pines del display 7 segmentos
    display_pins = (19, 18, 13, 15, 14, 16, 17) #Raspberry Pi Pico
    #display_pins = (16, 5, 4, 0, 2, 14, 12) #NodeMCU8266
    
    display7 = display7seg.Display(display_pins)
    
    #Inicia las variables
    contador = 0
    sentido = True
    
    
    while True:
        #Muestra el valor del contador en el display
        #mostrar_display(numeros[contador], display)
        display7.show(contador)
        
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