import ocr
import json
from itertools import chain
import Levenshtein

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

def find_closest_card(ocr_card_name):
  def dist_key(card_name):
    return Levenshtein.distance(ocr_card_name, str(card_name))
  return cards[min(cards, key=dist_key)]


cards = load_card_data()

test_path = "content/cards/abusive.png"

ocr_text = ocr.perform_ocr(test_path)
ocr_card_name =  ' '.join(ocr_text.split())

card = find_closest_card(ocr_card_name)

print card