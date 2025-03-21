import cv2
import numpy as np

# Đọc ảnh từ file đã tải lên
image_path = "sample/image.png"
image = cv2.imread(image_path)
if image is None:
    print("Không thể mở ảnh!")
    exit()

# Tạo bản sao để thao tác
image_copy = image.copy()

# Tạo cửa sổ hiển thị
cv2.namedWindow("Paint Fill")

# Hàm callback trống cho trackbar
def nothing(x):
    pass

# Tạo thanh kéo chọn màu
cv2.createTrackbar("R", "Paint Fill", 0, 255, nothing)
cv2.createTrackbar("G", "Paint Fill", 0, 255, nothing)
cv2.createTrackbar("B", "Paint Fill", 0, 255, nothing)

# Lấy danh sách màu lân cận (bỏ qua màu đen)
def get_adjacent_colors(x, y):
    adjacent_colors = set()
    h, w, _ = image.shape
    neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 4 hướng chính

    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h:
            color = tuple(image_copy[ny, nx])
            if color != (0, 0, 0):  # Bỏ qua viền đen
                adjacent_colors.add(color)

    return adjacent_colors

# Kiểm tra nếu màu mới vi phạm quy tắc
def is_invalid_fill(x, y, new_color):
    adjacent_colors = get_adjacent_colors(x, y)
    if new_color in adjacent_colors:
        return True  # Không được tô màu vì trùng màu lân cận
    return False

# Xử lý sự kiện chuột
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Khi click chuột trái
        old_color = tuple(image_copy[y, x])  # Lấy màu gốc của điểm click

        if old_color == (0, 0, 0):  # Không tô màu lên viền đen
            print("Cannot fill on black boundary!")
            return

        # Lấy màu từ thanh kéo
        r = cv2.getTrackbarPos("R", "Paint Fill")
        g = cv2.getTrackbarPos("G", "Paint Fill")
        b = cv2.getTrackbarPos("B", "Paint Fill")
        new_color = (b, g, r)  # OpenCV dùng BGR

        # Kiểm tra nếu tô màu này có làm hai vùng màu khác nhau chạm nhau
        if is_invalid_fill(x, y, new_color):
            print("Invalid color: This color would connect different regions!")
            return  # Không tô màu nếu vi phạm

        # Mask cho flood fill
        mask = np.zeros((image.shape[0] + 2, image.shape[1] + 2), np.uint8)

        # Thực hiện tô màu
        cv2.floodFill(image_copy, mask, (x, y), new_color, loDiff=(10, 10, 10), upDiff=(10, 10, 10))

        # Hiển thị ảnh sau khi tô màu
        cv2.imshow("Paint Fill", image_copy)

# Hiển thị ảnh ban đầu và thiết lập callback chuột
cv2.imshow("Paint Fill", image_copy)
cv2.setMouseCallback("Paint Fill", mouse_callback)

# Chờ ESC để thoát
while True:
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
