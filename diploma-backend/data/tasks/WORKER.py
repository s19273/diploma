from facenet_pytorch import MTCNN
import torch
import numpy as np
import cv2
import socket
import pickle
import struct
from PIL import Image, ImageDraw

# PyTorch setup

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(keep_all=True, device=device)

# DETEKCJA 

frame_numpy = cv2.cvtColor(frame_numpy, 0)
frame = Image.fromarray(
    cv2.cvtColor(frame_numpy, cv2.IMREAD_COLOR))
boxes, _ = mtcnn.detect(frame)
boxes = [] if boxes is None else boxes
frame_draw = frame.copy()
draw = ImageDraw.Draw(frame_draw)

## todo zapisz BOXES do zminnej tymczasowej poza tą klasą/pętlą (PREVIOUS_FRAME_BOXES)

for box in boxes: # BOXES = ilosc wykrytych osob
    
    # if (boxes != LAST_BOXES) then 
    #       { postujemy LOG, 
    #       zapisujemy ostatnia klatke jako img lokalnie 
    #       }

    # obiekt LOG {
    #   message = [data godzina minuta sekunda] + {boxes} + " of "
    #   image = box
    # }
    #  
    draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
