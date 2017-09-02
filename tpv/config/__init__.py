# @Author: Manuel Rodriguez <valle>
# @Date:   29-Aug-2017
# @Email:  valle.mrv@gmail.com
# @Filename: __init__.py
# @Last modified by:   valle
# @Last modified time: 02-Sep-2017
# @License: Apache license vesion 2.0


import sys
import os
reload(sys)
sys.setdefaultencoding('UTF8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

os.chdir(ROOT_DIR)
sys.path.append(ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, "valle_libs"))

from kivy.config import Config

try: # this is only for pygame window if pygame is avaliable
    import pygame
    pygame.display.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    Config.set('graphics', 'width', str(int(width * .96)))
    Config.set('graphics', 'height', str(int(height * .92)))
except:
    print "Error intentado configurar el tpv"
