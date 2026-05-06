import json
path = r"c:\Users\joost\My Drive (joostburgers@gmail.com)\Teaching\JMU\Courses\digital_studies_resources\repos\jupyter_hub_codespace\lesson_4_finding_locations\lesson_4_3_geoparsing_mapping.ipynb"
with open(path, encoding="utf-8") as f:
    nb = json.load(f)
for cell in nb["cells"]:
    if cell.get("cell_type") == "markdown":
        src = "".join(cell["source"])
        if "six distinct failure modes" in src:
            print("FOUND six failure modes")
            print(src[-700:])
            break
