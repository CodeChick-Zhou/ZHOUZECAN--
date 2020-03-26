#coding=utf-8
#Version:python3.6.0
#Tools:Pycharm 2017.3.2
__date__ = ' 17:22'
__author__ = 'Colby'

import pygame
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *

class MusicThread(QThread):
    timer = pyqtSignal()
    MusicFilePath = "../music/ding.mp3"
    pygame.mixer.init()

    def SetMusicFile(self,path):
        self.MusicFilePath = path

    def run(self):
        track = pygame.mixer.music.load(self.MusicFilePath)
        pygame.mixer.music.play()
        time.sleep(1)
        pygame.mixer.music.stop()

MusicSingleton = MusicThread()