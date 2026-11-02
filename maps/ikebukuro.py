# 이케부쿠로: 북쪽 역(위는 백화점) + 부엉이 동상 광장, 영화관 빌딩, 뒤쪽 초고층 전망 빌딩
#   가운데 큰길, 남쪽으로 이어지는 번화가(게임센터·노래방) + 동쪽 애니 상점 거리 + 작은 공원
NAME, NX, NY = 'tk_ikebukuro', 42, 36
exec(open('tk_lib.py').read())
fill('back', 0, 0, NX, NY)
fill('walk', 0, 9, NX, 12); fill('plaza', 1, 9, 15, 11)
fill('road', 0, 12, NX, 17); fill('walk', 0, 17, NX, 19)
fill('plaza', 0, 19, NX, NY); fill('redwalk', 16, 19, 21, NY)        # 번화가 (보행자 거리)
fill('walk', 27, 19, 30, NY)           # 애니 상점 거리
fill('grass', 2, 26, 14, 34); fill('gravel', 6, 26, 9, 34); fill('gravel', 2, 29, 14, 31)
def ov(fx, fy, t):
    if t == 'road': return road_x(fx, fy, 12, 17, cross=[(16, 19), (27, 30)])
    if t == 'walk' and tactile(fy, (10, 18)): return hexc('#E8C040') if (fx * 6) % 1 < .55 else hexc('#C89E2E')
ground(ov)
def floors(n, v0, step, L, R, lit=.3, blind=False):
    out = []
    for fl in range(n):
        v = v0 + fl * step
        for u in range(4, L - 8, 10): out.append(('L', u, v, 8, step - 4, win(random.random() < lit, blind=blind)))
        for u in range(4, R - 8, 10): out.append(('R', u, v, 8, step - 4, win(random.random() < lit, blind=blind)))
    return out
# ---- 역 + 백화점 ----
bld('station', [1, 0, 15, 8], shop(1, 0, 15, 8, 70, '#E2D8C8', [
    ('L', 0, 30, 112, 38, lambda u, v, w, h: hexc('#C8BCA8') if u % 8 < 2 else (hexc('#F0E8DC') if v % 10 < 6 else hexc('#D8CCB8'))),
    ('L', 30, 44, 52, 10, sign('#E8463A', '#FFFFFF', 12)), ('R', 6, 44, 52, 10, sign('#2E5A8A', '#FFFFFF', 12)),
    ('L', 0, 0, 112, 28, glass(True)), ('L', 40, 0, 30, 26, glass(False, door=(2, 28))),
    ('L', 0, 26, 112, 3, '#2E7A4A'), ('R', 0, 26, 64, 3, '#2E7A4A'), ('R', 0, 0, 64, 26, glass(True))], roofc='#8A8E96'),
    door=dict(tile=[8, 8], to='tk_station', label='이케부쿠로역 · 백화점', spawn=[6, 8]))
put('statue', 'statue_owl', 4, 9, act=('부엉이 동상', '만나기 약속 장소'))
for (x, y) in ((12, 9), (14, 10)): put('tree', 'tree_round', x, y)
# ---- 영화관 빌딩 ----
bld('cinema', [17, 1, 25, 8], combo(shop(17, 1, 25, 8, 84, '#4A4A5A', [
    ('L', 6, 34, 52, 40, poster(11)), ('R', 6, 34, 44, 40, poster(12)),
    ('L', 0, 0, 64, 28, glass(False, door=(24, 40), tint='#C8D8F0')), ('L', 0, 28, 64, 4, '#F2C85A'), ('R', 0, 28, 56, 4, '#F2C85A'), ('R', 0, 0, 56, 28, glass(False, tint='#C8D8F0'))], roofc='#3A3A48'),
    roof_sign(17, 1, 25, 8, 84, 12, '#1E1E26', '#F2C85A', latin=True)),
    door=dict(tile=[21, 8], to='tk_cinema', label='영화관', spawn=[6, 8]))
# ---- 초고층 전망 빌딩 (뒤쪽) ----
bld('tower', [29, 0, 37, 7], shop(29, 0, 37, 7, 230, '#5E6676', floors(15, 30, 13, 64, 56, .25, True) + [
    ('L', 0, 0, 64, 26, glass(False, door=(24, 40), tint='#A8C8E0')), ('R', 0, 0, 56, 26, glass(False, tint='#A8C8E0')),
    ('L', 0, 222, 64, 6, '#E8463A'), ('R', 0, 222, 56, 6, '#E8463A')], roofc='#4A5260'),
    door=dict(tile=[33, 7], to='tk_observatory', label='전망대 빌딩', spawn=[6, 8]))
bld('mall', [38, 2, 42, 8], shop(38, 2, 42, 8, 50, '#D8C8E0', [('L', 2, 0, 28, 26, glass(True, door=(10, 20))), ('L', 0, 30, 32, 14, poster(21)), ('R', 4, 6, 40, 30, glass(False))], roofc='#9A8AA8'),
    door=dict(tile=[40, 8], to='tk_mall', label='쇼핑몰', spawn=[6, 8]))
# ---- 번화가 서쪽 (옆면이 길을 봐요) ----
WEST = [('#2A2240', '게임센터', 'tk_arcade', lambda u, v, w, h: hexc(['#FF5A8A', '#5AD8FF', '#FFE45A'][(u // 4 + v // 6) % 3]) if (u % 4 and v % 6) else hexc('#2A2240')),
        ('#E8E4DA', '라멘집', 'tk_ramen', lambda u, v, w, h: hexc('#3A2418') if v > 12 else (hexc('#C8302A') if u % 6 else hexc('#5A1A16'))),
        ('#6A3A5A', '노래방', 'tk_karaoke', glass(False, tint='#F2A0D0')), ('#F2F0EA', '편의점', 'tk_konbini', glass(True))]
for i, (wall, lab, to, front) in enumerate(WEST):
    y0 = 19 + i * 4; h = [42, 28, 48, 32][i]
    lay = [('R', 2, 0, 28, 22, front), ('R', 0, 23, 32, 6, sign('#1E1E26', ['#FF5A8A', '#FFFFFF', '#5AD8FF', '#3E9C64'][i], 7)), ('L', 4, 6, 24, 16, poster(i + 30))]
    if i == 3: lay = [('R', 0, 26, 32, 4, '#3E9C64'), ('R', 0, 23, 32, 3, '#F08C2A'), ('R', 2, 0, 28, 22, glass(True, door=(8, 20)))]
    if h > 40: lay += [('R', 4, v, 8, 9, win(True)) for v in range(32, h - 6, 12)] + [('R', 18, v, 8, 9, win(random.random() < .5)) for v in range(32, h - 6, 12)]
    extra = [vsign(14, y0 + 4, 30, h - 4, 40, ['#FF5A8A', '#FFE45A', '#5AD8FF', '#E8463A'][i], '#FFFFFF')] if h > 40 else []
    bld('shop', [14, y0, 16, y0 + 4], combo(shop(14, y0, 16, y0 + 4, h, wall, lay, roofc='#6A6670'), *extra), door=dict(tile=[16, y0 + 2], to=to, label=lab, spawn=[6, 8]))
# ---- 번화가 동쪽 + 애니 상점 거리 ----
EAST = [(21, 25, '#F2E6F0', '애니 굿즈 가게', 'tk_anime'), (21, 25, '#E0E8F8', '만화 서점', 'tk_books')]
for i, (x0, x1, wall, lab, to) in enumerate(EAST):
    y0 = 21 + i * 7
    bld('anime', [x0, y0, x1, y0 + 5], shop(x0, y0, x1, y0 + 5, 34, wall, [
        ('L', 2, 0, 28, 22, glass(True, door=(10, 22), tint='#F8E8F8')), ('L', 0, 24, 32, 8, poster(40 + i)), ('R', 2, 2, 36, 20, poster(50 + i)), ('R', 0, 24, 40, 8, poster(60 + i))], roofc='#9A90A8'),
        door=dict(tile=[x0 + 2, y0 + 5], to=to, label=lab, spawn=[6, 8]))
for i in range(3):
    y0 = 20 + i * 5
    bld('anime', [31, y0, 35, y0 + 4], shop(31, y0, 35, y0 + 4, 30, ['#F2D8E4', '#E4E0F4', '#F8F0D8'][i], [
        ('L', 2, 0, 28, 20, glass(True, door=(10, 20), tint='#FFF0F8')), ('L', 0, 22, 32, 6, poster(70 + i)), ('R', 2, 2, 28, 18, poster(80 + i))], roofc='#9A90A8'),
        door=dict(tile=[33, y0 + 4], to='tk_otome%d' % i, label=['캐릭터 카페', '동인지 서점', '굿즈 교환 가게'][i], spawn=[6, 8]))
# ---- 작은 공원 ----
for (x, y) in ((2, 26), (5, 33), (12, 26), (13, 33), (3, 31), (11, 28)): put('tree', 'tree_big' if (x + y) % 2 else 'tree_round', x, y)
for (x, y) in ((4, 28), (10, 32)): put('bench', 'bench2', x, y, act=('공원 벤치', '앉아서 쉬기'))
for (x, y) in ((2, 28), (13, 31)): put('bush', 'bush', x, y)
# ---- 남동 광장 ----
for (x, y) in ((37, 21), (40, 21), (37, 27), (40, 27), (37, 33), (40, 33), (24, 34), (30, 34)): put('tree', 'tree_round' if (x + y) % 2 else 'tree_pink', x, y)
for (x, y) in ((38, 24), (38, 30)): put('bench', 'bench2', x, y, act=('광장 벤치', '앉아서 쉬기'))
for (x, y) in ((36, 24), (36, 30), (26, 34), (22, 34)): put('planter', 'planter', x, y)
put('vend', 'vend#E8E8E4', 21, 19, act=('자판기', '음료 뽑기'))
# ---- 길가 ----
POLES = [(2, 18), (12, 18), (24, 18), (38, 18)]
for (x, y) in POLES: put('pole', 'pole', x, y)
wires_between(POLES)
for (x, y) in ((6, 11), (27, 11), (39, 11), (21, 20), (26, 26), (21, 32)): put('lamp', 'lamp2', x, y)
for x in list(range(1, 15)) + list(range(20, 26)) + list(range(31, NX - 1)): put('rail', 'rail', x, 17, solid=False)
for (x, y, k) in ((3, 14, 'taxi'), (10, 15, 'car#3A4A6A'), (33, 13, 'taxiY'), (22, 15, 'car#E8C83A')): put('car', k, x, y, w=2, act=('달리던 차', '살펴보기'))
for x in (17, 18): put('vend', 'vend#D23A3A' if x == 17 else 'vend#3A6EC8', x, 9, act=('자판기', '음료 뽑기'))
for x in (31, 32, 33): put('bike', ['bike#D23A3A', 'bike#F2F2EE', 'bike#3E9C64'][x - 31], x, 10, solid=False)
edge_exits('tokyo')
finish([dict(n='이케부쿠로역', t=[8, 9]), dict(n='부엉이 동상', t=[4, 10]), dict(n='영화관', t=[21, 9]), dict(n='전망대 빌딩', t=[33, 8]), dict(n='번화가', t=[18, 26]),
        dict(n='애니 상점 거리', t=[28, 26]), dict(n='작은 공원', t=[8, 30])], [18, 19])
