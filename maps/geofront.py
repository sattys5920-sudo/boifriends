# 지오프론트 본부(특무기관 본부 느낌, 원작 로고·기체는 쓰지 않음): 지하 거대 공동 안의 검은 피라미드 본부,
#   육각 패널 광장, 경고 줄무늬 격납고 문, 전원 케이블 드럼, 붉은 경광등, 보안 게이트, 숲·호수·수박밭. 서쪽 터널로 시골 마을과 이어짐
NAME, NX, NY = 'tk_geofront', 44, 36
exec(open('tk_lib.py').read())
fill('grass', 0, 0, NX, NY)
fill('back', 10, 0, 36, 22)                  # 본부 부지 금속 바닥
fill('plaza', 12, 12, 34, 22)                # 육각 패널 광장
fill('asph', 0, 15, 12, 20)                  # 서쪽 터널 진입로
fill('asph', 21, 22, 25, NY)                 # 남쪽 도로
fill('water', 30, 25, 42, 34)                # 공동 호수
fill('soil', 3, 25, 12, 31)                  # 수박밭
def ov(fx, fy, t):
    if t == 'plaza':   # 육각 패널: 엇갈린 줄 + 가는 이음매
        hx = (fx * 2 + (int(fy * 2) % 2) * .5) % 1; hy = (fy * 2) % 1
        if hx < .08 or hy < .1: return hexc('#3a2e34')
        return hexc('#5a4a52') if (int(fx * 2) + int(fy * 2)) % 3 else hexc('#664e58')
    if t == 'back':
        if (fx % 2 < .06) or (fy % 2 < .06): return hexc('#2a2a32')
        return hexc('#45454f') if random.random() > .08 else hexc('#3a3a44')
    if t == 'asph':
        if 15 <= fy < 20 and abs(fy - 17.5) < .07 and (fx * .75) % 1 < .5: return hexc('#e8c040')
        if 21 <= fx < 25 and abs(fx - 23) < .07 and (fy * .75) % 1 < .5: return hexc('#e8c040')
    if t == 'soil': return hexc('#6a4a30') if (fy * 2) % 1 < .5 else hexc('#5a3e28')
ground(ov, edge='#3a2e2a')

# ---- 검은 피라미드 본부 ----
def pyramid(img):
    d = ImageDraw.Draw(img); x0, y0, x1, y1, base, ph = 14, 0, 32, 11, 12, 150
    box(d, x0, y0, x1, y1, base, '#2a2a34', '#34343e', '#3a3a46')
    Lp, Bp, Rp = up(P(x0, y1), base), up(P(x1, y1), base), up(P(x1, y0), base)
    apex = up(P((x0 + x1) / 2, (y0 + y1) / 2), base + ph)
    poly(d, [Lp, Bp, apex], hexc('#22222a')); poly(d, [Bp, Rp, apex], hexc('#30303c'))
    for k in range(1, 9):   # 유리 층 줄
        t = k / 9
        a = (Lp[0] + (apex[0] - Lp[0]) * t, Lp[1] + (apex[1] - Lp[1]) * t); b = (Bp[0] + (apex[0] - Bp[0]) * t, Bp[1] + (apex[1] - Bp[1]) * t); c2 = (Rp[0] + (apex[0] - Rp[0]) * t, Rp[1] + (apex[1] - Rp[1]) * t)
        d.line([a, b], fill=hexc('#3e3e4c')); d.line([b, c2], fill=hexc('#4a4a5a'))
    for t in (.32, .36):    # 붉은 띠
        a = (Lp[0] + (apex[0] - Lp[0]) * t, Lp[1] + (apex[1] - Lp[1]) * t); b = (Bp[0] + (apex[0] - Bp[0]) * t, Bp[1] + (apex[1] - Bp[1]) * t); c2 = (Rp[0] + (apex[0] - Rp[0]) * t, Rp[1] + (apex[1] - Rp[1]) * t)
        d.line([a, b], fill=hexc('#c8202a'), width=2); d.line([b, c2], fill=hexc('#a81a22'), width=2)
    d.line([Bp, apex], fill=hexc('#5a5a6a'))
    # 정문(앞면 가운데)
    X, Y = up(P(22, y1), 0)
    d.polygon([(X - 2, Y - 1), (X + 22, Y + 11), (X + 22, Y - 9), (X - 2, Y - 21)], fill=hexc('#14141a'))
    for k in range(3): d.line([(X + 2 + k * 7, Y + 1 + k * 3.5), (X + 2 + k * 7, Y - 18 + k * 3.5)], fill=hexc('#c8202a'))
    # 앞면 아래 경고 줄무늬
    for u in range(0, (x1 - x0) * 8, 6):
        Xa, Ya = on_wall(x0, y1, u, 2)
        d.polygon([(Xa, Ya), (Xa + 3, Ya + 1.5), (Xa + 3, Ya - 2.5), (Xa, Ya - 4)], fill=hexc('#e8c040'))
bld('hq', [14, 0, 32, 11], pyramid, door=dict(tile=[23, 11], to='tk_hq_inside', label='본부 · 보안 게이트', spawn=[6, 8]))
# ---- 양옆 격납고(경고 줄무늬 거대한 문) ----
def hangar(x0, y0, x1, y1, h):
    lay = [('L', 6, 0, (x1 - x0) * 8 - 12, h - 10, lambda u, v, w, hh: hexc('#e8c040') if ((u + v) // 5) % 2 and (v < 6 or v > hh - 7 or u < 5 or u > w - 6) else (hexc('#1a1a22') if (v < 6 or v > hh - 7 or u < 5 or u > w - 6) else (hexc('#4a4a56') if u % 10 else hexc('#33333e')))),
           ('L', (x1 - x0) * 4 - 1, 6, 2, h - 22, '#22222a'),
           ('R', 4, 6, (y1 - y0) * 8 - 8, 10, lambda u, v, w, hh: hexc('#e8c040') if ((u + v) // 4) % 2 else hexc('#1a1a22'))]
    return shop(x0, y0, x1, y1, h, '#5a5a66', lay, roofc='#3a3a44')
bld('hangar', [2, 2, 10, 10], hangar(2, 2, 10, 10, 64), act=('격납고 문', '틈새로 들여다보기'))
bld('hangar', [36, 2, 43, 10], hangar(36, 2, 43, 10, 64), act=('격납고 문', '틈새로 들여다보기'))
# ---- 관제 탑 ----
bld('tower', [33, 12, 36, 15], shop(33, 12, 36, 15, 70, '#3a3a46', [(s, 2, v, 20, 6, lambda u, vv, w, hh: hexc('#ff8a3a') if (u + vv) % 4 else hexc('#ffb070')) for s in ('L', 'R') for v in (20, 34, 48, 60)], roofc='#2a2a34'),
    act=('관제탑', '올려다보기'))
# ---- 소품 ----
def warn_lamp(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 26, cx + 1, cy], fill=hexc('#3a3a44')); d.rectangle([cx - 3, cy - 3, cx + 3, cy], fill=hexc('#2a2a32'))
    d.ellipse([cx - 4, cy - 34, cx + 4, cy - 26], fill=hexc('#e8202a')); d.ellipse([cx - 2, cy - 33, cx + 1, cy - 30], fill=hexc('#ff8a8a'))
shared('wlamp', warn_lamp)
def cable_drum(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + 1, y + .5)
    d.ellipse([cx - 14, cy - 22, cx + 2, cy + 2], fill=hexc('#2a2a32')); d.ellipse([cx - 12, cy - 20, cx, cy], fill=hexc('#e86a2a'))
    d.ellipse([cx - 8, cy - 14, cx - 4, cy - 6], fill=hexc('#2a2a32'))
    d.line([(cx - 2, cy - 4), (cx + 14, cy + 4), (cx + 22, cy + 2)], fill=hexc('#22222a'), width=4); d.line([(cx - 2, cy - 4), (cx + 14, cy + 4), (cx + 22, cy + 2)], fill=hexc('#e86a2a'))
shared('drum', cable_drum)
def gate_bar(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .3, y + .2, x + .7, y + .8, 14, '#3a3a44', '#4a4a56', '#5a5a66')
    X, Y = up(P(x + .5, y + .5), 10); d.line([(X, Y), (X + 14, Y + 7)], fill=hexc('#e8c040'), width=2)
    d.rectangle([X - 1, Y - 6, X + 1, Y - 4], fill=hexc('#3ae86a'))
shared('gatebar', gate_bar)
def watermelon(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.ellipse([cx - 5, cy - 7, cx + 5, cy + 1], fill=hexc('#2e7a3a'))
    for k in (-3, 0, 3): d.line([(cx + k, cy - 6), (cx + k, cy)], fill=hexc('#1a4a24'))
    d.line([(cx + 4, cy - 6), (cx + 8, cy - 9)], fill=hexc('#4e9244'))
shared('melon', watermelon)
def watering_can(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .3, y + .3, x + .7, y + .7, 7, '#5a8ab8', '#6a9ac8', '#7aaad8')
    X, Y = up(P(x + .7, y + .5), 5); d.line([(X, Y), (X + 6, Y - 4)], fill=hexc('#5a8ab8'), width=2)
shared('wcan', watering_can)
for (x, y) in ((12, 12), (33, 11), (12, 21), (33, 21), (0, 14), (0, 20), (20, 22), (25, 22)): put('lamp', 'wlamp', x, y)
for (x, y) in ((4, 12), (38, 12), (6, 21)): put('drum', 'drum', x, y, w=2, act=('전원 케이블 드럼', '케이블 따라가 보기'))
put('gate', 'gatebar', 21, 12, act=('보안 게이트', '카드 대 보기')); put('gate', 'gatebar', 25, 12, act=('보안 게이트', '카드 대 보기'))
for x in range(4, 12, 2):
    for y in range(26, 31, 2): put('melon', 'melon', x, y, solid=False, act=('수박', '두드려 보기'))
put('wcan', 'wcan', 12, 28, act=('물뿌리개', '수박에 물 주기'))
put('vend', 'vend#3A6EC8', 17, 13, act=('자판기', '음료 뽑기')); put('vend', 'vend#E8E8E4', 28, 13, act=('자판기', '음료 뽑기'))
put('bench', 'bench2', 15, 18, act=('광장 벤치', '앉아서 쉬기')); put('bench', 'bench2', 30, 18, act=('광장 벤치', '앉아서 쉬기'))
for x in range(0, NX):
    for y in range(22, NY):
        if T.get((x, y)) == 'grass' and random.random() < .22 and not (x < 14 and 24 <= y <= 32): put('tree', random.choice(['tree_pine', 'tree_round', 'tree_big']), x, y)
for (x, y) in ((1, 1), (11, 0), (0, 8), (35, 0), (43, 11), (42, 0)): put('tree', 'tree_pine', x, y)
edge_exits('tokyo')
finish([dict(n='본부 피라미드', t=[23, 12]), dict(n='육각 광장', t=[23, 17]), dict(n='서쪽 격납고', t=[6, 11]), dict(n='동쪽 격납고', t=[39, 11]), dict(n='관제탑', t=[34, 16]),
        dict(n='수박밭', t=[7, 28]), dict(n='지하 호수', t=[33, 25]), dict(n='터널 진입로', t=[3, 17])], [3, 17])
