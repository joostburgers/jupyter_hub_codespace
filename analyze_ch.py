import json, re
with open('project_mapping_emotions/interactive_tour_config.js', 'r', encoding='utf-8') as f:
    c = f.read()
j = re.sub(r'^.*?=\s*', '', c, count=1, flags=re.DOTALL).rstrip().rstrip(';')
d = json.loads(j)
ch0 = d['chapters'][0]
print('showData:', ch0.get('showData'))
print('id:', ch0.get('id'))
print('location:', ch0.get('location'))
