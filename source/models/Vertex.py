import pygame

class Vertex:
    def __init__(self, vertexId, adjList: list[int]) -> None:
        """
            vertexId: int,
            adjList: list[int],
            name_image: str,
            map_name: str,
        """
        self.__id = vertexId
        self.__adjacent = adjList
        self.__color = None
    
    def setColor(self, color):
        self.__color = color

    def getColor(self):
        return self.__color
    
    def getId(self):
        return self.__id

    def __str__(self):
        return str(self.__id) + ' connected to: ' + str([x for x in self.__adjacent]) + ' color: ' + str(self.__color)