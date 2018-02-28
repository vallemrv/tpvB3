# @Author: Manuel Rodriguez <valle>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: __init__.py
# @Last modified by:   valle
# @Last modified time: 27-Feb-2018
# @License: Apache license vesion 2.0


import sys
import os
try:
    reload(sys)
    sys.setdefaultencoding('UTF8')
except:
    from importlib import reload
    reload(sys)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
URL_SERVER = "http://btres.elbrasilia.com"

#URL_SERVER = "http://btres.elbrasilia.com/"
IP_PRINTER_CAJA = "192.168.1.5"
TOKEN_API = "4td-c40a6792be0f208a284f"
TOKEN_USER = 2


os.chdir(BASE_DIR)
sys.path.append(ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "valle_libs"))

from kivy.config import Config

try: # this is only for pygame window if pygame is avaliable
    import pygame
    pygame.display.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    Config.set('graphics', 'width', str(int(width * .96)))
    Config.set('graphics', 'height', str(int(height * .96)))
except:
    print ("Error intentado configurar el tpv")
    Config.set('graphics', 'width', "1250")
    Config.set('graphics', 'height', "700")
