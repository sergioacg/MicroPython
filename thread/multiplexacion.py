"""
USO DE LOS THREADS en la Raspberry Pi Pico
Display 7 Segmentos usando MicroPython
Importación de nuestro propio módulo display7seg

by: Sergio Andres Castaño Giraldo
Referencia: https://controlautomaticoeducacion.com/
"""

from machine import Pin, Timer
import utime
import display7seg


def temporizacion(display7, contador): 
   contret=50        #Cargue con 50 la variable CONTRET
   while (contret>0): #Mientras que la variable CONTRET sea mayor que cero
      display7.show(contador)      #Llamar la rutina MOSTRAR
      contret -= 1      #Decremente la variable CONTRET

def temporizador(timer):
    #Variables globales compartidas con el main
    global contador, sentido
    #Lógica de la interrupción
    if sentido:
        contador += 1
    else:
        contador -= 1
    

def main():
    global contador, sentido
    #Raspberry Pi PICO (4 digitos)
    display_pins = (16, 18, 13, 14, 15, 17, 12) #(a, b, c, d, e, f, g)
    transistor_pins = (22, 21, 20, 19)
    
    #NodeMCU 8266v3 (2 Digitos)
    #display_pins = (16, 5, 4, 0, 2, 14, 12)
    #transistor_pins = (13, 15)
    
    display7 = display7seg.Display(display_pins,transistor_pins = transistor_pins )
    
    #Inicia las variables
    contador = 0
    sentido = True
    
    tim = Timer()
    tim.init(period= 1000, mode=Timer.PERIODIC, callback=temporizador)
    
    while True:
        #Muestra el valor del contador en el display
        #temporizacion(display7, contador)
        display7.show(contador)      #Llamar la rutina MOSTRAR
        
        
        
        #Si contador es nueve coloque el sentido del contador a decrementar
        if contador == 9999:
            sentido = False
        
        #Si contador es cero coloque el sentido del contador a incrementar
        if contador == 0:
            sentido = True
        
    

#Entry Point
if __name__ == '__main__':
    main()