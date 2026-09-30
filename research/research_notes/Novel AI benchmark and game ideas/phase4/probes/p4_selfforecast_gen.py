"""Probe for C15 Prospective Self-Forecast / C14 Kelly Exam: random exact-answer tasks; answers hidden until forecasts and attempts are committed."""
import os, random, json, math
from functools import lru_cache
HERE=os.path.dirname(os.path.abspath(__file__)); rng=random.Random(int.from_bytes(os.urandom(4),'big'))
T=[]; A=[]
def add(q,a): T.append(q); A.append(a)
x,y=rng.randint(100,999),rng.randint(100,999); add(f"{x} * {y}", x*y)
x,y=rng.randint(1000,9999),rng.randint(1000,9999); add(f"{x} * {y}", x*y)
x,y=rng.randint(10000,99999),rng.randint(10000,99999); add(f"{x} * {y}", x*y)
x,y=rng.randint(100000,999999),rng.randint(100,999); add(f"{x} * {y}", x*y)
a,b,m=rng.randint(2,99),rng.randint(50,200),rng.choice([37,41,43,47,53,59,61,67,71,73,79,83,89,97]); add(f"{a}^{b} mod {m}", pow(a,b,m))
k=rng.randint(40,70); add(f"sum of the decimal digits of 2^{k}", sum(map(int,str(2**k))))
def paths(M,N,forb):
    @lru_cache(None)
    def f(i,j):
        if (i,j) in forb or i>M or j>N: return 0
        if (i,j)==(M,N): return 1
        return f(i+1,j)+f(i,j+1)
    return f(0,0)
M,N=rng.randint(4,6),rng.randint(4,6); cells=[(i,j) for i in range(M+1) for j in range(N+1) if (i,j) not in [(0,0),(M,N)]]
fb=tuple(rng.sample(cells,2)); add(f"number of monotone lattice paths (steps +1 in x or +1 in y) from (0,0) to ({M},{N}) avoiding points {list(fb)}", paths(M,N,frozenset(fb)))
cells=[(i,j) for i in range(8) for j in range(8) if (i,j) not in [(0,0),(7,7)]]; fb=tuple(rng.sample(cells,3))
add(f"number of monotone lattice paths from (0,0) to (7,7) avoiding points {list(fb)}", paths(7,7,frozenset(fb)))
Nn=rng.randint(1000,5000); ps=rng.sample([2,3,5,7,11,13],3); Mm=ps[0]*ps[1]*ps[2]
add(f"how many integers in 1..{Nn} are coprime to {Mm}", sum(1 for i in range(1,Nn+1) if math.gcd(i,Mm)==1))
n,m=rng.randint(50,90),rng.randint(50,150)
fa,fb2=0,1
for _ in range(n): fa,fb2=fb2,fa+fb2
add(f"F({n}) mod {m}, where F(0)=0, F(1)=1", fa%m)
def det(Mx):
    if len(Mx)==1: return Mx[0][0]
    return sum((-1)**c*Mx[0][c]*det([r[:c]+r[c+1:] for r in Mx[1:]]) for c in range(len(Mx)))
M3=[[rng.randint(-9,9) for _ in range(3)] for _ in range(3)]; add(f"determinant of {M3}", det(M3))
M4=[[rng.randint(-5,5) for _ in range(4)] for _ in range(4)]; add(f"determinant of {M4}", det(M4))
json.dump(A, open(os.path.join(HERE,".p4_hidden.json"),"w"))
for i,t in enumerate(T): print(i, t)
