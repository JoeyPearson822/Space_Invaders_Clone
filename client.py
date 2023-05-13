import pygame as pg

height = 500
width = 500
window = pg.display.set_mode((width, height))
pg.display.set_caption("Cap-Shin")


def redraw_window():
    window.fill(255, 255, 255)
    pg.display.update()

