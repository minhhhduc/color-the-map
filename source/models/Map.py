from .Vertex import Vertex
import numpy as np
import pygame

class MapGame:
    def __init__(self, edges: list[tuple[int, int]], map_path, map_name) -> None:
        self.__graph = {}
        self.__edges = edges
        self.__normalVertex()
        self.__addVertex()
        self.__map_path = map_path
        self.__image = pygame.image.load(map_path)
        self.__map_name = map_name
    
    def __normalVertex(self):
        for edge in self.__edges:
            if edge[0] not in self.__graph:
                self.__graph[edge[0]] = []
            if edge[1] not in self.__graph:
                self.__graph[edge[1]] = []
            self.__graph[edge[0]].append(edge[1])
            self.__graph[edge[1]].append(edge[0])
        
    def __addVertex(self):
        self.__vertices = []
        for k, v in self.__graph.items():
            self.__vertices.append(Vertex(k, v))

    def canSetColor(self, vertexId, color):
        for neighbor in self.__graph[vertexId]:
            if self.__vertices[neighbor].getColor() == color:
                return False
        return True
    
    def setColor(self, vertexId, color):
        if self.canSetColor(vertexId, color):
            self.__vertices[vertexId].setColor(color)
    
    def getImage(self):
        return self.__image

    def __str__(self):
        return [vertex.__str__() for vertex in self.__vertices].__str__()