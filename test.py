import json
import datetime
from PIL import Image, ImageFont, ImageDraw

f = open('data_clubs.json')
data_clubs = json.load(f)

im1 = Image.open(data_clubs['path_logo_bundesliga']+"/mainz_2.png")
pixels = im1.load()
for i in range(im1.size[0]):
    for j in range(im1.size[1]):
        if pixels[i,j] == (0,0,0,0):
            pixels[i,j] = (255,255,255)

im1.save(data_clubs['path_render']+"/test.png", quality=100)
