import utime
from machine import I2C,Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#Dirección del I2C y tamaño del LCD
I2C_ADDR  =  0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Raspberry Pi Pico
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

#Esp8266
#i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)

#Configuración LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

battery_0 = [0x0E,
  0x1B,
  0x11,
  0x11,
  0x11,
  0x11,
  0x11,
  0x1F]
battery_15 = [0x0E,
  0x1B,
  0x11,
  0x11,
  0x11,
  0x11,
  0x1F,
  0x1F]
battery_30 = [  0x0E,
  0x1B,
  0x11,
  0x11,
  0x11,
  0x1F,
  0x1F,
  0x1F]
battery_45 = [0x0E,
  0x1B,
  0x11,
  0x11,
  0x1F,
  0x1F,
  0x1F,
  0x1F]
battery_60 = [0x0E,
  0x1B,
  0x11,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F]
battery_75 = [0x0E,
  0x1B,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F]
battery_100 = [0x0E,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F,
  0x1F]


def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)


def main():
    lcd.custom_char(0, bytearray(battery_0))
    lcd.custom_char(1, bytearray(battery_15))
    lcd.custom_char(2, bytearray(battery_30))
    lcd.custom_char(3, bytearray(battery_45))
    lcd.custom_char(4, bytearray(battery_60))
    lcd.custom_char(5, bytearray(battery_75))
    lcd.custom_char(6, bytearray(battery_100))
    
    
    while True:
        lcd.clear()
        lcd_str("Battery:", 0, 0)
        lcd.move_to(0,1)
        for i in range(0,7):
            lcd.putchar(chr(i))
        utime.sleep(3)
        
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr("Suscribete a    ")
        utime.sleep(1)
        lcd.move_to(0,1)
        lcd.putstr("Control       ")
        utime.sleep(1)
        lcd_str("Automatico    ", 0, 0)
        utime.sleep(1)
        lcd_str("Educacion    ", 0, 1)
        utime.sleep(1)
        
        lcd.clear()
        lcd_str("Numeros en", 3,0)
        lcd_str("Esquinas", 4,1)
        utime.sleep(1)
        
        lcd_str("1", 0,0)
        utime.sleep(1)
        lcd_str("2", 15,0)
        utime.sleep(1)
        lcd_str("3", 0,1)
        utime.sleep(1)
        lcd_str("4", 15,1)
        utime.sleep(1)
        
        lcd.clear()
        lcd_str("Suscribete", 0, 0)
        lcd_str("Activa: CAMPANA", 0, 1)
        lcd.blink_cursor_on()
        utime.sleep(2)
        
        #Backspace
        for j in range(1, -1, -1):
            for i in range(15, -1, -1):
                lcd.move_to(i, j)
                lcd.putstr(' ')
                utime.sleep_ms(100)
        utime.sleep(1)
        lcd.hide_cursor()
        
        #BackLight
        lcd.clear()
        lcd.backlight_off()
        lcd_str("BackLight OFF", 0, 0)
        utime.sleep(3)
        
        lcd.clear()
        lcd.backlight_on()
        lcd_str("BackLight ON", 0, 0)
        utime.sleep(3)


if __name__ == '__main__':
    main()