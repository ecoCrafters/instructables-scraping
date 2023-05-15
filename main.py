from instructables.instructables import Instructables
from instructables.utils import add_material_data, open_csv
from instructables import constants as C
import pandas as pd

with Instructables() as it:
    # open file
    instruction_writer = open_csv(
        C.INSTRUCTIONS_DATA_PATH,
        fieldnames=['post_id', 'title', 'slug', 'content', 'thumbnail', 'num_of_likes', 'created_at', 'deleted_at',
                    'user_id'],
        delimiter='\t'
    )
    instruction_writer.writeheader()
    material_df = pd.DataFrame(
        columns=['id', 'ingredient', 'created_at']
    )
    instruction_material_df = pd.DataFrame(
        columns=['id', 'post_id', 'ingredient_id']
    )

    # scrape the web
    it.get_page()
    it.load_all()
    # it.scroll_down()
    instructions_links = it.get_instructions_links()
    for link in instructions_links[:2]:
        data = it.get_instructions_data(link)
        materials = data.pop('materials')
        # open file once and write to it in a loop is more efficient than using pandas dataframe
        instruction_writer.writerow(data)
        # although pandas implementation adding new data is not that efficient, it is more efficient to read and write
        # data to memory (e.g., using pandas dataframe) than to open and write to file
        material_df, instruction_material_df = add_material_data(materials, material_df, instruction_material_df,
                                                                 created_at=data['created_at'], post_id=data['post_id'])

    material_df.to_csv(C.MATERIAL_DATA_PATH, index=False)
    instruction_material_df.to_csv(C.INSTRUCTION_MATERIAL_DATA_PATH, index=False)
