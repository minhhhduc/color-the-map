import cv2
import os

from source.SolveData import *
from source.models.Vertex import Vertex

graphInit = 'sample/vietnam.npy'
mapInit = 'asset/maps/demo.csv'
mapSave = 'asset/maps/demo.csv'
idxPath = 'sample/currentIdx.txt'
imagePath = 'asset/image/image.png'

# Load data and initialize variables

if not os.path.exists(mapInit):
    df = convertGraphToAdj(graphInit)
    saveMap(df, mapInit)
    

df = loadMap(mapInit)
list_vertex = []
idx = open(idxPath).readline()
idx = int(idx.strip()) if idx.strip() else 0
dict_address = {idx: []}
# Create Vertex objects

for id, adj, address in attach(df):
    list_vertex.append(Vertex(id, adj, address))
    dict_address[id] = address

# Load and resize the image
image = cv2.imread(imagePath)
image = cv2.resize(image, (1100, 750))

print(idx)
# Mouse callback function to capture coordinates
def get_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"idx: {idx}, Coordinates: ({x}, {y})")
        dict_address[idx].append((x, y))

# Set up OpenCV window and callback
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', get_coordinates)

# Main loop
while True:
    cv2.imshow('Image', image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to exit
        break
    elif key == ord('n'):  # Press 'c' to create a new group
        idx += 1
        if idx > len(list_vertex):
            print("finished")
            break
        print(f"next idx: {idx}")
        # dict_address[idx] = []
    elif key == ord('b'):
        idx -= 1
        if idx < 0:
            idx = 0
        print(f"previous idx: {idx}")
# Clean up OpenCV resources
cv2.destroyAllWindows()

# Assign addresses to vertices
for vertex in list_vertex:
    if vertex.getId() in dict_address and dict_address[vertex.getId()]:
        vertex.setAddress(dict_address[vertex.getId()])
    # print(vertex)

print(detach(list_vertex))

# save currentIdx
with open(idxPath, 'w') as f:
    f.write(str(idx))

# save map
saveMap(detach(list_vertex), mapSave)