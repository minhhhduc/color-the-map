from functools import lru_cache
from .Map import MapGame
from pygame import Color
import pygame

class Player:
    @lru_cache(maxsize=1)
    def __init__(self, mapGames: list[MapGame]) -> None:
        self.__id = mapGames


    def setColor(self, mapGame: MapGame, vertexId, color: Color):
        mapGame.setColor(vertexId, color)

    def getColor(self, mapGame: MapGame, vertexId):
        return mapGame.getColor(vertexId)

    def flood_fill(self, image, x, y, new_color):
        """Hàm đổ màu nhưng dừng lại khi gặp viền đen."""
        new_image = image.copy()
        pixels = pygame.surfarray.array3d(new_image)

        width, height = new_image.get_size()
        old_color = pixels[x, y].tolist()

        if old_color == list(new_color) or old_color == [0, 0, 0]:  # Không tô nếu màu đen
            return new_image

        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()

            if cx < 0 or cy < 0 or cx >= width or cy >= height:
                continue
            
            if list(pixels[cx, cy]) == old_color and self.can_fill(new_image, cx, cy, new_color):
                pixels[cx, cy] = new_color

                stack.append((cx + 1, cy))
                stack.append((cx - 1, cy))
                stack.append((cx, cy + 1))
                stack.append((cx, cy - 1))

        return pygame.surfarray.make_surface(pixels)
    
    def can_fill(image, x, y, new_color):
        """Kiểm tra xem pixel có thể được tô màu không.
        
        - Không tô nếu tiếp giáp màu giống `new_color`, trừ khi viền là màu đen (0,0,0).
        """
        width, height = image.get_size()
        pixels = pygame.surfarray.array3d(image)  # Chuyển ảnh thành ma trận RGB

        # Màu gốc tại vị trí (x, y)
        old_color = pixels[x, y].tolist()

        # Nếu điểm cần tô đã có màu `new_color`, không tô
        if old_color == list(new_color):
            return False

        # Danh sách các pixel lân cận (trái, phải, trên, dưới)
        neighbors = [
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1)
        ]

        for nx, ny in neighbors:
            if 0 <= nx < width and 0 <= ny < height:
                neighbor_color = pixels[nx, ny].tolist()

                # Nếu pixel kề có màu giống `new_color`, chỉ được phép nếu nó là màu đen
                if neighbor_color == list(new_color) and neighbor_color != [0, 0, 0]:
                    return False  # Không được tô màu

        return True