import os
import time
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By

from html_sanitizer import Sanitizer

from instructables import config
from instructables import constants as C
from instructables.utils import get_materials


class Instructables(webdriver.Firefox):
    def __init__(self, webdriver_path=r'C:\SeleniumDriver', teardown=False):
        self.webdriver_path = webdriver_path
        self.teardown = teardown
        os.environ['PATH'] += self.webdriver_path
        super(Instructables, self).__init__()
        self.implicitly_wait(5)
        self.maximize_window()
        self.sanitizer = Sanitizer(config.SANITIZER_CONFIG)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def get_page(self):
        self.get(C.BASE_URL)

    def load_all(self):
        """
        Find main tag and find button tag. Click on that to load all.
        :return: None
        """
        main_element = self.find_element(By.TAG_NAME, 'main')
        button_element = main_element.find_element(By.TAG_NAME, 'button')
        button_element.click()

    def scroll_down(self):
        """
        Simulate scroll down in infinite scrolling page.
        :return: None
        """
        SCROLL_PAUSE_TIME = 1
        screen_height = self.execute_script('return window.screen.height;')
        i = 1
        while True:
            # scroll one screen height each time
            self.execute_script(f'window.scrollTo(0, {screen_height * i});')
            i += 1
            time.sleep(SCROLL_PAUSE_TIME)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.execute_script('return document.body.scrollHeight;')
            # break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height * i) > scroll_height:
                break

    def get_instructions_links(self):
        """
        Get all instructions links
        :return: list, list of links of instructions.
        """
        anchor_titles = self.find_elements(By.CSS_SELECTOR, 'a[class^="title_"]')
        instructions = [anchor.get_attribute('href') for anchor in anchor_titles]
        return instructions

    def get_instruction(self):
        """
        Get the content body
        :return: tuple, a tuple containing thumbnail image src and the simplified html content body
        """
        content = ''
        thumbnail_src = ''

        article_body = self.find_element(By.CSS_SELECTOR, 'div[class="article-body"]')

        # article_body consist of several sections.
        # Common section is intro, supplies, step1, step2, and so on
        # each section has title, images, and body, so loop on that
        sections = article_body.find_elements(By.TAG_NAME, 'section')
        for section in sections:
            # section_title
            section_title = section.find_element(By.TAG_NAME, 'h2').get_attribute('outerHTML')
            # title on the intro section is not needed
            if section.get_attribute('id') == 'intro':
                section_title = ''
                # however we need the first image in intro section for thumbnail
                thumbnail_src = section.find_element(By.CLASS_NAME, 'mediaset') \
                    .find_element(By.TAG_NAME, 'img') \
                    .get_attribute('data-src')
            content += section_title

            # section images
            if section.get_attribute('id') == 'stepsupplies':
                photoset_wrapper = section.find_element(By.CLASS_NAME, 'mediaset-supplies')
            else:
                photoset_wrapper = section.find_element(By.CLASS_NAME, 'mediaset')
            for img in photoset_wrapper.find_elements(By.TAG_NAME, 'img'):
                src = img.get_attribute('data-src')
                if src:
                    alt = img.get_attribute('alt')
                    img_html = f'<img src="{src}" alt="{alt}" />'
                    content += img_html

            # section body
            section_body = section.find_element(By.CLASS_NAME, 'step-body').get_attribute('outerHTML')
            content += section_body

        return thumbnail_src, content

    def get_instructions_data(self, url):
        """
        Get all instruction (tutorial) data
        :param url: String, the url of the tutorial
        :return: dict, a dictionary containing tutorial data
        """
        self.get(url)

        id = uuid.uuid4()
        title = self.find_element(By.CSS_SELECTOR, 'h1[class="header-title"]').text
        thumbnail_src, content = self.get_instruction()
        materials = get_materials(content)

        return {
            'post_id': str(id),
            'title': title,
            'slug': title.lower().replace(' ', '-'),
            'content': self.sanitizer.sanitize(content),
            'thumbnail': thumbnail_src,
            'num_of_likes': 0,
            'created_at': time.strftime(C.TIME_FORMAT, time.gmtime()),
            'deleted_at': None,
            'user_id': 'admin',
            'materials': materials
        }
