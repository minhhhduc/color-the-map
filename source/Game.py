import numpy as np
import cv2
from .config import COLORS
from .SolveData import *
from .models.Vertex import Vertex
from .models.Map import MapGame

class GameManager:
    def __init__(self, mapDataPath: str, mapImagePath: str, mapName: str):
        self.mapDataPath = mapDataPath
        self.mapImagePath = mapImagePath
        self.mapName = mapName

        self.list_vertex = loadVertex(mapDataPath)
        self.mapGame = MapGame(self.list_vertex, mapName, mapImagePath)
        self.mapImage = self.mapGame.getImage()  # Giữ nguyên BGR
        self.running = True
        self.color = COLORS['white']
        self.ix, self.iy = -1, -1  # Tọa độ chuột
        self.colors = list(COLORS.values())
        self.palette_img = None
        self.palette_width = 100

    def draw_color_palette(self, img_height):
        """Tạo bảng màu (sidebar) chỉ cần vẽ một lần"""
        palette_img = np.ones((img_height, self.palette_width, 3), np.uint8) * 255
        
        box_height = img_height // len(self.colors)
        for i, col in enumerate(self.colors):
            y_start = i * box_height
            y_end = (i + 1) * box_height
            cv2.rectangle(palette_img, (0, y_start), (self.palette_width, y_end), col, -1)
        
        return palette_img

    def draw_shape(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix, self.iy = x, y

            if x >= self.mapImage.shape[1]:
                row = y // (self.mapImage.shape[0] // len(self.colors))
                if row < len(self.colors):
                    self.color = self.colors[row]
                    print(f"Đã chọn màu: {self.color}")
                return
            else:
                self.mapGame.fill_color(x, y, self.color)
                self.mapImage = self.mapGame.getImage()  # Cập nhật ảnh sau khi tô

    def setMap(self, mapImagePath: str):
        self.mapImagePath = mapImagePath
        self.mapGame.setImage(mapImagePath)
        self.mapImage = self.mapGame.getImage()

    def main(self):
        img_height, img_width = self.mapImage.shape[:2]
        self.palette_img = self.draw_color_palette(img_height)

        cv2.namedWindow('Map Editor', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Map Editor', self.draw_shape)

        while self.running:
            combined = np.hstack((self.mapImage, self.palette_img))
            cv2.imshow('Map Editor', combined)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.running = False

        cv2.destroyAllWindows()