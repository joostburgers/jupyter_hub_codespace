import json, os
nb_path = r'lesson_4_finding_locations/lesson_4_1_extracting_locations.ipynb'
if not os.path.exists(nb_path):
    print(f"Error: {nb_path} not found")
else:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    cells = nb['cells']
    print(f"Total cells: {len(cells)}\n")
    for i, cell in enumerate(cells):
        src = cell.get('source', [])
        first = (src[0].strip() if src else '')[:70]
        cell_id = cell.get('id', '?')
        print(f"[{i:02d}] id={cell_id}  | {first}")
