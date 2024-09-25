import time
import LiquidCrystal_I2C 
# Giả định bạn đã có lớp lcd từ ví dụ trước (hoặc bạn có thể thay thế bằng LiquidCrystal_I2C nếu đã cài đặt thư viện đó)
lcd = LiquidCrystal_I2C.lcd()  # Thay thế bằng dòng này nếu bạn dùng thư viện LiquidCrystal_I2C
lcd_screen = lcd()  # Sử dụng lớp lcd đã tạo trước

# Xóa màn hình LCD
lcd_screen.clear()

# Hiển thị "Testing...." trên dòng 1 tại vị trí 0
lcd_screen.display("Testing....", 1, 0)
time.sleep(1)

# Xóa màn hình
lcd_screen.clear()

# Vẽ ký tự "*" trên dòng 1 và dòng 2 di chuyển từ trái sang phải
for j in range(1, 3):  # Lặp qua 2 dòng đầu tiên
    for i in range(16):  # Di chuyển qua 16 cột
        lcd_screen.display("*", j, i)
        time.sleep(0.1)

# Xóa màn hình sau khi hoàn thành
lcd_screen.clear()

# Vòng lặp nhập chuỗi từ người dùng và hiển thị lên màn hình
while True:
    try:
        # Hiển thị hướng dẫn cho người dùng
        lcd_screen.display("Enter String you", 1, 0)
        lcd_screen.display("want to display", 2, 0)
        time.sleep(1)
        
        # Yêu cầu người dùng nhập chuỗi và hiển thị chuỗi đó lên dòng 1
        user_input = input("Enter String You Want to Display: ")
        lcd_screen.display(user_input, 1, 0)
        time.sleep(2)
        
        # Xóa màn hình để chuẩn bị cho lần nhập tiếp theo
        lcd_screen.clear()
        
    except KeyboardInterrupt:
        # Dừng vòng lặp khi người dùng nhấn Ctrl+C
        print("Program stopped.")
        break
