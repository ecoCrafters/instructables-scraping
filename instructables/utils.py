from instructables.constants import INSTRUCTIONS_DATA_PATH

import os

from markdownify import markdownify as md
import pyperclip
import tempfile
import subprocess


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
        values = row.split('|')[1].strip()
        result.append(values)

    return result


def get_materials(id: str):
    """
    Get materials from the file. A human interaction will be needed to copy and paste data from chatGPT
    1. Read the file based on id
    2. Copy the content to clipboard. A human will need to paste that to chatGPT and copy response
    3. Create a temporary file, open it with notepad. Paste the response there, save and close
    4. As soon as it closed, read the file, parse it.
    :param id: String, document id
    :return: dict:, a dictionary of materials
    """
    prompt = 'Write a table summarizing materials used and its quantities in this tutorial'
    # read the file based on id
    with open(f'{os.path.join(INSTRUCTIONS_DATA_PATH, id)}.md', 'r') as f:
        content = f.read()
        # copy the content to clipboard + the prompt
        pyperclip.copy(f'{prompt}\n\n{content}')

    # open a temporary file
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write('')

    # open the file with notepad
    notepad = subprocess.Popen(['notepad', temp_file.name])
    notepad.wait()  # wait until the notepad is closed

    # read the contents of the file
    with open(temp_file.name, 'r') as f:
        md_table = f.read()

    # parse the table
    data = parse_markdown_table(md_table)

    return {
        'id': id,
        'data': data
    }
