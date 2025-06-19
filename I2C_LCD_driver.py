# -*- coding: utf-8 -*-
"""
I2C_LCD_driver.py
-----------------
Raspberry Pi ile I2C üzerinden 16x2 LCD ekranı kontrol etmek için sürücü.
PCF8574 tabanlı I2C LCD modülleriyle uyumludur.
Kaynak: https://github.com/the-raspberry-pi-guy/lcd
"""

import smbus2
from time import sleep

# LCD Adresi (genellikle 0x27 veya 0x3F)
I2C_ADDR  = 0x27
LCD_WIDTH = 16   # Maksimum karakter sayısı

# LCD Komutları
LCD_CHR = 1 # Karakter gönder
LCD_CMD = 0 # Komut gönder

LCD_LINE_1 = 0x80 # 1. satır adresi
LCD_LINE_2 = 0xC0 # 2. satır adresi

LCD_BACKLIGHT  = 0x08  # Arka ışık açık
# LCD_BACKLIGHT = 0x00  # Arka ışık kapalı

ENABLE = 0b00000100 # Enable bit

def delay_microseconds(microseconds):
    sleep(microseconds / 1_000_000.0)

class lcd:
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        self.lcd_init()

    def lcd_init(self):
        # LCD başlatma dizisi
        self.lcd_byte(0x33, LCD_CMD)
        self.lcd_byte(0x32, LCD_CMD)
        self.lcd_byte(0x06, LCD_CMD)
        self.lcd_byte(0x0C, LCD_CMD)
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)
        sleep(0.0005)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
        # Yüksek nibble
        self.bus.write_byte(I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)
        # Düşük nibble
        self.bus.write_byte(I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        sleep(0.0005)
        self.bus.write_byte(I2C_ADDR, (bits | ENABLE))
        sleep(0.0005)
        self.bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
        sleep(0.0005)

    def lcd_display_string(self, message, line):
        if line == 1:
            self.lcd_byte(LCD_LINE_1, LCD_CMD)
        elif line == 2:
            self.lcd_byte(LCD_LINE_2, LCD_CMD)
        else:
            self.lcd_byte(LCD_LINE_1, LCD_CMD)
        message = message.ljust(LCD_WIDTH, " ")
        for i in range(LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def lcd_clear(self):
        self.lcd_byte(0x01, LCD_CMD)
        sleep(0.0005) 