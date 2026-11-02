# 도와(ACCA 13구 감찰과, 왕가가 있는 구): 뒤쪽 돔 지붕 왕궁, 금장 철책과 정문(근위병 초소),
#   분수 광장, 좌우 대칭 정원, 앞으로 뻗은 가로수 대로, 양옆 ACCA 도와 지부·왕립 박물관
NAME, NX, NY = 'acca_dowa', 44, 36
exec(open('tk_lib.py').read())
AX0, AX1 = 19, 25                      # 가운데 대로
fill('grass', 0, 0, NX, NY)
fill('gravel', 2, 8, 42, 12)           # 왕궁 앞뜰
fill('plaza', 4, 13, 40, 24)           # 분수 광장
fill('stone', AX0, 12, AX1, NY)        # 대로
fill('gravel', 2, 24, 18, 26); fill('gravel', 26, 24, 42, 26)
def ov(fx, fy, t):
    if t == 'plaza':
        r = ((fx - 22) ** 2 + ((fy - 18.5) * 1.3) ** 2) ** .5
        if abs(r % 3 - 1.5) < .12: return hexc('#B8AE9C')          # 동심원 무늬 돌바닥
    if t == 'stone' and (abs(fx - AX0 - .2) < .1 or abs(fx - AX1 + .2) < .1): return hexc('#E0D8C8')
ground(ov, edge='#5A6A4A')
# ---- 왕궁 ----
def palace_layers():
    L, R = 32 * 8, 8 * 8
    out = []
    for v in (8, 36):
        for u in range(6, L - 8, 12): out.append(('L', u, v, 7, 18, win(random.random() < .5, arch=True, frame='#8A7A5A')))
        for u in range(6, R - 8, 12): out.append(('R', u, v, 7, 18, win(random.random() < .4, arch=True, frame='#8A7A5A')))
    out += [('L', 0, 30, L, 3, '#C8A84A'), ('R', 0, 30, R, 3, '#C8A84A'),
            ('L', 96, 0, 64, 62, columns('#F8F4EA', '#7A7060', 8)), ('L', 116, 0, 24, 30, door('#3A4A6A', '#C8A84A', '#F2D27A')),
            ('L', 0, 0, 10, 62, columns('#F8F4EA', '#7A7060', 5, False)), ('L', L - 10, 0, 10, 62, columns('#F8F4EA', '#7A7060', 5, False))]
    return out
bld('palace', [6, 0, 38, 8], combo(shop(6, 0, 38, 8, 66, '#EDE4D0', palace_layers(), cornice='#C8BCA0'),
                                  dome(22, 4, 66, 26, '#4A8A7A'), dome(9, 3, 66, 10, '#4A8A7A'), dome(35, 3, 66, 10, '#4A8A7A'),
                                  flag_on(22, 4, 128, '#2E3A6A', '#C8A84A'), flag_on(6.3, 7.7, 66, '#2E3A6A', '#C8A84A'), flag_on(37.7, 7.7, 66, '#2E3A6A', '#C8A84A')),
    door=dict(tile=[22, 8], to='dowa_palace', label='도와 왕궁', spawn=[6, 8]))
# ---- 철책 + 정문 ----
def fence_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 18, cx + 1, cy], fill=hexc('#2A2A32')); d.ellipse([cx - 2, cy - 21, cx + 2, cy - 17], fill=hexc('#E0C070'))
    for k in range(-6, 8, 3):
        X, Y = cx + k, cy + k * .5; d.line([(X, Y - 2), (X, Y - 15)], fill=hexc('#2A2A32')); d.point((X, Y - 16), fill=hexc('#E0C070'))
    d.line([(cx - 8, cy - 4 - 10), (cx + 8, cy + 4 - 10)], fill=hexc('#2A2A32')); d.line([(cx - 8, cy - 4 - 3), (cx + 8, cy + 4 - 3)], fill=hexc('#2A2A32'))
shared('fence', fence_at)
for x in list(range(2, AX0 - 1)) + list(range(AX1 + 1, 42)): put('fence', 'fence', x, 12)
def gate_post(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .15, y + .15, x + .85, y + .85, 34, '#D8D0C0', '#E8E0D0', '#F2EAD8')
    cx, cy = up(P(x + .5, y + .5), 34); d.ellipse([cx - 4, cy - 10, cx + 4, cy - 2], fill=hexc('#E0C070')); d.rectangle([cx - 1, cy - 14, cx, cy - 10], fill=hexc('#C8A84A'))
shared('gpost', gate_post)
put('gate', 'gpost', AX0 - 1, 12); put('gate', 'gpost', AX1, 12)
def guard_box(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .15, y + .15, x + .85, y + .85, 26, '#2E3A6A', '#F4F0E8', '#2E3A6A')
    X, Y = P(x + .85, y + .85)
    for k in range(0, 24, 6): d.rectangle([X + 1, Y - 2 - k - 3, X + 9, Y - 2 - k - 4 + 1], fill=hexc('#2E3A6A'))
    hip(d, x + .15, y + .15, x + .85, y + .85, 26, 10, '#2E3A6A', e=.15)
shared('guard', guard_box)
put('guard', 'guard', AX0 - 3, 13, act=('근위병 초소', '인사하기')); put('guard', 'guard', AX1 + 2, 13, act=('근위병 초소', '인사하기'))
# ---- 분수 광장 ----
put('fountain', 'fountain', 21, 17, w=3, d=3, act=('왕궁 분수', '동전 던지기'))
put('statue', 'statue_knight', 22, 22, act=('초대 국왕 기마상', '올려다보기'))
for (x, y) in ((6, 14), (37, 14), (6, 22), (37, 22), (12, 14), (31, 14)): put('lamp', 'elamp', x, y)
for (x, y) in ((10, 18), (33, 18)): put('bench', 'bench2', x, y, act=('광장 벤치', '앉아서 쉬기'))
# ---- 대칭 정원 ----
for side in (0, 1):
    xs = range(3, 18) if side == 0 else range(27, 42)
    for x in xs:
        put('hedge', 'hedge', x, 26); put('hedge', 'hedge', x, 34)
    for y in range(27, 34): put('hedge', 'hedge', xs[0], y); put('hedge', 'hedge', xs[-1], y)
    cx = 10 if side == 0 else 34
    for (dx, dy) in ((-3, 2), (3, 2), (-3, 5), (3, 5), (0, 3), (0, 4)): put('flower', 'flower', cx + dx, 27 + dy)
    for (dx, dy) in ((-5, 1), (5, 1), (-5, 6), (5, 6)): put('tree', 'tree_round', cx + dx, 27 + dy)
    for (x, y) in ((1, 13), (42, 13)): pass
for y in range(25, NY - 1, 3): put('tree', 'tree_big', AX0 - 1, y); put('tree', 'tree_big', AX1, y)
for y in range(26, NY - 1, 3): put('lamp', 'elamp', AX0, y); put('lamp', 'elamp', AX1 - 1, y)
# ---- 양옆 건물 (낮게) ----
bld('branch', [0, 14, 4, 22], shop(0, 14, 4, 22, 46, '#F2EEE4', [('R', 0, 0, 64, 30, columns('#F8F4EA', '#7A7060', 8)), ('R', 24, 0, 16, 26, door('#2E3A6A', '#C8A84A', glassy=True)),
    ('R', 4, 34, 56, 8, sign('#2E3A6A', '#F2EAD8', latin=True)), ('L', 4, 8, 24, 30, win(True, arch=True, frame='#8A7A5A'))], cornice='#C8BCA0'),
    door=dict(tile=[4, 18], to='acca_dowa_branch', label='ACCA 도와 지부', spawn=[6, 8]))
bld('museum', [40, 14, 44, 22], combo(shop(40, 14, 44, 22, 44, '#E4D8C0', [('L', 0, 0, 32, 30, columns('#F8F4EA', '#7A7060', 8)), ('L', 8, 0, 16, 26, door('#5A3420', '#3A2418')),
    ('R', 4, 6, 56, 26, lambda u, v, w, h: hexc('#8A7A5A') if u % 14 in (0, 1) else None)], cornice='#B8AC90'), dome(42, 18, 44, 10, '#8A6A4A')),
    door=dict(tile=[42, 22], to='dowa_museum', label='왕립 박물관', spawn=[6, 8]))
# ---- 가장자리 숲 ----
for (x, y) in ((1, 2), (1, 6), (40, 2), (42, 6), (2, 10), (41, 10), (0, 24), (43, 24), (1, 33), (42, 33), (43, 29), (0, 29)): put('tree', 'tree_pine' if y < 12 else 'tree_big', x, y)
edge_exits('euro')
finish([dict(n='도와 왕궁', t=[22, 9]), dict(n='왕궁 정문', t=[22, 12]), dict(n='분수 광장', t=[22, 16]), dict(n='초대 국왕 기마상', t=[22, 23]), dict(n='서쪽 정원', t=[10, 30]),
        dict(n='동쪽 정원', t=[34, 30]), dict(n='ACCA 도와 지부', t=[5, 18]), dict(n='왕립 박물관', t=[42, 23]), dict(n='가로수 대로', t=[22, 30])], [22, 34])
