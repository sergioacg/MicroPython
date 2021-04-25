"""
Clase de Display 7 Segmentos usando MicroPython
by: Sergio Andres Castaño Giraldo
Referencia: https://controlautomaticoeducacion.com/
"""

from machine import Pin
import utime

class Display:
    
    
    def __init__(self, Pins, kind = 'C', transistor_pins = 1):
        self.kind = kind
        self.number_digit = len(transistor_pins)
        
        #Configura los pines del display como salida
        display = list()
        for i in range(7):
            display.append( Pin(Pins[i], Pin.OUT) )
        
        #Configura los pines de los transistores como salida
        transistors = list()
        for i in range(self.number_digit):
            transistors.append( Pin(transistor_pins[i], Pin.OUT) )
        
        #Tupla con las posiciones del display
        self.display = display
        
        #Tupla con las posiciones de los transistores
        self.transistors = transistors
        
    def show(self, digits):
        #Realiza la multiplexación
        for i in range( self.number_digit ):
            number = int((digits % 10 ** (i+1)) / 10 ** i)
            self._show_one_display(number)
            self.transistors[i].on()
            utime.sleep_ms(1)
            self.transistors[i].off()
            
    
    #Metodo provado para mostrar número en un solo display
    def _show_one_display(self, digit):
        bit = 1;
        
        #Display Cátodo Común
        if self.kind.upper() == 'C':
            numbers = (int('3f',16),int('06',16),int('5b',16),int('4f',16),int('66',16),int('6d',16),int('7d',16),int('07',16),int('7f',16),int('67',16))
        #Display Ánodo Común
        elif self.kind.upper() == 'A':
            numbers = (int('40',16),int('79',16),int('24',16),int('30',16),int('19',16),int('12',16),int('02',16),int('78',16),int('00',16),int('18',16))
        else:
            return
        
        for i in range(7):
            if (numbers[digit]  & bit) == 0:
                self.display[i].off()
            else:
                self.display[i].on()
            bit = bit << 1
            

    