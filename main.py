import json,os,sys,urllib.request as u
U=os.environ["MAKEFUN_ENV_URL"]
def P(p,b):
 r=u.Request(U+p,json.dumps(b).encode(),{"content-type":"application/json"})
 with u.urlopen(r)as x:return json.load(x)
V=(0,100,320,330,500,900,0)
N8=(33,31,18,14,-14,-18,-31,-33)
D8=(15,17,-15,-17)
O8=(1,-1,16,-16)
SQ=[i for i in range(128)if not i&136]
RM={0:2,7:1,112:8,119:4}
M=100000;NG=60000
B=[0]*128;RT=0;EP=-1;KS=[0,0];N=0;T={};UU=[];PA=set();KI=[[0,0]for _ in range(64)]
class A(Exception):pass
def ps(p,f,r):
 return(6*r+(4 if f in(3,4)else 0)+(12 if r==6 else 0)if p==1 else(7-abs(2*f-7)-abs(2*r-7))*(2 if p==2 else 1)if p in(2,5)else 3*r+(4 if f in(2,3,4,5)else 0)if p==3 else 8*(r==6)+4*(r>=4)if p==4 else-6*r)
PV=[[0]*128 for _ in range(15)]
for p in range(1,7):
 for s in SQ:
  v=V[p]+ps(p,s&7,s>>4);PV[p+7][s]=v;PV[7-p][s^112]=-v
def E():
 s=0;w=b=0
 for i in SQ:
  x=B[i]
  if x:
   s+=PV[x+7][i]
   if abs(x)==3:
    if x>0:w+=1
    else:b+=1
 return s+30*(w==2)-30*(b==2)
def att(s,by):
 for t in((s-15,s-17)if by>0 else(s+15,s+17)):
  if not t&136 and B[t]==by:return 1
 for d in N8:
  t=s+d
  if not t&136 and B[t]==by*2:return 1
 for d in D8+O8:
  t=s+d
  while not t&136:
   x=B[t]
   if x:
    if x==by*5 or x==by*3 and d in D8 or x==by*4 and d in O8 or x==by*6 and t==s+d:return 1
    break
   t+=d
 return 0
def gen(sd):
 m=[]
 for s in SQ:
  x=B[s]
  if x==0 or(x>0)!=(sd>0):continue
  a=x if x>0 else-x
  if a==1:
   d=16*sd;pr=7 if sd>0 else 0
   t=s+d
   if B[t]==0:
    m+=[(s,t,p)for p in((5,4,3,2)if(t>>4)==pr else(0,))]
    if(s>>4)==(1 if sd>0 else 6)and B[t+d]==0:m.append((s,t+d,0))
   for t in(s+d-1,s+d+1):
    if t&136:continue
    y=B[t]
    if(y and(y>0)!=(sd>0))or t==EP:
     m+=[(s,t,p)for p in((5,4,3,2)if(t>>4)==pr else(0,))]
  else:
   ds=(N8,D8,O8,D8+O8,D8+O8)[a-2]
   sl=a>2 and a!=6
   for d in ds:
    t=s+d
    while 1:
     if t&136:break
     y=B[t]
     if y:
      if(y>0)!=(sd>0):m.append((s,t,0))
      break
     m.append((s,t,0))
     if not sl:break
     t+=d
 K=4 if sd>0 else 116
 for d in(2,-2):
  b=(1 if d>0 else 2)*(1 if sd>0 else 4)
  rf=K+(3 if d>0 else-4)
  es=(K+1,K+2)if d>0 else(K-1,K-2,K-3)
  cs=(K,K+1,K+2)if d>0 else(K,K-1,K-2)
  if RT&b and B[rf]==4*sd and all(not B[s]for s in es)and not any(att(s,-sd)for s in cs):m.append((K,K+d,0))
 return m
def make(m):
 global RT,EP
 f,t,p=m;x=B[f];y=B[t];cs=t;rf=-1
 if abs(x)==1 and t==EP and y==0:
  cs=t-16 if x>0 else t+16;y=B[cs];B[cs]=0
 if abs(x)==6:
  KS[0 if x>0 else 1]=t
  if abs(t-f)==2:
   rf=(7 if t>f else 0)+(112 if x<0 else 0);rt=(f+t)//2;B[rt]=B[rf];B[rf]=0
 UU.append((f,t,p,y,cs,RT,EP,rf))
 if abs(x)==6:RT&=~(3 if x>0 else 12)
 RT&=~RM.get(f,0);RT&=~RM.get(t,0)
 EP=(f+16 if x>0 else f-16)if abs(x)==1 and abs(t-f)==32 else-1
 B[t]=p*(1 if x>0 else-1)if p else x;B[f]=0
def unmake():
 global RT,EP
 f,t,p,y,cs,ort,oep,rf=UU.pop()
 x=B[t]
 if rf>=0:
  rt=(f+t)//2;B[rf]=B[rt];B[rt]=0
 if abs(x)==6:KS[0 if x>0 else 1]=f
 B[f]=x if not p else(1 if x>0 else-1)
 B[t]=0
 if y:B[cs]=y
 RT=ort;EP=oep
def mv(m):
 return 10*V[abs(B[m[1]])]-V[abs(B[m[0]])]//10+900*(m[2]>0)
def legal(sd):
 ms=[]
 for m in gen(sd):
  make(m)
  if not att(KS[0 if sd>0 else 1],-sd):ms.append(m)
  unmake()
 return ms
def qs(sd,al,be,pl):
 global N
 N+=1
 if N>NG:raise A
 ck=att(KS[0 if sd>0 else 1],-sd)
 if ck:
  ms=legal(sd)
  if not ms:return-M+pl
 else:
  st=E()*sd
  if st>=be:return be
  if st>al:al=st
  ms=[]
  for m in gen(sd):
   if B[m[1]]or m[1]==EP or m[2]:
    make(m)
    if not att(KS[0 if sd>0 else 1],-sd):ms.append(m)
    unmake()
 ms.sort(key=mv,reverse=True)
 for m in ms:
  make(m);sc=-qs(-sd,-be,-al,pl+1);unmake()
  if sc>=be:return be
  if sc>al:al=sc
 return al
def srch(sd,dp,al,be,pl):
 global N,EP
 N+=1
 if N>NG:raise A
 k=(tuple(B),sd)
 if k in PA:return 0
 if dp<=0:return qs(sd,al,be,pl)
 e=T.get(k);bm=e[1]if e else None
 if dp>=3 and not att(KS[0 if sd>0 else 1],-sd):
  oep=EP;EP=-1;sc=-srch(-sd,dp-3,-be,-be+1,pl+1);EP=oep
  if sc>=be:return be
 ms=gen(sd)
 ms.sort(key=lambda m:9999*(m==bm)+800*(m==KI[pl][0])+700*(m==KI[pl][1])+mv(m),reverse=True)
 PA.add(k)
 try:
  bs=-M;n=0
  for m in ms:
   make(m)
   if att(KS[0 if sd>0 else 1],-sd):unmake();continue
   n+=1
   sc=-srch(-sd,dp-1,-be,-al,pl+1)
   unmake()
   if sc>bs:bs=sc;bm=m
   if sc>al:al=sc
   if al>=be:
    if not B[m[1]]and not m[2]:KI[pl][1]=KI[pl][0];KI[pl][0]=m
    break
  if n==0:return(-M+pl)if att(KS[0 if sd>0 else 1],-sd)else 0
  T[k]=(dp,bm)
  return bs
 finally:PA.discard(k)
def parse(f):
 global B,RT,EP,KS
 a=f.split();B=[0]*128;RT=0;KS=[0,0]
 r=7;c=0
 for ch in a[0]:
  if ch=='/':r-=1;c=0
  elif ch.isdigit():c+=int(ch)
  else:
   x=("pnbrqk".index(ch.lower())+1)*(1 if ch.isupper() else-1)
   s=r*16+c;B[s]=x;c+=1
   if abs(x)==6:KS[0 if x>0 else 1]=s
 RT=sum(b for b,c in((1,'K'),(2,'Q'),(4,'k'),(8,'q'))if c in a[2])
 EP=-1 if a[3]=='-'else(ord(a[3][1])-49)*16+ord(a[3][0])-97
 return 1 if a[1]=='w' else-1
def uc(m):
 f,t,p=m
 return"abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)+("qrbn"[5-p]if p else"")
def choose(fen):
 global N
 sd=parse(fen)
 PA.clear();PA.add((tuple(B),sd))
 ms=legal(sd)
 if len(ms)==1:return uc(ms[0])
 if len(T)>200000:T.clear()
 best=ms[0];d=1;N=0
 while 1:
  try:
   bs=-M;bm=None;al=-M
   ms.sort(key=lambda m:m==best,reverse=True)
   for m in ms:
    make(m);sc=-srch(-sd,d-1,-M,-al,1);unmake()
    if sc>bs:bs=sc;bm=m
    if sc>al:al=sc
   best=bm
   if bs>M-1000:break
   d+=1
  except A:break
 return uc(best)
while True:
 g=P("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  try:mo=choose(g["fen"])
  except Exception as e:
   print("choose failed:",e,file=sys.stderr);mo=g["legal_moves"][0]
  try:g=P("/move",{"game":g["game"],"move":mo})
  except Exception:
   g=P("/game",{})
   if g["status"]=="your_move":g=P("/move",{"game":g["game"],"move":g["legal_moves"][0]})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
