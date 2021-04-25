import machine
import utime


def interrupcion(pin):
    global contador
    contador += 1
    print(contador)
    
    
    
contador = 0

boton = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
boton.irq(interrupcion, machine.Pin.IRQ_FALLING)
