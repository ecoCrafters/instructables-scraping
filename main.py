from instructables import constants as C
from instructables.instructables import Instructables
from instructables.utils import add_material_data, open_csv, read_url_csv, read_csv_to_dataframe

with Instructables() as it:
    # open file
    instruction_writer = open_csv(
        C.INSTRUCTIONS_DATA_PATH,
        fieldnames=['post_id', 'title', 'slug', 'content', 'thumbnail', 'num_of_likes', 'created_at', 'deleted_at',
                    'user_id'],
        mode='a+',
        delimiter='\t'
    )
    instruction_writer.writeheader()
    url_list = read_url_csv(C.URL_DATA_PATH)
    url_writer = open_csv(C.URL_DATA_PATH, fieldnames=['post_id', 'url'], mode='a')
    material_df = read_csv_to_dataframe(
        C.MATERIAL_DATA_PATH,
        columns=['id', 'ingredient', 'created_at']
    )
    instruction_material_df = read_csv_to_dataframe(
        C.INSTRUCTION_MATERIAL_DATA_PATH,
        columns=['id', 'post_id', 'ingredient_id']
    )

    # scrape the web
    it.get_page()
    it.load_all()
    # it.scroll_down()
    instructions_links = it.get_instructions_links()
    for link in instructions_links[10:12]:
        # check whether the url has been scraped before
        if link in url_list:
            continue

        # take precaution, these steps can sometime error
        # so use try and catch, if error happens, break the loop
        try:
            data = it.get_instructions_data(link)
            materials = data.pop('materials')
            # open file once and write to it in a loop is more efficient than using pandas dataframe
            instruction_writer.writerow(data)
            # although pandas implementation adding new data is not that efficient, it is more efficient to read and
            # write data to memory (e.g., using pandas dataframe) than to open and write to file
            material_df, instruction_material_df = add_material_data(materials, material_df, instruction_material_df,
                                                                     created_at=data['created_at'],
                                                                     post_id=data['post_id'])
        except:
            break

        # write scraped url to file, to set checkpoint in case something unintended happened so that scraping process
        # doesn't have to be started from the beginning again
        url_writer.writerow({'post_id': data['post_id'], 'url': link})

    material_df.to_csv(C.MATERIAL_DATA_PATH, index=False)
    instruction_material_df.to_csv(C.INSTRUCTION_MATERIAL_DATA_PATH, index=False)
