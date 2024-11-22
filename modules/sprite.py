import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
  def __init__(self, game, x, y, text):
    self.groups = game.all_sprites
    pygame.sprite.Sprite.__init__(self, self.groups)
    self.game = game
    self.image = pygame.Surface((TILESIZE, TILESIZE))
    self.x, self.y = x, y
    self.text = text
    self.rect = self.image.get_rect()

  def update(self):
    self.rect.x = self.x * TILESIZE
    self.rect.y = self.y * TILESIZE

  def click(self, mouse_x, mouse_y):
    return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom