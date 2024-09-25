import time
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.lcd import character

# Thiết lập thông số cho màn hình LCD
serial = i2c(port=1, address=0x27)  # Địa chỉ I2C của LCD
lcd = character(serial)

# Kích thước của màn hình LCD
lcd_width = 16  # Số cột
lcd_height = 2  # Số hàng

# Vật cản và vật thể T
obstacle = "X"
empty_space = " "
T = "T"

# Vị trí ban đầu của vật thể T
t_position = [0, 0]  # (hàng, cột)

# Thiết lập GPIO
button_up = 17  # Chân GPIO cho nút bấm lên
button_down = 27  # Chân GPIO cho nút bấm xuống

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Hàm hiển thị trạng thái trên LCD
def display(lcd, obstacles, t_position):
    lcd.clear()
    for row in range(lcd_height):
        line = ""
        for col in range(lcd_width):
            if [row, col] == t_position:
                line += T
            elif [row, col] in obstacles:
                line += obstacle
            else:
                line += empty_space
        lcd.display(line)

# Hàm di chuyển vật cản
def move_obstacles():
    obstacles = []
    for row in range(lcd_height):
        for col in range(lcd_width):
            if col % 4 == 0 and col < lcd_width:  # Vật cản cách nhau 3 ô
                obstacles.append([row, col])
    return obstacles

# Chương trình chính
try:
    while True:
        obstacles = move_obstacles()  # Tạo danh sách vật cản
        for i in range(lcd_width + 1):
            # Cập nhật vị trí của vật cản
            obstacles = [[row, col - 1] if col > 0 else [row, lcd_width - 1] for row, col in obstacles]
            display(lcd, obstacles, t_position)  # Hiển thị trạng thái lên LCD
            
            # Kiểm tra nút bấm
            if GPIO.input(button_up) == GPIO.LOW and t_position[0] > 0:  # Di chuyển lên
                t_position[0] -= 1
                time.sleep(0.2)  # Tránh nhấn nhiều lần
            if GPIO.input(button_down) == GPIO.LOW and t_position[0] < lcd_height - 1:  # Di chuyển xuống
                t_position[0] += 1
                time.sleep(0.2)  # Tránh nhấn nhiều lần
            
            time.sleep(0.2)  # Thời gian giữa các khung hình

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()  # Dọn dẹp GPIO
    lcd.clear()  # Xóa màn hình khi dừng
