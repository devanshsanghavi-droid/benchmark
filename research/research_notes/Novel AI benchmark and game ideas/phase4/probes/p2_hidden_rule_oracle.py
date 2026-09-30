"""Probe for C42 Hidden-Rule Lab / C43 Eleusis (text/JSON track).
Usage:
  new                -> draws a secret rule (hidden state file), prints 1 positive and 1 negative example
  query '<json>'     -> answers whether a scene has the hidden property (budget 25)
  probes             -> prints 20 label-balanced random probe scenes
  score 'YNYN...'    -> scores the 20 labels and reveals the rule
Scene JSON: list of blocks {"c": red|blue|green|yellow, "s": cube|pyramid|cylinder, "z": 1..3 (size/height), "x": 0..9 (distinct positions on a line)}.
Two blocks touch iff their x differ by exactly 1."""
import os, sys, json, random, pickle
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, ".p2_state.pkl")
C = ["red","blue","green","yellow"]; S = ["cube","pyramid","cylinder"]
def atoms(rng):
    k = rng.choice(["c","s","z","zge"])
    if k=="c": v=rng.choice(C); return (f"color={v}", lambda b,v=v: b["c"]==v)
    if k=="s": v=rng.choice(S); return (f"shape={v}", lambda b,v=v: b["s"]==v)
    if k=="z": v=rng.choice([1,2,3]); return (f"size={v}", lambda b,v=v: b["z"]==v)
    v=rng.choice([2,3]); return (f"size>={v}", lambda b,v=v: b["z"]>=v)
touch = lambda a,b: abs(a["x"]-b["x"])==1
def make_rule(rng):
    t = rng.randrange(7); (n1,p1) = atoms(rng); (n2,p2) = atoms(rng)
    if t==0: return (f"exists a block with {n1} and {n2}", lambda sc: any(p1(b) and p2(b) for b in sc))
    if t==1: return (f"every block with {n1} has {n2} (vacuous true)", lambda sc: all(p2(b) for b in sc if p1(b)))
    if t==2:
        n=rng.choice([2,3]); return (f"at least {n} blocks with {n1}", lambda sc: sum(p1(b) for b in sc)>=n)
    if t==3: return (f"every block with {n1} touches a block with {n2} (vacuous true)", lambda sc: all(any(touch(b,o) and p2(o) for o in sc if o is not b) for b in sc if p1(b)))
    if t==4: return (f"number of {n1} blocks > number of {n2} blocks", lambda sc: sum(p1(b) for b in sc) > sum(p2(b) for b in sc))
    if t==5: return (f"every block with {n1} touches something taller than itself (vacuous true)", lambda sc: all(any(touch(b,o) and o["z"]>b["z"] for o in sc if o is not b) for b in sc if p1(b)))
    return (f"leftmost block has {n1}", lambda sc: p1(min(sc, key=lambda b: b["x"])))
def rand_scene(rng):
    n = rng.randint(3,6); xs = rng.sample(range(10), n)
    return [{"c":rng.choice(C),"s":rng.choice(S),"z":rng.randint(1,3),"x":x} for x in sorted(xs)]
def valid(sc):
    try:
        assert isinstance(sc,list) and 1<=len(sc)<=8
        xs=[b["x"] for b in sc]; assert len(set(xs))==len(xs)
        for b in sc: assert b["c"] in C and b["s"] in S and b["z"] in (1,2,3) and 0<=b["x"]<=9
        return True
    except Exception: return False
cmd = sys.argv[1]
if cmd=="new":
    seed = int.from_bytes(os.urandom(4),'big'); rng = random.Random(seed)
    while True:
        rs = rng.getstate(); name, f = make_rule(rng)
        rate = sum(f(rand_scene(random.Random(i))) for i in range(400))/400
        if 0.25<=rate<=0.75: break
    pickle.dump({"seed":seed,"rs":rs,"q":0}, open(ST,"wb"))
    pos=neg=None; i=0
    while pos is None or neg is None:
        sc=rand_scene(random.Random(seed+10_000+i)); i+=1
        if f(sc) and pos is None: pos=sc
        if not f(sc) and neg is None: neg=sc
    print("POSITIVE example:", json.dumps(pos)); print("NEGATIVE example:", json.dumps(neg))
    sys.exit()
st = pickle.load(open(ST,"rb")); rng=random.Random(); rng.setstate(st["rs"]); name,f = make_rule(rng)
if cmd=="query":
    if st["q"]>=25: print("budget exhausted"); sys.exit()
    sc=json.loads(sys.argv[2])
    if not valid(sc): print("invalid scene (not counted)"); sys.exit()
    st["q"]+=1; pickle.dump(st, open(ST,"wb"))
    print(f"query {st['q']}/25:", "YES" if f(sc) else "NO")
elif cmd=="probes":
    r=random.Random(st["seed"]+999); out=[]; npos=nneg=0
    while len(out)<20:
        sc=rand_scene(r); y=f(sc)
        if y and npos<10: out.append(sc); npos+=1
        elif (not y) and nneg<10: out.append(sc); nneg+=1
    r.shuffle(out)
    for i,sc in enumerate(out): print(i, json.dumps(sc))
elif cmd=="score":
    r=random.Random(st["seed"]+999); out=[]; npos=nneg=0
    while len(out)<20:
        sc=rand_scene(r); y=f(sc)
        if y and npos<10: out.append(sc); npos+=1
        elif (not y) and nneg<10: out.append(sc); nneg+=1
    r.shuffle(out); lab=sys.argv[2].strip().upper()
    truth="".join("Y" if f(sc) else "N" for sc in out)
    acc=sum(a==b for a,b in zip(lab,truth))/20
    print("truth:", truth); print("mine: ", lab); print("accuracy:", acc, "queries used:", st["q"]); print("RULE:", name)
