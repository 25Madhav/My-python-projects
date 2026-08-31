import pygame,random
pygame.init()
W,H=800,500;s=pygame.display.set_mode((W,H));clock=pygame.time.Clock()
f=pygame.font.Font(None,24);big=pygame.font.Font(None,34)

D=[("Flamegrin","Fire",(230,70,40)),("Aquabbit","Water",(40,130,230)),
("Leafhorn","Grass",(60,180,70)),("Voltix","Electric",(240,210,30)),
("Rocko","Rock",(130,100,70)),("Fanglet","Dark",(150,60,150))]

def mon():
 n,t,c=random.choice(D);lv=random.randint(2,5);m=25+lv*6
 return {"n":n,"t":t,"c":c,"hp":m,"max":m,"lv":lv,"xp":0,"wins":0}

party=[mon()];active=0;pot=3;coins=0;cam=[0,0];battle=None;msg="Explore the world!"
P=pygame.Rect(400,250,22,28)

walls=[pygame.Rect(500,100,180,100),pygame.Rect(1050,250,180,120),
pygame.Rect(1500,80,200,130),pygame.Rect(1800,350,170,100)]
water=[pygame.Rect(700,0,260,250),pygame.Rect(1250,300,230,220)]
grass=[pygame.Rect(100,100,300,180),pygame.Rect(850,300,250,170),
pygame.Rect(1550,300,250,170),pygame.Rect(2050,80,250,200)]
trees=[pygame.Rect(40,360,90,120),pygame.Rect(420,300,100,130),
pygame.Rect(1150,50,100,130),pygame.Rect(1720,230,100,130),
pygame.Rect(2250,330,100,130)]
ruins=[pygame.Rect(1450,300,170,80),pygame.Rect(1950,20,180,70)]
paths=[pygame.Rect(0,230,2400,45),pygame.Rect(600,0,45,700),
pygame.Rect(1300,200,45,500),pygame.Rect(1750,0,45,700)]

types={"Fire":{"Grass":1.5,"Water":.7},"Water":{"Fire":1.5,"Electric":.7},
"Grass":{"Water":1.5,"Fire":.7},"Electric":{"Water":1.5,"Rock":.7},
"Rock":{"Electric":1.5,"Fire":1.3},"Dark":{"Dark":1.2}}

def drawmon(m,x,y,flip=False):
 c=m["c"];pygame.draw.ellipse(s,(25,25,30),(x-4,y+65,74,13))
 pygame.draw.ellipse(s,c,(x,y+15,65,55))
 pygame.draw.circle(s,c,(x+32,y+28),29)
 pygame.draw.polygon(s,c,[(x+8,y+22),(x-20,y-5),(x+3,y+5)])
 pygame.draw.polygon(s,c,[(x+55,y+22),(x+83,y-5),(x+62,y+8)])
 pygame.draw.polygon(s,(40,40,40),[(x+8,y+6),(x+18,y-18),(x+27,y+7)])
 pygame.draw.polygon(s,(40,40,40),[(x+37,y+7),(x+48,y-18),(x+54,y+12)])
 pygame.draw.circle(s,"white",(x+21,y+25),8)
 pygame.draw.circle(s,"black",(x+22,y+25),4)
 pygame.draw.circle(s,"white",(x+43,y+25),8)
 pygame.draw.circle(s,"black",(x+44,y+25),4)
 pygame.draw.arc(s,(30,20,20),(x+20,y+30,28,18),0,3.1,3)
 pygame.draw.circle(s,c,(x+7,y+57),13)
 pygame.draw.circle(s,c,(x+58,y+57),13)

def txt(t,x,y,c="white"):s.blit(f.render(str(t),True,c),(x,y))

def bar(x,y,w,h,val,mx,c):
 pygame.draw.rect(s,(35,35,35),(x,y,w,h))
 pygame.draw.rect(s,c,(x,y,max(0,w*val/mx),h))

def hit(r,objects):
 return any(r.colliderect(x) for x in objects)

run=True
while run:
 clock.tick(30)

 for e in pygame.event.get():
  if e.type==pygame.QUIT:
   run=False

  if e.type==pygame.KEYDOWN:
   if e.key==pygame.K_ESCAPE:
    run=False

   if battle:
    wild,i,turn=battle
    me=party[i]

    if not turn:
     if e.key==pygame.K_1:
      power=random.randint(7,11)+me["lv"]*2
      mult=types.get(me["t"],{}).get(wild["t"],1)
      crit=random.random()<.15
      dmg=int(power*mult*(2 if crit else 1))
      wild["hp"]-=dmg
      wild["hp"]=max(0,wild["hp"])
      msg=f"{'CRITICAL! ' if crit else ''}{me['n']} deals {dmg}!"
      battle[2]=1

     elif e.key==pygame.K_2 and pot:
      me["hp"]=min(me["max"],me["hp"]+25)
      pot-=1
      msg="Potion restored 25 HP!"
      battle[2]=1

     elif e.key==pygame.K_2 and not pot:
      msg="You have no Potions!"

     elif e.key==pygame.K_3 and len(party)<6:
      chance=.45+(wild["max"]-wild["hp"])/wild["max"]*.4
      if random.random()<chance:
       party.append(wild.copy())
       battle=None
       msg=f"{wild['n']} joined your team!"
      else:
       msg="The monster broke free!"
       battle[2]=1

     elif e.key==pygame.K_3 and len(party)>=6:
      msg="Your party is full!"

     elif e.key in [pygame.K_q,pygame.K_w,pygame.K_e]:
      j=[pygame.K_q,pygame.K_w,pygame.K_e].index(e.key)
      if j<len(party) and party[j]["hp"]>0:
       battle[1]=j
       battle[2]=1
       msg=f"{party[j]['n']} entered battle!"

    if battle and wild["hp"]<=0:
     gain=20+wild["lv"]*8
     me["xp"]+=gain
     me["wins"]+=1
     coins+=random.randint(5,15)
     msg=f"Victory! +{gain} XP + coins"
     battle=None

     if me["xp"]>=me["lv"]*30:
      me["xp"]-=me["lv"]*30
      me["lv"]+=1
      me["max"]+=7
      me["hp"]=me["max"]
      msg+=" LEVEL UP!"

    if battle and battle[2]:
     if random.random()<.12:
      msg+=" Enemy missed!"
     else:
      mult=types.get(wild["t"],{}).get(me["t"],1)
      dmg=int(random.randint(4,9)*mult)
      me["hp"]-=dmg
      msg+=f" Enemy hits for {dmg}!"

     if me["hp"]<=0:
      me["hp"]=0
      msg=f"{me['n']} fainted!"
      battle=None

      for j,m in enumerate(party):
       if m["hp"]>0:
        active=j
        break
      else:
       for m in party:
        m["hp"]=m["max"]
       active=0
       msg="Your whole team fainted!"

     if battle:
      battle[2]=0

 # CONTINUOUS MOVEMENT
 if not battle:
  old=P.copy()
  k=pygame.key.get_pressed()

  dx=k[pygame.K_RIGHT]-k[pygame.K_LEFT]
  dy=k[pygame.K_DOWN]-k[pygame.K_UP]

  if k[pygame.K_d]:dx+=1
  if k[pygame.K_a]:dx-=1
  if k[pygame.K_s]:dy+=1
  if k[pygame.K_w]:dy-=1

  P.x+=dx*5
  P.y+=dy*5

  if hit(P,walls+water+trees+ruins):
   P=old

  P.left=max(0,P.left)
  P.top=max(0,P.top)
  P.right=min(2400,P.right)
  P.bottom=min(700,P.bottom)

  if hit(P,grass) and random.random()<.018:
   battle=[mon(),active,0]
   battle[0]["lv"]=max(
    battle[0]["lv"],
    party[active]["lv"]+random.choice([-1,0,1])
   )
   battle[0]["max"]=25+battle[0]["lv"]*6
   battle[0]["hp"]=battle[0]["max"]
   msg="A wild monster appeared!"

  if P.colliderect(pygame.Rect(2150,350,100,100)):
   msg="Ancient Grove discovered!"

 cam[0]=max(0,min(1600,P.centerx-400))
 cam[1]=max(0,min(200,P.centery-250))

 s.fill((75,170,85))

 for r in paths:
  pygame.draw.rect(s,(190,165,105),
  (r.x-cam[0],r.y-cam[1],r.w,r.h))

 for r in grass:
  pygame.draw.rect(s,(45,140,55),
  (r.x-cam[0],r.y-cam[1],r.w,r.h))

 for r in water:
  q=r.move(-cam[0],-cam[1])
  pygame.draw.rect(s,(40,120,210),q)
  for x in range(q.x+20,q.right,45):
   pygame.draw.line(s,(80,170,240),
   (x,q.y+25),(x+20,q.y+25),3)

 for r in walls:
  q=r.move(-cam[0],-cam[1])
  pygame.draw.rect(s,(190,130,70),q)
  pygame.draw.rect(s,(120,70,40),
  (q.x+55,q.y+60,70,40))
  pygame.draw.polygon(s,(150,45,40),
  [(q.x-10,q.y),(q.x+q.w//2,q.y-45),(q.right+10,q.y)])

 for r in ruins:
  q=r.move(-cam[0],-cam[1])
  pygame.draw.rect(s,(105,100,90),q)
  pygame.draw.rect(s,(70,65,60),
  (q.x+20,q.y+20,q.w-40,35))

 for r in trees:
  q=r.move(-cam[0],-cam[1])
  pygame.draw.rect(s,(100,65,35),
  (q.x+38,q.y+55,18,65))
  pygame.draw.circle(s,(35,115,45),
  (q.x+45,q.y+40),38)

 if not battle:
  pygame.draw.rect(s,(50,80,220),
  P.move(-cam[0],-cam[1]))

  m=party[active]

  txt("ARROWS/WASD Explore | Grass = Battles",15,15)
  txt(f"Party {len(party)}/6  Potions:{pot}  Coins:{coins}",15,42)
  txt(f"{m['n']} Lv{m['lv']} {m['t']}  XP:{m['xp']}/{m['lv']*30}",15,69)
  bar(15,94,180,12,m["hp"],m["max"],(60,220,80))
  txt(msg,15,465)

 else:
  s.fill((25,30,50))
  pygame.draw.circle(s,(55,70,100),(650,100),75)
  pygame.draw.circle(s,(45,55,80),(140,330),90)

  wild,i,_=battle
  me=party[i]

  drawmon(wild,590,90)
  drawmon(me,120,260)

  txt(f"{wild['n']} Lv{wild['lv']} [{wild['t']}]",525,55)
  bar(525,155,200,15,wild["hp"],wild["max"],(220,60,60))
  txt(f"HP {wild['hp']}/{wild['max']}",525,175)

  txt(f"{me['n']} Lv{me['lv']} [{me['t']}]",70,350)
  bar(70,375,200,15,me["hp"],me["max"],(60,220,80))
  txt(f"HP {me['hp']}/{me['max']}",70,395)

  txt("1 Attack   2 Potion   3 Catch   Q/W/E Switch",15,440)
  txt(msg,15,20)
  txt("Type advantage = stronger damage!",
  450,465,(240,220,80))

 pygame.display.flip()

pygame.quit()