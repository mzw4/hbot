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
    print 'Splitting image and getting card info...'
    print image.shape
    (ih, iw, iz) = image.shape

    card_text_img = image[ih/2 - 50 : ih/2 + 50, 0: iw]
    cost_img = image[0 : 100, 0: iw/2]
    attack_img = image[ih - 100 : ih, 0: iw/2]
    defense_img = image[ih - 100 : ih, iw/2: iw]

    cv2.imwrite('temp/original_image.png', image)
    cv2.imwrite('temp/original_text_image.png', card_text_img)
    cv2.imwrite('temp/original_cost_image.png', cost_img)
    cv2.imwrite('temp/original_attack_image.png', attack_img)
    cv2.imwrite('temp/original_defense_image.png', defense_img)

    ocr_text = ocr.perform_ocr(card_text_img)
    cost = ocr.perform_ocr(cost_img)
    attack = ocr.perform_ocr(attack_img)
    defense = ocr.perform_ocr(defense_img)

    if not ocr_text:
      print 'No ocr text'
      return None
    print "==== OCR text:"
    print ocr_text
    print cost
    print attack
    print defense
    print '\n'
    return self.find_closest_card(ocr_text)

  def identify_card_in_hand(self):
    card_img = self.screen_parser.find_card_in_hand()
    return self.get_card_info(card_img)

# test_path = "content/cards/abusive.png"
# image = cv2.imread(test_path)

# card_parser = CardParser()
# card = card_parser.get_card_info(image)
# print card
