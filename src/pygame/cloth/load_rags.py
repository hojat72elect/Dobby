import os
from src.pygame.cloth.read_json import read_json

def load_rags(path: str):
    rag_list = os.listdir(path)
    rags = {}
    for rag in rag_list:
        rags[rag.split('.')[0]] = read_json(f"{path}/{rag}")
    return rags
