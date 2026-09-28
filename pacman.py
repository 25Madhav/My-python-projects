import pygame,sys,math

W,H,T=560,620,20
BLACK=(0,0,0);BLUE=(0,0,255);YELLOW=(255,255,0)
WHITE=(255,255,255);RED=(255,0,0);PINK=(255,182,193)

M=[
"############################",
"#............##............#",
"#.####.#####.##.#####.####.#",
"#.#  #.#   #.##.#   #.#  #.#",
"#.####.#####.##.#####.####.#",
"#..........................#",
"#.####.##.########.##.####.#",
"#......##....##....##......#",
"######.#####.##.#####.######",
"#............##............#",
"#.####.#####.##.#####.####.#",
"#..........................#",
"#.####.##.########.##.####.#",
"#......##....##....##......#",
"#.####.#####....#####.####.#",
"#..........................#",
"#.####.##.########.##.####.#",
"#............##............#",
"############################"]

M=[list(r) for r in M]

class Player:
 def __init__(self,x,y):
  self.x,self.y=x*T+10,y*T+10;self.d=(0,0);self.n=(0,0)
 def move(self):
  nx,ny=self.x+self.n[0]*2,self.y+self.n[1]*2
  if M[int(ny//T)][int(nx//T)]!="#":self.d=self.n
  nx,ny=self.x+self.d[0]*2,self.y+self.d[1]*2
  if M[int(ny//T)][int(nx//T)]!="#":self.x,self.y=nx,ny
 def draw(self):
  a={(1,0):0,(0,1):270,(-1,0):180,(0,-1):90}.get(self.d,0)
  pygame.draw.arc(s,YELLOW,(self.x-9,self.y-9,18,18),
   math.radians(a+30),math.radians(a+330),9)

class Ghost:
 def __init__(self,x,y,c):
  self.x,self.y=x*T+10,y*T+10;self.c=c;self.d=(1,0)
 def move(self):
  dirs=[(1,0),(-1,0),(0,1),(0,-1)]
  if int(self.x)%T==10 and int(self.y)%T==10:
   choices=[]
   for d in dirs:
    nx,ny=self.x+d[0]*T,self.y+d[1]*T
    if 0<=nx<W and 0<=ny<H and M[int(ny//T)][int(nx//T)]!="#":
     dist=abs(nx-p.x)+abs(ny-p.y)
     if d!=(-self.d[0],-self.d[1]):choices.append((dist,d))
   if choices:self.d=min(choices)[1]
  self.x+=self.d[0];self.y+=self.d[1]
 def draw(self):
  pygame.draw.circle(s,self.c,(int(self.x),int(self.y)),9)

pygame.init()
s=pygame.display.set_mode((W,H));clock=pygame.time.Clock()
font=pygame.font.SysFont("Arial",40)
p=Player(13,15);g=[Ghost(1,1,RED),Ghost(26,1,PINK)]
score=0;run=True;gameover=False

while run:
 for e in pygame.event.get():
  if e.type==pygame.QUIT:run=False
  if e.type==pygame.KEYDOWN:
   p.n={pygame.K_RIGHT:(1,0),pygame.K_LEFT:(-1,0),
        pygame.K_UP:(0,-1),pygame.K_DOWN:(0,1)}.get(e.key,p.n)
   if gameover and e.key==pygame.K_r:
    p=Player(13,15);g=[Ghost(1,1,RED),Ghost(26,1,PINK)]
    M=[list(r) for r in M];score=0;gameover=False
 if not gameover:
  p.move()
  for x in g:x.move()
  x,y=int(p.x//T),int(p.y//T)
  if M[y][x]==".":
   M[y][x]=" ";score+=10
  for x in g:
   if abs(p.x-x.x)<15 and abs(p.y-x.y)<15:gameover=True

 s.fill(BLACK)
 for y,row in enumerate(M):
  for x,v in enumerate(row):
   if v=="#":pygame.draw.rect(s,BLUE,(x*T,y*T,T,T),1)
   elif v==".":pygame.draw.circle(s,WHITE,(x*T+10,y*T+10),3)
 p.draw()
 for x in g:x.draw()
 pygame.display.flip();clock.tick(60)

 if gameover:
  text=font.render("GAME OVER",True,WHITE)
  s.blit(text,(180,190));pygame.display.flip()
  pygame.time.wait(1000)



pygame.quit();sys.exit()
