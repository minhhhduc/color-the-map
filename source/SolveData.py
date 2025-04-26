import pandas as pd
import ast
import numpy as np
from .models.Vertex import Vertex
import cv2
import os

# load data from map.csv
def load_data(mapPath: str) -> list[tuple[int, int]]:
    df = pd.read_csv(mapPath)

    return [(ast.literal_eval(df['adjacent'][idx]),\
            ast.literal_eval(df['address'][idx])) for idx in range(len(df))]

def loadMap(mapPath: str):
    return pd.read_csv(mapPath)

def attach(df: pd.DataFrame):
    keys = df.columns

    llist = [df[key].to_list() for key in keys]
    n, m = np.shape(llist)

    for i in range(n):
        for j in range(m):
            llist[i][j] = ast.literal_eval(str(llist[i][j]))
    
    return zip(*llist)

def detach(list_vertex: list[Vertex]):
    list_by_id = [(vertex.getId(), vertex.getAdjacent(), vertex.getAddress()) 
                  for vertex in list_vertex]
    
    return pd.DataFrame(list_by_id, columns=['id', 'adjacent', 'address'])

def convertGraphToAdj(graphPath: str):
    graph = np.load(graphPath)
    adj = [(vertex, np.where(vector == 1)[0].tolist(), []) for vertex, vector in enumerate(graph)]
    return pd.DataFrame(adj, columns=['id', 'adjacent', 'address'])

def saveMap(df, mapPath: str):
    df.to_csv(mapPath, index=False)
    print(f"Map saved to {mapPath}")

def loadVertex(df: pd.DataFrame, mapDataPath: str):
    if not os.path.exists(mapDataPath):
        raise FileNotFoundError(f"Map data file {mapDataPath} not found.")
    
    df = loadMap(mapDataPath)

    list_vertex = []

    for id, adj, address in attach(df):
        list_vertex.append(Vertex(id, adj, address))
    
    return list_vertex

def loadImage(imagePath: str):
    if not os.path.exists(imagePath):
        raise FileNotFoundError(f"Image file {imagePath} not found.")
    
    image = cv2.imread(imagePath)
    if image is None:
        raise ValueError(f"Could not read image file {imagePath}.")
    
    image = cv2.resize(image, (1100, 750))

    return image