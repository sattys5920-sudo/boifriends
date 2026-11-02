# 긴자: 넓은 두 대로가 만나는 네거리. 북서 모퉁이 시계탑 건물, 북동 석조 백화점, 뒤쪽 명품 빌딩들
#   남쪽은 낮은 부티크·파출소·노천 카페(보행자 천국: 길 위 파라솔)
NAME, NX, NY = 'tk_ginza', 44, 34
exec(open('tk_lib.py').read())
RX0, RX1, RY0, RY1 = 18, 24, 14, 19
fill('walk', 0, 0, NX, NY)
fill('road', 0, RY0, NX, RY1); fill('road', RX0, 0, RX1, NY)
fill('plaza', 26, 22, 42, 32)
def ov(fx, fy, t):
    if t == 'walk':   # 긴자 인도: 큰 석판
        if (fx % 1 < .05) or (fy % 1 < .08): return hexc('#A89E92')
        return [hexc('#D8D0C4'), hexc('#CEC6BA')][(int(fx) + int(fy)) % 2]
    if t != 'road': return None
    inx, iny = RX0 <= fx < RX1, RY0 <= fy < RY1
    if inx and iny: return None
    if iny and (RX0 - 2.2 < fx < RX0 - .2 or RX1 + .2 < fx < RX1 + 2.2): return hexc('#ECECE6') if (fy * 2.5) % 1 < .5 else None
    if inx and (RY0 - 2.2 < fy < RY0 - .2 or RY1 + .2 < fy < RY1 + 2.2): return hexc('#ECECE6') if (fx * 2.5) % 1 < .5 else None
    if iny: return road_x(fx, fy, RY0, RY1)
    if inx: return road_y(fx, fy, RX0, RX1)
ground(ov)
def stone_floors(n, v0, step, L, R, arch=True, lit=.5):
    out = []
    for fl in range(n):
        v = v0 + fl * step
        for u in range(5, L - 8, 11): out.append(('L', u, v, 7, step - 5, win(random.random() < lit, arch=arch and fl == n - 1, frame='#6A5A48')))
        for u in range(5, R - 8, 11): out.append(('R', u, v, 7, step - 5, win(random.random() < lit, arch=arch and fl == n - 1, frame='#6A5A48')))
        out += [('L', 0, v - 3, L, 2, '#B8AC98'), ('R', 0, v - 3, R, 2, '#B8AC98')]
    return out
# ---- 북서 모퉁이: 시계탑 건물 ----
bld('clock', [9, 5, 16, 12], combo(shop(9, 5, 16, 12, 68, '#D8CCB4', stone_floors(3, 30, 13, 56, 56) + [
    ('L', 0, 0, 56, 26, glass(False, door=(20, 36), tint='#E8DCC0')), ('R', 0, 0, 56, 26, glass(False, door=(20, 36), tint='#E8DCC0')),
    ('L', 0, 26, 56, 2, '#8A7A5A'), ('R', 0, 26, 56, 2, '#8A7A5A')], cornice='#A89878'),
    clock_tower(14.6, 10.6, 68, 2.2, 30, '#D8CCB4', '#4A5A58')),
    door=dict(tile=[12, 12], to='tk_clockstore', label='시계탑 백화점', spawn=[6, 8]))
# ---- 북동: 석조 백화점 ----
bld('depart', [26, 3, 37, 12], combo(shop(26, 3, 37, 12, 88, '#E2D6C2', stone_floors(4, 34, 13, 88, 72) + [
    ('L', 0, 0, 88, 30, glass(True, door=(36, 52), tint='#F2E8D4')), ('R', 0, 0, 72, 30, glass(True, tint='#F2E8D4')),
    ('L', 0, 30, 88, 2, '#C8A84A'), ('R', 0, 30, 72, 2, '#C8A84A'),
    ('L', 30, 60, 28, 22, lambda u, v, w, h: hexc('#C8402E') if 2 < u < w - 3 else None)], cornice='#B8AA90'),
    flag_on(26.3, 11.7, 88, '#C8402E'), flag_on(36.7, 11.7, 88, '#C8402E')),
    door=dict(tile=[31, 12], to='tk_depart', label='백화점', spawn=[6, 8]))
bld('lux', [38, 4, 43, 12], combo(shop(38, 4, 43, 12, 100, '#2A2A30', [
    ('L', 2, 30, 36, 66, lambda u, v, w, h: hexc('#3A3A44') if u % 6 == 0 else (hexc('#C8A84A') if v % 12 == 0 else hexc('#4A4A58'))),
    ('L', 4, 0, 32, 26, glass(False, door=(10, 22), tint='#F2E6C8')), ('R', 4, 0, 56, 26, glass(False, tint='#F2E6C8')),
    ('R', 2, 30, 60, 66, lambda u, v, w, h: hexc('#3A3A44') if u % 6 == 0 else (hexc('#C8A84A') if v % 12 == 0 else hexc('#4A4A58')))], roofc='#1E1E24')),
    door=dict(tile=[40, 12], to='tk_jewel', label='보석 가게', spawn=[6, 8]))
# ---- 뒤쪽 명품 빌딩 줄 ----
for (x0, y0, x1, y1, h, wall, tint) in ((1, 2, 8, 12, 76, '#F2F0EA', '#DCE8F0'), (9, 0, 16, 4, 92, '#B8C0C8', '#C8DCEC'), (26, 0, 34, 2, 110, '#8A9098', '#A8C0D8')):
    lay = [(s, u, v, 6, 9, win(random.random() < .4, blind=True)) for s, L in (('L', (x1 - x0) * 8), ('R', (y1 - y0) * 8)) for v in range(30, h - 10, 12) for u in range(4, L - 6, 9)]
    lay += [('L', 0, 0, (x1 - x0) * 8, 26, glass(True, door=((x1 - x0) * 4 - 6, (x1 - x0) * 4 + 6), tint=tint)), ('R', 0, 0, (y1 - y0) * 8, 26, glass(True, tint=tint))]
    bld('bldg', [x0, y0, x1, y1], shop(x0, y0, x1, y1, h, wall, lay, roofc=shade(hexc(wall), .7)),
        door=dict(tile=[(x0 + x1) // 2, y1], to='tk_brand%d' % x0, label='명품 매장', spawn=[6, 8]))
# ---- 남쪽: 낮은 부티크 · 파출소 · 카페 ----
bld('boutique', [3, 22, 10, 28], shop(3, 22, 10, 28, 36, '#F4F0E8', [('L', 2, 0, 52, 24, glass(False, door=(22, 32), tint='#F8EEE4')), ('L', 0, 26, 56, 6, sign('#F4F0E8', '#2A2A30', latin=True)),
    ('R', 2, 0, 44, 24, glass(False, tint='#F8EEE4'))], cornice='#C8BCA8'), door=dict(tile=[6, 28], to='tk_boutique', label='부티크', spawn=[6, 8]))
bld('koban', [12, 22, 16, 26], combo(shop(12, 22, 16, 26, 30, '#C8C0B4', [('L', 4, 0, 24, 22, glass(False, door=(8, 16))), ('L', 0, 24, 32, 5, '#2E3A5A'), ('R', 4, 4, 22, 14, win(True))], roofc='#6A6E78'),
    lambda img: ImageDraw.Draw(img).ellipse([on_wall(12, 26, 16, 34)[0] - 3, on_wall(12, 26, 16, 34)[1] - 3, on_wall(12, 26, 16, 34)[0] + 3, on_wall(12, 26, 16, 34)[1] + 3], fill=hexc('#E8463A'))),
    door=dict(tile=[14, 26], to='tk_koban', label='파출소', spawn=[6, 8]))
bld('cafe', [26, 21, 32, 25], shop(26, 21, 32, 25, 34, '#3A4A3E', [('L', 2, 0, 44, 22, glass(False, door=(18, 30), tint='#F2E0B8')), ('L', 0, 24, 48, 6, stripes('#2E5A3E', '#F2EAD8')),
    ('R', 2, 2, 28, 20, glass(False, tint='#F2E0B8'))], roofc='#2E3A30'), door=dict(tile=[29, 25], to='tk_parlor', label='과일 파르페 카페', spawn=[6, 8]))
def parasol(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        d.ellipse([cx - 6, cy - 4, cx + 6, cy + 2], fill=hexc('#E8E4DA')); d.line([(cx, cy), (cx, cy - 22)], fill=hexc('#5A5A60'))
        for dx in (-9, 9): d.rectangle([cx + dx - 1, cy - 5, cx + dx + 1, cy], fill=hexc('#8A6A4A'))
        d.polygon([(cx - 14, cy - 18), (cx, cy - 26), (cx + 14, cy - 18), (cx, cy - 14)], fill=hexc(col))
        d.polygon([(cx - 14, cy - 18), (cx, cy - 26), (cx, cy - 14)], fill=shade(hexc(col), .85))
    return f
for c in ('#E8463A', '#F2EAD8', '#3E8A6A'): shared('para' + c, parasol(c))
for i, (x, y) in enumerate(((28, 27), (31, 27), (34, 27), (28, 30), (31, 30), (34, 30), (21, 25), (21, 29))):
    put('parasol', 'para' + ('#E8463A', '#F2EAD8', '#3E8A6A')[i % 3], x, y, act=('노천 테이블', '앉아서 쉬기'))
bld('shop', [36, 22, 42, 27], shop(36, 22, 42, 27, 38, '#E8DCC8', [('L', 2, 0, 44, 24, glass(True, door=(18, 30), tint='#F8F0E0')), ('L', 0, 26, 48, 8, sign('#F8F0E0', '#8A2A3A', 9)),
    ('R', 2, 2, 36, 20, glass(True, tint='#F8F0E0'))], cornice='#B8A890'), door=dict(tile=[39, 27], to='tk_sweets', label='화과자 가게', spawn=[6, 8]))
# ---- 가로수·소품 ----
for x in list(range(1, RX0 - 1, 3)) + list(range(RX1 + 2, NX - 1, 3)):
    put('tree', 'tree_round', x, RY0 - 1); put('tree', 'tree_round', x, RY1)
for y in list(range(1, RY0 - 2, 3)) + list(range(RY1 + 2, NY - 1, 3)):
    put('tree', 'tree_round', RX0 - 1, y); put('tree', 'tree_round', RX1, y)
for (x, y) in ((4, 13), (14, 13), (27, 13), (40, 13), (3, 20), (15, 20), (28, 20), (40, 20)): put('lamp', 'elamp', x, y)
shared('kiosk', kiosk_at('#2E5A3E'))
put('kiosk', 'kiosk', 25, 13, act=('신문 가판대', '구경하기'))
for (x, y, k) in ((4, 15, 'taxi'), (34, 17, 'car#2A2A30' if False else 'car#3A4A6A'), (20, 6, 'taxiY'), (12, 16, 'car#F2F2EE')): put('car', k, x, y, w=2, act=('달리던 차', '살펴보기'))
edge_exits('tokyo')
finish([dict(n='긴자 네거리', t=[21, 16]), dict(n='시계탑 백화점', t=[12, 13]), dict(n='석조 백화점', t=[31, 13]), dict(n='보석 가게', t=[40, 13]),
        dict(n='파출소', t=[14, 27]), dict(n='노천 카페 거리', t=[31, 28]), dict(n='부티크', t=[6, 29])], [21, 21])
