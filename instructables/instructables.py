import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from instructables import constants as C
from instructables.utils import write_to_file, get_materials


class Instructables(webdriver.Firefox):
    def __init__(self, webdriver_path=r'C:\SeleniumDriver', teardown=False):
        self.webdriver_path = webdriver_path
        self.teardown = teardown
        os.environ['PATH'] += self.webdriver_path
        super(Instructables, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

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

    def get_instruction(self, url):
        self.get(url)
        # id = url.split('/')[-1]
        title = self.find_element(By.CSS_SELECTOR, 'h1[class="header-title"]').text
        # write_to_file(id, title=title)
        article_body = self.find_element(By.CSS_SELECTOR, 'div[class="article-body"]')

        # article_body consist of several sections.
        # Common section is intro, supplies, step1, step2, and so on
        # each section has title, images, and body, so loop on that
        sections = article_body.find_elements(By.TAG_NAME, 'section')
        for section in sections:
            write_section_title = True
            images_dict = {}
            mediaset_class_name = 'mediaset'

            # section_title
            section_title = section.find_element(By.TAG_NAME, 'h2').text

            # section images
            if section.get_attribute('id') == 'stepsupplies':
                mediaset_class_name = 'mediaset-supplies'
            photoset_wrapper = section.find_element(By.CLASS_NAME, mediaset_class_name)\
                                      .find_elements(By.TAG_NAME, 'img')
            for src in photoset_wrapper:
                images_dict[src.get_attribute('src')] = src.get_attribute('alt')

            # section body
            # keep raw html to get markdownified later to preserve the formatting
            section_body = section.find_element(By.CLASS_NAME, 'step-body').get_attribute('outerHTML')

            # title on the intro section is not needed
            if section.get_attribute('id') == 'intro':
                write_section_title = False

            # write each section to file
            write_to_file(id, section_title, section_body, images_dict, write_section_title, title=None)

        materials = get_materials(id)
        print(materials)
        # TODO: extract to database
