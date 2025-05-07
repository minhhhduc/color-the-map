from source.SolveData import *
from ai.Solution import *
from source.models.Vertex import Vertex
from source.models.Map import MapGame
from source.config import *
from source.Game import GameManager
import sys

mapName = 'vietnam'

mapDataPath = 'asset/maps/{}.csv'.format(mapName)
mapImagePath = 'asset/image/{}.png'.format(mapName)

def visualize_solution():
    list_vertex = loadVertex(mapDataPath)

    m = MapGame(list_vertex, mapName, mapImagePath)

    model = Solution()
    model.setEdges(m.getEdges())

    model.optimal(0)
    v = 0

    try:
        for v, c in enumerate(model.result()):
            vA = m.getVertex(v).getAddress()[0]
            m.fill_color(vA[0], vA[1], COLORS.values()[c])

        print('map: ')
        for v in m.getVertices():
            print(v)
        m.showMap()

    except Exception as e:
        print(e)
        print(f"vertex {v} no address")
        
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'solution':
        visualize_solution()
        exit(0)
    else:
        gameManager = GameManager(mapDataPath, mapImagePath, mapName)
        gameManager.main()