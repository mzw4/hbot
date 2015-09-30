import pyautogui as pg
import numpy as np
import time
import util

from card_identifier import CardParser
from screen_parser import ScreenParser

# failsafe - move mouse to top left to trigger abort
pg.FAILSAFE = True

screenWidth, screenHeight = pg.size()

class Game():
  def __init__(self):
    self.turn = 0
    self.bot = HBot()

class HBot():
  def __init__(self):
    self.hand = []
    self.max_mana = 1
    self.mana = 1
    self.health = 30
    self.parser = CardParser()
    self.screenParser = ScreenParser()
    self.turn = 0
    self.scan_num = 100 # number of cards to scan in hand
    self.my_turn = True
    self.game_over = False

  def start(self):
    while not self.game_over:
      if self.screenParser.check_turn():
        self.turn += 1
        print '==== Start turn...'
        print 'Mana: ' + str(self.mana)

        self.scan_cards(self.scan_num)

        ended_turn = False
        while self.mana > 0 and not ended_turn:
          success = self.make_move()
          if not success:
            self.end_turn()
            ended_turn = True

  def end_turn(self):
    pg.moveTo(screenWidth/2 + 470, screenHeight/2 - 25, duration=0.5)
    pg.click()
    self.max_mana += 1
    self.mana = self.max_mana
    self.turn += 1
    time.sleep(5)

  def scan_cards(self, count):
    print '==== Scanning cards...'

    # start on the right side of the hand
    pg.moveTo(screenWidth/2 + 250, screenHeight - 50)

    prev_card_loc = None
    prev_card_name = None
    cards_left = True
    found_card = False
    while (cards_left and count > 0) or not found_card:
      card_info = self.parser.identify_card_in_hand()
      # location = True
      # card_info = {}

      time.sleep(0.2)
      # if location:
      print 'Card info:'
      print card_info
      if card_info:
        # ignore duplicates for now
        # if location != prev_card_loc: # need to make this approximate check
        
        if card_info['name'] != prev_card_name:
          self.hand += [(card_info, pg.position())]
          print '==== Added ' + card_info['name'] + '\n'
          count -= 1

        found_card = True
        # prev_card_loc = location
        prev_card_name = card_info['name']
      elif found_card:
        print 'No cards left to scan'
        cards_left = False

      pg.moveRel(-50, None, duration=0.15)

    for card in self.hand:
      print card
    self.scan_num = 1

  def play_card(self, card, position):
    print '=== Playing card: ' + card['name'] + ' at position ' + str(position)
    pg.moveTo(position[0], position[1], duration=0.3)
    pg.PAUSE = 1
    pg.dragRel(None, -screenHeight/2, button='left', duration=0.75)
    pg.PAUSE = 1
    return True

  """
  Make a move.
  Returns True if move was made, or False if there is no move
  """
  def make_move(self):
    print "==== Making move..."
    for i, (card, position) in enumerate(self.hand):
      if 'cost' not in card or card['cost'] < self.mana:
        if 'attack' not in card: continue # temp
        success = self.play_card(card, position)
        if success:
          self.mana -= card['cost'] if 'cost' in card else 0
          del self.hand[i]
          if card['name'] == 'The Coin':
            self.mana += 1
          return True
    return False


bot = HBot()
# bot.screenParser.check_turn()
bot.start()
