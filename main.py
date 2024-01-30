import sys
import random

import pygame as pg
import pygame.freetype as ft

import pathlib
import settings


class App:
  current_index = 0
  keys_collected = set()
  invalid_key_count = 0
  random_words = [
      "apple",
      "banana",
      "cherry",
      "date",
      "elderberry",
      "fig",
      "grape",
      "honeydew",
      "kiwi",
      "lemon",
      "mango",
      "nectarine",
      "orange",
      "peach",
      "quince",
      "raspberry",
      "strawberry",
      "tangerine",
      "ugli",
      "vanilla",
      "watermelon",
      "xigua",
      "yellow",
      "zucchini",
      "almond",
      "blackberry",
      "cantaloupe",
      "date",
      "elderberry",
      "fig",
      "grape",
      "honeydew",
      "kiwi",
      "lemon",
      "mango",
      "nectarine",
      "orange",
      "peach",
      "quince",
      "raspberry",
      "strawberry",
      "tangerine",
      "ugli",
      "vanilla",
      "watermelon",
      "xigua",
      "yellow",
  ]
  guess_word = random.choice(random_words)

  def __init__(self):
    pg.init()
    self.screen = pg.display.set_mode(settings.WIN_SIZE)
    self.clock = pg.time.Clock()
    self.font = ft.SysFont("Verdana", settings.FONT_SIZE)
    self.dt = 0.0

    # for item in pathlib.Path(settings.SPRITE_DIR_PATH).glob("*.png"):
    #   if item.is_file():
    #     self.sprite_paths.append(item)

    self.sprite_paths = [
        item for item in pathlib.Path(settings.SPRITE_DIR_PATH).glob("*.png")
        if item.is_file()
    ]

    self.guessed_word_length = len(self.guess_word)

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

  def game_was_won(self):
    return len(self.keys_collected & set(self.guess_word)) == len(
        set(self.guess_word))

  def is_valid_letter(self, letter):
    return list(self.guess_word).count(letter) > 0

  def draw_keys_pressed(self):
    x, y = 0, 20
    message = "Guessed letters: " + "".join(self.keys_collected)
    self.draw_message(message, "blue", x, y)

  def draw_masked_word(self):
    x, y = 100, 200
    message = "Solve word: "

    for i in range(self.guessed_word_length):
      if self.guess_word[i] in self.keys_collected:
        message += self.guess_word[i] + " "
      else:
        message += "? "

    self.draw_message(message, "blue", x, y)

  def draw_actual_word(self):
    x, y = 100, 200
    message = f"The word was: {self.guess_word}"
    self.draw_message(message, "blue", x, y)

  def draw_game_lost(self):
    return pg.image.load("images/oh-no.png").convert_alpha()

  def draw_game_won(self):
    return pg.image.load("images/oh-yeah.jpg").convert_alpha()

  def display_current_sprite(self, current_index):
    return pg.image.load(self.sprite_paths[current_index]).convert_alpha()

  def draw(self):
    self.screen.fill("white")

    self.screen.blit(self.display_current_sprite(self.current_index), (0, 0))

    self.draw_fps()

    if self.loser():
      self.screen.blit(self.draw_game_lost(), (0, 0))
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
        if not self.is_valid_letter(e.unicode):
          self.current_index += 1
      # elif e.type == pg.MOUSEBUTTONDOWN:
      #   if not self.loser():
      #     self.current_index = self.current_index + 1

  def run(self):
    while True:
      if self.game_was_won():
        # Do something to indicate to the user that they won
        self.screen.blit(self.draw_game_won(), (0, 0))
        self.update()
      else:
        self.check_events()
        self.update()
        self.draw()


if __name__ == "__main__":
  app = App()
  app.run()
