import pandas as pd
import ast
import numpy as np
from .models.Vertex import Vertex
import os

# load data from map.csv
def load_data(mapPath: str) -> list[tuple[int, int]]:
    df = pd.read_csv(mapPath)

    return [(ast.literal_eval(df['adjacent'][idx]),\
            ast.literal_eval(df['address'][idx])) for idx in range(len(df))]

def loadMap(mapPath: str):
    return pd.read_csv(mapPath)

def attach(df):
    return [ast.literal_eval(df['adjacent'][idx]) for idx in range(len(df))]

def detach(list_vertex: list[Vertex]):
    list_by_id = [(vertex.getId(), vertex.getAdjacent(), vertex.getAddress()) 
                  for vertex in list_vertex]
    
    return pd.DataFrame(list_by_id, columns=['id', 'adjacent', 'address'])

def convertGraphToAdj(graphPath: str):
    graph = np.load(graphPath)
    adj = [(vertex, np.where(vector == 1)[0].tolist()) for vertex, vector in enumerate(graph)]

    return pd.DataFrame(adj, columns=['id', 'adjacent'])

def saveMap(df, mapPath: str):
    df.to_csv(mapPath, index=False)
    print(f"Map saved to {mapPath}")


