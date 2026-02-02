import json
names= {
    "upside_down": {"nancy": "wheeler"},
    "will_be_dead": {"will": "byers"},
    "jane": "hopper",
    "steve": "harrington",
}

print("Without json" + str(names))

json = json.dumps(names,  indent=5)
print(json)

for value in names.values():
    print(value)
