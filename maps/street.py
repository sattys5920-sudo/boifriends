# 우리 동네 거리 (tokyo.py를 연결용으로 옮긴 판): 북쪽 상가(편의점·라멘집·맨션·이자카야·빌딩 카페·드럭스토어), 도로, 남쪽 공원·신사·주차장
NAME, NX, NY = 'tk_street', 48, 28
exec(open('tk_lib.py').read())
random.seed(1964)
# ---------------- 땅 ----------------
T = {}
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
fill('back', 0, 0, NX, 10)          # 건물 뒤 골목 콘크리트
fill('walk', 0, 10, NX, 12)         # 북쪽 인도
fill('road', 0, 12, NX, 17)         # 2차선 도로
fill('walk', 0, 17, NX, 19)         # 남쪽 인도
fill('grass', 1, 19, 20, 27)        # 동네 공원
fill('gravel', 3, 21, 18, 23); fill('gravel', 9, 19, 11, 27)
fill('sand', 13, 24, 17, 27)        # 모래놀이터
fill('stone', 22, 19, 31, 27)       # 신사 경내 돌바닥
fill('gravel', 25, 19, 28, 27)      # 참배길
fill('asph', 33, 19, NX, 27)        # 코인 주차장
fill('walk', 20, 19, 22, 27); fill('walk', 31, 19, 33, 27)
for x in range(NX):
    for y in range(NY): T.setdefault((x, y), 'grass')
CROSS = (22, 25)                    # 횡단보도 x 범위
GRASS = [hexc('#5E9A4A'), hexc('#548E42'), hexc('#68A452'), hexc('#4E863E')]
PAVE = [hexc('#C8C2B6'), hexc('#BEB8AC'), hexc('#D0CABE')]
bg = Image.new('RGBA', (W, H), hexc('#1A1826')); px = bg.load()
for y in range(H):
    for x in range(W):
        a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
        if not (0 <= fx < NX and 0 <= fy < NY): continue
        t = T[(int(fx), int(fy))]
        if t == 'walk':
            bx, by = int(fx * 2), int(fy * 2)
            c = PAVE[(bx * 5 + by * 3) % 3]
            if (fx * 2) % 1 < .08 or (fy * 2) % 1 < .12: c = hexc('#9E988C')
            band = fy - int(fy)
            if int(fy) in (10, 18) and .35 < band < .65:          # 점자블록(노란 줄)
                c = hexc('#E8C040') if ((fx * 6) % 1 < .55) else hexc('#C89E2E')
            if int(fy) in (11, 17) and ((int(fy) == 11 and band > .86) or (int(fy) == 17 and band < .14)): c = hexc('#E4E0D8')  # 연석
        elif t == 'road':
            c = hexc('#4E5060') if random.random() > .1 else random.choice([hexc('#44465A'), hexc('#5A5C6C')])
            band = fy - 12
            if .15 < band < .3 or 4.7 < band < 4.85: c = hexc('#E8E8E0')               # 가장자리 흰 선
            if 2.42 < band < 2.58 and (fx * .75) % 1 < .5: c = hexc('#E8E8E0')       # 가운데 점선
            if CROSS[0] <= fx < CROSS[1] and .4 < band < 4.6:
                c = hexc('#ECECE6') if (fy * 2.5) % 1 < .5 else hexc('#4E5060')     # 횡단보도
            if CROSS[0] - .6 < fx < CROSS[0] - .4 and band < 2.4: c = hexc('#E8E8E0')  # 정지선
            if CROSS[1] + .4 < fx < CROSS[1] + .6 and band > 2.6: c = hexc('#E8E8E0')
        elif t == 'asph':
            c = hexc('#5A5C6A') if random.random() > .1 else hexc('#50525E')
            if (fx - 33) % 3 < .12 and 20 < fy < 25: c = hexc('#E8E8E0')            # 주차 칸 선
            if 20.4 < fy < 20.55 and fx > 33: c = hexc('#E8E8E0')
        elif t == 'back':
            c = hexc('#7A7680') if random.random() > .1 else hexc('#6E6A74')
        elif t in ('gravel', 'sand'):
            c = (hexc('#C8BCA0') if random.random() > .2 else hexc('#B4A88C')) if t == 'gravel' else (hexc('#E0CC96') if random.random() > .12 else hexc('#CCB884'))
        elif t == 'stone':
            bx, by = int(fx * 1.5 + (int(fy * 1.5) % 2) * .5), int(fy * 1.5)
            c = [hexc('#A8A49C'), hexc('#9C988E'), hexc('#B2AEA6')][(bx * 7 + by * 3) % 3]
            if (fx * 1.5 + (int(fy * 1.5) % 2) * .5) % 1 < .07 or (fy * 1.5) % 1 < .1: c = hexc('#7E7A72')
        else:
            c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
            if random.random() < .008: c = random.choice([hexc('#F2E27A'), hexc('#F2A0C0'), hexc('#FFFFFF')])
        px[x, y] = c
for x in range(W):     # 앞쪽 두 면 단면
    for y in range(H):
        if px[x, y][:3] != (0x1A, 0x18, 0x26): continue
        a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
        if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = hexc('#6E6A62') if (y // 3) % 2 else hexc('#5E5A54')
os.makedirs('out', exist_ok=True)
bg.save('out/tokyo_bg.png'); print('bg', W, H)

# ---------------- 그림 도구 ----------------
def combo(*fs):
    def f(img):
        for g in fs: g(img)
    return f
GLYPHS = [["111", "010", "111", "101"], ["101", "111", "101", "111"], ["111", "101", "111", "001"], ["010", "111", "010", "101"],
          ["111", "100", "111", "111"], ["110", "011", "110", "011"], ["011", "110", "011", "111"]]
def sign(bgc, fg, n=None, edge=None, vertical=False):
    """읽을 수 없는 가짜 글자 간판"""
    rnd = random.Random(len(bgc) * 31 + sum(bgc[:3]) + (n or 0))
    pick = [rnd.choice(GLYPHS) for _ in range(12)]
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return edge or shade(bgc, .6)
        if vertical:
            k, gx, gy = (h - 3 - v) // 5, u - (w - 3) // 2, (h - 3 - v) % 5
        else:
            k, gx, gy = (u - 2) // 4, (u - 2) % 4, (h - 3 - v)
        if 0 <= gx < 3 and 0 <= gy < 4 and 0 <= k < (n or 12) and (u >= 2) and (vertical or u < w - 2) and (not vertical or v >= 2):
            if pick[k % 12][gy][gx] == '1': return fg
        return bgc
    return f
def glass(shelf=True, door=None):
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return hexc('#5A5E6A')
        if door and door[0] <= u < door[1]:
            if u in (door[0], door[1] - 1, (door[0] + door[1]) // 2): return hexc('#6A7484')
            return hexc('#D8ECF6') if (u + v) % 9 else hexc('#FFFFFF')
        c = hexc('#BCE0F0')
        if shelf and v % 6 in (1, 2): c = [hexc('#E86A6A'), hexc('#F2C85A'), hexc('#7AC87A'), hexc('#6AA0E8'), hexc('#F4F4F4')][(u // 3 + v // 6) % 5]
        if shelf and v % 6 == 3: c = hexc('#9ABACA')
        if (u + v) % 11 == 0 and not shelf: c = hexc('#E8F6FF')
        return c
    return f
def win(lit=False, blind=False, frame='#4A4E5A'):
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return hexc(frame)
        if u == w // 2: return shade(hexc(frame), 1.3)
        if blind and v % 2 == 0: return hexc('#D8E0E8')
        if lit: return hexc('#FFE0A0') if (u + v) % 7 else hexc('#FFF0C8')
        return hexc('#8AB4D8') if (u - v) % 9 else hexc('#D8ECFA')
    return f
def stripes(c1, c2, k=3):
    def f(u, v, w, h): return c1 if (u // k) % 2 == 0 else c2
    return f
def shop(x0, y0, x1, y1, h, wall, layers=(), roof=None, rh=0, roofc=None, brick=False, tex=6):
    """앞(L)·옆(R) 면에 사각 층(간판·유리·창문)을 쌓아 그리는 상가 건물. roof=None이면 평지붕"""
    def draw(img):
        d = ImageDraw.Draw(img)
        def fn(side, dark):
            def f(u, v):
                if v >= h: return None
                c = wall
                if brick:
                    row = v // 4
                    if v % 4 == 0 or (u + (row % 2) * 5) % 10 == 0: c = shade(wall, .86)
                elif v % tex == 0: c = shade(wall, .94)
                for (s, u0, v0, w_, h_, col) in layers:
                    if s != side or not (u0 <= u < u0 + w_ and v0 <= v < v0 + h_): continue
                    cc = col(u - u0, v - v0, w_, h_) if callable(col) else col
                    if cc is not None: c = cc
                if v >= h - 2 and roof is None: c = shade(wall, .78)
                return shade(c, dark)
            return f
        face(img, x0, y0, x1, y1, 'L', fn('L', .9)); face(img, x0, y0, x1, y1, 'R', fn('R', 1.0))
        Tt, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
        if roof is None:
            rc = roofc or hexc('#9A9AA2')
            poly(d, [up(Tt, h), up(R, h), up(B, h), up(L, h)], shade(rc, 1.08))
            poly(d, [up(P(x0 + .3, y0 + .3), h), up(P(x1 - .3, y0 + .3), h), up(P(x1 - .3, y1 - .3), h), up(P(x0 + .3, y1 - .3), h)], rc)
        else:   # 기와 박공(우진각) 지붕: 처마가 살짝 나와요
            e = .35; T2, R2, B2, L2 = P(x0 - e, y0 - e), P(x1 + e, y0 - e), P(x1 + e, y1 + e), P(x0 - e, y1 + e)
            Th, Rh, Bh, Lh = up(T2, h - 2), up(R2, h - 2), up(B2, h - 2), up(L2, h - 2)
            ry = (y0 + y1) / 2; r1, r2 = up(P(x0 + (y1 - y0) / 2, ry), h + rh), up(P(x1 - (y1 - y0) / 2, ry), h + rh)
            dark, mid, light = shade(roof, .72), shade(roof, .86), roof
            poly(d, [Th, Rh, r2, r1], dark); poly(d, [Th, Lh, r1], dark); poly(d, [Rh, Bh, r2], mid); poly(d, [Lh, Bh, r2, r1], light)
            a = img.load()
            for yy in range(int(min(r1[1], r2[1])), int(Bh[1]) + 1, 2):
                for xx in range(int(Lh[0]), int(Rh[0]) + 1):
                    if 0 <= xx < W and 0 <= yy < H and a[xx, yy][3] and a[xx, yy][:3] in (light[:3], mid[:3]): a[xx, yy] = shade(a[xx, yy], .88)
            d.line([tuple(map(int, r1)), tuple(map(int, r2))], fill=shade(roof, .55), width=2)
    return draw
def on_wall(x0, y1, u, v):
    """앞면(L) 위의 점 → 화면 좌표"""
    bx, by = P(x0, y1); return (bx + u, by + u * .5 - v)
def lantern_on(x0, y1, u, v, c='#E8463A'):
    def f(img):
        d = ImageDraw.Draw(img); X, Y = on_wall(x0, y1, u, v)
        d.line([(X, Y - 9), (X, Y - 7)], fill=OUTL)
        d.ellipse([X - 3, Y - 7, X + 3, Y + 2], fill=hexc(c)); d.rectangle([X - 2, Y - 7, X + 2, Y - 6], fill=OUTL); d.rectangle([X - 2, Y + 1, X + 2, Y + 2], fill=OUTL)
        d.line([(X - 1, Y - 4), (X - 1, Y - 1)], fill=hexc('#FFB080'))
    return f
def vsign(x0, y1, u, v, h, bgc, fg):
    """벽에서 튀어나온 세로 간판"""
    def f(img):
        d = ImageDraw.Draw(img); X, Y = on_wall(x0, y1, u, v)
        d.polygon([(X, Y), (X + 3, Y + 2), (X + 3, Y + 2 - h), (X, Y - h)], fill=shade(hexc(bgc), .6))
        d.polygon([(X - 9, Y + 4), (X, Y), (X, Y - h), (X - 9, Y - h + 4)], fill=hexc(bgc))
        g = sign(hexc(bgc), hexc(fg), 7, vertical=True); a = img.load()
        for k in range(h - 2):
            for j in range(7):
                c = g(j + 1, k + 1, 9, h)
                xx, yy = int(X - 8 + j), int(Y - h + 4 + (h - 3 - k) + j * -.44 + 3)
                if c == hexc(fg) and 0 <= xx < W and 0 <= yy < H: a[xx, yy] = c
    return f
def box(d, x0, y0, x1, y1, h, cl, cr, ct, lift=0):
    Tt, R, B, L = [up(P(*p), lift) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    poly(d, [L, B, up(B, h), up(L, h)], cl); poly(d, [B, R, up(R, h), up(B, h)], cr); poly(d, [up(Tt, h), up(R, h), up(B, h), up(L, h)], ct)
    return Tt, R, B, L

# ---------------- 건물 (북쪽, 앞면이 길을 봐요) ----------------
YB0, YB1 = 3, 10
# 편의점
L1 = 9 * 8
unique('konbini', [1, YB0, 10, YB1], shop(1, YB0, 10, YB1, 42, hexc('#F2F0EA'), [
    ('L', 0, 30, L1, 4, hexc('#3E9C64')), ('L', 0, 27, L1, 3, hexc('#F08C2A')), ('L', 0, 24, L1, 3, hexc('#3C6EBE')),
    ('L', 22, 32, 28, 9, sign(hexc('#FFFFFF'), hexc('#3C6EBE'), 6)),
    ('L', 3, 1, L1 - 6, 21, glass(True, door=(26, 42))),
    ('R', 0, 30, 56, 4, hexc('#3E9C64')), ('R', 0, 27, 56, 3, hexc('#F08C2A')), ('R', 0, 24, 56, 3, hexc('#3C6EBE')),
    ('R', 6, 4, 22, 16, glass(True)), ('R', 32, 0, 14, 22, hexc('#C8C8C8')),
], roofc=hexc('#A4A4AA')), door=dict(tile=[5, 10], to='tokyo_konbini', label='편의점', spawn=[6, 8]))
# 라멘집 (나무 + 기와)
unique('ramen', [11, YB0 + 1, 16, YB1], combo(shop(11, YB0 + 1, 16, YB1, 34, hexc('#7A5238'), [
    ('L', 4, 22, 32, 8, sign(hexc('#F2E4C4'), hexc('#B0302A'), 7)),
    ('L', 8, 0, 24, 20, lambda u, v, w, h: hexc('#3A2418') if v > 12 else (hexc('#E8B070') if (u + v) % 6 else hexc('#FFD8A0'))),
    ('L', 8, 12, 24, 8, lambda u, v, w, h: (hexc('#C8302A') if u % 6 else hexc('#5A1A16')) if not (u % 6 in (2, 3) and v in (4, 5)) else hexc('#FFF2E0')),
    ('R', 10, 6, 10, 10, win(True, frame='#4A3020')), ('R', 30, 6, 10, 10, win(True, frame='#4A3020')),
], roof=hexc('#3E4250'), rh=12, tex=3), lantern_on(11, YB1, 4, 18), lantern_on(11, YB1, 36, 18)),
    door=dict(tile=[13, 10], to='tokyo_ramen', label='라멘집', spawn=[6, 8]))
# 맨션 (벽돌, 베란다, 실외기)
def mansion_layers():
    out = []
    for fl in range(4):
        v = 30 + fl * 18
        for u in (6, 22, 38):
            out.append(('L', u, v, 12, 11, win(random.random() < .35)))
        out.append(('L', 2, v - 3, 52, 2, hexc('#E8E8E8'))); out.append(('L', 2, v - 5, 52, 2, hexc('#9A9AA0')))
        for u in (8, 30):
            out.append(('R', u, v, 12, 11, win(random.random() < .3)))
    out += [('L', 20, 0, 16, 22, glass(False, door=(2, 14))), ('L', 18, 22, 20, 3, hexc('#5A5A62')), ('L', 4, 6, 10, 10, hexc('#9A9AA2'))]
    return out
def ac_units(img):
    d = ImageDraw.Draw(img)
    for (u, v) in ((44, 28), (8, 46), (44, 64), (24, 82)):
        X, Y = on_wall(17, YB1, u, v)
        d.polygon([(X, Y), (X + 9, Y + 4.5), (X + 9, Y - 2.5), (X, Y - 7)], fill=hexc('#ECECE8'))
        d.ellipse([X + 2, Y - 4, X + 6, Y + 1], fill=hexc('#A0A0A6'))
    d2 = ImageDraw.Draw(img); X, Y = up(P(20, 6.5), 102)
    d2.rectangle([X - 6, Y - 12, X + 6, Y], fill=hexc('#B8BCC4')); d2.rectangle([X - 6, Y - 12, X, Y], fill=hexc('#A0A4AC')); d2.ellipse([X - 6, Y - 15, X + 6, Y - 9], fill=hexc('#C8CCD4'))
unique('mansion', [17, YB0, 24, YB1], combo(shop(17, YB0, 24, YB1, 100, hexc('#C49A78'), mansion_layers(), brick=True, roofc=hexc('#8E8A86')), ac_units),
       door=dict(tile=[20, 10], to='tokyo_mansion', label='맨션 입구', spawn=[6, 8]))
# 자판기 (맨션 앞)
def vending(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img)
        Tt, R, B, L = box(d, x + .1, y + .2, x + .9, y + .7, 22, shade(hexc(col), .85), hexc(col), shade(hexc(col), 1.15))
        X, Y = L;
        for k in range(3):
            for j in range(2):
                xx, yy = X + 2 + k * 3, Y - 18 + j * 5 + k * 1.5
                d.rectangle([xx, yy, xx + 1, yy + 2], fill=hexc(['#F2C85A', '#E86A6A', '#7AC87A', '#FFFFFF', '#6AA0E8', '#B07A4A'][(k + j * 3) % 6]))
        d.polygon([(X + 1, Y - 21), (X + 11, Y - 16), (X + 11, Y - 7), (X + 1, Y - 12)], fill=None, outline=hexc('#E8F2F8'))
        d.rectangle([X + 4, Y - 4 + 1, X + 8, Y - 2 + 2], fill=hexc('#26262C'))
    return f
shared('vend_r', vending('#D23A3A')); shared('vend_b', vending('#3A6EC8')); shared('vend_w', vending('#E8E8E4'))
# 이자카야 (나무 격자 + 붉은 등)
unique('izakaya', [25, YB0 + 1, 31, YB1], combo(shop(25, YB0 + 1, 31, YB1, 36, hexc('#5E4636'), [
    ('L', 2, 0, 44, 22, lambda u, v, w, h: hexc('#3E2C22') if u % 3 == 0 else hexc('#86603E')),
    ('L', 16, 0, 16, 20, lambda u, v, w, h: hexc('#C88A4A') if u % 4 == 0 or v == 10 else hexc('#FFD08A')),
    ('L', 16, 14, 16, 6, lambda u, v, w, h: hexc('#3A3A44') if u % 5 == 0 else hexc('#F2EEE2')),
    ('L', 6, 24, 36, 9, sign(hexc('#EADCB0'), hexc('#2A2020'), 8)),
    ('R', 8, 4, 14, 14, lambda u, v, w, h: hexc('#3E2C22') if u % 3 == 0 or v % 4 == 0 else hexc('#FFD08A')),
], roof=hexc('#34363E'), rh=12, tex=3), lantern_on(25, YB1, 5, 20), lantern_on(25, YB1, 12, 20), lantern_on(25, YB1, 36, 20), lantern_on(25, YB1, 43, 20)),
    door=dict(tile=[28, 10], to='tokyo_izakaya', label='이자카야', spawn=[6, 8]))
# 빌딩 (회색 사무실, 1층 카페, 세로 네온 간판)
def office_layers():
    out = []
    for fl in range(5):
        v = 34 + fl * 16
        for u in range(4, 60, 12): out.append(('L', u, v, 10, 11, win(fl == 1 and u < 30, blind=True)))
        for u in (6, 22, 38): out.append(('R', u, v, 10, 11, win(False, blind=True)))
        out.append(('L', 0, v - 3, 64, 1, hexc('#8A8E98'))); out.append(('R', 0, v - 3, 56, 1, hexc('#8A8E98')))
    out += [('L', 0, 22, 64, 6, stripes(hexc('#2E7A5A'), hexc('#F2EEE0'))), ('L', 0, 0, 64, 22, hexc('#E8DCC4')),
            ('L', 4, 2, 22, 16, glass(False)), ('L', 28, 0, 12, 20, lambda u, v, w, h: hexc('#3A2418') if u in (0, w - 1) or v == h - 1 else (hexc('#8A5A3A') if u != 8 or v != 9 else hexc('#F2C85A'))),
            ('L', 42, 2, 18, 16, glass(False)), ('R', 0, 0, 56, 22, hexc('#E8DCC4')), ('R', 8, 4, 20, 14, glass(False))]
    return out
unique('office', [32, YB0, 40, YB1], combo(shop(32, YB0, 40, YB1, 116, hexc('#9EA4B0'), office_layers(), roofc=hexc('#7E828C')),
                                          vsign(32, YB1, 6, 96, 52, '#F25C8C', '#FFFFFF')),
       door=dict(tile=[36, 10], to='tokyo_cafe', label='카페', spawn=[6, 8]))
# 드럭스토어
unique('drug', [41, YB0 + 1, 47, YB1], shop(41, YB0 + 1, 47, YB1, 40, hexc('#F4F4F0'), [
    ('L', 0, 26, 48, 12, sign(hexc('#F8D028'), hexc('#2A3C9C'), 10)), ('L', 0, 24, 48, 2, hexc('#E03A4A')),
    ('L', 3, 1, 42, 21, glass(True, door=(16, 28))),
    ('R', 0, 26, 48, 12, hexc('#F8D028')), ('R', 0, 24, 48, 2, hexc('#E03A4A')), ('R', 8, 4, 18, 16, glass(True)),
], roofc=hexc('#A8A8AE')), door=dict(tile=[44, 10], to='tokyo_drug', label='드럭스토어', spawn=[6, 8]))

# ---------------- 남쪽: 신사 ----------------
def torii(img):
    d = ImageDraw.Draw(img); red, dk = hexc('#D8452E'), hexc('#A8301E')
    pa, pb = P(25.2, 19.6), P(27.8, 19.6)
    for p_ in (pa, pb):
        d.rectangle([p_[0] - 2, p_[1] - 46, p_[0] + 2, p_[1]], fill=red); d.rectangle([p_[0] - 2, p_[1] - 46, p_[0] - 1, p_[1]], fill=dk)
        d.rectangle([p_[0] - 3, p_[1] - 3, p_[0] + 3, p_[1]], fill=hexc('#2A2226'))
    a1, b1 = up(pa, 36), up(pb, 36); d.line([(a1[0] - 4, a1[1] + 2), (b1[0] + 4, b1[1] - 2)], fill=red, width=3)
    a2, b2 = up(pa, 46), up(pb, 46)
    d.polygon([(a2[0] - 9, a2[1] + 1), (b2[0] + 9, b2[1] - 10), (b2[0] + 9, b2[1] - 6), (a2[0] - 9, a2[1] + 5)], fill=hexc('#2A2226'))
    d.polygon([(a2[0] - 8, a2[1] + 4), (b2[0] + 8, b2[1] - 5), (b2[0] + 8, b2[1] - 1), (a2[0] - 8, a2[1] + 8)], fill=red)
    m = ((a2[0] + b2[0]) / 2, (a2[1] + b2[1]) / 2 + 6); d.rectangle([m[0] - 2, m[1] - 3, m[0] + 2, m[1] + 4], fill=hexc('#2A2226'))
unique('torii', [25, 19, 28, 20], torii, solid=False)
unique('shrine', [24, 23, 29, 27], combo(shop(24, 23, 29, 27, 26, hexc('#E8DCC4'), [
    ('L', 0, 0, 40, 26, lambda u, v, w, h: hexc('#C8442E') if u % 10 in (0, 1) or v < 3 else None),
    ('L', 12, 2, 16, 18, lambda u, v, w, h: hexc('#6A4A30') if u % 4 == 0 or v % 6 == 0 else hexc('#F4ECDA')),
    ('R', 0, 0, 32, 26, lambda u, v, w, h: hexc('#C8442E') if u % 10 in (0, 1) or v < 3 else None),
], roof=hexc('#4A5A5E'), rh=16, tex=4), lambda img: ImageDraw.Draw(img).ellipse([on_wall(24, 27, 18, 22)[0] - 2, on_wall(24, 27, 18, 22)[1] - 2, on_wall(24, 27, 18, 22)[0] + 2, on_wall(24, 27, 18, 22)[1] + 2], fill=hexc('#E8C040'))),
    act=('동네 신사', '참배하기'))
def stone_lantern(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); s, sd = hexc('#B4B0A6'), hexc('#8E8A80')
    d.rectangle([cx - 4, cy - 3, cx + 4, cy], fill=sd); d.rectangle([cx - 2, cy - 14, cx + 2, cy - 3], fill=s)
    d.rectangle([cx - 5, cy - 17, cx + 5, cy - 14], fill=sd); d.rectangle([cx - 4, cy - 23, cx + 4, cy - 17], fill=s); d.rectangle([cx - 2, cy - 21, cx + 1, cy - 18], fill=hexc('#FFD88A'))
    d.polygon([(cx - 7, cy - 23), (cx, cy - 29), (cx + 7, cy - 23)], fill=sd); d.rectangle([cx - 1, cy - 31, cx, cy - 29], fill=s)
shared('tourou', stone_lantern)
def offering_box(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .15, y + .3, x + .85, y + .7, 8, hexc('#6A4428'), hexc('#7E5432'), hexc('#9A6A42'))
shared('saisen', offering_box)

# ---------------- 길가 소품 ----------------
def pole_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 2, cy - 92, cx + 2, cy], fill=hexc('#A8A8AA')); d.rectangle([cx - 2, cy - 92, cx - 1, cy], fill=hexc('#C4C4C6')); d.rectangle([cx + 2, cy - 92, cx + 2, cy], fill=hexc('#7E7E82'))
    d.rectangle([cx - 10, cy - 86, cx + 10, cy - 84], fill=hexc('#6E6E72'))
    for k in (-8, -3, 3, 8): d.rectangle([cx + k, cy - 88, cx + k, cy - 87], fill=hexc('#E8E8E8'))
    d.rectangle([cx - 9, cy - 78, cx - 3, cy - 66], fill=hexc('#9A9CA0')); d.rectangle([cx - 9, cy - 78, cx - 7, cy - 66], fill=hexc('#B4B6BA'))
    for k in range(30, 76, 7): d.point((cx + (3 if k % 14 else -3), cy - k), fill=hexc('#5A5A5E'))
    d.rectangle([cx - 2, cy - 30, cx + 2, cy - 22], fill=hexc('#E8C040')); d.rectangle([cx - 2, cy - 27, cx + 2, cy - 25], fill=hexc('#2A2A2A'))
shared('pole', pole_at)
POLES = [(10, 10), (24, 10), (39, 10)]
def wires(img):
    d = ImageDraw.Draw(img)
    for dx, dy, sag in ((-8, -86, 6), (8, -86, 6)):
        for i in range(len(POLES) - 1):
            a, b = P(POLES[i][0] + .5, POLES[i][1] + .5), P(POLES[i + 1][0] + .5, POLES[i + 1][1] + .5)
            pts = [(a[0] + dx + (b[0] - a[0]) * t, a[1] + dy + (b[1] - a[1]) * t + sag * 4 * t * (1 - t)) for t in [k / 60 for k in range(61)]]
            d.point([tuple(map(int, p_)) for p_ in pts], fill=hexc('#2A2630'))
def road_sign(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 40, cx, cy], fill=hexc('#B8B8BC'))
    d.ellipse([cx - 7, cy - 52, cx + 7, cy - 38], fill=hexc('#2E62C8')); d.ellipse([cx - 6, cy - 51, cx + 6, cy - 39], fill=hexc('#3A72D8'))
    d.rectangle([cx - 4, cy - 46, cx + 4, cy - 44], fill=hexc('#FFFFFF'))
shared('sign', road_sign)
def lamp2_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 44, cx + 1, cy], fill=hexc('#5A6070')); d.rectangle([cx - 3, cy - 3, cx + 3, cy], fill=hexc('#4A5060'))
    d.line([(cx, cy - 44), (cx + 8, cy - 47)], fill=hexc('#5A6070'), width=2)
    d.rectangle([cx + 4, cy - 48, cx + 12, cy - 45], fill=hexc('#4A5060')); d.rectangle([cx + 5, cy - 45, cx + 11, cy - 44], fill=hexc('#FFF0B8'))
shared('lamp2', lamp2_at)
def bike_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for (wx, wy) in ((-5, 2), (5, -3)):
            d.ellipse([cx + wx - 4, cy + wy - 7, cx + wx + 4, cy + wy + 1], outline=hexc('#2A2A2E'))
        d.line([(cx - 5, cy - 1), (cx, cy - 6), (cx + 5, cy - 5), (cx - 1, cy - 2), (cx - 5, cy - 1)], fill=hexc(col), width=1)
        d.line([(cx, cy - 6), (cx - 1, cy - 9)], fill=hexc(col)); d.rectangle([cx - 3, cy - 10, cx, cy - 9], fill=hexc('#2A2A2E'))
        d.line([(cx + 5, cy - 5), (cx + 5, cy - 10)], fill=hexc('#A8A8AE')); d.line([(cx + 3, cy - 10), (cx + 7, cy - 11)], fill=hexc('#A8A8AE'))
        d.rectangle([cx + 5, cy - 9, cx + 9, cy - 6], fill=hexc('#B8B8BE'))
    return f
for c in ('#D23A3A', '#F2F2EE', '#3A6EC8', '#3E9C64'): shared('bike' + c, bike_at(c))
def rail_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 12, cx, cy], fill=hexc('#F0F0EC'))
    a, b = (cx - 8, cy - 4), (cx + 8, cy + 4)
    for k in (11, 6): d.line([(a[0], a[1] - k), (b[0], b[1] - k)], fill=hexc('#F4F4F0'), width=2)
shared('rail', rail_at)
def cone_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.polygon([(cx - 5, cy), (cx, cy + 2), (cx + 5, cy), (cx, cy - 2)], fill=hexc('#C85A1E'))
    d.polygon([(cx - 3, cy), (cx, cy - 12), (cx + 3, cy)], fill=hexc('#F0782A')); d.line([(cx - 2, cy - 5), (cx + 2, cy - 5)], fill=hexc('#FFFFFF'))
shared('cone', cone_at)
def car_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); c = hexc(col)
        box(d, x + .1, y + .15, x + 1.9, y + .95, 7, shade(c, .8), c, shade(c, 1.1), lift=2)
        box(d, x + .55, y + .25, x + 1.45, y + .85, 6, hexc('#6E8AA8'), hexc('#8EAAC8'), shade(c, 1.15), lift=9)
        for (wx, wy) in ((x + .45, y + .95), (x + 1.55, y + .95), (x + 1.9, y + .5)):
            X, Y = P(wx, wy); d.ellipse([X - 3, Y - 4, X + 3, Y + 1], fill=hexc('#22222A'))
        X, Y = up(P(x + 1.9, y + .3), 4); d.rectangle([X - 1, Y - 1, X + 1, Y], fill=hexc('#FFF2B8'))
    return f
for c in ('#F2F2EE', '#3A4A6A', '#E8C83A'): shared('car' + c, car_at(c))
def pay_machine(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .3, y + .3, x + .7, y + .7, 16, hexc('#C8C8CC'), hexc('#E0E0E4'), hexc('#F0F0F2'))
    cx, cy = P(x + .5, y + .5); d.rectangle([cx - 2, cy - 18, cx + 1, cy - 16], fill=hexc('#E8C040'))
shared('paym', pay_machine)
def swing_at(img, x, y):
    d = ImageDraw.Draw(img); a, b = P(x, y + .5), P(x + 2, y + .5)
    for p_ in (a, b): d.line([(p_[0] - 3, p_[1]), (p_[0], p_[1] - 26), (p_[0] + 3, p_[1] + 1)], fill=hexc('#3A72D8'), width=2)
    d.line([up(a, 26), up(b, 26)], fill=hexc('#3A72D8'), width=2)
    for t in (.33, .66):
        X, Y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        d.line([(X, Y - 26), (X, Y - 8)], fill=hexc('#8A8A90')); d.rectangle([X - 2, Y - 8, X + 2, Y - 7], fill=hexc('#E8C040'))
shared('swing', swing_at)
def toilet_sign(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    for dx in (-5, 4): d.rectangle([cx + dx, cy - 10, cx + dx + 1, cy], fill=hexc('#5A4A3A'))
    d.rectangle([cx - 7, cy - 22, cx + 7, cy - 10], fill=hexc('#2E6A44')); d.rectangle([cx - 6, cy - 21, cx + 6, cy - 11], fill=hexc('#3E8A58'))
    g = sign(hexc('#3E8A58'), hexc('#FFFFFF'), 3)
    for u in range(12):
        for v in range(10):
            if g(u, v, 12, 10) == hexc('#FFFFFF'): d.point((cx - 6 + u, cy - 12 - v), fill=hexc('#FFFFFF'))
shared('board', toilet_sign)
def planter_at(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .05, y + .25, x + .95, y + .75, 6, hexc('#8A7A6A'), hexc('#A08E7C'), hexc('#6A5A3A'))
    cx, cy = P(x + .5, y + .5)
    for dx, dy in ((-5, -8), (0, -10), (5, -8), (-2, -7), (3, -7)): d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=hexc('#4E9244'))
    for dx, dy in ((-4, -10), (2, -12), (5, -9)): d.point((cx + dx, cy + dy), fill=hexc('#F2A0C0'))
shared('planter', planter_at)

# ---------------- 놓기 ----------------
occupied = set()
for o in objs:
    b = o['box']
    for x in range(b[0], b[2]):
        for y in range(b[1], b[3]): occupied.add((x, y))
def put(name, key, x, y, **kw):
    if (x, y) in occupied: return
    place(name, key, x, y, **kw); occupied.add((x, y))
for (x, y) in POLES: put('pole', 'pole', x, y)
unique('wires', [0, 0, 0, 0], wires, solid=False)
_w = Image.new('RGBA', (W, H), (0, 0, 0, 0)); wires(_w); _bb = _w.getbbox()   # 전선은 테두리 없이 1px로
SPR[objs[-1]['spr']] = _w.crop(_bb); objs[-1]['x'], objs[-1]['y'] = _bb[0], _bb[1]
put('sign', 'sign', 32, 11)
put('vend', 'vend_r', 22, 10, act=('자판기', '음료 뽑기')); put('vend', 'vend_b', 23, 10, act=('자판기', '음료 뽑기'))
put('vend', 'vend_w', 9, 18, act=('자판기', '음료 뽑기'))
for (x, c) in ((2, '#D23A3A'), (3, '#F2F2EE'), (30, '#3A6EC8'), (46, '#3E9C64')): put('bike', 'bike' + c, x, 10, solid=False)
put('cone', 'cone', 41, 11, solid=False)
put('planter', 'planter', 15, 10); put('planter', 'planter', 31, 10)
for x in list(range(1, CROSS[0] - 1)) + list(range(CROSS[1] + 1, NX - 1)):
    if x % 1 == 0: put('rail', 'rail', x, 17, solid=False)
for x in (4, 14, 34, 44): put('lamp', 'lamp2', x, 18)
# 공원
for (x, y, k) in ((2, 20, 'tree_big'), (6, 26, 'tree_round'), (2, 25, 'tree_pink'), (18, 20, 'tree_round'), (12, 19, 'tree_pink'), (19, 25, 'tree_big'), (7, 19, 'tree_round')):
    put('tree', k, x, y)
for (x, y) in ((5, 23), (14, 23)): put('bench', 'bench', x, y, act=('공원 벤치', '앉아서 쉬기'))
put('swing', 'swing', 3, 21, w=2, act=('그네', '타 보기')); occupied.add((4, 21))
put('board', 'board', 11, 25, act=('공원 안내판', '읽어 보기'))
for (x, y) in ((1, 22), (18, 23), (8, 25)): put('bush', 'bush', x, y)
# 신사
for (x, y) in ((24, 21), (29, 21)): put('tourou', 'tourou', x, y, act=('돌등롱', '살펴보기'))
put('saisen', 'saisen', 26, 22, act=('새전함', '동전 넣기'))
for (x, y, k) in ((22, 19, 'tree_pine'), (30, 19, 'tree_pine'), (22, 26, 'tree_pine'), (30, 25, 'tree_pine')): put('tree', k, x, y)
# 코인 주차장
for (x, c) in ((34, '#F2F2EE'), (40, '#3A4A6A'), (43, '#E8C83A')):
    put('car', 'car' + c, x, 21, w=2, act=('주차된 차', '살펴보기')); occupied.add((x + 1, 21))
put('paym', 'paym', 37, 19, act=('주차 정산기', '살펴보기'))
for x in range(34, NX - 1, 2): put('planter', 'planter', x, 26)

edge_exits('tokyo')
finish([dict(n='편의점', t=[5, 10]), dict(n='라멘집', t=[13, 10]), dict(n='맨션', t=[20, 10]), dict(n='이자카야', t=[28, 10]), dict(n='카페', t=[36, 10]),
        dict(n='드럭스토어', t=[44, 10]), dict(n='횡단보도', t=[23, 14]), dict(n='동네 공원', t=[10, 22]), dict(n='동네 신사', t=[26, 21]), dict(n='코인 주차장', t=[40, 23])], [23, 18])
