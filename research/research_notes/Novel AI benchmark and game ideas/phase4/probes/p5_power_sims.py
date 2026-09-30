"""Illustrative power calculations for R2 (assumed SDs are labelled in the report as assumptions)."""
import math, random
z=1.96+0.84
def mde(sd,n): return z*sd*math.sqrt(2/n)
print("Dyad success MDE (pp), SD 0.25/0.30, n=100/150 per arm:")
for sd in (0.25,0.30):
    for n in (100,150): print(f"  sd={sd} n={n}: {100*mde(sd,n):.1f} pp")
print("Learning-slope MDE, 8 campaigns/model, SD of per-campaign slope 0.10/0.15:", [round(mde(s,8),3) for s in (0.10,0.15)])
# Elo SE from n games at ~50%
for n in (8,60,480):
    se_p=0.5/math.sqrt(n); se_elo=se_p*400/(math.log(10)*0.25); print(f"Elo SE for {n} games at 50%: {se_elo:.0f} (95% CI +/-{1.96*se_elo:.0f}); diff of two: 95% +/-{1.96*se_elo*math.sqrt(2):.0f}")
# L50 vs L95 precision in a C17-style staircase: logistic on log2 L with procedure random intercepts, cluster bootstrap
def sim(seed, nproc=50, Ls=None, k=5, a_sd=1.0, slope=1.2, log2L50=9.0):
    rng=random.Random(seed); Ls=Ls or [3+i*0.75 for i in range(12)]  # log2 L from 8 to ~1400... 
    data=[]
    for p in range(nproc):
        u=rng.gauss(0,a_sd)
        for x in Ls:
            pr=1/(1+math.exp(-(slope*(log2L50-x)+u)))
            for _ in range(k): data.append((p,x,1 if rng.random()<pr else 0))
    return data
def fit(data, iters=300):
    a,b=0.0,0.0
    for _ in range(iters):  # Newton for logit p = a + b*x
        g0=g1=h00=h01=h11=0
        for _,x,y in data:
            p=1/(1+math.exp(-(a+b*x))); r=y-p; w=p*(1-p)
            g0+=r; g1+=r*x; h00+=w; h01+=w*x; h11+=w*x*x
        det=h00*h11-h01*h01; da=(h11*g0-h01*g1)/det; db=(-h01*g0+h00*g1)/det
        a+=da; b+=db
        if abs(da)+abs(db)<1e-8: break
    L50=-a/b; L95=(math.log(0.95/0.05)-a)/b
    return L50,L95
data=sim(1)
base=fit(data); print(f"point: log2 L50={base[0]:.2f}, log2 L95={base[1]:.2f}")
procs=sorted(set(p for p,_,_ in data)); byp={p:[d for d in data if d[0]==p] for p in procs}
rng=random.Random(7); b50=[]; b95=[]
for _ in range(200):
    samp=[d for p in (rng.choice(procs) for _ in procs) for d in byp[p]]
    l50,l95=fit(samp,60); b50.append(l50); b95.append(l95)
b50.sort(); b95.sort()
print(f"cluster-bootstrap 95% CI log2 L50: [{b50[5]:.2f},{b50[194]:.2f}] (width x{2**(b50[194]-b50[5]):.2f})")
print(f"cluster-bootstrap 95% CI log2 L95: [{b95[5]:.2f},{b95[194]:.2f}] (width x{2**(b95[194]-b95[5]):.2f})")
