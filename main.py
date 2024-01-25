import sys
import random

import pygame as pg
import pygame.freetype as ft

import pathlib
import settings


class App:
  current_index = 0
  keys_collected = set()
  guess_word = "cat"

  def __init__(self):
    pg.init()
    self.screen = pg.display.set_mode(settings.WIN_SIZE)
    self.clock = pg.time.Clock()
    self.font = ft.SysFont("Verdana", settings.FONT_SIZE)
    self.dt = 0.0

    self.sprite_paths = [
        item for item in pathlib.Path(settings.SPRITE_DIR_PATH).glob("*.png")
        if item.is_file()
    ]

    # print(self.sprite_paths)

  def loser(self):
    return self.current_index == len(self.sprite_paths) - 1

  def update(self):
    pg.display.flip()

    self.dt = self.clock.tick() * 0.001

  def draw_message(self, message, color, x, y):
    self.font.render_to(self.screen, (x, y), message, color)

  def draw_fps(self):
    x, y = 0, 0

    self.draw_message(f"{self.clock.get_fps() :.0f} FPS", "blue", x, y)

  def draw_keys_pressed(self):
    x, y = 0, 20
    message = "Guessed letters: " + "".join(self.keys_collected)
    self.draw_message(message, "blue", x, y)

  def draw_masked_word(self):
    x, y = 100, 200
    message = "Solve word: "
    self.draw_message(message, "blue", x, y)

  def draw_actual_word(self):
    x, y = 100, 200
    message = f"The word was: {self.guess_word}"
    self.draw_message(message, "blue", x, y)

  def display_current_sprite(self, current_index):
    return pg.image.load(self.sprite_paths[current_index]).convert_alpha()

  def draw(self):
    self.screen.fill("white")

    self.screen.blit(self.display_current_sprite(self.current_index), (0, 0))

    self.draw_fps()

    if self.loser():
      self.draw_actual_word()
    else:
      self.draw_keys_pressed()
      self.draw_masked_word()

  def check_events(self):
    for e in pg.event.get():
      if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
        pg.quit()
        sys.exit()
      elif e.type == pg.KEYDOWN:
        self.keys_collected.add(e.unicode)
      elif e.type == pg.MOUSEBUTTONDOWN:
        if not self.loser():
          self.current_index = self.current_index + 1

  def run(self):
    while True:
      self.check_events()
      self.update()
      self.draw()


if __name__ == "__main__":
  app = App()
  app.run()
