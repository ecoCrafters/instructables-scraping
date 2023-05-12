from instructables.constants import INSTRUCTIONS_DATA_PATH

from markdownify import markdownify as md
from html_sanitizer import Sanitizer
import pyperclip

import tempfile
import os
import subprocess
import re

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def write_to_file(id: str, section_title: str = None, body: str = None, images: dict = None,
                  write_section_title: bool = None, title: str = None):
    """
    Write markdownified content to file
    :param id: string, document id taken from the last part of url
    :param title: string, the title of the tutorial
    :param section_title: string, the title of the section
    :param body: string, the content body, in raw HTML
    :param images: dict, dictionary of alt-src value pair of images
    :param write_section_title: bool, whether to write the section title or not
    :return: None
    """
    # check if the directory exists, if not create it
    if not os.path.exists(INSTRUCTIONS_DATA_PATH):
        os.makedirs(INSTRUCTIONS_DATA_PATH)
    # write to file
    # if title is not none, write it to the file
    if title:
        with open(f'{os.path.join(INSTRUCTIONS_DATA_PATH, id)}.md', 'w') as f:
            f.write(f'# {title}\n\n')
    else:
        # write the rest of the content to the file
        with open(f'{os.path.join(INSTRUCTIONS_DATA_PATH, id)}.md', 'a+') as f:
            if write_section_title:
                f.write(f'## {section_title}\n\n')
            f.write(md(body))
            for src, alt in images.items():
                f.write(f'![{alt}]({src})\n')
            f.write('\n')


def parse_markdown_table(table: str):
    """
    Parse a Markdown table and return a dictionary of the data
    :param table: string, the Markdown table
    :return: list: a list of materials
    """
    result = []

    for row in table.split('\n')[2:]:
        values = [f'{cell[2].strip()} {cell[1].strip()}' for cell in row.split('|')]
        result.append(values)

    return result


def parse_list(response: str):
    """
    Parse pasted response from chatGPT in list form
    :param response: string, pasted response from chatGPT
    :return: list: a list of materials
    """
    response_list = response.split('\n')
    material_list = [material[2:].split('(')[0].strip() for material in response_list if material.startswith('-')]
    return material_list


def cleanhtml(raw_html):
    """
    Remove all html tag
    :param raw_html: String, a html in string
    :return: String, a cleaned html in string.
    """
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def get_materials(html_content: str, prompt=None):
    """
    Get materials from the file. A human interaction will be needed to copy and paste data from chatGPT
    1. Read the file based on id
    2. Copy the content to clipboard. A human will need to paste that to chatGPT and copy response
    3. Create a temporary file, open it with notepad. Paste the response there, save and close
    4. As soon as it closed, read the file, parse it.
    :param html_content: String, a raw html content in string
    :return: List:, a list of materials
    """
    if not prompt:
        prompt = "extract the materials name used from this html pages"
    sanitizer = Sanitizer()
    content = sanitizer.sanitize(html_content)
    # copy the content to clipboard + the prompt
    pyperclip.copy(f'{prompt}\n\n{content}')

    # create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write('')

    # open the file with notepad
    notepad = subprocess.Popen(['notepad', temp_file.name])
    notepad.wait()  # wait until the notepad is closed

    # read the contents of the file
    with open(temp_file.name, 'r') as f:
        response = f.read()

    # parse the table/list
    data = parse_list(response)

    return data
