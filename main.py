import json
from PIL import Image, ImageFont, ImageDraw

f = open('data_clubs.json')
data_clubs = json.load(f)


################## BUNDESLIGA TEST ####################
# LOAD IMAGE & COPY
template = Image.open(data_clubs['path_templates']+"/calendrier_bundesliga.png")
new_image = template.copy()

#FONT
league_gothic = ImageFont.truetype(data_clubs['path_font']+'/league_gothic/LeagueGothic-Regular.otf', 30)
ruda_bold = ImageFont.truetype(data_clubs['path_font']+'/ruda/Ruda-Bold.ttf', 21)

#DRAW IMAGE
edit_image = ImageDraw.Draw(new_image)
start_height = 260
for i in range(9):
    edit_image.text((335,start_height), "FC Augsburg", (255,255,255), ruda_bold)
    edit_image.text((704,start_height), "FC Augsburg", (255,255,255), ruda_bold)
    start_height += 87



#SAVE IMAGE
new_image.save(data_clubs['path_render']+"/bundesliga.png")
