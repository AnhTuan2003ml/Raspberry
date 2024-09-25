import time
import random
import RPi.GPIO as GPIO
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from LiquidCrystal_I2C import lcd # Đảm bảo rằng tệp LiquidCrystal_I2C.py nằm trong cùng thư mục

# Thiết lập GPIO cho nút nhấn
UP_BUTTON_PIN = 17
DOWN_BUTTON_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(UP_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DOWN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Khởi tạo màn hình LCD
lcd_screen = lcd()
lcd_width = 16
lcd_height = 2

# Các tham số trò chơi
obstacle_positions = [lcd_width - 1, lcd_width - 5, lcd_width - 9, lcd_width - 13]  # Vị trí ban đầu của các vật cản
player_position = 0  # Vị trí của vật thể T
speed = 0.2  # Tốc độ di chuyển

try:
    while True:
        # Xóa màn hình
        lcd_screen.clear()

        # Hiển thị vật thể T
        for row in range(lcd_height):
            if row == player_position:
                lcd_screen.display_line('T', row + 1)

        # Hiển thị các vật cản
        for pos in obstacle_positions:
            if pos >= 0:
                lcd_screen.display_char('X', player_position + 1, pos)
        
        # Di chuyển các vật cản sang trái
        for i in range(len(obstacle_positions)):
            obstacle_positions[i] -= 1
            
            # Khi vật cản ra ngoài màn hình, tạo vật cản mới
            if obstacle_positions[i] < 0:
                obstacle_positions[i] = lcd_width - 1  # Đặt lại vị trí vật cản mới ở bên phải

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
