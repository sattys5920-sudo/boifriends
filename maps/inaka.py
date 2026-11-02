# 시골 마을: 뒤쪽 철길과 작은 나무 역(시부야행 열차), 역 앞 버스 정류장·과자 가게·우체통,
#   논과 밭, 작은 개울과 다리, 기와집들, 언덕 위 작은 신사
NAME, NX, NY = 'tk_inaka', 46, 36
exec(open('tk_lib.py').read())
fill('grass', 0, 0, NX, NY)
fill('gravel', 0, 2, NX, 6)               # 철길 자갈
fill('plaza', 4, 6, 18, 8); fill('plaza', 25, 6, 40, 8)                # 승강장
fill('dirt', 0, 10, NX, 13)               # 역 앞 흙길(가로)
fill('dirt', 20, 13, 23, NY)              # 마을 길(세로)
fill('water', 26, 13, 29, NY)             # 개울
fill('wood', 20, 22, 23, 23)
for (x0, y0) in ((2, 15), (9, 15), (2, 24), (9, 24)): fill('paddy', x0, y0, x0 + 6, y0 + 7)
fill('field', 31, 25, 44, 33)
fill('gravel', 34, 14, 37, 22)            # 신사 오르는 길
def ov(fx, fy, t):
    if t == 'gravel' and 2 <= fy < 6:
        band = fy - 2
        if any(abs(band - r) < .08 for r in (1.2, 2.0)): return hexc('#9A9AA4')
        if any(abs(band - r) < .16 for r in (1.2, 2.0)): return hexc('#4A4048')
        if (fx * 3) % 1 < .25 and .9 < band < 2.3: return hexc('#6A5444')
    if t == 'paddy':
        if (fy * 2) % 1 < .5 and (fx * 2) % 1 < .3: return hexc('#8ACC5A')
        return hexc('#6A9AB8') if random.random() > .05 else hexc('#BFE2FF')
    if t == 'field':
        return hexc('#6A4A30') if (fy * 2) % 1 < .45 else (hexc('#5E9A4A') if (fx * 3) % 1 < .6 else hexc('#6A4A30'))
    if t == 'water' and 22 <= fy < 23 and False: return None
ground(ov, edge='#5A4A3A')
def base_fix():  # 'paddy','field'는 ov가 모두 칠해요
    pass
# ---- 작은 나무 역 + 승강장 ----
bld('station', [18, 7, 25, 10], combo(shop(18, 7, 25, 10, 28, '#C8A878', [('L', 0, 0, 56, 28, lambda u, v, w, h: hexc('#6A4A30') if u % 10 in (0, 1) else None),
    ('L', 20, 0, 16, 22, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 or v % 6 == 0 else hexc('#FFE6B0')), ('L', 2, 22, 52, 5, sign('#F2EAD8', '#2A2020', 8)),
    ('R', 4, 6, 14, 10, win(True, frame='#6A4A30'))], roof='#4A5A6A', rh=14, tex=4)),
    door=dict(tile=[21, 10], to='tk_shibuya', label='역', spawn=[8, 10]))
def platform_roof(img):
    d = ImageDraw.Draw(img)
    for x in (27, 32, 37):
        p_ = P(x + .5, 7.3); d.line([p_, up(p_, 24)], fill=hexc('#5A5048'), width=2)
    poly(d, [up(P(26, 6.2), 26), up(P(39, 6.2), 26), up(P(39, 7.8), 24), up(P(26, 7.8), 24)], hexc('#5A6A6A'))
    X, Y = P(30, 7.5); d.rectangle([X - 6, Y - 20, X + 6, Y - 14], fill=hexc('#F4F0E8'))
flat_unique('platform', platform_roof)
def train(img):
    d = ImageDraw.Draw(img)
    box(d, 3, 2.7, 16, 4.6, 20, '#C8D0D8', '#E0E6EC', '#B8C0C8', lift=2)
    box(d, 3, 2.7, 16, 4.6, 3, '#E8803A', '#F09050', '#E8803A', lift=10)
    for k in range(12):
        X, Y = up(P(3.4 + k, 4.6), 14); d.rectangle([X, Y - 5, X + 5, Y - 1], fill=hexc('#6E8AA8'))
bld('train', [3, 2, 16, 5], train, act=('한 칸짜리 열차', '창문 들여다보기'))
# ---- 역 앞: 버스 정류장 · 과자 가게 · 우체통 ----
def bus_stop(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 30, cx, cy], fill=hexc('#8A8A90')); d.ellipse([cx - 6, cy - 40, cx + 6, cy - 28], fill=hexc('#F4F0E8'), outline=hexc('#2E62C8'))
    box(d, x + .1, y + .5, x + .9, y + .8, 2, '#8A6A4A', '#9A7A54', '#AA8A5E', lift=6)
shared('busstop', bus_stop)
put('busstop', 'busstop', 26, 9, act=('버스 정류장', '시간표 보기 (하루 4대)'))
def postbox(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .3, y + .3, x + .7, y + .7, 16, '#C8302A', '#E8403A', '#E8403A')
    X, Y = up(P(x + .3, y + .7), 12); d.line([(X + 1, Y), (X + 5, Y + 2)], fill=OUTL)
shared('postbox', postbox)
put('postbox', 'postbox', 13, 9, act=('빨간 우체통', '편지 넣기'))
bld('dagashi', [8, 6, 13, 10], combo(shop(8, 6, 13, 10, 26, '#B89A70', [('L', 2, 0, 36, 18, glass(True, door=(12, 24), tint='#F8EAC8')), ('L', 0, 19, 40, 6, sign('#F2EAD8', '#C8302A', 7)),
    ('R', 4, 4, 22, 14, glass(True, tint='#F8EAC8'))], roof='#4A5A6A', rh=12, tex=4)),
    door=dict(tile=[10, 10], to='tk_dagashi', label='막과자 가게', spawn=[6, 8]))
put('vend', 'vend#E8E8E4', 14, 9, act=('시골 자판기', '음료 뽑기 (100엔)'))
# ---- 기와집들 ----
HOUSES = [(1, 34, 7, '#D8C8A8', '#3E4A5A'), (9, 34, 6, '#C8B898', '#4A3E3A'), (16, 34, 4, '#E0D4BC', '#3E4A5A')]
for i, (x0, y1, w_, wall, roof) in enumerate(HOUSES):
    bld('house', [x0, y1 - 1, x0 + w_, y1 + 1] if False else [x0, 32, x0 + w_, 36], shop(x0, 32, x0 + w_, 36, 24, wall, [('L', 4, 0, 16, 18, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 or v % 6 == 0 else hexc('#F4ECDA')),
        ('L', w_ * 8 - 20, 6, 12, 10, win(random.random() < .5, frame='#6A4A30')), ('R', 4, 6, 12, 10, win(True, frame='#6A4A30'))], roof=roof, rh=14, tex=4),
        door=dict(tile=[x0 + 1, 35] if False else [x0 + 1, 36], to='tk_inaka_house%d' % i, label=['할머니 댁', '농가', '빈집'][i], spawn=[6, 8]))
for o in objs:   # 마지막 줄 집 문은 집 옆(오른쪽)으로
    if o['name'] == 'house': o['door']['tile'] = [o['box'][2], 34]
bld('house', [30, 14, 34, 19], shop(30, 14, 34, 19, 26, '#D8C8A8', [('L', 4, 0, 16, 18, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 or v % 6 == 0 else hexc('#F4ECDA')), ('R', 8, 6, 14, 10, win(True, frame='#6A4A30'))], roof='#5A3E3A', rh=14, tex=4),
    door=dict(tile=[32, 19], to='tk_inaka_house3', label='이장님 댁', spawn=[6, 8]))
# ---- 다리 · 개울 ----
for y in range(13, NY):
    for x in range(26, 29): occupied.add((x, y))
def wood_bridge(img):
    d = ImageDraw.Draw(img)
    box(d, 25.6, 21.6, 29.4, 23.4, 3, '#7A5434', '#8A6440', '#A87A50', lift=1)
    for yy in (21.7, 23.3):
        for x in range(26, 30):
            p_ = P(x, yy); d.line([up(p_, 4), up(p_, 10)], fill=hexc('#6A4428'))
        d.line([up(P(25.6, yy), 10), up(P(29.4, yy), 10)], fill=hexc('#8A6440'), width=2)
bld('bridge', [26, 22, 29, 23], wood_bridge, solid=False)
for x in range(26, 29): occupied.discard((x, 22))
fill('wood', 26, 22, 29, 23)
# ---- 신사 (언덕 위) ----
def small_torii(img):
    d = ImageDraw.Draw(img); red = hexc('#D8452E'); pa, pb = P(34.2, 21.5), P(36.8, 21.5)
    for p_ in (pa, pb): d.rectangle([p_[0] - 2, p_[1] - 34, p_[0] + 2, p_[1]], fill=red)
    d.line([up(pa, 26), up(pb, 26)], fill=red, width=2); d.line([(up(pa, 34)[0] - 6, up(pa, 34)[1] + 2), (up(pb, 34)[0] + 6, up(pb, 34)[1] - 2)], fill=hexc('#2A2226'), width=4)
bld('torii', [34, 21, 37, 22], small_torii, solid=False)
for p_ in ((34, 21), (36, 21)): occupied.add(p_)
bld('shrine', [34, 11, 38, 14], shop(34, 11, 38, 14, 20, '#E8DCC4', [('L', 0, 0, 32, 20, lambda u, v, w, h: hexc('#C8442E') if u % 8 in (0, 1) else None), ('L', 10, 2, 12, 14, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 else hexc('#F4ECDA'))],
    roof='#4A5A5E', rh=12, tex=4), act=('언덕 위 작은 신사', '참배하기'))
# ---- 전봇대 · 나무 · 소품 ----
POLES = [(2, 13), (12, 13), (24, 13), (40, 13)]
for (x, y) in POLES: put('pole', 'pole', x, y)
wires_between(POLES)
for (x, y) in ((1, 22), (8, 22), (17, 15), (17, 28), (38, 16), (39, 20), (33, 20), (42, 23), (44, 14), (30, 34), (44, 34), (24, 30)): put('tree', 'tree_big' if (x + y) % 2 else 'tree_round', x, y)
for x in (0, 8, 44): put('tree', 'tree_pine', x, 0)
def scarecrow(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.line([(cx, cy), (cx, cy - 24)], fill=hexc('#6A4A30')); d.line([(cx - 8, cy - 18), (cx + 8, cy - 14)], fill=hexc('#6A4A30'))
    d.ellipse([cx - 4, cy - 30, cx + 4, cy - 22], fill=hexc('#F2E6CC')); d.polygon([(cx - 7, cy - 28), (cx, cy - 34), (cx + 7, cy - 28)], fill=hexc('#D8B04A'))
    d.rectangle([cx - 4, cy - 20, cx + 4, cy - 10], fill=hexc('#3A6AA8'))
shared('scare', scarecrow)
put('scare', 'scare', 5, 18, act=('허수아비', '말 걸어 보기')); put('scare', 'scare', 37, 28, act=('허수아비', '말 걸어 보기'))
for x in range(31, 44, 3): put('fence', 'rail', x, 24, solid=False)
for (x, y) in ((24, 18), (18, 26)): put('bench', 'bench2', x, y, act=('나무 벤치', '쉬면서 논 바라보기'))
edge_exits('wood')
finish([dict(n='시골 역', t=[21, 11]), dict(n='막과자 가게', t=[10, 11]), dict(n='논', t=[8, 20]), dict(n='개울 다리', t=[27, 22]), dict(n='언덕 위 신사', t=[35, 18]),
        dict(n='밭', t=[37, 29]), dict(n='할머니 댁', t=[4, 34])], [21, 12])
