import json

mods = {mod: G.app.selectedHuman.getModifier(mod).getValue() for mod in G.app.selectedHuman.getModifierNames()}

with open("Data/default_modifiers.json", "w") as file:
	json.dump(mods, file, indent=4)
