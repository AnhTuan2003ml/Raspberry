import time
import I2C_LCD_driver
import RPi.GPIO as GPIO
import random

# Thiết lập GPIO cho nút nhấn
UP_BUTTON_PIN = 17
DOWN_BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Khởi tạo màn hình LCD
lcd = I2C_LCD_driver.lcd()

# Các tham số trò chơi
lcd_width = 16
lcd_height = 2
obstacle_positions = [random.randint(0, 1) for _ in range(4)]  # Vị trí của 4 vật cản
player_position = 0  # Vị trí của vật thể T
speed = 0.1  # Tốc độ di chuyển

try:
    while True:
        # Xóa màn hình
        lcd.lcd_clear()

        # Hiển thị vật thể T
        for row in range(lcd_height):
            if row == player_position:
                lcd.lcd_display_string('T', 1)
            else:
                lcd.lcd_display_string(' ', 1)

        # Hiển thị các vật cản
        for i in range(len(obstacle_positions)):
            if obstacle_positions[i] == 0:
                lcd.lcd_display_string('X', lcd_width - (i*4 + 1))
            else:
                lcd.lcd_display_string(' ', lcd_width - (i*4 + 1))

        # Di chuyển các vật cản sang trái
        for i in range(len(obstacle_positions)):
            if obstacle_positions[i] > 0:
                obstacle_positions[i] -= 1
            
            # Khi vật cản ra ngoài màn hình, tạo vật cản mới
            if obstacle_positions[i] < 0:
                obstacle_positions[i] = 1
                obstacle_positions[i] = random.randint(0, 1)

        # Kiểm tra nút nhấn để di chuyển vật thể T
        if GPIO.input(UP_BUTTON_PIN) == GPIO.LOW and player_position > 0:
            player_position -= 1
            time.sleep(0.1)  # Thời gian trễ để tránh nhấn liên tục
        elif GPIO.input(DOWN_BUTTON_PIN) == GPIO.LOW and player_position < lcd_height - 1:
            player_position += 1
            time.sleep(0.1)  # Thời gian trễ để tránh nhấn liên tục

        time.sleep(speed)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
