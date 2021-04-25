from machine import Pin
import utime


def main():
    
    # Salidas Digitales GPIO Raspberry Pi Pico
    led_amarillo = Pin(20, Pin.OUT)
    led_azul     = Pin(19, Pin.OUT)
    led_rojo     = Pin(18, Pin.OUT)
    
    # Entradas Digitales GPIO Raspberry Pi Pico
    boton_izquierda = Pin(17, Pin.IN, Pin.PULL_UP)
    boton_derecha   = Pin(16, Pin.IN)
    
    """
    # Salidas Digitales GPIO NodeMCU 8266v3
    led_amarillo = Pin(16, Pin.OUT)
    led_azul     = Pin(5, Pin.OUT)
    led_rojo     = Pin(4, Pin.OUT)
    
    # Entradas Digitales GPIO NodeMCU 8266v3
    boton_izquierda = Pin(0, Pin.IN, Pin.PULL_UP)
    boton_derecha   = Pin(2, Pin.IN)
    """
    
    # Almaceno los leds en una lista
    leds = [led_amarillo, led_azul, led_rojo]
    
    #variables de desplazamiento
    izquierda = True
    derecha   = False
    
    for led in leds:
        led.off()

    #Ciclo infinito
    while True:
        #Si presiona el botón de la izquierda
        if boton_izquierda.value() == 0:
            izquierda = True
            derecha   = False
            
        #Si presiona el botón de la derecha
        if boton_derecha.value() == 1:
            izquierda = False
            derecha   = True
            
        #Si presiona ambos botones
        if boton_izquierda.value() == 0 and boton_derecha.value() == 1 :
            izquierda = True
            derecha   = True
        
        #Rotación de leds a la izquierda
        if izquierda and not derecha:
            for led in leds:
                led.on()
                utime.sleep_ms(100)
                led.off()
                utime.sleep_ms(100)
                
        #Rotación de leds a la derecha
        if not izquierda and derecha:
            for i in range(2,-1,-1):
                leds[i].on()
                utime.sleep_ms(100)
                leds[i].off()
                utime.sleep_ms(100)
                
        if  izquierda and derecha:
            for led in leds:
                led.on()
                


if __name__ == '__main__':
    main()
