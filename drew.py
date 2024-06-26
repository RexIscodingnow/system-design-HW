"""
Reference source code: https://github.com/channel2007/Python_Tetris
"""

# encoding: utf-8

import pygame

#-------------------------------------------------------------------------
# 畫Box.
#-------------------------------------------------------------------------
class Box(object):
    #-------------------------------------------------------------------------
    # 建構式.
    #   pygame    : pygame.
    #   canvas    : 畫佈.
    #   name    : 物件名稱.
    #   rect      : 位置、大小.
    #   color     : 顏色.
    #-------------------------------------------------------------------------
    def __init__( self, pygame: pygame, canvas: pygame.Surface, name, rect, color):
        self.pygame = pygame
        self.canvas = canvas
        self.name = name
        self.rect = rect
        self.color = color

        self.visivle = True
        
    #-------------------------------------------------------------------------
    # 更新.
    #-------------------------------------------------------------------------
    def update(self):
        if(self.visivle):
            self.pygame.draw.rect(self.canvas, self.color, self.rect)