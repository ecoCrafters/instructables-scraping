import os
from dotenv import load_dotenv
from html_sanitizer.sanitizer import DEFAULT_SETTINGS
import copy

load_dotenv()

SCRAPE_DO_TOKEN = os.getenv("SCRAPE_DO_TOKEN")

SANITIZER_CONFIG = copy.deepcopy(DEFAULT_SETTINGS)
SANITIZER_CONFIG['tags'].add('img')
SANITIZER_CONFIG['empty'].add('img')
SANITIZER_CONFIG['attributes'].update({'img': ('src', 'alt')})
SANITIZER_CONFIG['separate'].add('img')
