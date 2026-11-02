# 하라주쿠: 북쪽 신궁 숲 + 큰 나무 도리이(이케부쿠로 쪽 길), 서쪽 뾰족 지붕 옛 역사, 가운데 큰길,
#   남쪽 좁고 알록달록한 다케시타 거리(크레페 노점) + 동쪽 가로수 명품 거리
NAME, NX, NY = 'tk_harajuku', 40, 36
exec(open('tk_lib.py').read())
fill('grass', 0, 0, NX, 11); fill('gravel', 16, 0, 23, 13)    # 신궁 숲길
fill('walk', 0, 11, NX, 13); fill('road', 0, 13, NX, 17); fill('walk', 0, 17, NX, 19)
fill('redwalk', 14, 19, 23, NY)                                # 다케시타 거리
fill('walk', 23, 19, NX, NY); fill('plaza', 25, 21, 38, 34)
def ov(fx, fy, t):
    if t == 'road': return road_x(fx, fy, 13, 17, cross=[(16, 21)])
    if t == 'redwalk' and (int(fx) + int(fy)) % 5 == 0 and (fx % 1) < .5 and (fy % 1) < .5: return hexc('#F2A0C0')   # 알록달록 보도
ground(ov)
# ---- 신궁 숲 + 큰 나무 도리이 ----
def wood_torii(img):
    d = ImageDraw.Draw(img); wd, dk = hexc('#8A6A4A'), hexc('#6A4E36')
    pa, pb = P(16.8, 4.5), P(22.2, 4.5)
    for p_ in (pa, pb): d.rectangle([p_[0] - 3, p_[1] - 64, p_[0] + 3, p_[1]], fill=wd); d.rectangle([p_[0] - 3, p_[1] - 64, p_[0] - 1, p_[1]], fill=dk)
    a1, b1 = up(pa, 50), up(pb, 50); d.line([(a1[0] - 6, a1[1] + 3), (b1[0] + 6, b1[1] - 3)], fill=wd, width=4)
    a2, b2 = up(pa, 64), up(pb, 64)
    d.polygon([(a2[0] - 12, a2[1] + 2), (b2[0] + 12, b2[1] - 14), (b2[0] + 12, b2[1] - 8), (a2[0] - 12, a2[1] + 8)], fill=dk)
bld('torii', [16, 4, 23, 5], wood_torii, solid=False, act=('큰 나무 도리이', '고개 숙여 인사하기'))
for p_ in ((16, 4), (22, 4)): occupied.add(p_)
for x in range(0, NX):
    for y in range(0, 10):
        if 15 <= x <= 23: continue
        if random.random() < .55: put('tree', random.choice(['tree_big', 'tree_round', 'tree_pine']), x, y)
# ---- 서쪽 옛 역사 (뾰족 지붕) ----
bld('station', [2, 7, 11, 11], combo(shop(2, 7, 11, 11, 30, '#F2EEE4', [('L', 0, 0, 72, 30, lambda u, v, w, h: hexc('#6A4A3A') if u % 12 in (0, 1) or v in (0, 1, 14) else None),
    ('L', 28, 0, 16, 22, glass(False, door=(2, 14))), ('L', 6, 4, 12, 12, win(True, frame='#6A4A3A')), ('L', 54, 4, 12, 12, win(True, frame='#6A4A3A'))], roof='#5A6A8A', rh=22, tex=4),
    clock_tower(6.5, 9, 30, 1.4, 14, '#F2EEE4', '#5A6A8A')),
    door=dict(tile=[6, 11], to='tk_station_h', label='하라주쿠역', spawn=[6, 8]))
# ---- 다케시타 거리 서쪽 가게 (옆면이 길을 봐요) ----
COLS = ['#F8C8DC', '#C8E8F8', '#F8F0A8', '#D8C8F8', '#C8F8D8', '#F8D8B8']
LABS = ['크레페 가게', '빈티지 옷 가게', '솜사탕 가게', '액세서리 가게', '양말 가게', '프리쿠라 가게']
for i in range(6):
    y0 = 19 + i * 3 - (0 if i < 5 else 1)
    if y0 + 3 > NY: break
    bld('takeshita', [10, y0, 14, y0 + 3], shop(10, y0, 14, y0 + 3, 30 + (i % 3) * 6, COLS[i], [('R', 1, 0, 22, 20, glass(True, door=(8, 16), tint='#FFF4FA')), ('R', 0, 21, 24, 7, sign('#FFFFFF', '#E8468A', 5)),
        ('L', 4, 4, 24, 18, poster(90 + i))], roofc=shade(hexc(COLS[i]), .7)), door=dict(tile=[14, y0 + 1], to='tk_takeshita%d' % i, label=LABS[i], spawn=[6, 8]))
def take_arch(img):
    d = ImageDraw.Draw(img); a, b = P(14.2, 19.4), P(22.8, 19.4)
    for p_ in (a, b): d.rectangle([p_[0] - 1, p_[1] - 40, p_[0] + 1, p_[1]], fill=hexc('#E8E8F0'))
    d.line([up(a, 40), up(b, 40)], fill=hexc('#E8E8F0'), width=2)
    for k in range(9):
        t = (k + .5) / 9; X, Y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t - 46 - 4 * math.sin(math.pi * t)
        d.ellipse([X - 3, Y - 4, X + 3, Y + 3], fill=hexc(['#F2A0C0', '#8AD0F0', '#F2E27A', '#C8A0F0', '#8AF0B0'][k % 5]))
bld('arch', [14, 19, 23, 20], take_arch, solid=False, act=('다케시타 거리 입구', '올려다보기'))
def crepe(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .1, y + .1, x + .9, y + .9, 14, '#F8C8DC', '#FFE0EC', '#FFFFFF')
    hip(d, x + .1, y + .1, x + .9, y + .9, 18, 4, '#E8468A', e=.15)
    X, Y = up(P(x + .5, y + .9), 8); d.polygon([(X - 2, Y), (X + 2, Y), (X, Y + 6)], fill=hexc('#D8A060')); d.ellipse([X - 3, Y - 4, X + 3, Y + 1], fill=hexc('#FFF8F0'))
shared('crepe', crepe)
for y in (22, 27, 32): put('stall', 'crepe', 22, y, act=('크레페 노점', '크레페 사기'))
# ---- 동쪽 가로수 명품 거리 ----
for (x0, y0, x1, y1, h, wall) in ((26, 20, 31, 24, 40, '#F2F0EA'), (32, 20, 38, 24, 46, '#D8D0C4')):
    bld('boutique', [x0, y0, x1, y1], shop(x0, y0, x1, y1, h, wall, [('L', 0, 0, (x1 - x0) * 8, 26, glass(False, door=(16, 28), tint='#F2EAE0')), ('L', 0, 30, (x1 - x0) * 8, 6, sign(wall, '#2A2A30', latin=True)),
        ('R', 0, 0, (y1 - y0) * 8, 26, glass(False, tint='#F2EAE0'))], cornice=shade(hexc(wall), .8)[:3] and '#B8B0A4'),
        door=dict(tile=[(x0 + x1) // 2, y1], to='tk_omote%d' % x0, label='명품 매장', spawn=[6, 8]))
for y in range(25, 35, 3): put('tree', 'tree_big', 25, y); put('tree', 'tree_big', 38, y)
for (x, y) in ((29, 28), (33, 31)): put('bench', 'bench2', x, y, act=('가로수 벤치', '앉아서 쉬기'))
put('statue', 'statue_owl', 31, 26, act=('작은 동상', '살펴보기')) if False else None
for (x, y) in ((3, 12), (12, 12), (26, 12), (37, 12), (3, 18), (12, 18), (26, 18), (37, 18)): put('lamp', 'lamp2', x, y)
for (x, y, k) in ((4, 14, 'taxi'), (28, 15, 'car#F2F2EE')): put('car', k, x, y, w=2, act=('달리던 차', '살펴보기'))
for x in (24, 25): put('vend', 'vend#3A6EC8' if x == 24 else 'vend#D23A3A', x, 11, act=('자판기', '음료 뽑기'))
edge_exits('tokyo')
finish([dict(n='신궁 숲', t=[19, 6]), dict(n='큰 나무 도리이', t=[19, 5]), dict(n='하라주쿠역', t=[6, 12]), dict(n='다케시타 거리', t=[18, 26]), dict(n='가로수 명품 거리', t=[31, 27])], [18, 20])
