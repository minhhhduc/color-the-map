import gurobipy as gp
import numpy as np
from gurobipy import GRB

class Solution:
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
        self.__graph = np.zeros((self.__numVertices, self.__numVertices))
        edges = np.array(edges)
        self.__graph[edges[:, 0], edges[:, 1]] = 1
        self.__graph[edges[:, 1], edges[:, 0]] = 1
    
    def getGraph(self):
        return self.__graph
    
    def getEdges(self):
        return self.__edges

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
        
    def __backtrackSolution(self):
        def is_safe(graph, colors, vertex, c):
            for neighbor in range(len(graph)):
                if graph[vertex][neighbor] == 1 and colors[neighbor] == c:
                    return False
            return True

        def graph_coloring_util(graph, m, colors, vertex):
            if vertex == len(graph):
                return True

            for c in range(1, m + 1):
                if is_safe(graph, colors, vertex, c):
                    colors[vertex] = c
                    if graph_coloring_util(graph, m, colors, vertex + 1):
                        return True
                    colors[vertex] = 0

            return False

        def graph_coloring(graph, m):
            colors = [0] * len(graph)
            if graph_coloring_util(graph, m, colors, 0):
                return colors
            else:
                return 'No solution'

        self.__result = graph_coloring(self.__graph, self.__numColors)
        minColors = len(set(self.__result))
        print(f"minimize number of colors: {minColors}")
        for v, c in enumerate(self.__result):
            print(f"Vertex {v} is colored with color {c}")

    def __LPSolution(self):
        self.__initModel()
        self.__model.optimize()
        self.__result = []
        print("minimize number of colors: %d" % (self.__model.objVal))
        for v in range(self.__numVertices):
            for c in range(self.__numColors):
                if self.__x[v, c].x > 0.5:
                    print(f"Vertex {v} is colored with color {c}")
                    self.__result.append(c)

    def optimal(self, type=1):
        if type == 1:
            self.__LPSolution()
        else:
            self.__backtrackSolution()

    def result(self):
        return self.__result