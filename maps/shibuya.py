# 시부야: 가운데 스크램블 교차로, 북서 역 광장(충견 동상), 북동 전광판 빌딩들, 남쪽 낮은 상점가(아치 간판 골목)
NAME, NX, NY = 'tk_shibuya', 44, 34
exec(open('tk_lib.py').read())
RX0, RX1, RY0, RY1 = 19, 24, 15, 20          # 세로길 x범위, 가로길 y범위
fill('back', 0, 0, NX, NY)
fill('walk', 0, 12, NX, 23); fill('walk', 16, 0, 27, NY)
fill('plaza', 2, 8, 16, 13)                  # 역 앞 광장
fill('road', 0, RY0, NX, RY1); fill('road', RX0, 0, RX1, NY)
fill('redwalk', 7, 23, 10, NY)               # 남서 상점가 골목
fill('walk', 30, 23, 36, NY)                 # 남동 광장
fill('plaza', 30, 26, 42, 32)
def ov(fx, fy, t):
    if t == 'walk' and (tactile(fy, (13, 21)) and not (RX0 - 2 < fx < RX1 + 2)): return hexc('#E8C040') if (fx * 6) % 1 < .55 else hexc('#C89E2E')
    if t != 'road': return None
    inx, iny = RX0 <= fx < RX1, RY0 <= fy < RY1
    if inx and iny:                           # 스크램블: 대각선 두 줄
        a, b = (fx - RX0) - (fy - RY0), (fx - RX0) + (fy - RY0) - 5
        if (abs(a) < .55 or abs(b) < .55) and ((fx + fy) * 2.2) % 1 < .5: return hexc('#ECECE6')
        return None
    if iny and (RX0 - 2.2 < fx < RX0 - .2 or RX1 + .2 < fx < RX1 + 2.2): return hexc('#ECECE6') if (fy * 2.5) % 1 < .5 else None
    if inx and (RY0 - 2.2 < fy < RY0 - .2 or RY1 + .2 < fy < RY1 + 2.2): return hexc('#ECECE6') if (fx * 2.5) % 1 < .5 else None
    if iny: return road_x(fx, fy, RY0, RY1)
    if inx: return road_y(fx, fy, RX0, RX1)
ground(ov)

# ---- 북서: 역 (낮고 길게) ----
def station_layers():
    out = [('L', 0, 30, 112, 8, sign('#2E5A8A', '#FFFFFF', 12)), ('R', 0, 30, 64, 8, '#2E5A8A')]
    for u in range(4, 108, 14): out.append(('L', u, 6, 10, 18, glass(False)))
    out += [('L', 40, 0, 26, 24, glass(False, door=(2, 24))), ('R', 4, 0, 24, 24, glass(False, door=(2, 22))), ('R', 34, 6, 24, 16, glass(False))]
    return out
bld('station', [2, 0, 16, 8], shop(2, 0, 16, 8, 44, '#D8D0C0', station_layers(), roofc='#8A8E96'),
    door=dict(tile=[8, 8], to='tk_station', label='시부야역 · 개찰구', spawn=[6, 8]))
put('statue', 'statue_dog', 11, 10, act=('충견 동상', '쓰다듬기'))
for (x, y) in ((4, 9), (14, 9), (4, 12), (9, 12)): put('tree', 'tree_round', x, y)
for (x, y) in ((6, 11), (13, 12)): put('bench', 'bench2', x, y, act=('광장 벤치', '앉아서 쉬기'))
# ---- 북동: 전광판 빌딩들 ----
bld('qfront', [26, 2, 32, 12], combo(shop(26, 2, 32, 12, 112, '#3A4A5E', [
    ('L', 2, 40, 44, 60, screen(3)), ('R', 2, 40, 76, 60, screen(4)),
    ('L', 0, 0, 48, 34, glass(False, door=(18, 30), tint='#9ACDE8')), ('R', 0, 0, 80, 34, glass(False, tint='#9ACDE8')),
    ('L', 0, 102, 48, 8, sign('#1E1E26', '#5AD8FF', latin=True)), ('R', 0, 102, 80, 8, sign('#1E1E26', '#5AD8FF', latin=True))], roofc='#4A4E58')),
    door=dict(tile=[29, 12], to='tk_cafe', label='전광판 빌딩 · 카페', spawn=[6, 8]))
def office(seed, n, col, fl0=40):
    out = []
    for fl in range(n):
        v = fl0 + fl * 14
        for u in range(4, 44, 10): out.append(('L', u, v, 8, 10, win(random.random() < .3, blind=True)))
        for u in range(6, 60, 12): out.append(('R', u, v, 8, 10, win(random.random() < .2, blind=True)))
    return out
bld('tower', [33, 1, 39, 12], combo(shop(33, 1, 39, 12, 140, '#B8C0CC', office(1, 6, '#B8C0CC') + [
    ('L', 0, 0, 48, 34, glass(True, door=(18, 30))), ('L', 0, 34, 48, 4, '#E05A8A'), ('R', 0, 0, 88, 34, glass(True)), ('R', 0, 34, 88, 4, '#E05A8A')], roofc='#8A909A'),
    roof_sign(33, 1, 39, 12, 140, 12, '#E8463A', '#FFFFFF', latin=True)),
    door=dict(tile=[36, 12], to='tk_store', label='패션 빌딩', spawn=[6, 8]))
bld('slim', [40, 3, 43, 12], combo(shop(40, 3, 43, 12, 96, '#6A5A7A', office(2, 4, '#6A5A7A', 36) + [('L', 0, 0, 24, 28, glass(False, door=(4, 20))), ('R', 4, 4, 60, 24, poster(5))], roofc='#4A4058'),
    vsign(40, 12, 4, 90, 50, '#FFE45A', '#2A2230')), door=dict(tile=[41, 12], to='tk_karaoke', label='노래방', spawn=[6, 8]))
# ---- 남서: 상점가 골목 + 아치 ----
def arch(img):
    d = ImageDraw.Draw(img); a, b = P(7.2, 23.4), P(9.8, 23.4)
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 44, p_[0] + 1, p_[1]], fill=hexc('#5A5E68'))
    lw = int(b[0] - a[0]) + 12; g = sign('#E8463A', '#FFFFFF', 6); px_ = img.load()
    for u in range(lw):
        for v in range(10):
            xx, yy = int(a[0] - 6 + u), int(a[1] - 44 - v + (u - 6) * .5)
            if 0 <= xx < W and 0 <= yy < H: px_[xx, yy] = g(u, v, lw, 10)
bld('arch', [7, 23, 10, 24], arch, solid=False)
SW = [(0, 3, 30, '#E8E4DA', [('L', 2, 0, 20, 22, glass(True, door=(6, 14))), ('L', 0, 22, 24, 6, sign('#E86A2A', '#FFFFFF', 5))], ('tk_fastfood', '햄버거 가게')),
      (3, 7, 34, '#4A3A6A', [('L', 2, 0, 28, 24, lambda u, v, w, h: hexc(['#FF5A8A', '#5AD8FF', '#FFE45A'][(u // 4 + v // 6) % 3]) if (u % 4 and v % 6) else hexc('#2A2240')), ('L', 0, 26, 32, 7, sign('#2A2240', '#FF5A8A', 7))], ('tk_arcade', '게임센터'))]
for (x0, x1, h, col, lay, (to, lab)) in SW:
    bld('shop', [x0, 24, x1, 30], shop(x0, 24, x1, 30, h, col, lay + [('R', 4, 4, 30, 14, poster(x0))], roofc='#7A7680'), door=dict(tile=[(x0 + x1) // 2, 30], to=to, label=lab, spawn=[6, 8]))
bld('shop', [10, 24, 16, 30], shop(10, 24, 16, 30, 32, '#D8C8B0', [('L', 2, 0, 44, 22, glass(True, door=(18, 32), tint='#F2E0C8')), ('L', 0, 22, 48, 7, sign('#3E9C64', '#FFFFFF', 10))], roofc='#8A8070'),
    door=dict(tile=[13, 30], to='tk_drug', label='드럭스토어', spawn=[6, 8]))
for x in (1, 4, 11, 14): put('vend', 'vend#D23A3A' if x % 2 else 'vend#3A6EC8', x, 31, act=('자판기', '음료 뽑기'))
# ---- 남동: 낮은 부티크 + 광장 ----
bld('boutique', [27, 23, 30, 30], shop(27, 23, 30, 30, 36, '#F2EEE8', [('R', 4, 2, 48, 22, glass(False, door=(18, 30), tint='#F8E8F0')), ('R', 0, 26, 56, 6, sign('#1E1E26', '#F2D0E0', latin=True)), ('L', 3, 2, 18, 22, poster(9))], roofc='#B8B0B8'),
    door=dict(tile=[30, 27], to='tk_boutique', label='부티크', spawn=[6, 8]))
bld('boutique', [36, 23, 42, 26], shop(36, 23, 42, 26, 34, '#C8A878', [('L', 2, 0, 44, 22, glass(True, door=(18, 30), tint='#F2E8D8')), ('L', 0, 24, 48, 6, stripes('#8A3A3A', '#F2EAD8'))], roofc='#8A7A68'),
    door=dict(tile=[39, 26], to='tk_bakery', label='빵집', spawn=[6, 8]))
put('fountain', 'fountain', 33, 28, w=3, d=3, act=('광장 분수', '구경하기'))
for (x, y) in ((31, 27), (40, 27), (31, 31), (40, 31)): put('tree', 'tree_pink', x, y)
for (x, y) in ((37, 28), (37, 30)): put('bench', 'bench2', x, y, act=('광장 벤치', '앉아서 쉬기'))
# ---- 길가 ----
for (x, y) in ((1, 13), (14, 13), (27, 13), (42, 13), (1, 21), (14, 21), (28, 21), (42, 21), (17, 2), (25, 2), (17, 30), (25, 30)): put('lamp', 'lamp2', x, y)
for x in list(range(2, RX0 - 3)) + list(range(RX1 + 3, NX - 1)):
    put('rail', 'rail', x, RY0 - 1, solid=False); put('rail', 'rail', x, RY1, solid=False)
for y in list(range(1, RY0 - 3)) + list(range(RY1 + 3, NY - 1)):
    put('rail', 'railY', RX0 - 1, y, solid=False); put('rail', 'railY', RX1, y, solid=False)
for (x, y, k) in ((5, 16, 'taxi'), (9, 16, 'car#F2F2EE'), (30, 18, 'taxiY'), (36, 17, 'car#B83A3A')): put('car', k, x, y, w=2, act=('달리던 차', '살펴보기'))
for (x, y) in ((26, 22), (16, 22)): put('cone', 'cone', x, y, solid=False)
for x in (3, 5): put('bike', 'bike#3A6EC8' if x == 3 else 'bike#F2F2EE', x, 22, solid=False)
edge_exits('tokyo')
finish([dict(n='스크램블 교차로', t=[21, 17]), dict(n='시부야역', t=[8, 9]), dict(n='충견 동상', t=[11, 11]), dict(n='전광판 빌딩', t=[29, 13]), dict(n='상점가 골목', t=[8, 27]), dict(n='남쪽 광장', t=[34, 29])], [21, 22])
