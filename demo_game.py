import smbus2
import time
import RPi.GPIO as GPIO
import random

# Địa chỉ I2C của LCD
I2C_ADDR = 0x27
LCD_WIDTH = 16  # Kích thước màn hình LCD 16x2

# Một số hằng số điều khiển LCD
LCD_CHR = 1  # Chế độ ký tự
LCD_CMD = 0  # Chế độ lệnh

LCD_LINE_1 = 0x80  # Địa chỉ của dòng 1 trên LCD
LCD_LINE_2 = 0xC0  # Địa chỉ của dòng 2 trên LCD

# Định nghĩa các chân nút bấm
BUTTON_UP_PIN = 17  # Chân GPIO nút lên
BUTTON_DOWN_PIN = 27  # Chân GPIO nút xuống

# Khởi tạo giao tiếp I2C
bus = smbus2.SMBus(1)

# Thiết lập GPIO cho các nút bấm
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Hàm gửi dữ liệu đến LCD
def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | 0x08
    bits_low = mode | ((bits << 4) & 0xF0) | 0x08

    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

# Bật tín hiệu cho LCD
def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | 0x04))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~0x04))
    time.sleep(0.0005)

# Khởi tạo LCD
def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.0005)

# Viết chuỗi lên màn hình LCD, chỉ cập nhật ký tự thay đổi
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Hiển thị vật thể và chướng ngại vật trên màn hình LCD
def display_objects(player_pos, obstacles):
    line1 = [' '] * LCD_WIDTH
    line2 = [' '] * LCD_WIDTH

    # Cập nhật vị trí vật cản
    for pos, line in obstacles:
        if line == 1:
            line1[pos] = 'O'
        elif line == 2:
            line2[pos] = 'O'

    # Cập nhật vị trí người chơi
    if player_pos == 1:
        line1[0] = 'P'
    else:
        line2[0] = 'P'

    # Hiển thị lên màn hình
    lcd_string("".join(line1), LCD_LINE_1)
    lcd_string("".join(line2), LCD_LINE_2)

# Tạo vật cản với khoảng cách cách nhau ít nhất 3 ô
def generate_obstacles(obstacles):
    new_obstacles = []
    for pos, line in obstacles:
        if pos > 0:
            new_obstacles.append((pos - 1, line))

    # Kiểm tra xem có thể tạo thêm vật cản mới không
    if len(new_obstacles) == 0 or new_obstacles[-1][0] < (LCD_WIDTH - 4):
        # Tạo ngẫu nhiên chướng ngại vật, dòng 1 hoặc dòng 2
        line = random.choice([1, 2])
        new_obstacles.append((LCD_WIDTH - 1, line))

    return new_obstacles

# Hàm chính điều khiển trò chơi
def main():
    lcd_init()

    # Vị trí khởi tạo
    player_position = 1  # Người chơi ban đầu ở dòng 1
    obstacles = [(LCD_WIDTH - 1, random.choice([1, 2]))]  # Tạo chướng ngại vật ban đầu
    speed = 0.3  # Tốc độ di chuyển chướng ngại vật ban đầu

    prev_player_position = player_position
    prev_obstacles = obstacles.copy()

    while True:
        # Điều khiển người chơi di chuyển lên hoặc xuống
        if GPIO.input(BUTTON_UP_PIN) == GPIO.LOW:
            player_position = 1  # Di chuyển người chơi lên dòng 1
            display_objects(player_position, obstacles)
            time.sleep(0.1)  # Debounce với tốc độ nhanh hơn

        if GPIO.input(BUTTON_DOWN_PIN) == GPIO.LOW:
            player_position = 2  # Di chuyển người chơi xuống dòng 2
            display_objects(player_position, obstacles)
            time.sleep(0.1)  # Debounce với tốc độ nhanh hơn

        # Di chuyển chướng ngại vật
        obstacles = generate_obstacles(obstacles)

        # Chỉ cập nhật phần thay đổi để tránh nhấp nháy
        display_objects(player_position, obstacles)

        # Kiểm tra va chạm
        if any(pos == 0 and line == player_position for pos, line in obstacles):
            lcd_string("GAME OVER", LCD_LINE_1)
            break

        # Tăng dần tốc độ trò chơi
        speed = max(0.05, speed - 0.001)

        time.sleep(speed)  # Tốc độ di chuyển của chướng ngại vật

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)  # Xóa màn hình LCD
        GPIO.cleanup()  # Dọn dẹp GPIO
