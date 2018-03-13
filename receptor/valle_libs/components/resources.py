# @Author: Manuel Rodriguez <valle>
# @Date:   08-Jul-2017
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 27-Feb-2018
# @License: Apache license vesion 2.0


import os
try:
    FA_ENTER = unichr(0xf090)
except Exception as e:
    unichr = lambda s: chr(s)

PATH_RES = os.path.join(os.path.dirname(__file__), "res")
PATH_FONT = os.path.join(PATH_RES, "fonts")
PATH_ICON = os.path.join(PATH_RES, "icon")
PATH_IMG = os.path.join(PATH_RES, "img")
FONT_AWESOME = os.path.join(PATH_FONT, "fontawesome-webfont.ttf")
IMG_SHADOW = os.path.join(PATH_IMG, 'shadow.png')
IMG_SHADOW_REC = os.path.join(PATH_IMG, 'shadow_rec.png')

FA_ENTER = unichr(0xf090)
FA_EDIT = unichr(0xf040)
FA_BOOKS = unichr(0xf2b9)
FA_CHART = unichr(0xf1fe)
FA_UNIVERSITY = unichr(0xf19c)
FA_CUBES = unichr(0xf1b3)
FA_DATABSE = unichr(0xf1c0)
FA_COGS = unichr(0xf085)
FA_TRUCK = unichr(0xf0d1)
FA_EUR = unichr(0xf153)
FA_ANGLE_RIGHT = unichr(0xf105)
FA_ANGLE_LEFT = unichr(0xf104)
FA_CHEVRON_LEFT = unichr(0xf053)
FA_USERS = unichr(0xf0c0)
FA_CHECK = unichr(0xf00c)
FA_LIST = unichr(0xf03a)
FA_CUBE = unichr(0xf1b2)
FA_FOLDER = unichr(0xf07b)
FA_TABLE = unichr(0xf0ce)
FA_SPINNER = unichr(0xf110)
FA_CIRCLE = unichr(0xf1ce)
FA_REFRESH = unichr(0xf021)
FA_CUTLERY = unichr(0xf0f5)
FA_PLUS = unichr(0xf067)
FA_TRASH = unichr(0xf1f8)
FA_QUESTION = unichr(0xf128)
FA_HANDSHAK_O = unichr(0xf2b5)
FA_LEMON = unichr(0xf094)
FA_BAN = unichr(0xf05e)
FA_EXIT = unichr(0xf08b)
FA_CREDIT_CARD = unichr(0xf283)

def get_kv(name):
    name = name if "kv" in name else name+".kv"
    return os.path.join(PATH_RES, 'kvs', name)
