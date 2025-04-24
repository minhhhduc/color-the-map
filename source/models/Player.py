from functools import lru_cache
from .Map import MapGame

class Player:
    @lru_cache(maxsize=1)
    def __init__(self) -> None:
        pass
    
    def setColor(self, map: MapGame, vertexId: int, color: tuple[int, int, int]):
        if map.hasColorAround(vertexId, color):
            return ""
        map.setColorVertex(vertexId, color)
        vertex = map.getVertex(vertexId)
        
        for address in vertex.getAddress():
            map.fill_color(address, color)

        return "Color set successfully"
    
    def setColor(self, map: MapGame, point: tuple[int, int], color: tuple[int, int, int]):
        vertex = map.getVertexByAddress(point)

        self.setColor(map, vertex.getId(), color)
