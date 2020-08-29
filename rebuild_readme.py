import yaml

result = yaml.load(open('table_of_contents.yml'))
content = """# Job templates

"""
for template in result['templates']:
    content += f"- [{template['name']}]({template['long_description_path']}) - {template['short_description']}\n"
with open('README.md', 'w') as f:
    f.write(content)
