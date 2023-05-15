from instructables import config as c
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
INSTRUCTIONS_DATA_PATH = os.path.join(ROOT, 'data', 'posts.tsv')
MATERIAL_DATA_PATH = os.path.join(ROOT, 'data', 'ingredients.csv')
INSTRUCTION_MATERIAL_DATA_PATH = os.path.join(ROOT, 'data', 'posts_ingredients.csv')
URL_DATA_PATH = os.path.join(ROOT, 'data', 'post_urls.csv')
INSTRUCTIONS_DIR_PATH = os.path.join(ROOT, 'data', 'instructions')

BASE_URL = 'https://www.instructables.com/search/?q=waste&projects=all'
ENCODED_URL = 'https%3A%2F%2Fwww.instructables.com%2Fsearch%2F%3Fq%3Dwaste%26projects%3Dall'
SCRAPE_URL = f'http://api.scrape.do?token={c.SCRAPE_DO_TOKEN}&url={ENCODED_URL}'

TIME_FORMAT = '%d-%m-%Y %H:%M:%S'
