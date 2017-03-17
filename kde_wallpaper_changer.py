#!/usr/bin/python3
import requests
import re
from random import randint
import shutil
from PIL import Image
from io import BytesIO
import dbus
import os


def regen_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)


def get_wallpapers():
    page = randint(1, 9)
    url = 'https://alpha.wallhaven.cc/search?categories=100&purity=100&resolutions=3840x2160%2C5120x2880&sorting=favorites&order' \
          '=desc&page=' + str(page)
    r = requests.get(url)

    rgxp = re.compile(r'wallpaper/([0-9]*)\"')
    wall_codes = rgxp.findall(r.text)
    wall_number = randint(0, 22)
    r_1 = requests.get('https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + str(wall_codes[wall_number]) + '.jpg')
    r_2 = requests.get('https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-' + str(wall_codes[wall_number+1]) + '.jpg')

    try:
        i_1 = Image.open(BytesIO(r_1.content))
        i_1.save(image_1)
    except:
        pass
    try:
        i_2 = Image.open(BytesIO(r_2.content))
        i_2.save(image_2)
    except:
        pass


def change_wallpapers():
    js_wallpaper_1 = '''
    var allDesktops = desktops();
    d = allDesktops[0];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
    d.writeConfig("Image", "file://%s")
    '''

    js_wallpaper_2 = '''
    var allDesktops = desktops();
    d = allDesktops[1];
    d.wallpaperPlugin = "org.kde.image";
    d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
    d.writeConfig("Image", "file://%s")
    '''

    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')

    plasma.evaluateScript(js_wallpaper_1 % image_1)
    plasma.evaluateScript(js_wallpaper_2 % image_2)


image = randint(1, 100)
path = '/tmp/wallpapers/'
image_1 = path + 'wallpaper' + str(image) + '.jpg'
image_2 = path + 'wallpaper' + str(image + 1) + '.jpg'

regen_dir(path)
get_wallpapers()
change_wallpapers()
