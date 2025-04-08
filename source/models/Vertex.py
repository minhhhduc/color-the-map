import numpy as np

class Vertex:
    def __init__(self, vertexId, adjList, address = None) -> None:
        """
            vertexId: int,
            adjList: list[int],
            address: np.array([(x, y)])
        """
        self.__id = vertexId
        self.__adjacent = adjList
        self.__color = None
        if address:
            self.__address = []
        else:
            self.__address = []

    def setColor(self, color):
        self.__color = color

    def getColor(self):
        return self.__color
    
    def getId(self):
        return self.__id

    def addAddress(self, address):
        self.__address.append(address)

    def getAddress(self):
        return self.__address


    def setAddress(self, address):
        self.__address = address

    def getAdjacent(self):
        return self.__adjacent
    
    def __str__(self):
        return str(self.__id) + ' -- connected to: ' + \
            str([x for x in self.__adjacent]) + ' -- color: ' + \
            str(self.__color) + ' -- address: ' + \
            str(self.__address)