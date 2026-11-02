# 바동(ACCA 13구 감찰과, 도와 왕국의 수도가 있는 구): 운하를 따라 늘어선 알록달록 박공집, 동쪽 ACCA 본부(옆에 바동 지부),
#   남쪽 트램 길 + 정류장 옆 담배 가판대, 노천 카페, 빵집, 작은 분수 공원
NAME, NX, NY = 'acca_badon', 44, 34
exec(open('tk_lib.py').read())
CY0, CY1 = 13, 16                       # 운하
fill('cobble', 0, 0, NX, NY)
fill('canal', 0, CY0, 29, CY1)
fill('stone', 12, CY0, 15, CY1)         # 다리
fill('plaza', 29, 10, NX, 18)           # ACCA 본부 앞 광장
fill('road', 0, 18, NX, 22)             # 트램 길
fill('plaza', 29, 23, 43, 33); fill('grass', 31, 25, 41, 31)
def ov(fx, fy, t):
    if t == 'road':
        band = fy - 18
        if any(abs(band - r) < .07 for r in (.9, 1.5, 2.5, 3.1)): return hexc('#9A9AA4')     # 트램 레일 두 줄
        if any(abs(band - r) < .16 for r in (.9, 1.5, 2.5, 3.1)): return hexc('#3A3A44')
        if (fx * 4) % 1 < .12 and (.7 < band < 1.7 or 2.3 < band < 3.3): return hexc('#5A4A3E')   # 침목
        return hexc('#6A6470') if random.random() > .1 else hexc('#5E5864')
    if t == 'stone' and CY0 <= fy < CY1: return _brick(fx, fy, 2, [hexc('#B8AE9C'), hexc('#A89E8C')], hexc('#7E7464'))
    if t == 'cobble' and (abs(fy - CY0) < .12 or abs(fy - CY1) < .12) and fx < 29: return hexc('#D8D0C0')   # 운하 둑 갓돌
ground(ov, edge='#5A5048')
# ---- 운하 박공집 줄 ----
HOUSES = [('#3E7A5A', 'step', 56), ('#B85A3E', 'bell', 64), ('#D8B04A', 'tri', 52), ('#E8DCC8', 'step', 60), ('#C87A8A', 'bell', 56),
          ('#5A6A8A', 'tri', 66), ('#8A4A3A', 'step', 58), ('#F2EAD8', 'bell', 52), ('#4A7A8A', 'tri', 60)]
def house_layers(w, h):
    out = []
    for v in range(28, h - 8, 14):
        for u in (4, 14):
            out.append(('L', u, v, 6, 10, lambda uu, vv, ww, hh, lit=random.random() < .4: hexc('#F4F0E8') if uu in (0, ww - 1) or vv in (0, hh - 1, hh // 2) else (hexc('#FFE0A0') if lit else hexc('#7AA0C0'))))
    out += [('L', 2, 0, w - 4, 22, lambda u, v, ww, hh: hexc('#F4F0E8') if u in (0, ww - 1) or v == hh - 1 else None),
            ('L', 4, 0, 6, 18, door('#2E3A4A', '#F4F0E8')), ('L', 12, 4, 8, 12, win(random.random() < .5, frame='#F4F0E8'))]
    out += [('R', u, v, 6, 10, win(random.random() < .3, frame='#F4F0E8')) for v in range(28, h - 8, 14) for u in range(6, 44, 12)]
    return out
for i, (col, kind, h) in enumerate(HOUSES):
    x0 = 1 + i * 3
    bld('house', [x0, 4, x0 + 3, 11], shop(x0, 4, x0 + 3, 11, h, col, house_layers(24, h), brick=col in ('#B85A3E', '#8A4A3A'), gable=(col, 16, kind)),
        door=dict(tile=[x0 + 1, 11], to='badon_house%d' % i, label=['꽃집', '서점', '양복점', '하숙집', '모자 가게', '시계방', '술집', '게스트하우스', '문구점'][i], spawn=[6, 8]))
# ---- ACCA 본부 + 바동 지부 ----
def hq_layers():
    out = [('L', 0, 0, 96, 30, columns('#F4F2EC', '#6A6A74', 8)), ('R', 0, 0, 72, 30, columns('#F4F2EC', '#6A6A74', 8)),
           ('L', 36, 0, 24, 26, door('#2E3A4A', '#C8A84A', glassy=True))]
    for v in range(38, 132, 14):
        for u in range(6, 90, 10): out.append(('L', u, v, 6, 10, win(random.random() < .45, frame='#8A8A94')))
        for u in range(6, 66, 10): out.append(('R', u, v, 6, 10, win(random.random() < .35, frame='#8A8A94')))
    out += [('L', 0, 32, 96, 3, '#C8A84A'), ('R', 0, 32, 72, 3, '#C8A84A')]
    return out
def emblem(img):
    d = ImageDraw.Draw(img); X, Y = on_wall(30, 9, 48, 146)
    d.ellipse([X - 9, Y - 9, X + 9, Y + 9], fill=hexc('#2E3A5A')); d.ellipse([X - 7, Y - 7, X + 7, Y + 7], fill=hexc('#F4F2EC'))
    d.polygon([(X, Y - 5), (X + 5, Y + 4), (X - 5, Y + 4)], fill=hexc('#2E3A5A'))
    for k in range(-4, 5, 4): d.point((X + k, Y + 2), fill=hexc('#C8A84A'))
bld('acca_hq', [30, 0, 42, 9], combo(shop(30, 0, 42, 9, 152, '#E8E6E0', hq_layers(), cornice='#B8B6B0'), emblem,
                                    flag_on(30.4, 8.7, 152, '#2E3A5A', '#C8A84A'), flag_on(41.6, 8.7, 152, '#2E3A5A', '#C8A84A')),
    door=dict(tile=[36, 9], to='acca_hq', label='ACCA 본부', spawn=[6, 8]))
bld('acca_branch', [30, 10, 34, 13], shop(30, 10, 34, 13, 44, '#F4F4F0', [('L', 2, 0, 28, 24, glass(False, door=(8, 20), tint='#DCE8F4')), ('L', 0, 26, 32, 8, sign('#2E3A5A', '#FFFFFF', latin=True)),
    ('R', 2, 4, 20, 16, glass(False, tint='#DCE8F4'))], cornice='#C8C8C8'), door=dict(tile=[32, 13], to='acca_badon_branch', label='ACCA 바동 지부', spawn=[6, 8]))
for x in (35, 38, 41): put('flower', 'flower', x, 12)
# ---- 다리 난간 · 운하 난간 ----
for y in range(CY0, CY1): put('rail', 'grailY', 11, y, solid=False); put('rail', 'grailY', 15, y, solid=False)
for x in list(range(0, 11)) + list(range(16, 29)):
    put('rail', 'grail', x, CY0 - 1, solid=False); put('rail', 'grail', x, CY1, solid=False)
for y in range(CY0, CY1):
    for x in list(range(0, 12)) + list(range(15, 29)): occupied.add((x, y))
def boat(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + 1, y + .5)
    d.polygon([(cx - 18, cy - 8), (cx + 14, cy + 8), (cx + 18, cy + 4), (cx - 14, cy - 12)], fill=hexc('#6A4A30'))
    d.polygon([(cx - 16, cy - 10), (cx + 14, cy + 5), (cx + 16, cy + 3), (cx - 14, cy - 12)], fill=hexc('#8A6A44'))
    d.polygon([(cx - 6, cy - 9), (cx + 6, cy - 3), (cx + 6, cy - 11), (cx - 6, cy - 17)], fill=hexc('#E8E4DA'))
shared('boat', boat)
put('boat', 'boat', 4, 14, w=2, solid=False); put('boat', 'boat', 22, 14, w=2, solid=False)
# ---- 트램 ----
def tram(img):
    d = ImageDraw.Draw(img)
    box(d, 32, 19.15, 39, 20.85, 18, '#2E6A54', '#3E8A6A', '#E8E4DA', lift=2)
    box(d, 32.1, 19.25, 38.9, 20.75, 8, '#F2EAD8', '#F8F0E0', '#F2EAD8', lift=10)
    for k in range(7):
        X, Y = up(P(32.3 + k, 20.85), 11); d.rectangle([X, Y - 6 + 0, X + 5, Y - 1], fill=hexc('#6E8AA8'))
    X, Y = up(P(35.5, 20), 22); d.line([(X, Y), (X - 4, Y - 10), (X + 4, Y - 10)], fill=hexc('#3A3A40'))
bld('tram', [32, 19, 39, 21], tram, act=('트램', '올라타기'))
def tram_stop(img, x, y):
    d = ImageDraw.Draw(img)
    for p_ in (P(x + .1, y + .9), P(x + 1.9, y + .9), P(x + 1.9, y + .2)): d.line([p_, up(p_, 24)], fill=hexc('#3A4A3E'), width=2)
    poly(d, [up(P(x, y), 26), up(P(x + 2, y), 26), up(P(x + 2, y + 1), 24), up(P(x, y + 1), 24)], hexc('#2E5A44'))
    box(d, x + .3, y + .5, x + 1.7, y + .8, 2, '#8A6A4A', '#9A7A54', '#AA8A5E', lift=6)
    X, Y = P(x + 1.9, y + .9); d.ellipse([X - 4, Y - 34, X + 4, Y - 26], fill=hexc('#F2EAD8'), outline=hexc('#2E5A44'))
shared('tramstop', tram_stop)
put('tramstop', 'tramstop', 27, 22, w=2, act=('트램 정류장', '시간표 보기'))
shared('tabako', kiosk_at('#8A2A2A'))
put('tabako', 'tabako', 29, 22, act=('담배 가판대', '한 개비 사기'))
# ---- 남쪽: 카페 · 빵집 · 아파트 ----
bld('cafe', [2, 24, 9, 29], combo(shop(2, 24, 9, 29, 40, '#E8DCC8', [('L', 2, 0, 52, 24, glass(False, door=(22, 32), tint='#F2E0B8')), ('L', 0, 26, 56, 4, stripes('#2E5A44', '#F2EAD8')),
    ('L', 4, 31, 48, 7, sign('#2E5A44', '#F2EAD8', latin=True)), ('R', 2, 2, 36, 20, glass(False, tint='#F2E0B8'))], cornice='#C8B8A0')),
    door=dict(tile=[5, 29], to='badon_cafe', label='카페', spawn=[6, 8]))
def para(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.ellipse([cx - 5, cy - 4, cx + 5, cy + 1], fill=hexc('#E8E4DA')); d.line([(cx, cy), (cx, cy - 20)], fill=hexc('#4A4A50'))
        for dx in (-8, 8): d.rectangle([cx + dx - 1, cy - 5, cx + dx + 1, cy], fill=hexc('#3A3A40'))
        d.polygon([(cx - 13, cy - 16), (cx, cy - 24), (cx + 13, cy - 16), (cx, cy - 12)], fill=hexc(col)); d.polygon([(cx - 13, cy - 16), (cx, cy - 24), (cx, cy - 12)], fill=shade(hexc(col), .85))
    return f
shared('para', para('#2E5A44')); shared('para2', para('#F2EAD8'))
for i, (x, y) in enumerate(((2, 31), (5, 31), (8, 31), (3, 33), (7, 33))): put('parasol', 'para' if i % 2 == 0 else 'para2', x, y, act=('카페 테라스', '앉아서 커피 마시기'))
bld('bakery', [11, 24, 16, 29], combo(shop(11, 24, 16, 29, 46, '#D8B04A', [('L', 2, 0, 36, 22, glass(True, door=(14, 24), tint='#F8E8C8')), ('L', 0, 24, 40, 6, stripes('#8A3A2A', '#F2EAD8')),
    ('L', 4, 32, 6, 10, win(True, frame='#F4F0E8')), ('L', 26, 32, 6, 10, win(False, frame='#F4F0E8')), ('R', 2, 2, 36, 20, glass(True, tint='#F8E8C8'))], gable=('#D8B04A', 12, 'bell'))),
    door=dict(tile=[13, 29], to='badon_bakery', label='빵집', spawn=[6, 8]))
bld('apart', [18, 24, 27, 30], shop(18, 24, 27, 30, 50, '#C8A898', [(s, u, v, 6, 10, win(random.random() < .5, frame='#F4F0E8')) for s, L in (('L', 72), ('R', 48)) for v in (24, 38) for u in range(6, L - 6, 11)] +
    [('L', 30, 0, 12, 20, door('#3A2A2A', '#F4F0E8')), ('L', 4, 4, 8, 12, win(True, frame='#F4F0E8')), ('L', 56, 4, 8, 12, win(False, frame='#F4F0E8'))], brick=True, cornice='#F4F0E8'),
    door=dict(tile=[22, 30], to='badon_apart', label='오래된 아파트', spawn=[6, 8]))
# ---- 분수 공원 ----
put('fountain', 'fountain', 35, 27, w=3, d=3, act=('분수', '동전 던지기'))
put('statue', 'statue_knight', 32, 24, act=('기마상', '올려다보기'))
for (x, y) in ((31, 25), (40, 25), (31, 30), (40, 30), (37, 32), (30, 32)): put('tree', 'tree_round' if (x + y) % 2 else 'tree_big', x, y)
for (x, y) in ((34, 31), (39, 28)): put('bench', 'bench2', x, y, act=('공원 벤치', '앉아서 쉬기'))
for (x, y) in ((1, 12), (9, 12), (18, 12), (26, 12), (1, 17), (9, 17), (18, 17), (26, 17), (29, 17), (43, 17), (1, 23), (29, 23), (43, 23)): put('lamp', 'elamp', x, y)
for (x, y) in ((28, 11), (28, 16)): put('tree', 'tree_round', x, y)
edge_exits('euro')
finish([dict(n='운하 거리', t=[8, 12]), dict(n='돌다리', t=[13, 14]), dict(n='ACCA 본부', t=[36, 10]), dict(n='ACCA 바동 지부', t=[32, 14]), dict(n='트램 정류장', t=[28, 23]),
        dict(n='담배 가판대', t=[29, 23]), dict(n='카페 테라스', t=[5, 31]), dict(n='빵집', t=[13, 30]), dict(n='분수 공원', t=[36, 26])], [13, 17])
