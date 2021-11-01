"""
Control PID de Nivel

by: Sergio Andrés Castaño Giraldo
Sitio web: https://controlautomaticoeducacion.com/
Canal de YouTube: https://www.youtube.com/c/SergioACastañoGiraldo
"""

from machine import Pin, PWM, ADC, I2C, Timer
from utime import sleep_ms
from ssd1306 import SSD1306_I2C


#OLED
WIDTH = 128
HEIGHT = 64  
#Configuración de PINES
sensor = ADC(26) 
voltaje = ADC(27)
potenciometro = ADC(28)
pwm = PWM(Pin(20)) 
pwm.freq(40000)
i2c = I2C(1, scl = Pin(19), sda = Pin(18), freq = 200000)

#OLED
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

#Global Variables
t = 0
z = [55, 55]
y = [55, 55]
x = [25, 25]
level = 0
dt = 1


#Modelo del Sistema
K=5
tau=350
theta=3
Ts = 10;                  
L = theta + Ts/2

e = [0,0,0]    #Vector de error
u = [0,0] #Vector de Ley de Contr
    
def update_past(v,kT):
   for i in range(1,kT,1):
      v[i-1]=v[i]
   return v
   
def PID_Controller(u, e, q0, q1, q2):
    # Controle PID
    # e[2] = e(k)
    # e[1] = e(k-1)
    # e[0] = e(k-2)
    # u[0] = u(k-1)
    lu = u[0] + q0*e[2] + q1*e[1] + q2*e[0]; #Ley del controlador PID discreto
    
    # Anti - Windup
    if (lu >= 100.0):        
        lu = 100.0
    
    if (lu <= 0.0):
        lu = 0.0
     
    return(lu)

    
def temporizador(timer):
   global u, e, q0, q1, q2 
   #Actualiza los vectores u y e
   u = update_past(u,len(u));
   e= update_past(e,len(e));
   
   #Calcula el error actual
   e[len(e)-1] = setpoint - level;
   #Calcula la Acción de Control PID
   u_end = PID_Controller(u, e, q0, q1, q2);  #Max= 100, Min=0
   u[len(u)-1] = u_end
   velocidad = int(u[len(u)-1] * 65535 /100);
   #Aplica la acción de control en el PWM
   
   pwm.duty_u16(velocidad)
   
    
def plot_time(yp, sp, t, x, y, var = [0.0,18], vpts=[25, 16, 40], hpts = [25, 55, 112]):
    """"
    Graph function of the Cartesian plane in relation to time:
    by: Sergio Andres Castaño Giraldo
    
    plot_time(yp, t, x, y, var = [0.0,3.3], vpts=[25, 16, 40], hpts = [25, 55, 112]):

    yp: dependent variable
    t: time (used while the Cartesian plane is not complete)
    x: List of two positions of variable x, x[0] is the position in past x and x[1] position of current x.
    y: List of two positions of the variable y, y[0] is the position in y past and y[1] position of current x.
    var = [0.0,3.3]: Magnitude of the variable (default voltage)
    vpts = [25, 16, 40]: points on the vertical y axis.
    hpts = [25, 55, 112]: points on the vertical x axis.

    Example:
    #Global Variables
    t = 0
    y = [55, 55]
    x = [25, 25]
    #Function:
    volts = pot.read_u16 () * FACTOR
    t, x, y = plot_time (volts, t, x, y)
    sleep_ms (500)
    """
    global dt
    #Axis
    oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
    oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
    oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
    oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    #Level
    y[1] = int((yp-var[0])/(var[1]-var[0]) * (vpts[1]-hpts[1]) + hpts[1]) #Interpolation
    #Set-Point
    z[1] = int((sp-var[0])/(var[1]-var[0]) * (vpts[1]-hpts[1]) + hpts[1]) #Interpolation
    
    if t < hpts[2] - hpts[0]:
        x[1] = x[0]+1
    else:
        x[1] = hpts[2]
    
    #Plot the line
    oled.line(x[0],y[0],x[1],y[1],1)
    oled.line(x[0],z[0],x[1],z[1], dt)
    dt ^= 1  #Dotted setpoint plot
    oled.show()
    
    #Update past values
    y[0] = y[1]
    x[0] = x[1]
    z[0] = z[1]
    
    #If you have already reached the end of the graph then ...
    if t > hpts[2] - hpts[0]:
        #Erases the first few pixels of the graph and the y-axis.
        oled.fill_rect(vpts[0],vpts[1],2,vpts[2],0)
        #Clears the entire y-axis scale
        oled.fill_rect(vpts[0]-25, vpts[1],vpts[0],vpts[2]+5,0)
        #shifts the graph one pixel to the left
        oled.scroll(-1,0)
        #Axis
        oled.vline(vpts[0], vpts[1], vpts[2], 1) #x, y, h
        oled.hline(hpts[0], hpts[1], hpts[2], 1) #x, y, w
        oled.text(str(round(var[0],1)), vpts[0]-25, hpts[1]-5)
        oled.text(str(round(var[1],1)), vpts[0]-25, vpts[1])
    else:
        t += 1
    
    return t,x,y

        

def main():
    global level, t, y, x, setpoint, q0, q1, q2, u, e
    #Placa -> Raspberry Pi Pico = True, ESP8266 = False  
    placa= True
    
    #Sensor Presión
    tolP=0.5 # Ajusta la medida de presión
    rho = 1000 #Densidad del Agua
    g=9.8     #Gravedad
    factor_16 = 3.3 / (65535)
    factor_sp = 18 / (65535)
    
    tim = Timer()
    tim.init(period= 10000, mode=Timer.PERIODIC, callback=temporizador)
    
    kp=(1.2*tau)/(K*L)
    ti=2*L
    td=0.5*L

    q0=kp*(1+Ts/(2*ti)+td/Ts)
    q1=-kp*(1-Ts/(2*ti)+(2*td)/Ts)
    q2=(kp*td)/Ts

    while True:         
        
        #Presión en Kpa según gráfica 4 del Datasheet
        level_sum = 0
        for i in range(200):
            Vout = sensor.read_u16() * factor_16
            Vs = voltaje.read_u16() * factor_16
            presion = ( Vout - 0.04*Vs ) / (0.09 * Vs) + tolP #kPa
            level_sum += ((presion*1000)/(rho*g))*100;  #Medida de Nivel del tanque
            
        level_x = level_sum / 200
        level = 1.157 * level_x - 2.1208    
        #print(level)
        
        setpoint = potenciometro.read_u16() * factor_sp
        
        t,x,y = plot_time(level,setpoint,t,x,y)
        oled.fill_rect(0,0,128,15,0)
        oled.text("Lvl: ", 0, 0)
        oled.text(str(round(level,1)), 32, 0)
        oled.text("SP: ", 70, 0)
        oled.text(str(round(setpoint,1)), 95, 0)
        oled.show()
        
        sleep_ms(100)
    

if __name__ == '__main__':
    main()