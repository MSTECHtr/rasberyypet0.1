import RPi.GPIO as GPIO
import time
from datetime import datetime
import smbus2
import I2C_LCD_driver

# --- Pin Tanımları ---
PIR_PIN = 17
BUZZER_PIN = 18
LED_LEFT = 22
LED_RIGHT = 23

# --- GPIO Ayarları ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_LEFT, GPIO.OUT)
GPIO.setup(LED_RIGHT, GPIO.OUT)

# --- LCD Ayarları ---
lcd = I2C_LCD_driver.lcd()

# --- LED Animasyonu ---
def led_blink(times=6, delay=0.1):
    for _ in range(times):
        GPIO.output(LED_LEFT, GPIO.HIGH)
        GPIO.output(LED_RIGHT, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(LED_LEFT, GPIO.LOW)
        GPIO.output(LED_RIGHT, GPIO.LOW)
        time.sleep(delay)

# --- Buzzer Bip ---
def buzzer_beep(times=3, delay=0.15):
    for _ in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(delay)

# --- LCD'de Merhaba ve Saat Göster ---
def show_welcome_and_time():
    now = datetime.now().strftime('%H:%M:%S')
    lcd.lcd_display_string("Merhaba!", 1)
    lcd.lcd_display_string(f"Saat: {now}", 2)

try:
    print("Sistem başlatıldı. Hareket bekleniyor...")
    while True:
        if GPIO.input(PIR_PIN):
            print("Hareket algılandı!")
            buzzer_beep()
            led_blink()
            show_welcome_and_time()
            time.sleep(2)  # Fazla tetiklenmeyi önle
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Çıkılıyor...")
finally:
    lcd.lcd_clear()
    GPIO.cleanup() 