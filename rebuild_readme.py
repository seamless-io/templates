from typing import List

import yaml

result = yaml.load(open('table_of_contents.yml'), Loader=yaml.FullLoader)
content = """# Job templates

"""


def check_name_uniqueness(names: List[str]):
    names_set = set(names)
    if len(names) != len(names_set):
        raise RuntimeError('Template names should be unique!')


names = []
for template in result['templates']:
    names.append(template['name'])
    content += f"- [{template['name']}]({template['path_to_files']}) - {template['short_description']}\n"
check_name_uniqueness(names)
with open('README.md', 'w') as f:
    f.write(content)
