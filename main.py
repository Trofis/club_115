import json
from PIL import Image, ImageFont, ImageDraw
import requests

f = open('data_clubs.json')
data_clubs = json.load(f)


################## BUNDESLIGA TEST ####################
# LOAD IMAGE & COPY
template = Image.open(data_clubs['path_templates']+"/calendrier_bundesliga.png")
new_image = template.copy()

#FONT
league_gothic = ImageFont.truetype(data_clubs['path_font']+'/league_gothic/LeagueGothic-Regular.otf', 30, layout_engine=ImageFont.LAYOUT_RAQM)
ruda_bold = ImageFont.truetype(data_clubs['path_font']+'/ruda/Ruda-Bold.ttf', 21, layout_engine=ImageFont.LAYOUT_RAQM)

#DRAW IMAGE
edit_image = ImageDraw.Draw(new_image)

f = open('test.json')
germany = json.load(f)['germany']


start_height = 260
for play in germany:
    edit_image.text((230,start_height), play[3][1], (255,255,255), ruda_bold)
    size = ruda_bold.getsize(play[4][1])
    edit_image.text((868-size[0],start_height), play[4][1], (255,255,255), ruda_bold)
    start_height += 85



#SAVE IMAGE
new_image.save(data_clubs['path_render']+"/bundesliga.png")
