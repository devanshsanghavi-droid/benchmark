"""Compile the engine to sourceless bytecode in public/ and write the 5 public maps (SEALED tool)."""
import json, os, py_compile, sys
SEALED = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = sys.argv[1]
sys.path.insert(0, SEALED)
import mapgen
py_compile.compile(os.path.join(SEALED, "engine_src", "brackwater_engine.py"),
                   cfile=os.path.join(PUBLIC, "brackwater_engine.pyc"),
                   dfile="brackwater_engine", optimize=2, doraise=True)
PUBLIC_MAP_SEEDS = json.load(open(os.path.join(SEALED, "seeds.json")))["public_maps"]
os.makedirs(os.path.join(PUBLIC, "maps"), exist_ok=True)
for i, s in enumerate(PUBLIC_MAP_SEEDS, 1):
    m = mapgen.generate(s, name="public-%d" % i)
    with open(os.path.join(PUBLIC, "maps", "map%d.json" % i), "w") as fh:
        json.dump(m, fh, indent=1)
print("ok")
