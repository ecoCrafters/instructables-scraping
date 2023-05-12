from instructables import config as c
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
INSTRUCTIONS_DATA_PATH = os.path.join(ROOT, 'data', 'instructions')
BASE_URL = 'https://www.instructables.com/search/?q=waste&projects=all'
ENCODED_URL = 'https%3A%2F%2Fwww.instructables.com%2Fsearch%2F%3Fq%3Dwaste%26projects%3Dall'
SCRAPE_URL = f'http://api.scrape.do?token={c.SCRAPE_DO_TOKEN}&url={ENCODED_URL}'

LOCAL_AI_ENDPOINT = 'http://localhost:8000/v1/chat/completions'
MODEL_PATH = r'D:\Projects\alpaca-native-7B-ggml\sdkl'
HEADERS = {'Content-Type': 'application/json'}
PROMPT = "What are the materials from this tutorial?"

TIME_FORMAT = '%d-%m-%Y %H:%M:%S'
