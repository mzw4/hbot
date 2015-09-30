import cv2
import ocr
import json
from itertools import chain
import Levenshtein

from screen_parser import ScreenParser

"""
Parse the card data json and load into memory
"""
def load_card_data():
  cards_data = json.load(open("AllSets.json"))
  cards_data.pop('Hero Skins')
  cards_data.pop('System')
  cards_data.pop('Debug')
  cards_data.pop('Credits')
  cards_data.pop('Reward')
  cards_list = chain.from_iterable(cards_data.values())

  cards = {}
  def add_to_dict(card):
    cards[card['name']] = card
  map(add_to_dict, cards_list)
  return cards

class CardParser():
  def __init__(self):
    self.cards = load_card_data()
    self.screen_parser = ScreenParser()

  """
  Find the closest card to the given card name string from OCR
  Uses Levenshtein (edit) distance
  """
  def find_closest_card(self, ocr_text):
    def dist_key(card_name):
      return Levenshtein.distance(ocr_text, str(card_name))
    return self.cards[min(self.cards, key=dist_key)]

  """
  Parses a card image to get the name with OCR, then
  finds the closest card and returns the card data
  """
  def get_card_info(self, image):
    # cv2.imshow('', image)
    # cv2.waitKey(0)
    ocr_text = ocr.perform_ocr(image)
    if not ocr_text:
      print 'No ocr text'
      return None
    print "==== OCR text:"
    print ocr_text + '\n'
    return self.find_closest_card(ocr_text)

  def identify_card_in_hand(self):
    print 'Identifying new card...'
    card_img = self.screen_parser.find_card_in_hand()
    print "Got image, identifying..." + str(card_img.shape)
    return self.get_card_info(card_img)

# test_path = "content/cards/abusive.png"
# image = cv2.imread(test_path)

# card_parser = CardParser()
# card = card_parser.get_card_info(image)
# print card
