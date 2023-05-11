from instructables.instructables import Instructables

with Instructables() as it:
    it.get_page()
    it.load_all()
    # it.scroll_down()
    instructions_links = it.get_instructions_links()
    # print(instructions_list)
    for link in instructions_links[1:2]:
        it.get_instruction(link)
