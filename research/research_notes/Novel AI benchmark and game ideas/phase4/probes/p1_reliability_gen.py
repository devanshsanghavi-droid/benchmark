"""Probe for C17 Reliability Horizon: random invented register machine.
Prints the spec only; writes the answers to a hidden json the reviewer must not read until answers are committed."""
import os, random, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
seed = int.from_bytes(os.urandom(4), 'big')
rng = random.Random(seed)
names = rng.sample(["BRISK","ZAP","FLIP","KNOT","SWIVEL","HOP","GRIND","TWIRL","PLUCK","DRAPE","MUNCH","VEER"], 5)
N_ADD, N_INV, N_ROT, N_SKIP, N_MUL = names
def gen_prog():
    prog = []
    for _ in range(7):
        t = rng.choice(["add","inv","rot","skip","mul"])
        if t=="add": a,b = rng.sample(range(5),2); prog.append((t,a,b))
        elif t=="inv": prog.append((t,rng.randrange(5)))
        elif t=="rot": prog.append((t,))
        elif t=="skip": prog.append((t,rng.randrange(5),rng.choice([1,2])))
        else: prog.append((t,rng.randrange(5),rng.choice([3,7,9])))
    return prog
def degenerate(prog, init):
    R = init[:]; pc = 0; seen=set(); lines=set()
    for s in range(60):
        key=(pc,tuple(R))
        if key in seen: return True
        seen.add(key); lines.add(pc)
        ins=prog[pc]; t=ins[0]; nxt=(pc+1)%7
        if t=="add": R[ins[1]]=(R[ins[1]]+R[ins[2]])%10
        elif t=="inv": R[ins[1]]=9-R[ins[1]]
        elif t=="rot":
            if R[2] in (2,3,5,7): R=[R[4]]+R[:4]
        elif t=="skip":
            if R[ins[1]]%2==0: nxt=(pc+1+ins[2])%7
        else: R[ins[1]]=(R[ins[1]]*ins[2])%10
        pc=nxt
        if s==39 and len(lines)<7: return True
    return False
NONDEG = "--nondegenerate" in sys.argv
while True:
    prog = gen_prog()
    init = [rng.randrange(10) for _ in range(5)]
    if not NONDEG or not degenerate(prog, init): break
def fmt(ins):
    t=ins[0]
    if t=="add": return f"{N_ADD} R{ins[1]} R{ins[2]}"
    if t=="inv": return f"{N_INV} R{ins[1]}"
    if t=="rot": return f"{N_ROT}"
    if t=="skip": return f"{N_SKIP} R{ins[1]} {ins[2]}"
    return f"{N_MUL} R{ins[1]} {ins[2]}"
def run(L):
    R = init[:]; pc = 0; steps = 0
    while steps < L:
        ins = prog[pc]; t = ins[0]; nxt = (pc+1) % 7
        if t=="add": R[ins[1]] = (R[ins[1]]+R[ins[2]])%10
        elif t=="inv": R[ins[1]] = 9-R[ins[1]]
        elif t=="rot":
            if R[2] in (2,3,5,7): R = [R[4]]+R[:4]
        elif t=="skip":
            if R[ins[1]]%2==0: nxt = (pc+1+ins[2]) % 7
        else: R[ins[1]] = (R[ins[1]]*ins[2])%10
        pc = nxt; steps += 1
    return R
Ls = [20, 40] if NONDEG else [12, 30, 60]
ans = {str(L): run(L) for L in Ls}
json.dump({"seed":seed,"answers":ans,"prog":[fmt(i) for i in prog],"init":init}, open(os.path.join(HERE,".p1_hidden.json"),"w"))
print("Machine with registers R0..R4, all values are digits 0-9 (arithmetic mod 10).")
print(f"{N_ADD} Ra Rb : Ra <- (Ra + Rb) mod 10")
print(f"{N_INV} Ra    : Ra <- 9 - Ra")
print(f"{N_ROT}       : if R2 is prime (2,3,5,7), rotate right: (R0,R1,R2,R3,R4) <- (R4,R0,R1,R2,R3); else do nothing")
print(f"{N_SKIP} Ra k  : if Ra is even, jump forward so the next executed instruction is k+1 lines ahead (skipping k lines, wrapping); else continue normally")
print(f"{N_MUL} Ra c  : Ra <- (Ra * c) mod 10")
print("Program (lines 0-6), executed in a loop, wrapping from line 6 to line 0. Each executed instruction is one step; skipped lines are not steps.")
for i,ins in enumerate(prog): print(f"  {i}: {fmt(ins)}")
print("Initial:", " ".join(f"R{i}={v}" for i,v in enumerate(init)))
print("Question: register values after", Ls, "steps.")
