import json
from PIL import Image, ImageFont, ImageDraw, ImageChops
import requests
from datetime import datetime
import os
import glob
from enum import Enum

f = open('data_clubs.json')
data_clubs = json.load(f)


class Ligues(Enum):
    Germany = 1,
    Spain = 2,
    England = 3,
    Italy = 4,
    France = 5


################# FUNCTIONS ####################


def init():
    if not os.path.isdir(data_clubs['path_logo_resized_bundesliga']):
        os.mkdir(data_clubs['path_logo_resized_bundesliga'])

    if not os.path.isdir(data_clubs['path_logo_resized_seria_a']):
        os.mkdir(data_clubs['path_logo_resized_seria_a'])

    if not os.path.isdir(data_clubs['path_logo_resized_liga']):
        os.mkdir(data_clubs['path_logo_resized_liga'])

    if not os.path.isdir(data_clubs['path_logo_resized_ligue_1']):
        os.mkdir(data_clubs['path_logo_resized_ligue_1'])

    if not os.path.isdir(data_clubs['path_logo_resized_premier_league']):
        os.mkdir(data_clubs['path_logo_resized_premier_league'])

# Remove borders from imgage
# param : im (obj Image)


def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
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


# Delete images from ligue directory
# param : lige (Enum Ligues)
def delete_imgs(ligue):
    files = glob.glob(get_path_img_resized_per_ligue(ligue)+"/*.png")
    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


# Generate correct images
# param : path_clubs_images (String)
#         ligue (Enum Ligues)
def generate_img(ligue):
    ratio = 0.35
    # Delete existing render images before generating new ones
    delete_imgs(ligue)

    print("###### GENERATING LOGOS {} #######".format(ligue.name))
    for filename in os.listdir(get_path_img_per_ligue(ligue)):
        print(filename)
        img = Image.open(get_path_img_per_ligue(ligue)+"/"+filename)
        width, height = img.size
        #rgba = img.convert("RGBA")

        #rgba = transparent(img)
        resized_img = img.resize((65, 65))
        # rgba = trim(rgba.resize(
        #    (int(width*ratio), int(height*ratio)), Image.ANTIALIAS))
        rgba = resized_img.convert("RGBA")

        rgba.save(get_path_img_resized_per_ligue(ligue)+"/"+filename)


# Get league img logo path
# param : ligue (Enum Ligues)
#
def get_path_img_per_ligue(ligue):
    if ligue == Ligues.Germany:
        return data_clubs['path_logo_bundesliga']
    elif ligue == ligue.Spain:
        return data_clubs['path_logo_liga']
    elif ligue == ligue.England:
        return data_clubs['path_logo_premier_league']
    elif ligue == ligue.Italy:
        return data_clubs['path_logo_seria_a']
    return data_clubs['path_logo_ligue_1']

# Get league img logo resized path
# param : ligue (Enum Ligues)
#


def get_path_img_resized_per_ligue(ligue):
    if ligue == ligue.Germany:
        return data_clubs['path_logo_resized_bundesliga']
    elif ligue == ligue.Spain:
        return data_clubs['path_logo_resized_liga']
    elif ligue == ligue.England:
        return data_clubs['path_logo_resized_premier_league']
    elif ligue == ligue.Italy:
        return data_clubs['path_logo_resized_seria_a']
    return data_clubs['path_logo_resized_ligue_1']


################## BUNDESLIGA TEST ####################
# Generate next kick off image
# param : ligue (Enum Ligues)
#
def generate_next_kick_off(ligue):
    # LOAD IMAGE & COPY
    template = Image.open(
        data_clubs['path_templates']+"/calendrier_bundesliga.png")
    new_image = template.copy()

    # FONT
    league_gothic = ImageFont.truetype(
        data_clubs['path_font']+'/league_gothic/LeagueGothic-Regular.otf', 30, layout_engine=ImageFont.LAYOUT_RAQM)
    ruda_bold_teams = ImageFont.truetype(
        data_clubs['path_font']+'/ruda/Ruda-Bold.ttf', 20, layout_engine=ImageFont.LAYOUT_RAQM)
    ruda_bold_time = ImageFont.truetype(
        data_clubs['path_font']+'/ruda/Ruda-Bold.ttf', 25, layout_engine=ImageFont.LAYOUT_RAQM)

    # DRAW ON TEMPLATE
    edit_image = ImageDraw.Draw(new_image)

    # LOAD DATA
    f = open('coming_rounds.json')
    Germany = json.load(f)[ligue.name]

    start_height = 260
    for play in Germany:
        img1 = Image.open(get_path_img_resized_per_ligue(
            ligue)+"/"+play["team_name_home"]+".png")

        img2 = Image.open(get_path_img_resized_per_ligue(
            ligue)+"/"+play["team_name_away"]+".png")

        rgba1 = img1.convert("RGBA")
        rgba2 = img2.convert("RGBA")

        new_image.paste(img1, (145, start_height-15), img1)
        new_image.paste(img2, (890, start_height-15), img2)

        date_time = datetime.fromisoformat(play["event_date"])
        edit_image.text((35, start_height), "{}".format(
            str(date_time.day)+"/"+str(date_time.month)).upper(), (0, 0, 0), ruda_bold_time)
        edit_image.text((998, start_height), "{}".format(
            str(date_time.hour)+":"+str(date_time.minute)).upper(), (0, 0, 0), ruda_bold_time)
        edit_image.text((220, start_height),
                        play["team_name_home"].upper(), (255, 255, 255), ruda_bold_teams)
        size = ruda_bold_teams.getsize(play["team_name_away"].upper())
        edit_image.text((872-size[0], start_height),
                        play["team_name_away"].upper(), (255, 255, 255), ruda_bold_teams)
        start_height += 85

    # SAVE IMAGE
    new_image.save(data_clubs['path_render']+"/bundesliga.png", quality=100)


# Init project
init()

# First when project is load up, need to create right logos
generate_img(Ligues.Germany)
generate_img(Ligues.France)
generate_img(Ligues.Spain)
generate_img(Ligues.Italy)
generate_img(Ligues.England)


# Generate next kick-off

# generate_next_kick_off(Ligues.Germany)
