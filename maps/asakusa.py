# 아사쿠사: 앞쪽 큰 대문(거대한 붉은 초롱) → 참배길 상점가 → 향로 광장 → 본당, 옆에 오층탑, 동쪽 강변 산책로
NAME, NX, NY = 'tk_asakusa', 40, 36
exec(open('tk_lib.py').read())
SX0, SX1 = 17, 21                         # 참배길 x범위
fill('back', 0, 0, NX, NY)
fill('gravel', 8, 0, 33, 10)              # 경내
fill('stone', SX0, 8, SX1, 31)            # 참배길
fill('stone', 14, 7, 24, 11)              # 향로 광장
fill('road', 0, 32, NX, 36); fill('walk', 0, 31, NX, 32)
fill('walk', 31, 6, 34, 31); fill('water', 34, 0, NX, 31); fill('grass', 37, 0, NX, 4)   # 강변 산책로 + 강 + 건너편 둑
fill('grass', 25, 10, 31, 30); fill('grass', 8, 10, 12, 30)
def ov(fx, fy, t):
    if t == 'road': return road_x(fx, fy, 32, 36, cross=[(SX0, SX1)])
    if t == 'stone' and SX0 + 1.8 < fx < SX1 - 1.8 and int(fy) % 2 == 0: return hexc('#C0BAAE')   # 가운데 디딤돌
ground(ov)
RED, RED2 = '#C8402E', '#A8301E'
# ---- 본당 ----
bld('hall', [13, 0, 25, 6], combo(shop(13, 0, 25, 6, 34, RED, [
    ('L', 0, 0, 96, 34, lambda u, v, w, h: hexc('#2A2226') if u % 16 in (0, 1) else (hexc('#F2E6CC') if v < 26 and 4 < u % 16 < 13 else None)),
    ('L', 40, 0, 16, 26, lambda u, v, w, h: hexc('#3A2418') if u in (0, w - 1) else hexc('#6A3A20')),
    ('R', 0, 0, 48, 34, lambda u, v, w, h: hexc('#2A2226') if u % 16 in (0, 1) else None)], roof='#3E4A4E', rh=34, tex=4),
    lantern_on(13, 6, 48, 36, '#E8463A', big=True)),
    door=dict(tile=[19, 6], to='tk_temple', label='본당', spawn=[6, 8]))
def incense(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .1, y + .1, x + 1.9, y + 1.9, 8, '#5A5048', '#6A5E54', '#3A3430')
    hip(d, x + .4, y + .4, x + 1.6, y + 1.6, 22, 8, '#4A4038', e=.3)
    for p_ in (P(x + .5, y + .5), P(x + 1.5, y + .5), P(x + .5, y + 1.5), P(x + 1.5, y + 1.5)): d.line([up(p_, 8), up(p_, 22)], fill=hexc('#4A4038'), width=2)
    cx, cy = up(P(x + 1, y + 1), 30)
    for k in range(5): d.point((cx + random.randint(-3, 3), cy - k * 3), fill=hexc('#D8D4E0'))
shared('incense', incense)
put('incense', 'incense', 18, 8, w=2, d=2, act=('향로', '연기 쐬기'))
# ---- 오층탑 ----
def pagoda(img):
    d = ImageDraw.Draw(img); x0, y0, s = 26, 2, 4
    base = 0
    box(d, x0 - .3, y0 - .3, x0 + s + .3, y0 + s + .3, 4, '#A8A296', '#B8B2A6', '#C8C2B6')
    base = 4
    for i in range(5):
        m = i * .25; wh = 14
        box(d, x0 + m, y0 + m, x0 + s - m, y0 + s - m, wh, RED2, RED, RED, lift=base)
        X, Y = up(P(x0 + m, y0 + s - m), base); d.rectangle([X + 8, Y + 1 - 10, X + 14, Y + 4 - 4], fill=hexc('#F2E6CC'))
        hip(d, x0 + m, y0 + m, x0 + s - m, y0 + s - m, base + wh, 6, '#3E4A4E', e=.7)
        base += wh + 4
    cx, cy = up(P(x0 + s / 2, y0 + s / 2), base + 2)
    d.rectangle([cx - 1, cy - 34, cx + 1, cy], fill=hexc('#C8A84A'))
    for k in range(0, 30, 5): d.line([(cx - 3, cy - 4 - k), (cx + 3, cy - 4 - k)], fill=hexc('#C8A84A'))
bld('pagoda', [26, 2, 30, 6], pagoda, act=('오층탑', '올려다보기'))
# ---- 참배길 상점(서쪽 줄: 옆면이 길을 봐요) ----
SHOPS = [('#F2E6CC', '#C8402E', '센베이 가게'), ('#E8D8B8', '#3A6A4A', '기념품 가게'), ('#F2E6CC', '#2E4A8A', '닌교야키'), ('#E8D0C0', '#C8402E', '부채 가게'), ('#F2E6CC', '#6A3A8A', '빗과 비녀')]
for i, (wall, cl, lab) in enumerate(SHOPS):
    y0 = 11 + i * 4
    bld('nakamise', [13, y0, 17, y0 + 4], combo(shop(13, y0, 17, y0 + 4, 26, wall, [
        ('R', 2, 0, 28, 18, lambda u, v, w, h, c=cl: hexc('#F8E8C8') if v < 12 else (hexc(c) if u % 5 else hexc('#FFFFFF'))),
        ('R', 2, 2, 28, 9, glass(True, tint='#F2E0C0')), ('R', 0, 19, 32, 6, sign('#F8F0E0', cl, 6)),
        ('L', 0, 0, 32, 26, lambda u, v, w, h: hexc('#8A5A3A') if u % 8 == 0 else None)], roof='#4A4A52', rh=10, tex=4)),
        door=dict(tile=[17, y0 + 2], to='tk_shop%d' % i, label=lab, spawn=[6, 8]))
def stall(col, goods):
    def f(img, x, y):
        d = ImageDraw.Draw(img)
        box(d, x + .1, y + .1, x + .9, y + .9, 10, '#8A5A3A', '#9A6A44', '#C08A5E')
        for k, g in enumerate(goods):
            X, Y = up(P(x + .3 + k * .2, y + .5), 11); d.ellipse([X - 2, Y - 2, X + 2, Y + 1], fill=hexc(g))
        for p_ in (P(x + .1, y + .9), P(x + .9, y + .9), P(x + .9, y + .1)): d.line([up(p_, 10), up(p_, 24)], fill=hexc('#5A3A22'))
        a1, a2, a3, a4 = up(P(x, y), 24), up(P(x + 1, y), 24), up(P(x + 1, y + 1), 26), up(P(x, y + 1), 26)
        poly(d, [a1, a2, a3, a4], hexc(col))
        for k in range(3):
            q = lambda s, e, t: (s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t)
            poly(d, [q(a4, a3, k / 3), q(a4, a3, (k + .5) / 3), q(a1, a2, (k + .5) / 3), q(a1, a2, k / 3)], hexc('#F2EAD8'))
    return f
for k, c in enumerate(('#C8402E', '#3A6A4A', '#2E4A8A', '#C88A2E')): shared('stall%d' % k, stall(c, ['#F2C85A', '#E86A6A', '#FFFFFF']))
for i, y in enumerate(range(12, 30, 3)): put('stall', 'stall%d' % (i % 4), 21, y, act=(['당고 노점', '모찌 노점', '부채 노점', '과자 노점'][i % 4], '구경하기'))
# 참배길 초롱 줄
def lantern_post(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 30, cx, cy], fill=hexc('#3A2A20'))
    d.ellipse([cx - 4, cy - 34, cx + 3, cy - 22], fill=hexc('#E8463A')); d.rectangle([cx - 3, cy - 34, cx + 2, cy - 33], fill=OUTL); d.rectangle([cx - 3, cy - 23, cx + 2, cy - 22], fill=OUTL)
    d.line([(cx - 2, cy - 30), (cx - 2, cy - 26)], fill=hexc('#FFB080'))
shared('lpost', lantern_post)
for y in range(12, 30, 3): put('lpost', 'lpost', 16, y + 1 if (16, y + 1) not in occupied else y)
# ---- 큰 대문(거대 초롱) ----
def gate(img):
    d = ImageDraw.Draw(img)
    for xa in (15.4, 21.6):
        box(d, xa, 28.6, xa + 1, 30.4, 36, RED2, RED, RED)
        X, Y = P(xa, 30.4); d.rectangle([X + 2, Y - 30, X + 9, Y - 8], fill=hexc('#3A2A2A'))   # 수호상 자리
    box(d, 15.2, 28.5, 22.8, 30.5, 6, RED2, RED, '#8A2A1E', lift=36)
    hip(d, 15.2, 28.5, 22.8, 30.5, 42, 16, '#3E4A4E', e=.6)
    X, Y = up(P(19, 29.5), 36)
    d.line([(X, Y), (X, Y + 4)], fill=OUTL)
    d.ellipse([X - 9, Y + 4, X + 9, Y + 30], fill=hexc('#D8382A')); d.rectangle([X - 7, Y + 3, X + 7, Y + 6], fill=OUTL); d.rectangle([X - 7, Y + 28, X + 7, Y + 31], fill=OUTL)
    for k in range(3): d.line([(X - 8, Y + 11 + k * 6), (X + 8, Y + 11 + k * 6)], fill=hexc('#B82A20'))
    d.rectangle([X - 3, Y + 10, X + 3, Y + 24], fill=OUTL); d.rectangle([X - 2, Y + 11, X + 2, Y + 23], fill=hexc('#D8382A'))
    d.line([(X - 6, Y + 8), (X - 6, Y + 26)], fill=hexc('#F87A5A'))
bld('gate', [15, 28, 23, 31], gate, solid=False, act=('큰 대문의 거대한 초롱', '올려다보기'))
for y in (29, 30):
    for x in (15, 16, 22): occupied.add((x, y))
for o in objs:
    if o['name'] == 'gate': o['box'] = [17, 28, 21, 31]
# ---- 서쪽 골목: 료칸 + 찻집 ----
bld('ryokan', [2, 11, 10, 18], shop(2, 11, 10, 18, 30, '#E8DCC4', [
    ('L', 0, 0, 64, 30, lambda u, v, w, h: hexc('#5A3A22') if u % 12 in (0, 1) or v in (0, 1, 29) else None),
    ('L', 24, 0, 16, 22, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 or v % 6 == 0 else hexc('#FFE6B0')),
    ('R', 6, 6, 40, 14, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 or v % 5 == 0 else hexc('#FFE6B0'))], roof='#3E4A4E', rh=16, tex=4),
    door=dict(tile=[6, 18], to='tk_ryokan', label='료칸', spawn=[6, 8]))
bld('teahouse', [2, 21, 8, 27], combo(shop(2, 21, 8, 27, 26, '#8A6A4A', [
    ('L', 4, 0, 40, 18, lambda u, v, w, h: hexc('#2A1E18') if v > 10 else hexc('#FFD8A0')),
    ('L', 4, 10, 40, 8, lambda u, v, w, h: hexc('#3A5A8A') if u % 8 else hexc('#1E2E4A')), ('L', 2, 19, 44, 6, sign('#F2E6CC', '#2A2020', 9)),
    ('R', 8, 4, 30, 14, win(True, frame='#4A3020'))], roof='#3E4A4E', rh=12, tex=3), lantern_on(2, 27, 3, 18), lantern_on(2, 27, 45, 18)),
    door=dict(tile=[5, 27], to='tk_tea', label='찻집', spawn=[6, 8]))
# 인력거
def rickshaw(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 9, cy - 12, cx + 1, cy - 1], outline=hexc('#2A2226'), width=2); d.point((cx - 4, cy - 6), fill=hexc('#C8402E'))
    d.polygon([(cx - 6, cy - 14), (cx + 6, cy - 10), (cx + 6, cy - 6), (cx - 6, cy - 10)], fill=hexc('#1E1E26'))
    d.polygon([(cx - 7, cy - 24), (cx + 2, cy - 22), (cx + 3, cy - 12), (cx - 6, cy - 14)], fill=hexc('#2A2226')); d.polygon([(cx - 6, cy - 23), (cx + 1, cy - 21), (cx + 1, cy - 15), (cx - 5, cy - 16)], fill=hexc('#C8402E'))
    d.line([(cx + 4, cy - 9), (cx + 16, cy - 3)], fill=hexc('#2A2226'), width=2)
shared('rickshaw', rickshaw)
put('rickshaw', 'rickshaw', 24, 30, act=('인력거', '타 보기')); put('rickshaw', 'rickshaw', 12, 30, act=('인력거', '타 보기'))
# ---- 강변 ----
for y in range(6, 31, 2): put('rail', 'grailY', 33, y, solid=False)
for (x, y) in ((32, 8), (32, 14), (32, 20), (32, 26)): put('lamp', 'elamp', x, y)
for (x, y) in ((32, 11), (32, 23)): put('bench', 'bench2', x, y, act=('강변 벤치', '강 바라보기'))
def far_tower(img):
    d = ImageDraw.Draw(img); X, Y = P(38.5, 1.5)
    for k in range(0, 190):
        wd = max(1, int(7 - k / 30)); c = hexc('#D8E4F0') if (k // 6) % 2 else hexc('#B8C8DC')
        d.line([(X - wd, Y - k), (X + wd, Y - k)], fill=c)
    for kk in (120, 150): d.ellipse([X - 7, Y - kk - 4, X + 7, Y - kk + 4], fill=hexc('#8AA0BC'))
    d.line([(X, Y - 190), (X, Y - 214)], fill=hexc('#E8E8F0'))
bld('tower', [38, 1, 39, 2], far_tower, solid=False, act=('멀리 보이는 전파탑', '올려다보기'))
# ---- 나무·소품 ----
for (x, y) in ((9, 2), (10, 6), (31, 2), (32, 5), (12, 1), (25, 8), (8, 9)): put('tree', 'tree_pine', x, y)
for (x, y) in ((26, 12), (28, 16), (26, 20), (29, 24), (27, 27), (9, 12), (10, 20), (9, 25), (11, 28)): put('tree', 'tree_pink' if (x + y) % 3 else 'tree_round', x, y)
for (x, y) in ((3, 31), (36, 31)): put('lamp', 'lamp2', x, y)
for (x, y, k) in ((4, 33, 'taxi'), (28, 33, 'car#F2F2EE')): put('car', k, x, y, w=2, act=('달리던 차', '살펴보기'))
edge_exits('tokyo')
finish([dict(n='큰 대문', t=[19, 30]), dict(n='참배길 상점가', t=[19, 20]), dict(n='향로', t=[19, 9]), dict(n='본당', t=[19, 7]), dict(n='오층탑', t=[28, 7]),
        dict(n='강변 산책로', t=[32, 18]), dict(n='료칸', t=[6, 19]), dict(n='찻집', t=[5, 28])], [19, 31])
