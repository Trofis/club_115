import json
from PIL import Image, ImageFont, ImageDraw, ImageChops
import requests
from datetime import datetime
import os
from enum import Enum

f = open('data_clubs.json')
data_clubs = json.load(f)

class Ligues(Enum):
    GERMANY = 1,
    SPAIN = 2,
    ENGLAND = 3,
    ITALY = 4,
    FRANCE = 5


################# FUNCTIONS ####################

# Remove borders from imgage
# param : im (obj Image)
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

# Replace transparent to white background
# param : im (obj Image)
def transparent(img):
    rgba = img.convert("RGBA")
    datas = rgba.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding yellow colour
            # replacing it with a transparent value
            newData.append((255, 255, 255, 255))
        else:
            newData.append(item)
  
    rgba.putdata(newData)

    return rgba

# Generate correct images
# param : path_clubs_images (String)
#         ligue (Enum Ligues)
def generate_img(ligue):
    ratio = 0.35
    print(os.listdir(get_path_img_per_ligue(ligue)))
    for filename in os.listdir(get_path_img_per_ligue(ligue)):
        print(filename)
        img = Image.open(get_path_img_per_ligue(ligue)+"/"+filename)
        width, height = img.size
        print(img)
        rgba = transparent(img)
        print(rgba)

        rgba = trim(rgba.resize((int(width*ratio),int(height*ratio)), Image.ANTIALIAS))
        print(rgba)

        rgba.save(get_path_img_resized_per_ligue(ligue)+"/"+filename)


# Get league img logo path 
# param : ligue (Enum Ligues)
#         
def get_path_img_per_ligue(ligue):
    if ligue.GERMANY:
        return  data_clubs['path_logo_bundesliga'] 
    elif ligue.SPAIN:
        return  data_clubs['path_logo_seria_a'] 
    elif ligue.ENGLAND:
        return  data_clubs['path_logo_premier_league'] 
    elif ligue.ITALY:
        return  data_clubs['path_logo_seria_a'] 
    return data_clubs['path_logo_ligue_1'] 

# Get league img logo resized path 
# param : ligue (Enum Ligues)
#       
def get_path_img_resized_per_ligue(ligue):
    if ligue.GERMANY:
        return  data_clubs['path_logo_resized_bundesliga'] 
    elif ligue.SPAIN:
        return  data_clubs['path_logo_resized_seria_a'] 
    elif ligue.ENGLAND:
        return  data_clubs['path_logo_resized_premier_league'] 
    elif ligue.ITALY:
        return  data_clubs['path_logo_resized_seria_a'] 
    return data_clubs['path_logo_resized_ligue_1'] 


    
    

################## BUNDESLIGA TEST ####################
# Generate next kick off image
# param : ligue (Enum Ligues)
#       
def generate_next_kick_off(ligue):
    # LOAD IMAGE & COPY
    template = Image.open(data_clubs['path_templates']+"/calendrier_bundesliga.png")
    new_image = template.copy()

    # FONT
    league_gothic = ImageFont.truetype(data_clubs['path_font']+'/league_gothic/LeagueGothic-Regular.otf', 30, layout_engine=ImageFont.LAYOUT_RAQM)
    ruda_bold_teams = ImageFont.truetype(data_clubs['path_font']+'/ruda/Ruda-Bold.ttf', 20, layout_engine=ImageFont.LAYOUT_RAQM)
    ruda_bold_time = ImageFont.truetype(data_clubs['path_font']+'/ruda/Ruda-Bold.ttf', 25, layout_engine=ImageFont.LAYOUT_RAQM)

    # DRAW ON TEMPLATE
    edit_image = ImageDraw.Draw(new_image)

    # LOAD DATA
    f = open('test.json')
    germany = json.load(f)['germany']


    start_height = 260
    for play in germany:
        img = Image.open(get_path_img_per_ligue(ligue)+"/"+filename)

        
        new_image.paste(rgba, (145,start_height-15) )
        new_image.paste(rgba, (890,start_height-15) )

        date_time = datetime.fromisoformat(play[1]) 
        edit_image.text((35,start_height),"{}".format(str(date_time.day)+"/"+str(date_time.month)).upper(), (0,0,0), ruda_bold_time )
        edit_image.text((998,start_height),"{}".format(str(date_time.hour)+":"+str(date_time.minute)).upper(), (0,0,0), ruda_bold_time )
        edit_image.text((220,start_height), play[3][1].upper(), (255,255,255), ruda_bold_teams)
        size = ruda_bold_teams.getsize(play[4][1])
        edit_image.text((872-size[0],start_height), play[4][1], (255,255,255), ruda_bold_teams)
        start_height += 85



    #SAVE IMAGE
    new_image.save(data_clubs['path_render']+"/bundesliga.png", quality=100)

# First when project is load up, need to create right logos
#generate_img(Ligues.GERMANY)

# Generate next kick-off

generate_next_kick_off(Ligues.GERMANY)