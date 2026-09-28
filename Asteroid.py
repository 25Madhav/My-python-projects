import turtle, time, random, math

wn = turtle.Screen()
wn.title("Retro Asteroids")
wn.bgcolor("#18187F")
wn.setup(width=800, height=800)
wn.tracer(0)

def init_t(shape, color, sw, sl, x=0, y=0, h=90, vis=True):
    t = turtle.Turtle()
    t.speed(0)
    t.shape(shape)
    t.color(color)
    t.penup()
    t.goto(x, y)
    t.setheading(h)
    t.shapesize(stretch_wid=sw, stretch_len=sl)
    if not vis: t.hideturtle()
    return t

player = init_t("triangle", "#00ffcc", 0.6, 1.2)
exhaust = init_t("triangle", "#ff6600", 0.4, 0.6, vis=False)
hud = init_t("square", "white", 1, 1, -370, 360, vis=False)

player.dx = player.dy = player.rotation_speed = score = 0
player.is_thrusting = game_over = False
lives = 3

lasers, asteroids = [], []

def draw_hud():
    hud.clear()
    hud.write(f"SCORE: {score}  LIVES: {lives}", align="left", font=("Courier", 16, "bold"))

draw_hud()

def rotate_l(): player.rotation_speed = 4
def rotate_r(): player.rotation_speed = -4
def stop_rot(): player.rotation_speed = 0
def start_th(): player.is_thrusting = True
def stop_th(): player.is_thrusting = False

def fire_laser():
    if len(lasers) < 5 and not game_over:
        r = math.radians(player.heading())
        l = init_t("square", "#ffff00", 0.15, 0.8, player.xcor(), player.ycor(), player.heading())
        l.dx, l.dy, l.spawn_time = math.cos(r) * 9 + player.dx, math.sin(r) * 9 + player.dy, time.time()
        lasers.append(l)

def spawn_ast(x, y, size):
    sz_map = {3: 3.0, 2: 1.8, 1: 0.8}
    a = init_t("circle", "#888899", sz_map[size], sz_map[size], x, y, random.randint(0, 360))
    r = math.radians(a.heading())
    sp = random.uniform(0.8, 1.8) * (4 - size)
    a.dx, a.dy, a.size = math.cos(r) * sp, math.sin(r) * sp, size
    asteroids.append(a)

def reset_field():
    for lst in (asteroids, lasers):
        for x in lst: x.hideturtle()
        lst.clear()
    exhaust.hideturtle()
    for _ in range(5):
        spawn_ast(random.choice([random.randint(-380, -100), random.randint(100, 380)]), random.choice([random.randint(-380, -100), random.randint(100, 380)]), 3)

reset_field()

wn.listen()
for k, f in [("Left", rotate_l), ("a", rotate_l), ("Right", rotate_r), ("d", rotate_r), ("Up", start_th), ("w", start_th)]:
    wn.onkeypress(f, k)
for k, f in [("Left", stop_rot), ("a", stop_rot), ("Right", stop_rot), ("d", stop_rot), ("Up", stop_th), ("w", stop_th)]:
    wn.onkeyrelease(f, k)
wn.onkeypress(fire_laser, "space")

def wrap(t, b=410):
    if t.xcor() > b: t.setx(-b)
    if t.xcor() < -b: t.setx(b)
    if t.ycor() > b: t.sety(-b)
    if t.ycor() < -b: t.sety(b)

while not game_over:
    wn.update()
    time.sleep(0.015)
    player.left(player.rotation_speed)
    
    if player.is_thrusting:
        r = math.radians(player.heading())
        player.dx += math.cos(r) * 0.15
        player.dy += math.sin(r) * 0.15
        exhaust.goto(player.xcor() - math.cos(r) * 14, player.ycor() - math.sin(r) * 14)
        exhaust.setheading(player.heading() + 180)
        if random.random() > 0.3:
            exhaust.color(random.choice(["#ff3300", "#ff6600", "#ffcc00"]))
            exhaust.showturtle()
        else: exhaust.hideturtle()
    else: exhaust.hideturtle()

    player.dx, player.dy = player.dx * 0.99, player.dy * 0.99
    player.setx(player.xcor() + player.dx)
    player.sety(player.ycor() + player.dy)
    wrap(player)

    for l in lasers[:]:
        l.setx(l.xcor() + l.dx)
        l.sety(l.ycor() + l.dy)
        wrap(l)
        if time.time() - l.spawn_time > 1.2:
            l.hideturtle()
            lasers.remove(l)

    for a in asteroids[:]:
        a.setx(a.xcor() + a.dx)
        a.sety(a.ycor() + a.dy)
        wrap(a, 420)

        if player.distance(a) < (a.size * 13 + 8):
            lives -= 1
            draw_hud()
            player.goto(0, 0)
            player.setheading(90)
            player.dx = player.dy = 0
            player.is_thrusting = False
            exhaust.hideturtle()
            
            if lives <= 0:
                game_over = True
                for lst in (asteroids, lasers, [player]):
                    for x in lst: x.hideturtle()
                hud.clear()
                hud.goto(0, 20); hud.color("red")
                hud.write("GAME OVER", align="center", font=("Courier", 40, "bold"))
                hud.goto(0, -30); hud.color("white")
                hud.write(f"FINAL SCORE: {score}", align="center", font=("Courier", 24, "bold"))
                wn.update()
                break
            else:
                reset_field()
                time.sleep(1)
                break

        for l in lasers[:]:
            if l.distance(a) < (a.size * 13 + 5):
                l.hideturtle()
                if l in lasers: lasers.remove(l)
                score += (4 - a.size) * 10
                draw_hud()
                if a.size > 1:
                    spawn_ast(a.xcor(), a.ycor(), a.size - 1)
                    spawn_ast(a.xcor(), a.ycor(), a.size - 1)
                a.hideturtle()
                asteroids.remove(a)
                break

    if not asteroids and not game_over:
        for _ in range(6):
            spawn_ast(random.choice([random.randint(-380, -100), random.randint(100, 380)]), random.choice([random.randint(-380, -100), random.randint(100, 380)]), 3)

wn.mainloop()