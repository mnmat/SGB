#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.join(sys._MEIPASS)) # pyinstaller executables use this hidden folder as their working directory

import pygame as pg
from data.main import main
import cProfile


if __name__=='__main__':
    main()
    pg.quit()
    sys.exit()