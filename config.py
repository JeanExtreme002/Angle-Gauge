from os.path import exists
import json

fn = "cfg.json"

config = {
    "background":"gray2",
    "camera":True,
    "color":"red",
    "line_width":2,
    "mirror_effect":False,
    "pause_event":["<Button-1>","<space>"],
    "transparent":True
}

if not exists(fn):
    with open(fn,'w') as file:
        file.write(json.dumps(config, indent = 2))
        
else:
    with open(fn) as file:
        config.update(json.loads(file.read()))
