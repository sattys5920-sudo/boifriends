# 도쿄 학교: 뒤쪽 4층 본관(가운데 시계), 동쪽 체육관, 서쪽 수영장, 가운데 큰 운동장(트랙·골대),
#   앞쪽 교문(벚나무 줄) + 자전거 보관소 + 학교 앞 도로
NAME, NX, NY = 'tk_school', 44, 36
exec(open('tk_lib.py').read())
fill('walk', 0, 0, NX, NY)
fill('dirt', 6, 12, 38, 28)               # 운동장
fill('grass', 0, 28, NX, 31); fill('walk', 18, 28, 24, 31)   # 앞 울타리 화단 + 교문 길
fill('road', 0, 32, NX, 36); fill('walk', 0, 31, NX, 32)
fill('water', 1, 3, 5, 9)                 # 수영장
def ov(fx, fy, t):
    if t == 'dirt':   # 타원 트랙
        cx, cy, rx, ry = 22, 20, 13, 6
        ex = max(0, abs(fx - cx) - (rx - ry)); r = (ex ** 2 + (fy - cy) ** 2) ** .5
        if ry - .9 < r < ry + .9:
            if abs(r - ry) < .05 or abs(r - (ry - .45)) < .04 or abs(r - (ry + .45)) < .04: return WHITE
            return hexc('#B8604A') if random.random() > .1 else hexc('#A85440')
        if abs(fx - cx) < .05 and abs(fy - cy) < ry - 1: return WHITE
        if abs(r - 2) < .06 and abs(fx - cx) < 2.1: return WHITE
    if t == 'water':
        if int(fy) in (4, 5, 6, 7) and abs(fy % 1 - .5) < .06: return hexc('#E8F4FF')     # 레인 줄
        if fx < 1.2 or fx > 4.8 or fy < 3.2 or fy > 8.8: return hexc('#E8F0F4')
        return hexc('#5AB4E0') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#8AD0F0')
    if t == 'road': return road_x(fx, fy, 32, 36, cross=[(19, 23)])
ground(ov)
# ---- 본관 ----
def main_layers():
    L, R = 26 * 8, 7 * 8
    out = []
    for fl in range(4):
        v = 6 + fl * 18
        for u in range(6, L - 8, 12):
            if fl == 0 and 92 <= u <= 112: continue
            out.append(('L', u, v, 9, 12, win(random.random() < .25, frame='#7A8A9A')))
        for u in range(6, R - 8, 12): out.append(('R', u, v, 9, 12, win(random.random() < .2, frame='#7A8A9A')))
        out += [('L', 0, v - 4, L, 2, '#D0D4D8'), ('R', 0, v - 4, R, 2, '#D0D4D8')]
    out += [('L', 90, 0, 28, 20, glass(False, door=(2, 26))), ('L', 86, 20, 36, 4, '#7A8A9A'),
            ('L', 94, 74, 18, 18, lambda u, v, w, h: hexc('#E4E4DE') if clock_face(u, v, w, h) is None else clock_face(u, v, w, h))]
    return out
bld('main', [8, 0, 34, 7], shop(8, 0, 34, 7, 96, '#F2F2EE', main_layers(), roofc='#9AA0A8'),
    door=dict(tile=[20, 7], to='school_hall', label='본관 · 신발장', spawn=[6, 8]))
# 옥상 물탱크·펜스
def rooftop(img):
    d = ImageDraw.Draw(img)
    box(d, 30, 1, 32, 3, 12, '#B8BCC4', '#C8CCD4', '#D8DCE4', lift=96)
    for x in range(9, 34, 1):
        X, Y = up(P(x, 6.7), 96); d.line([(X, Y), (X, Y - 8)], fill=hexc('#8A9A8A'))
    a, b = up(P(8.3, 6.7), 104), up(P(33.7, 6.7), 104); d.line([a, b], fill=hexc('#8A9A8A'))
bld('rooftop', [30, 1, 32, 3], rooftop, solid=False)
# ---- 체육관 ----
bld('gym', [36, 2, 43, 12], combo(shop(36, 2, 43, 12, 46, '#E4DCCC', [
    ('L', 0, 0, 56, 6, '#8A8A90'), ('L', 6, 10, 44, 10, lambda u, v, w, h: hexc('#7A8A9A') if u % 8 == 0 else hexc('#BCD4E8')),
    ('L', 20, 0, 16, 20, door('#7A8A9A', '#5A6070', glassy=True)), ('R', 0, 0, 80, 6, '#8A8A90'),
    ('R', 6, 22, 68, 10, lambda u, v, w, h: hexc('#7A8A9A') if u % 8 == 0 else hexc('#BCD4E8'))], roof='#3E7A6A', rh=18)),
    door=dict(tile=[39, 12], to='school_gym', label='체육관', spawn=[6, 8]))
# ---- 수영장 펜스 ----
for x in range(0, 6): put('fence', 'rail', x, 9, solid=False)
for y in range(2, 10): put('fence', 'railY', 5, y, solid=False)
for y in range(3, 9):
    for x in range(1, 5): occupied.add((x, y))
# ---- 운동장 소품 ----
def goal(img, x, y):
    d = ImageDraw.Draw(img); w_ = hexc('#F4F4F0')
    a, b = P(x, y), P(x, y + 2)
    for p_ in (a, b): d.line([p_, up(p_, 18)], fill=w_, width=2)
    d.line([up(a, 18), up(b, 18)], fill=w_, width=2)
    for k in range(1, 6):
        t = k / 6; X, Y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        d.line([(X, Y - 18), (X - 6, Y - 12)], fill=hexc('#C8C8C8'))
shared('goal', goal)
put('goal', 'goal', 9, 19, d=2, act=('축구 골대', '공 차기')); put('goal', 'goal', 34, 19, d=2, act=('축구 골대', '공 차기'))
def bar(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x + .2, y + .5), P(x + 1.8, y + .5)
    for p_ in (a, b): d.line([p_, up(p_, 20)], fill=hexc('#5A6A8A'), width=2)
    d.line([up(a, 20), up(b, 20)], fill=hexc('#A8B0C0')); d.line([up(a, 12), up(b, 12)], fill=hexc('#A8B0C0'))
shared('bar', bar)
put('bar', 'bar', 2, 14, w=2, act=('철봉', '매달려 보기'))
def podium(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .1, y + .1, x + 1.9, y + .9, 10, '#C8C8C8', '#D8D8D8', '#E8E8E8')
shared('podium', podium)
put('podium', 'podium', 21, 9, w=2, act=('조회대', '올라가 보기'))
def flagpole(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.line([(cx, cy), (cx, cy - 70)], fill=hexc('#C8C8D0')); d.polygon([(cx + 1, cy - 70), (cx + 15, cy - 66), (cx + 1, cy - 62)], fill=hexc('#FFFFFF'))
    d.ellipse([cx + 5, cy - 68, cx + 9, cy - 64], fill=hexc('#E8463A'))
shared('flagpole', flagpole)
put('flag', 'flagpole', 24, 9)
# ---- 자전거 보관소 ----
def bike_shed(img):
    d = ImageDraw.Draw(img)
    for p_ in (P(38, 27.9), P(43, 27.9), P(43, 24.1)): d.line([p_, up(p_, 24)], fill=hexc('#5A6070'), width=2)
    poly(d, [up(P(37.8, 23.8), 26), up(P(43.2, 23.8), 26), up(P(43.2, 28.2), 24), up(P(37.8, 28.2), 24)], hexc('#3E7A6A'))
    for k in range(5): bike_at(['#D23A3A', '#F2F2EE', '#3A6EC8', '#3E9C64', '#E8C040'][k])(img, 38 + k, 26)
bld('shed', [38, 24, 43, 28], bike_shed, act=('자전거 보관소', '자전거 찾기'))
# ---- 화단 · 벚나무 · 교문 ----
for x in list(range(0, 17, 2)) + list(range(25, NX, 2)): put('tree', 'tree_pink', x, 29)
for x in list(range(1, 17, 2)) + list(range(26, NX, 2)): put('flower', 'flower', x, 29)
for x in list(range(0, 18)) + list(range(24, NX)): put('fence', 'rail', x, 30, solid=False)
def school_gate(img):
    d = ImageDraw.Draw(img)
    for xa in (17.1, 23.9):
        box(d, xa - .45, 29.6, xa + .45, 30.5, 22, '#B8B0A0', '#C8C0B0', '#D8D0C0')
    X, Y = P(17.55, 30.5); g = sign('#F4F0E4', '#2A2A30', 4, vertical=True); a = img.load()
    for u in range(5):
        for v in range(18):
            c = g(u, v, 5, 18); xx, yy = int(X + 1 + u), int(Y - 20 + v * 1 - u * .5)
            if 0 <= xx < W and 0 <= yy < H: a[xx, yy] = c
bld('gate', [17, 29, 25, 31], school_gate, solid=False, act=('교문', '학교 이름 읽기'))
for y in (29, 30): occupied.update({(16, y), (17, y), (24, y), (25, y)})
for (x, y) in ((4, 31), (14, 31), (28, 31), (40, 31)): put('lamp', 'lamp2', x, y)
for (x, y) in ((1, 11), (42, 13), (1, 25), (42, 21)): put('tree', 'tree_round', x, y)
for (x, y) in ((2, 20), (40, 17)): put('bench', 'bench2', x, y, act=('운동장 벤치', '앉아서 쉬기'))
put('vend', 'vend#3A6EC8', 35, 12, act=('자판기', '음료 뽑기')); put('vend', 'vend#D23A3A', 34, 12, act=('자판기', '음료 뽑기'))
for (x, k) in ((6, 'car#F2F2EE'), (30, 'taxi')): put('car', k, x, 33, w=2, act=('달리던 차', '살펴보기'))
edge_exits('tokyo')
finish([dict(n='본관', t=[20, 8]), dict(n='운동장', t=[22, 20]), dict(n='체육관', t=[39, 13]), dict(n='수영장', t=[3, 10]), dict(n='교문', t=[21, 30]),
        dict(n='자전거 보관소', t=[40, 29]), dict(n='조회대', t=[22, 11])], [21, 31])
