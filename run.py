from source.SolveData import *
from ai.Solution import *
from source.models.Vertex import Vertex
from source.models.Map import MapGame
import numpy as np
from source.iconfig import *

mapDataPath = 'asset/maps/demo.csv'
mapImagePath = 'asset/image/image.png'
mapName = 'demo'

def visualize_solution():
    df = loadMap(mapDataPath)

    list_vertex = []

    for id, adj, address in attach(df):
        list_vertex.append(Vertex(id, adj, address))

    m = MapGame(list_vertex, mapName, mapImagePath)

    model = Solution()
    model.setEdges(m.getEdges())

    model.optimal(0)
    v = 0
    try:
        for v, c in enumerate(model.result()):
            vA = m.getVertex(v).getAddress()[0]
            m.fill_color(vA[0], vA[1], COLORS[c])

        print('map: ')
        for v in m.getVertices():
            print(v)
        m.showMap()

    except Exception as e:
        print(e)
        print(f"vertex {v} no address")
    
visualize_solution()
