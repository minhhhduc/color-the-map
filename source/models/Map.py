from .Vertex import Vertex
import numpy as np
import cv2

class MapGame:
    
    def __init__(self, vertices: list[Vertex], name: str, imagePath: str):
        self.__vertices = vertices
        self.__name = name
        self.img = cv2.imread(imagePath)
        self.img = cv2.resize(self.img, (1100, 750))
        self.original = self.img.copy()
        self.h, self.w = self.img.shape[:2]
        self.mask = np.zeros((self.h + 2, self.w + 2), np.uint8)
        pass
    
    def getVertices(self):
        return self.__vertices
    
    def getVertex(self, vertexId: int):
        assert(vertexId < len(self.__vertices))
        
        return self.__vertices[vertexId]
    
    def getName(self):
        return self.__name
    
    def setName(self, name: str):
        self.__name = name

    def setColorVertex(self, vertexId: int, color: tuple[int, int, int]):
        assert(vertexId < self.__vertices)

        return self.__vertices[vertexId].setColor(color)
    
    def getImage(self):
        return self.img

    def hasColorAround(self, vertexId: int, color: tuple[int, int, int]):
        assert(vertexId < self.__vertices)

        for vertex in self.__vertices[vertexId].getAdjacent():
            if self.__vertices[vertex].getColor() == color:
                return True
        return False

    def getEdges(self):
        edges = []
        for vertex in self.__vertices:
            for adj in vertex.getAdjacent():
                edges.append((vertex.getId(), adj))
        return edges

    def getVertexByAddress(self, address: tuple[int, int]):
        pass

    def fill_color(self, x, y, color):
        """ color is a tuple (R, G, B) """
        current_color = self.img[y, x]  # BGR

        if np.all(current_color == [0, 0, 0]):
            print("⛔ Không thể tô lên viền đen.")
            return  # Không làm gì nếu là màu đen

        color_bgr = tuple(color)  # RGB → BGR
        tolerance = 25
        self.mask[:] = 0  # Reset lại mask
        cv2.floodFill(self.img, self.mask, (x, y), color_bgr,
                    loDiff=(tolerance,) * 3,
                    upDiff=(tolerance,) * 3)
        for vertex in self.__vertices:
            for x_0, y_0 in vertex.getAddress():
                if x_0 == x and y_0 == y:
                    vertex.setColor(color)
                    return

    def showMap(self):
        cv2.imshow(self.__name, self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def __str__(self):
        return [vertex.__str__() for vertex in self.__vertices].__str__()