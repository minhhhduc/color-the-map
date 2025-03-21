import pandas as pd
import os

edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4)]

def load_data(mapName: str) -> list[tuple[int, int]]:
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), f'{mapName}.csv'))

    return list(zip(data['u'].tolist(), data['v'].tolist()))