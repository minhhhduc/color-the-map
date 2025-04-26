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

        self.list_vertex = loadVertex(mapDataPath, mapDataPath)
        self.mapGame = MapGame(self.list_vertex, mapName, mapImagePath)
        self.mapImage = self.mapGame.getImage()
        self.mapImage = cv2.cvtColor(self.mapImage, cv2.COLOR_BGR2RGB)
        self.running = True
        self.color = COLORS['white']
        self.ix, self.iy = -1, -1  # Mouse coordinates
        self.colors = list(COLORS.values())

    def draw_color_palette(self, img_height):
        """Create a color palette sidebar"""
        palette_width = 100
        palette_img = np.ones((img_height, palette_width, 3), np.uint8) * 255
        
        # Calculate color box height based on number of colors
        box_height = img_height // len(self.colors)
        
        for i, col in enumerate(self.colors):
            y_start = i * box_height
            y_end = (i + 1) * box_height
            cv2.rectangle(palette_img, (0, y_start), (palette_width, y_end), col[::-1], -1)
        
        return palette_img, palette_width

    def draw_shape(self, event, x, y, flags, param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            self.ix, self.iy = x, y
            # Check if clicking in palette area
            if x >= self.mapImage.shape[1]:
                row = y // (self.mapImage.shape[0] // len(self.colors))
                if row < len(self.colors):
                    self.color = self.colors[row][::-1]  # Convert RGB to BGR
                    print(f"Selected color: {self.color}")
                return
            else:
                self.mapGame.fill_color(x, y, self.color)  # Fill color on map image
                self.mapImage = self.mapGame.getImage()

    def setMap(self, mapImagePath: str):
        self.mapImagePath = mapImagePath
        self.mapGame.setImage(mapImagePath)
        self.mapImage = self.mapGame.getImage()
        self.mapImage = cv2.cvtColor(self.mapImage, cv2.COLOR_BGR2RGB)

    def main(self):
        
        # Get image dimensions
        img_height, img_width = self.mapImage.shape[:2]
        
        # Create color palette
        palette, palette_width = self.draw_color_palette(img_height)
        
        # Create window
        cv2.namedWindow('Map Editor', cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('Map Editor', self.draw_shape)

        
        while self.running:
            # Update palette in case colors changed
            palette, palette_width = self.draw_color_palette(img_height)
            
            # Combine map and palette
            combined = np.hstack((self.mapImage, palette))
            
            cv2.imshow('Map Editor', combined)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        cv2.destroyAllWindows()
