import gurobipy as gp
import numpy as np
from gurobipy import GRB
from functools import lru_cache


class Solution:
    @lru_cache(maxsize=1)
    def __init__(self) -> None:
        pass

    def setGraph(self, graph: np.ndarray):
        self.__graph = graph
        self.__edges = np.array([(i, j) for i in range(len(graph)) for j in range(len(graph[i])) if graph[i][j] != 0])
        self.__numVertices = len(graph)
        self.__numColors = self.__numVertices
    
    def setEdges(self, edges: list):
        self.__edges = edges
        self.__numVertices = max(max(edges, key=lambda x: x[0])[0], max(edges, key=lambda x: x[1])[1]) + 1
        self.__numColors = self.__numVertices

    def __initModel(self):
        self.__model = gp.Model("Graph Coloring")
        self.__model.setParam('OutputFlag', 0)
        
        self.__x = self.__model.addVars(self.__numVertices, self.__numColors, vtype=GRB.BINARY, name="x")
        self.__y = self.__model.addVars(self.__numColors, vtype=GRB.BINARY, name="y")

        for v in range(self.__numVertices):
            self.__model.addConstr(gp.quicksum(self.__x[v, c] for c in range(self.__numColors)) == 1)
        
        for u, v in self.__edges:
            for c in range(self.__numColors):
                self.__model.addConstr(self.__x[u, c] + self.__x[v, c] <= 1)
        
        for v in range(self.__numVertices):
            for c in range(self.__numColors):
                self.__model.addConstr(self.__x[v, c] <= self.__y[c])

        self.__model.setObjective(gp.quicksum(self.__y[c] for c in range(self.__numColors)), GRB.MINIMIZE)
        
    
    def solve(self, type=1):
        if type == 1:
            self.__initModel()
            opm = self.__model.optimize()
            print("minimize number of colors: %d" % (self.__model.objVal))
            for v in range(self.__numVertices):
                for c in range(self.__numColors):
                    if self.__x[v, c].x > 0.5:
                        print(f"Vertex {v} is colored with color {c}")
        else:
            pass