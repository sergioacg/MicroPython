from machine import Pin

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