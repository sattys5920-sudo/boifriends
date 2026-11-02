# 롯폰기: 교차로 위를 지나는 고가 고속도로, 북동 초고층 타워와 광장의 거대한 거미 조각, 뒤쪽 붉은 철탑,
#   북서 유리 물결 미술관, 남쪽 밤거리(클럽·바·잡화 할인점)
NAME, NX, NY = 'tk_roppongi', 44, 34
exec(open('tk_lib.py').read())
RX0, RX1, RY0, RY1 = 19, 24, 15, 20
fill('walk', 0, 0, NX, NY)
fill('plaza', 26, 9, 43, 14); fill('plaza', 2, 9, 16, 14)
fill('road', 0, RY0, NX, RY1); fill('road', RX0, 0, RX1, NY)
fill('redwalk', 4, 22, 16, 33)
def ov(fx, fy, t):
    if t != 'road': return None
    inx, iny = RX0 <= fx < RX1, RY0 <= fy < RY1
    if inx and iny: return None
    if iny and (RX0 - 2.2 < fx < RX0 - .2 or RX1 + .2 < fx < RX1 + 2.2): return hexc('#ECECE6') if (fy * 2.5) % 1 < .5 else None
    if inx and (RY0 - 2.2 < fy < RY0 - .2 or RY1 + .2 < fy < RY1 + 2.2): return hexc('#ECECE6') if (fx * 2.5) % 1 < .5 else None
    if iny: return road_x(fx, fy, RY0, RY1)
    if inx: return road_y(fx, fy, RX0, RX1)
ground(ov)
# ---- 뒤쪽 붉은 철탑 ----
def red_tower(img):
    d = ImageDraw.Draw(img); X, Y = P(14, 1)
    for k in range(0, 200):
        wd = max(1, int(18 * (1 - k / 200) ** 1.6)); c = hexc('#E8503A') if (k // 18) % 2 == 0 else hexc('#F4F0EA')
        if k % 6 == 0 or k < 4: d.line([(X - wd, Y - k), (X + wd, Y - k)], fill=c)
        d.point((X - wd, Y - k), fill=c); d.point((X + wd, Y - k), fill=c)
        if k % 12 == 0:
            d.line([(X - wd, Y - k), (X + wd, Y - k - 12)], fill=shade(c, .8)); d.line([(X + wd, Y - k), (X - wd, Y - k - 12)], fill=shade(c, .8))
    for kk in (70, 130): d.rectangle([X - 8, Y - kk - 6, X + 8, Y - kk], fill=hexc('#F4F0EA')); d.rectangle([X - 8, Y - kk - 6, X + 8, Y - kk - 5], fill=hexc('#E8503A'))
    d.line([(X, Y - 200), (X, Y - 226)], fill=hexc('#F4F0EA'))
bld('redtower', [13, 0, 15, 2], red_tower, act=('붉은 철탑', '올려다보기'))
# ---- 북서: 유리 물결 미술관 ----
def wave_glass(u, v, w, h):
    edge = 6 + 4 * math.sin(u / 9)
    if v > h - edge: return None if v > h - 2 else hexc('#5A6A80')
    c = hexc('#9AC4DC') if (u // 4 + v // 6) % 2 else hexc('#B4D8EC')
    if v % 6 == 0: c = hexc('#6A8098')
    return c
bld('museum', [1, 1, 12, 8], shop(1, 1, 12, 8, 60, '#9AC4DC', [('L', 0, 0, 88, 60, wave_glass), ('R', 0, 0, 56, 60, wave_glass), ('L', 38, 0, 14, 22, glass(False, door=(1, 13)))], roofc='#6A7A8A'),
    door=dict(tile=[6, 8], to='tk_artmuseum', label='미술관', spawn=[6, 8]))
# ---- 북동: 초고층 타워 ----
def tower_layers():
    out = []
    for v in range(30, 236, 10):
        for u in range(2, 70, 6): out.append(('L', u, v, 4, 7, win(random.random() < .3, frame='#3A4A5A')))
        for u in range(2, 54, 6): out.append(('R', u, v, 4, 7, win(random.random() < .25, frame='#3A4A5A')))
    out += [('L', 0, 0, 72, 26, glass(False, door=(28, 44), tint='#A8C8E0')), ('R', 0, 0, 56, 26, glass(False, tint='#A8C8E0'))]
    return out
bld('hills', [32, 0, 41, 7], combo(shop(32, 0, 41, 7, 240, '#4A5A6A', tower_layers(), roofc='#3A4652'),
                                   lambda img: [ImageDraw.Draw(img).line([up(P(36.5, 3.5), 240), up(P(36.5, 3.5), 262)], fill=hexc('#E8503A'), width=2)]),
    door=dict(tile=[36, 7], to='tk_observatory', label='전망대 타워', spawn=[6, 8]))
def spider(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + 1.5, y + 1.5); bz = hexc('#3A3230'); hb = up((cx, cy), 46)
    for ang in (-150, -120, -60, -30, 30, 60, 120, 150):
        a = math.radians(ang); kx, ky = hb[0] + 20 * math.cos(a), hb[1] - 10 + 6 * math.sin(a)
        fx_, fy_ = cx + 30 * math.cos(a), cy + 12 * math.sin(a)
        d.line([hb, (kx, ky - 14)], fill=bz, width=2); d.line([(kx, ky - 14), (fx_, fy_)], fill=bz, width=2)
    d.ellipse([hb[0] - 8, hb[1] - 6, hb[0] + 8, hb[1] + 6], fill=bz); d.ellipse([hb[0] - 6, hb[1] + 2, hb[0] + 6, hb[1] + 12], fill=hexc('#4A403C'))
    for k in range(3): d.ellipse([hb[0] - 2 + k * 2 - 2, hb[1] + 5, hb[0] - 2 + k * 2, hb[1] + 7], fill=hexc('#E8E4DA'))
shared('spider', spider)
put('spider', 'spider', 30, 9, w=3, d=3, act=('거대한 거미 조각', '다리 사이로 지나가 보기'))
for (x, y) in ((27, 10), (41, 10), (27, 13), (41, 13)): put('tree', 'tree_round', x, y)
# ---- 고가 고속도로 (가로길 위) ----
def expressway(img):
    d = ImageDraw.Draw(img); Hh = 54
    for x in range(1, NX, 6):
        for y in (RY0 + .6, RY1 - .6):
            if RX0 - 1 < x < RX1 + 1: continue
            p_ = P(x + .5, y); d.rectangle([p_[0] - 3, p_[1] - Hh, p_[0] + 3, p_[1]], fill=hexc('#A8A8AC')); d.rectangle([p_[0] - 3, p_[1] - Hh, p_[0] - 1, p_[1]], fill=hexc('#C4C4C8'))
    box(d, 0, RY0 + .1, NX, RY1 - .1, 8, '#8A8A90', '#9A9AA0', '#5A5C68', lift=Hh)
    a, b = up(P(0, RY1 - .1), Hh + 8), up(P(NX, RY1 - .1), Hh + 8); d.line([a, b], fill=hexc('#C8C8CC'), width=2)
    for x in range(0, NX, 2):
        p_ = up(P(x + .5, (RY0 + RY1) / 2), Hh + 8); d.line([p_, (p_[0] + 5, p_[1] + 2.5)], fill=hexc('#E8E8E0'))
flat_unique('expressway', expressway)
# ---- 남쪽 밤거리 (낮게) ----
NIGHT = [(1, 4, 22, 28, 38, '#1E1A2A', '클럽', 'tk_club', '#FF4AA8'), (1, 4, 28, 33, 34, '#2A1E1E', '재즈 바', 'tk_bar', '#FFB84A')]
for (x0, x1, y0, y1, h, wall, lab, to, neon) in NIGHT:
    bld('night', [x0, y0, x1, y1], combo(shop(x0, y0, x1, y1, h, wall, [('R', 2, 0, 36, 22, glass(False, door=(12, 24), tint='#4A2A5A')), ('R', 0, 24, 40, 8, sign('#1E1A2A', neon, latin=True)),
        ('L', 2, 6, 20, 20, poster(len(lab)))], roofc='#2A2630'), vsign(x0, y1, 18, h - 2, 30, neon, '#FFFFFF')),
        door=dict(tile=[x1, (y0 + y1) // 2], to=to, label=lab, spawn=[6, 8]))
bld('discount', [26, 22, 34, 28], shop(26, 22, 34, 28, 40, '#F2D028', [('L', 0, 0, 64, 24, glass(True, door=(26, 38), tint='#FFF4C8')), ('L', 0, 24, 64, 14, sign('#2A3C9C', '#F2D028', 14)),
    ('R', 0, 0, 48, 24, glass(True, tint='#FFF4C8')), ('R', 0, 24, 48, 14, sign('#E8463A', '#FFFFFF', 10))], roofc='#B89A20'),
    door=dict(tile=[30, 28], to='tk_discount', label='잡화 할인점', spawn=[6, 8]))
bld('bar', [36, 22, 42, 26], shop(36, 22, 42, 26, 34, '#3A2A3A', [('L', 2, 0, 44, 22, glass(False, door=(18, 30), tint='#C88A5A')), ('L', 0, 24, 48, 8, sign('#3A2A3A', '#5AD8FF', latin=True)),
    ('R', 2, 2, 28, 20, glass(False, tint='#C88A5A'))], roofc='#2A2030'), door=dict(tile=[39, 26], to='tk_rooftop', label='루프톱 바', spawn=[6, 8]))
for (x, y) in ((8, 24), (12, 24), (8, 30), (12, 30)): put('tree', 'tree_round', x, y)
for (x, y) in ((10, 27), (14, 28)): put('bench', 'bench2', x, y, act=('거리 벤치', '앉아서 쉬기'))
put('vend', 'vend#D23A3A', 26, 30, act=('자판기', '음료 뽑기')); put('vend', 'vend#E8E8E4', 27, 30, act=('자판기', '음료 뽑기'))
for (x, y, k) in ((5, 16, 'taxiY'), (34, 18, 'taxi'), (12, 18, 'car#2A2A30' if False else 'car#3A4A6A')): put('car', k, x, y, w=2, act=('달리던 차', '살펴보기'))
for (x, y) in ((2, 13), (16, 13), (26, 14), (42, 14), (2, 21), (16, 21), (26, 21), (42, 21)): put('lamp', 'lamp2', x, y)
edge_exits('tokyo')
finish([dict(n='롯폰기 교차로', t=[21, 17]), dict(n='미술관', t=[6, 9]), dict(n='전망대 타워', t=[36, 8]), dict(n='거미 조각 광장', t=[31, 12]), dict(n='붉은 철탑', t=[14, 3]),
        dict(n='밤거리', t=[10, 27]), dict(n='잡화 할인점', t=[30, 29])], [21, 22])
