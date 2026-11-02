# 도쿄·ACCA 맵들이 같이 쓰는 그리기 도구 (tokyo.py에서 뽑아 일반화)
#   맵 파일 맨 위에서:  NAME, NX, NY = 'shibuya', 44, 30 ; exec(open('tk_lib.py').read())
#   그다음 T(땅 종류)를 채우고 ground(overlay) → 건물·소품 unique/put → finish(areas, start)
import json, os, random, math
from PIL import Image, ImageDraw
random.seed(hash(NAME) & 0xffff)
W, H = (NX + NY) * 8 + 40, (NX + NY) * 4 + 240
OX, OY = NY * 8 + 20, 200
def P(tx, ty): return (OX + (tx - ty) * 8, OY + (tx + ty) * 4)
def hexc(h, a=255): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (a,)
def shade(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (c[3] if len(c) > 3 else 255,)
def up(p, k): return (p[0], p[1] - k)
OUTL = hexc('#1C1420')
_src = open('world.py').read()
exec(_src[_src.index('def poly(d, pts, c)'):_src.index('# 본관 (크게, 탑 두 개)')])
exec(_src[_src.index('def tree_at(kind):'):_src.index('def rock_at(')])
os.makedirs('out', exist_ok=True)

# ---------------- 땅 ----------------
T = {}
def fill(kind, x0, y0, x1, y1):
    for x in range(max(0, x0), min(NX, x1)):
        for y in range(max(0, y0), min(NY, y1)): T[(x, y)] = kind
GRASS = [hexc('#5E9A4A'), hexc('#548E42'), hexc('#68A452'), hexc('#4E863E')]
WHITE = hexc('#E8E8E0')
def _brick(fx, fy, s, cols, line, stagger=True):
    bx = int(fx * s + ((int(fy * s) % 2) * .5 if stagger else 0)); by = int(fy * s)
    if (fx * s + ((int(fy * s) % 2) * .5 if stagger else 0)) % 1 < .08 or (fy * s) % 1 < .12: return line
    return cols[(bx * 7 + by * 3) % len(cols)]
def base_color(t, fx, fy):
    r = random.random()
    if t == 'walk':   return _brick(fx, fy, 2, [hexc('#C8C2B6'), hexc('#BEB8AC'), hexc('#D0CABE')], hexc('#9E988C'), False)
    if t == 'redwalk':return _brick(fx, fy, 2, [hexc('#B86A5A'), hexc('#A85E50'), hexc('#C47462')], hexc('#8A4A40'))
    if t == 'plaza':  return _brick(fx, fy, 1, [hexc('#D4CCBE'), hexc('#C8C0B2')], hexc('#A89E90'), False)
    if t == 'road':   return hexc('#4E5060') if r > .1 else (hexc('#44465A') if r > .05 else hexc('#5A5C6C'))
    if t == 'asph':   return hexc('#5A5C6A') if r > .1 else hexc('#50525E')
    if t == 'back':   return hexc('#7A7680') if r > .1 else hexc('#6E6A74')
    if t == 'gravel': return hexc('#C8BCA0') if r > .2 else hexc('#B4A88C')
    if t == 'sand':   return hexc('#E0CC96') if r > .12 else hexc('#CCB884')
    if t == 'dirt':   return hexc('#C8A878') if r > .15 else hexc('#B89868')
    if t == 'stone':  return _brick(fx, fy, 1.5, [hexc('#A8A49C'), hexc('#9C988E'), hexc('#B2AEA6')], hexc('#7E7A72'))
    if t == 'cobble': return _brick(fx, fy, 3, [hexc('#9A8E80'), hexc('#8E8274'), hexc('#A69A8C')], hexc('#6A6056'))
    if t == 'wood':   return hexc('#9A6A44') if (fx * 3) % 1 > .12 else hexc('#6A4428')
    if t == 'water':
        c = hexc('#3E7AB8') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#5A96CC')
        return hexc('#BFE2FF') if r < .01 else c
    if t == 'canal':
        c = hexc('#3A6A7A') if (int(fx * 3) + int(fy * 5)) % 7 else hexc('#5A8A98')
        return hexc('#A8D8E0') if r < .01 else c
    if t == 'track':  return hexc('#B8604A') if r > .12 else hexc('#A85440')
    if t == 'tatami': return hexc('#B8B070') if (fy * 2) % 1 > .1 else hexc('#8A8450')
    if t == 'floor':  return hexc('#C89A64') if (fx * 2) % 1 > .08 else hexc('#9A7048')
    c = GRASS[(int(fx * 4) * 13 + int(fy * 4) * 7 + random.randint(0, 2)) % 4]
    if r < .008: c = random.choice([hexc('#F2E27A'), hexc('#F2A0C0'), hexc('#FFFFFF')])
    return c
def ground(overlay=None, edge='#6E6A62'):
    """overlay(fx, fy, t) → 색(차선·횡단보도 등) 또는 None"""
    global bg
    for x in range(NX):
        for y in range(NY): T.setdefault((x, y), 'grass')
    bg = Image.new('RGBA', (W, H), hexc('#1A1826')); px = bg.load()
    for y in range(H):
        for x in range(W):
            a, b = (x - OX) / 8, (y - OY) / 4; fx, fy = (a + b) / 2, (b - a) / 2
            if not (0 <= fx < NX and 0 <= fy < NY): continue
            t = T[(int(fx), int(fy))]
            c = overlay(fx, fy, t) if overlay else None
            px[x, y] = c or base_color(t, fx, fy)
    e1, e2 = hexc(edge), shade(hexc(edge), .86)
    for x in range(W):
        for y in range(H):
            if px[x, y][:3] != (0x1A, 0x18, 0x26): continue
            a, b = (x - OX) / 8, (y - 12 - OY) / 4; gx, gy = (a + b) / 2, (b - a) / 2
            if 0 <= gx < NX and 0 <= gy < NY and (gx > NX - 2 or gy > NY - 2): px[x, y] = e1 if (y // 3) % 2 else e2
# 자주 쓰는 길 표시
def tactile(fy, rows):
    """인도 가운데 노란 점자블록 (가로 길용)"""
    return int(fy) in rows and .38 < fy % 1 < .62
def road_x(fx, fy, y0, y1, cross=()):
    """x 방향 도로(y0~y1)의 차선. cross=[(x0,x1),...] 횡단보도"""
    band = fy - y0; wd = y1 - y0; mid = wd / 2
    for (c0, c1) in cross:
        if c0 <= fx < c1 and .4 < band < wd - .4: return hexc('#ECECE6') if (fy * 2.5) % 1 < .5 else hexc('#4E5060')
    if .15 < band < .3 or wd - .3 < band < wd - .15: return WHITE
    if mid - .08 < band < mid + .08 and (fx * .75) % 1 < .5: return WHITE
def road_y(fx, fy, x0, x1, cross=()):
    band = fx - x0; wd = x1 - x0; mid = wd / 2
    for (c0, c1) in cross:
        if c0 <= fy < c1 and .4 < band < wd - .4: return hexc('#ECECE6') if (fx * 2.5) % 1 < .5 else hexc('#4E5060')
    if .15 < band < .3 or wd - .3 < band < wd - .15: return WHITE
    if mid - .08 < band < mid + .08 and (fy * .75) % 1 < .5: return WHITE

# ---------------- 벽 무늬 ----------------
def combo(*fs):
    def f(img):
        for g in fs: g(img)
    return f
GLYPHS = [["111", "010", "111", "101"], ["101", "111", "101", "111"], ["111", "101", "111", "001"], ["010", "111", "010", "101"],
          ["111", "100", "111", "111"], ["110", "011", "110", "011"], ["011", "110", "011", "111"]]
_sign_n = [0]
def sign(bgc, fg, n=None, edge=None, vertical=False, latin=False):
    """읽을 수 없는 가짜 글자 간판 (latin=True면 알파벳처럼 얇은 글자)"""
    _sign_n[0] += 1; rnd = random.Random(_sign_n[0] * 977)
    bgc, fg = (hexc(bgc) if isinstance(bgc, str) else bgc), (hexc(fg) if isinstance(fg, str) else fg)
    pick = [rnd.choice(GLYPHS) for _ in range(16)]
    lat = [rnd.choice(["101", "111", "110", "011", "010"]) for _ in range(16)]
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return edge or shade(bgc, .6)
        if vertical: k, gx, gy = (h - 3 - v) // 5, u - (w - 3) // 2, (h - 3 - v) % 5
        else: k, gx, gy = (u - 2) // 4, (u - 2) % 4, (h - 3 - v) - (h - 6) // 2 + 0
        if latin and not vertical:
            k, gx = (u - 2) // 3, (u - 2) % 3
            if 0 <= gx < 2 and 0 <= gy < 3 and k < (n or 16) and u < w - 2 and lat[k % 16][gy] == '1': return fg
            return bgc
        if 0 <= gx < 3 and 0 <= gy < 4 and 0 <= k < (n or 16) and u >= 2 and (vertical or u < w - 2) and (not vertical or v >= 2):
            if pick[k % 16][gy][gx] == '1': return fg
        return bgc
    return f
def glass(shelf=True, door=None, tint='#BCE0F0'):
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return hexc('#5A5E6A')
        if door and door[0] <= u < door[1]:
            if u in (door[0], door[1] - 1, (door[0] + door[1]) // 2): return hexc('#6A7484')
            return hexc('#D8ECF6') if (u + v) % 9 else hexc('#FFFFFF')
        c = hexc(tint)
        if shelf and v % 6 in (1, 2): c = [hexc('#E86A6A'), hexc('#F2C85A'), hexc('#7AC87A'), hexc('#6AA0E8'), hexc('#F4F4F4')][(u // 3 + v // 6) % 5]
        if shelf and v % 6 == 3: c = shade(hexc(tint), .8)
        if (u + v) % 11 == 0 and not shelf: c = hexc('#E8F6FF')
        return c
    return f
def win(lit=False, blind=False, frame='#4A4E5A', arch=False):
    def f(u, v, w, h):
        if arch:
            top = h - w / 2
            if v > top and (u + .5 - w / 2) ** 2 + (v - top) ** 2 > (w / 2) ** 2: return None
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return hexc(frame)
        if u == w // 2: return shade(hexc(frame), 1.3)
        if blind and v % 2 == 0: return hexc('#D8E0E8')
        if lit: return hexc('#FFE0A0') if (u + v) % 7 else hexc('#FFF0C8')
        return hexc('#8AB4D8') if (u - v) % 9 else hexc('#D8ECFA')
    return f
def door(col='#5A3420', frame='#3A2418', knob='#E0C070', glassy=False):
    def f(u, v, w, h):
        if u == 0 or u == w - 1 or v == h - 1: return hexc(frame)
        if glassy: return hexc('#D8ECF6') if u != w // 2 else hexc(frame)
        if u == w // 2: return shade(hexc(col), .7)
        if v == h // 2 and u in (w // 2 - 2, w // 2 + 1): return hexc(knob)
        return hexc(col)
    return f
def stripes(c1, c2, k=3):
    c1, c2 = (hexc(c1) if isinstance(c1, str) else c1), (hexc(c2) if isinstance(c2, str) else c2)
    def f(u, v, w, h): return c1 if (u // k) % 2 == 0 else c2
    return f
def screen(seed=0, cols=('#FF5A8A', '#5AD8FF', '#FFE45A', '#8A5AFF', '#5AFF9A')):
    """빌딩 대형 전광판: 모자이크 화면"""
    rnd = random.Random(seed); cc = [hexc(c) for c in cols]
    blobs = [(rnd.randint(0, 40), rnd.randint(0, 24), rnd.randint(4, 12), rnd.choice(cc)) for _ in range(6)]
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return hexc('#22222A')
        c = hexc('#2A2A4A')
        for (bx, by, r, col) in blobs:
            if (u - bx % w) ** 2 + (v - by % h) ** 2 < r * r: c = col
        if v % 2 == 0: c = shade(c, .85)
        return c
    return f
def poster(seed=0):
    rnd = random.Random(seed)
    cols = [hexc(rnd.choice(['#F2A0C0', '#8AD0F0', '#F2E27A', '#C8A0F0', '#F08A6A'])) for _ in range(4)]
    def f(u, v, w, h):
        if u == 0 or v == 0 or u == w - 1 or v == h - 1: return hexc('#F4F4F0')
        c = cols[(u * 4) // w]
        if (h * .55 < v < h * .85) and (u * 4) % w > 1: c = hexc('#FFF0E0') if (u // 2 + v) % 3 else shade(c, .7)   # 얼굴
        return c
    return f
def clock_face(u, v, w, h):
    r = w / 2; dx, dy = u + .5 - r, v + .5 - h / 2
    dd = dx * dx + dy * dy
    if dd > r * r: return None
    if dd > (r - 1.3) ** 2: return hexc('#3A3040')
    if (abs(dx) < .7 and 0 < dy < r * .7) or (abs(dy) < .7 and 0 < dx < r * .5): return hexc('#2A2230')
    return hexc('#FFF8E8')

# ---------------- 건물 ----------------
def shop(x0, y0, x1, y1, h, wall, layers=(), roof=None, rh=0, roofc=None, brick=False, tex=6, gable=None, cornice=None):
    """앞(L)·옆(R) 면에 층(간판·유리·창문)을 쌓은 건물.
       roof=None 평지붕 / roof=색 → 기와 우진각 지붕(rh 높이)
       gable=(색, 높이, 'step'|'bell'|'tri') → 앞면 위로 솟은 박공(네덜란드 운하집)"""
    wall = hexc(wall) if isinstance(wall, str) else wall
    roof = hexc(roof) if isinstance(roof, str) else roof
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
                    cc = col(u - u0, v - v0, w_, h_) if callable(col) else (hexc(col) if isinstance(col, str) else col)
                    if cc is not None: c = cc
                if cornice and v >= h - 4: c = hexc(cornice) if v != h - 4 else shade(hexc(cornice), .7)
                elif v >= h - 2 and roof is None and not gable: c = shade(wall, .78)
                return shade(c, dark)
            return f
        face(img, x0, y0, x1, y1, 'L', fn('L', .9)); face(img, x0, y0, x1, y1, 'R', fn('R', 1.0))
        Tt, R, B, L = P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)
        if gable:
            gc, gh, kind = gable; gc = hexc(gc) if isinstance(gc, str) else gc
            # 뒤로 이어지는 맞배지붕
            rf = hexc('#5A3E3A'); ry0, ry1 = up(P(x0 + (x1 - x0) / 2, y1), h + gh - 2), up(P(x0 + (x1 - x0) / 2, y0), h + gh - 2)
            poly(d, [up(R, h), up(B, h), ry0, ry1], shade(rf, 1.1)); poly(d, [up(Tt, h), up(L, h), ry0, ry1], shade(rf, .8))
            lw = (x1 - x0) * 8; bx, by = L
            pts = []
            if kind == 'step':
                n = 3; sw = lw / (2 * n + 1)
                pts = [(0, h)]
                for i in range(n): pts += [(i * sw, h + (i + 1) * gh / (n + 1)), ((i + 1) * sw, h + (i + 1) * gh / (n + 1))]
                pts += [(n * sw, h + gh), ((n + 1) * sw, h + gh)]
                for i in range(n, 0, -1): pts += [(lw - i * sw, h + i * gh / (n + 1)), (lw - (i - 1) * sw, h + i * gh / (n + 1))]
                pts += [(lw, h)]
            elif kind == 'bell':
                for k in range(0, 21):
                    t = k / 20; u = t * lw
                    vv = h + gh * (math.sin(math.pi * t) ** .6) * (1 if .2 < t < .8 else (.75 + .25 * math.sin(math.pi * t)))
                    pts.append((u, vv))
            else: pts = [(0, h), (lw / 2, h + gh), (lw, h)]
            scr = [(bx + u, by + u * .5 - v) for (u, v) in pts]
            poly(d, scr, shade(gc, .9))
            # 박공 창(작은 창 하나) + 장식 띠
            cx, cy = bx + lw / 2, by + lw / 4 - h - gh * .45
            d.rectangle([cx - 2, cy - 4, cx + 2, cy + 3], fill=hexc('#FFE0A0') if random.random() < .5 else hexc('#8AB4D8'))
            d.line([(bx, by - h), (bx + lw, by + lw / 2 - h)], fill=hexc('#F4F0E8'))
            hook = (cx, by + lw / 4 - h - gh + 3); d.line([hook, (hook[0] + 4, hook[1])], fill=hexc('#2A2230'))
        elif roof is None:
            rc = hexc(roofc) if isinstance(roofc, str) else (roofc or hexc('#9A9AA2'))
            poly(d, [up(Tt, h), up(R, h), up(B, h), up(L, h)], shade(rc, 1.08))
            poly(d, [up(P(x0 + .3, y0 + .3), h), up(P(x1 - .3, y0 + .3), h), up(P(x1 - .3, y1 - .3), h), up(P(x0 + .3, y1 - .3), h)], rc)
        else:
            e = .35; T2, R2, B2, L2 = P(x0 - e, y0 - e), P(x1 + e, y0 - e), P(x1 + e, y1 + e), P(x0 - e, y1 + e)
            Th, Rh, Bh, Lh = up(T2, h - 2), up(R2, h - 2), up(B2, h - 2), up(L2, h - 2)
            long_x = (x1 - x0) >= (y1 - y0)
            if long_x: ry = (y0 + y1) / 2; r1, r2 = up(P(x0 + (y1 - y0) / 2, ry), h + rh), up(P(x1 - (y1 - y0) / 2, ry), h + rh)
            else: rx = (x0 + x1) / 2; r1, r2 = up(P(rx, y0 + (x1 - x0) / 2), h + rh), up(P(rx, y1 - (x1 - x0) / 2), h + rh)
            dark, mid, light = shade(roof, .72), shade(roof, .86), roof
            if long_x: poly(d, [Th, Rh, r2, r1], dark); poly(d, [Th, Lh, r1], dark); poly(d, [Rh, Bh, r2], mid); poly(d, [Lh, Bh, r2, r1], light)
            else: poly(d, [Th, Lh, r1], dark); poly(d, [Th, Rh, r2, r1], dark); poly(d, [Lh, Bh, r2, r1], mid); poly(d, [Rh, Bh, r2], light)
            a = img.load()
            for yy in range(int(min(r1[1], r2[1])), int(Bh[1]) + 1, 2):
                for xx in range(int(Lh[0]), int(Rh[0]) + 1):
                    if 0 <= xx < W and 0 <= yy < H and a[xx, yy][3] and a[xx, yy][:3] in (light[:3], mid[:3]): a[xx, yy] = shade(a[xx, yy], .88)
            d.line([tuple(map(int, r1)), tuple(map(int, r2))], fill=shade(roof, .55), width=2)
    return draw
def on_wall(x0, y1, u, v):
    bx, by = P(x0, y1); return (bx + u, by + u * .5 - v)
def on_rwall(x1, y1, u, v):
    """옆면(R) 위의 점: u는 앞(y1)에서 뒤로"""
    bx, by = P(x1, y1); return (bx + u, by - u * .5 - v)
def lantern_on(x0, y1, u, v, c='#E8463A', big=False):
    def f(img):
        d = ImageDraw.Draw(img); X, Y = on_wall(x0, y1, u, v); s = 2 if big else 1
        d.line([(X, Y - 9 * s), (X, Y - 7 * s)], fill=OUTL)
        d.ellipse([X - 3 * s, Y - 7 * s, X + 3 * s, Y + 2 * s], fill=hexc(c)); d.rectangle([X - 2 * s, Y - 7 * s, X + 2 * s, Y - 6 * s], fill=OUTL); d.rectangle([X - 2 * s, Y + 1 * s, X + 2 * s, Y + 2 * s], fill=OUTL)
        d.line([(X - s, Y - 4 * s), (X - s, Y - s)], fill=hexc('#FFB080'))
    return f
def vsign(x0, y1, u, v, h, bgc, fg):
    def f(img):
        d = ImageDraw.Draw(img); X, Y = on_wall(x0, y1, u, v)
        d.polygon([(X, Y), (X + 3, Y + 2), (X + 3, Y + 2 - h), (X, Y - h)], fill=shade(hexc(bgc), .6))
        d.polygon([(X - 9, Y + 4), (X, Y), (X, Y - h), (X - 9, Y - h + 4)], fill=hexc(bgc))
        g = sign(bgc, fg, 9, vertical=True); a = img.load()
        for k in range(h - 2):
            for j in range(7):
                c = g(j + 1, k + 1, 9, h)
                xx, yy = int(X - 8 + j), int(Y - h + 4 + (h - 3 - k) + j * -.44 + 3)
                if c == hexc(fg) and 0 <= xx < W and 0 <= yy < H: a[xx, yy] = c
    return f
def roof_sign(x0, y0, x1, y1, h, sh, bgc, fg, latin=False):
    """옥상 위에 선 간판(앞면과 나란히)"""
    def f(img):
        d = ImageDraw.Draw(img); a = img.load(); lw = int((x1 - x0) * 8) - 8
        g = sign(bgc, fg, latin=latin)
        X0, Y0 = up(P(x0 + .5, y1 - .6), h)
        for u in range(lw):
            for v in range(sh):
                c = g(u, v, lw, sh); xx, yy = int(X0 + u), int(Y0 + u * .5 - v - 3)
                if 0 <= xx < W and 0 <= yy < H: a[xx, yy] = c
        for u in (4, lw - 5):
            xx, yy = X0 + u, Y0 + u * .5; d.line([(xx, yy), (xx, yy - 4)], fill=hexc('#4A4A52'))
    return f
def box(d, x0, y0, x1, y1, h, cl, cr, ct, lift=0):
    cl, cr, ct = [hexc(c) if isinstance(c, str) else c for c in (cl, cr, ct)]
    Tt, R, B, L = [up(P(*p), lift) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    poly(d, [L, B, up(B, h), up(L, h)], cl); poly(d, [B, R, up(R, h), up(B, h)], cr); poly(d, [up(Tt, h), up(R, h), up(B, h), up(L, h)], ct)
    return Tt, R, B, L
def hip(d, x0, y0, x1, y1, base, rh, roof, e=.4):
    """처마가 나온 우진각 지붕만 (탑·탑문용)"""
    roof = hexc(roof) if isinstance(roof, str) else roof
    T2, R2, B2, L2 = [up(P(*p), base) for p in ((x0 - e, y0 - e), (x1 + e, y0 - e), (x1 + e, y1 + e), (x0 - e, y1 + e))]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if abs((x1 - x0) - (y1 - y0)) < .01: r1 = r2 = up(P(cx, cy), base + rh)
    elif (x1 - x0) > (y1 - y0): r1, r2 = up(P(x0 + (y1 - y0) / 2, cy), base + rh), up(P(x1 - (y1 - y0) / 2, cy), base + rh)
    else: r1, r2 = up(P(cx, y0 + (x1 - x0) / 2), base + rh), up(P(cx, y1 - (x1 - x0) / 2), base + rh)
    poly(d, [T2, R2, r2, r1], shade(roof, .7)); poly(d, [T2, L2, r1], shade(roof, .7)); poly(d, [R2, B2, r2], shade(roof, .86)); poly(d, [L2, B2, r2, r1], roof)
    d.line([L2, B2, R2], fill=shade(roof, .5))

# ---------------- 공용 소품 (shared) ----------------
def pole_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 2, cy - 92, cx + 2, cy], fill=hexc('#A8A8AA')); d.rectangle([cx - 2, cy - 92, cx - 1, cy], fill=hexc('#C4C4C6')); d.rectangle([cx + 2, cy - 92, cx + 2, cy], fill=hexc('#7E7E82'))
    d.rectangle([cx - 10, cy - 86, cx + 10, cy - 84], fill=hexc('#6E6E72'))
    for k in (-8, -3, 3, 8): d.rectangle([cx + k, cy - 88, cx + k, cy - 87], fill=hexc('#E8E8E8'))
    d.rectangle([cx - 9, cy - 78, cx - 3, cy - 66], fill=hexc('#9A9CA0')); d.rectangle([cx - 9, cy - 78, cx - 7, cy - 66], fill=hexc('#B4B6BA'))
    d.rectangle([cx - 2, cy - 30, cx + 2, cy - 22], fill=hexc('#E8C040')); d.rectangle([cx - 2, cy - 27, cx + 2, cy - 25], fill=hexc('#2A2A2A'))
def lamp2_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 44, cx + 1, cy], fill=hexc('#5A6070')); d.rectangle([cx - 3, cy - 3, cx + 3, cy], fill=hexc('#4A5060'))
    d.line([(cx, cy - 44), (cx + 8, cy - 47)], fill=hexc('#5A6070'), width=2)
    d.rectangle([cx + 4, cy - 48, cx + 12, cy - 45], fill=hexc('#4A5060')); d.rectangle([cx + 5, cy - 45, cx + 11, cy - 44], fill=hexc('#FFF0B8'))
def euro_lamp(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); g = hexc('#2E4A3E')
    d.rectangle([cx - 3, cy - 4, cx + 2, cy], fill=g); d.rectangle([cx - 1, cy - 34, cx, cy], fill=g)
    d.rectangle([cx - 4, cy - 42, cx + 3, cy - 34], fill=g); d.rectangle([cx - 3, cy - 41, cx + 2, cy - 35], fill=hexc('#FFE6A0'))
    d.polygon([(cx - 5, cy - 42), (cx - .5, cy - 47), (cx + 4, cy - 42)], fill=g)
def bike_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        for (wx, wy) in ((-5, 2), (5, -3)): d.ellipse([cx + wx - 4, cy + wy - 7, cx + wx + 4, cy + wy + 1], outline=hexc('#2A2A2E'))
        d.line([(cx - 5, cy - 1), (cx, cy - 6), (cx + 5, cy - 5), (cx - 1, cy - 2), (cx - 5, cy - 1)], fill=hexc(col))
        d.line([(cx, cy - 6), (cx - 1, cy - 9)], fill=hexc(col)); d.rectangle([cx - 3, cy - 10, cx, cy - 9], fill=hexc('#2A2A2E'))
        d.line([(cx + 5, cy - 5), (cx + 5, cy - 10)], fill=hexc('#A8A8AE')); d.line([(cx + 3, cy - 10), (cx + 7, cy - 11)], fill=hexc('#A8A8AE'))
        d.rectangle([cx + 5, cy - 9, cx + 9, cy - 6], fill=hexc('#B8B8BE'))
    return f
def rail_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 12, cx, cy], fill=hexc('#F0F0EC'))
    for k in (11, 6): d.line([(cx - 8, cy - 4 - k), (cx + 8, cy + 4 - k)], fill=hexc('#F4F4F0'), width=2)
def rail_y_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.rectangle([cx - 1, cy - 12, cx, cy], fill=hexc('#F0F0EC'))
    for k in (11, 6): d.line([(cx + 8, cy - 4 - k), (cx - 8, cy + 4 - k)], fill=hexc('#F4F4F0'), width=2)
def green_rail(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); g = hexc('#3E8A6A')
    d.rectangle([cx - 1, cy - 10, cx, cy], fill=g)
    d.line([(cx - 8, cy - 14), (cx + 8, cy - 6)], fill=g, width=2); d.line([(cx - 8, cy - 8), (cx + 8, cy)], fill=g)
def green_rail_y(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5); g = hexc('#3E8A6A')
    d.rectangle([cx - 1, cy - 10, cx, cy], fill=g)
    d.line([(cx + 8, cy - 14), (cx - 8, cy - 6)], fill=g, width=2); d.line([(cx + 8, cy - 8), (cx - 8, cy)], fill=g)
def cone_at(img, x, y):
    d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
    d.polygon([(cx - 5, cy), (cx, cy + 2), (cx + 5, cy), (cx, cy - 2)], fill=hexc('#C85A1E'))
    d.polygon([(cx - 3, cy), (cx, cy - 12), (cx + 3, cy)], fill=hexc('#F0782A')); d.line([(cx - 2, cy - 5), (cx + 2, cy - 5)], fill=hexc('#FFFFFF'))
def car_at(col, taxi=False):
    def f(img, x, y):
        d = ImageDraw.Draw(img); c = hexc(col)
        box(d, x + .1, y + .15, x + 1.9, y + .95, 7, shade(c, .8), c, shade(c, 1.1), lift=2)
        box(d, x + .55, y + .25, x + 1.45, y + .85, 6, hexc('#6E8AA8'), hexc('#8EAAC8'), shade(c, 1.15), lift=9)
        if taxi: box(d, x + .85, y + .45, x + 1.15, y + .65, 3, hexc('#E8E8E0'), hexc('#F4F4EC'), hexc('#FFFFFF'), lift=15)
        for (wx, wy) in ((x + .45, y + .95), (x + 1.55, y + .95), (x + 1.9, y + .5)):
            X, Y = P(wx, wy); d.ellipse([X - 3, Y - 4, X + 3, Y + 1], fill=hexc('#22222A'))
    return f
def vending(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img)
        Tt, R, B, L = box(d, x + .1, y + .2, x + .9, y + .7, 22, shade(hexc(col), .85), hexc(col), shade(hexc(col), 1.15))
        X, Y = L
        for k in range(3):
            for j in range(2):
                xx, yy = X + 2 + k * 3, Y - 18 + j * 5 + k * 1.5
                d.rectangle([xx, yy, xx + 1, yy + 2], fill=hexc(['#F2C85A', '#E86A6A', '#7AC87A', '#FFFFFF', '#6AA0E8', '#B07A4A'][(k + j * 3) % 6]))
        d.rectangle([X + 4, Y - 3, X + 8, Y], fill=hexc('#26262C'))
    return f
def planter_at(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .05, y + .25, x + .95, y + .75, 6, '#8A7A6A', '#A08E7C', '#6A5A3A')
    cx, cy = P(x + .5, y + .5)
    for dx, dy in ((-5, -8), (0, -10), (5, -8), (-2, -7), (3, -7)): d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], fill=hexc('#4E9244'))
    for dx, dy in ((-4, -10), (2, -12), (5, -9)): d.point((cx + dx, cy + dy), fill=hexc('#F2A0C0'))
def flowerbed_at(img, x, y):
    d = ImageDraw.Draw(img); box(d, x, y + .1, x + 1, y + .9, 4, '#B8AE9C', '#C8BEAC', '#5A3E28')
    cx, cy = P(x + .5, y + .5)
    for k in range(9):
        dx, dy = (k % 3 - 1) * 5 + (k // 3 - 1) * -2, (k // 3 - 1) * 2 + (k % 3 - 1) * 1 - 6
        d.point((cx + dx, cy + dy), fill=hexc(['#F2A0C0', '#F2E27A', '#FFFFFF', '#E05A5A', '#C08AFF'][k % 5])); d.point((cx + dx, cy + dy + 1), fill=hexc('#3E7A3A'))
def hedge_at(img, x, y):
    d = ImageDraw.Draw(img); box(d, x, y + .15, x + 1, y + .85, 9, '#3E7A3A', '#4E8E44', '#6AAE52')
def kiosk_at(col):
    def f(img, x, y):
        d = ImageDraw.Draw(img); c = hexc(col)
        box(d, x + .1, y + .1, x + .9, y + .9, 18, shade(c, .85), c, shade(c, 1.1))
        T2, R2, B2, L2 = box(d, x + .1, y + .1, x + .9, y + .9, 2, '#F4F0E8', '#FFFFFF', '#F4F0E8', lift=10)
        X, Y = P(x + .1, y + .9); d.rectangle([X + 2, Y - 9, X + 10, Y - 4], fill=hexc('#FFF0C8'))
        for k in range(4): d.point((X + 3 + k * 2, Y - 6 + k), fill=hexc(['#E86A6A', '#6AA0E8', '#F2C85A', '#FFFFFF'][k]))
        d.polygon([up(P(x - .05, y - .05), 18), up(P(x + 1.05, y - .05), 18), up(P(x + 1.05, y + 1.05), 18), up(P(x - .05, y + 1.05), 18)], fill=shade(c, .7))
    return f
def bench2_at(img, x, y):
    d = ImageDraw.Draw(img); box(d, x + .1, y + .35, x + .9, y + .65, 2, '#9A6A44', '#AA7A54', '#C08A5E', lift=5)
    for p_ in (P(x + .15, y + .6), P(x + .85, y + .6)): d.line([p_, up(p_, 5)], fill=hexc('#3A3A40'))
def statue_at(kind):
    """동상 받침 + 동물 (dog=충견, owl=부엉이, knight=기마상)"""
    def f(img, x, y):
        d = ImageDraw.Draw(img); box(d, x + .1, y + .1, x + .9, y + .9, 10, '#8A8478', '#A8A296', '#B8B2A6')
        cx, cy = up(P(x + .5, y + .5), 10); bz, bz2 = hexc('#7A6A4A'), hexc('#9A8A5E')
        if kind == 'dog':
            d.ellipse([cx - 6, cy - 9, cx + 4, cy - 3], fill=bz); d.ellipse([cx + 1, cy - 15, cx + 7, cy - 8], fill=bz2)
            d.polygon([(cx + 2, cy - 15), (cx + 3, cy - 18), (cx + 4, cy - 15)], fill=bz); d.rectangle([cx - 5, cy - 4, cx - 4, cy], fill=bz); d.rectangle([cx + 2, cy - 4, cx + 3, cy], fill=bz)
        elif kind == 'owl':
            d.ellipse([cx - 5, cy - 14, cx + 5, cy], fill=hexc('#8A8A90')); d.ellipse([cx - 4, cy - 12, cx - 1, cy - 9], fill=hexc('#E8E8E8')); d.ellipse([cx + 1, cy - 12, cx + 4, cy - 9], fill=hexc('#E8E8E8'))
            d.point((cx - 2, cy - 11), fill=OUTL); d.point((cx + 2, cy - 11), fill=OUTL); d.polygon([(cx - 5, cy - 14), (cx - 4, cy - 17), (cx - 2, cy - 14)], fill=hexc('#8A8A90')); d.polygon([(cx + 5, cy - 14), (cx + 4, cy - 17), (cx + 2, cy - 14)], fill=hexc('#8A8A90'))
        else:
            d.ellipse([cx - 8, cy - 12, cx + 6, cy - 4], fill=bz); d.ellipse([cx + 3, cy - 18, cx + 9, cy - 10], fill=bz2)
            for dx in (-6, -2, 2, 4): d.rectangle([cx + dx, cy - 5, cx + dx + 1, cy], fill=bz)
            d.rectangle([cx - 3, cy - 22, cx + 1, cy - 11], fill=bz2); d.ellipse([cx - 3, cy - 26, cx + 1, cy - 22], fill=bz2)
    return f
def fountain_at(img, x, y):
    d = ImageDraw.Draw(img)
    cx, cy = P(x + 1.5, y + 1.5)
    d.ellipse([cx - 22, cy - 13, cx + 22, cy + 9], fill=hexc('#A8A296')); d.ellipse([cx - 19, cy - 12, cx + 19, cy + 6], fill=hexc('#5A96CC'))
    for k in range(18): d.point((cx + random.randint(-15, 15), cy + random.randint(-9, 3)), fill=hexc('#BFE2FF'))
    d.rectangle([cx - 3, cy - 22, cx + 3, cy - 2], fill=hexc('#B8B2A6')); d.ellipse([cx - 9, cy - 26, cx + 9, cy - 19], fill=hexc('#A8A296')); d.ellipse([cx - 7, cy - 25, cx + 7, cy - 21], fill=hexc('#7AB4E0'))
    for dx in (-6, -2, 2, 6): d.line([(cx, cy - 32), (cx + dx, cy - 24)], fill=hexc('#D8F0FF'))
    d.ellipse([cx - 2, cy - 34, cx + 2, cy - 30], fill=hexc('#E8F8FF'))
def sakura_trees():
    shared('tree_round', tree_at('round')); shared('tree_big', tree_at('big')); shared('tree_pine', tree_at('pine')); shared('tree_pink', tree_at('pink'))
for k, fn in (('pole', pole_at), ('lamp2', lamp2_at), ('elamp', euro_lamp), ('rail', rail_at), ('railY', rail_y_at), ('grail', green_rail), ('grailY', green_rail_y), ('cone', cone_at),
              ('planter', planter_at), ('flower', flowerbed_at), ('hedge', hedge_at), ('bench2', bench2_at), ('fountain', fountain_at)):
    shared(k, fn)
for c in ('#D23A3A', '#F2F2EE', '#3A6EC8', '#3E9C64'): shared('bike' + c, bike_at(c))
for c in ('#F2F2EE', '#3A4A6A', '#E8C83A', '#B83A3A'): shared('car' + c, car_at(c))
shared('taxi', car_at('#2E3A5A', taxi=True)); shared('taxiY', car_at('#E8C040', taxi=True))
for c in ('#D23A3A', '#3A6EC8', '#E8E8E4'): shared('vend' + c, vending(c))
for k in ('dog', 'owl', 'knight'): shared('statue_' + k, statue_at(k))
sakura_trees()

# ---------------- 놓기 / 저장 ----------------
occupied = set()
def mark(o):
    b = o['box']
    for x in range(b[0], b[2]):
        for y in range(b[1], b[3]): occupied.add((x, y))
def bld(name, box_, draw, door=None, solid=True, act=None):
    unique(name, box_, draw, door=door, solid=solid, act=act); mark(objs[-1])
def put(name, key, x, y, w=1, d=1, **kw):
    if any((xx, yy) in occupied for xx in range(x, x + w) for yy in range(y, y + d)): return False
    if not (0 <= x < NX and 0 <= y < NY): return False
    place(name, key, x, y, w=w, d=d, **kw)
    for xx in range(x, x + w):
        for yy in range(y, y + d): occupied.add((xx, yy))
    return True
def flat_unique(name, fn):
    """테두리 없이 그리는 큰 물건(전선 등)"""
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fn(img); bb = img.getbbox()
    key = f'{name}#{len(objs)}'; SPR[key] = img.crop(bb)
    objs.append(dict(name=name, spr=key, box=[0, 0, 0, 0], x=bb[0], y=bb[1], door=None, solid=False, act=None))
def wires_between(poles, dy=-86):
    def fn(img):
        d = ImageDraw.Draw(img)
        for dx in (-8, 8):
            for i in range(len(poles) - 1):
                a, b = P(poles[i][0] + .5, poles[i][1] + .5), P(poles[i + 1][0] + .5, poles[i + 1][1] + .5)
                pts = [(a[0] + dx + (b[0] - a[0]) * t, a[1] + dy + (b[1] - a[1]) * t + 24 * t * (1 - t)) for t in [k / 80 for k in range(81)]]
                d.point([tuple(map(int, p_)) for p_ in pts], fill=hexc('#2A2630'))
    flat_unique('wires', fn)
def finish(areas, start, extra_lights=()):
    used = {o['spr'] for o in objs}
    keys = [k for k in SPR if not k.endswith('@') and k in used]
    rowW, cx_, cy_, rowH, pos = 2048, 0, 0, 0, {}
    for k in sorted(keys, key=lambda k: -SPR[k].height):
        w_, h_ = SPR[k].size
        if cx_ + w_ > rowW: cx_ = 0; cy_ += rowH + 1; rowH = 0
        pos[k] = (cx_, cy_); cx_ += w_ + 1; rowH = max(rowH, h_)
    sheet = Image.new('RGBA', (rowW, cy_ + rowH + 1), (0, 0, 0, 0))
    for k in keys: sheet.paste(SPR[k], pos[k])
    meta = [dict(name=o['name'], box=o['box'], sx=pos[o['spr']][0], sy=pos[o['spr']][1], sw=SPR[o['spr']].width, sh=SPR[o['spr']].height, x=o['x'], y=o['y'], door=o['door'], solid=o['solid'], act=o['act']) for o in objs]
    lights = []
    for o in objs:
        x, y = o['box'][:2]
        if o['spr'] in ('lamp2', 'elamp'): lights.append(dict(p=P(x + .5, y + .5), dy=-44, r=34, c=[255, 230, 160], a=.5, f=0))
        if o['door']: X, Y = P(o['door']['tile'][0] + .5, o['door']['tile'][1] - .5); lights.append(dict(p=(X, Y), dy=-14, r=30, c=[255, 200, 120], a=.4, f=0))
    lights += list(extra_lights)
    bg.save(f'out/{NAME}_bg.png'); sheet.save(f'out/{NAME}_obj.png')
    json.dump(dict(W=W, H=H, NX=NX, NY=NY, OX=OX, OY=OY, objs=meta, lights=lights, areas=areas, water=[[x, y] for (x, y), t in T.items() if t in ('water', 'canal')], ponds=[], start=start),
              open(f'out/{NAME}.json', 'w'), ensure_ascii=False)
    prev = bg.copy()
    for o in sorted(meta, key=lambda o: (o['y'] + o['sh'])):
        prev.alpha_composite(sheet.crop((o['sx'], o['sy'], o['sx'] + o['sw'], o['sy'] + o['sh'])), (o['x'], o['y']))
    from PIL import ImageChops
    diff = ImageChops.difference(prev.convert('RGB'), Image.new('RGB', prev.size, (0x1A, 0x18, 0x26)))
    bb = diff.getbbox(); prev = prev.crop((max(0, bb[0] - 8), max(0, bb[1] - 8), min(W, bb[2] + 8), min(H, bb[3] + 8)))
    prev.save(f'out/{NAME}_preview.png')
    print(NAME, 'objs', len(objs), 'sheet', sheet.size, 'map', W, H)

# ---------------- 고전 건물용 ----------------
def columns(col='#F2EEE4', gap='#8A8478', step=8, cap=True):
    """기둥 줄(신전·궁전 앞면)"""
    c1, c2 = hexc(col), hexc(gap)
    def f(u, v, w, h):
        if cap and (v >= h - 3 or v < 2): return shade(c1, .9) if v >= h - 3 else shade(c1, .8)
        k = u % step
        if k in (0, 1, step - 1): return shade(c2, .8)
        if k == 2: return shade(c1, 1.05)
        if k < step - 2: return c1
        return shade(c1, .85)
    return f
def dome(cx_t, cy_t, base, r, col='#4A8A7A', drum='#E8E0D0', lantern=True):
    """둥근 지붕(타일 좌표 중심, 높이 base)"""
    def f(img):
        d = ImageDraw.Draw(img); X, Y = up(P(cx_t, cy_t), base)
        d.rectangle([X - r + 2, Y - 10, X + r - 2, Y], fill=hexc(drum)); d.rectangle([X - r + 2, Y - 10, X, Y], fill=shade(hexc(drum), .9))
        for k in range(X - r + 4, X + r - 3, 4): d.rectangle([k, Y - 8, k + 1, Y - 3], fill=hexc('#5A6A8A'))
        d.pieslice([X - r, Y - 10 - r, X + r, Y - 10 + r], 180, 360, fill=hexc(col))
        d.pieslice([X - r, Y - 10 - r, X + r, Y - 10 + r], 180, 270, fill=shade(hexc(col), .85))
        for a in (-.5, 0, .5): d.line([(X + a * r * .9, Y - 10), (X + a * .5 * r * .3, Y - 10 - r + 2)], fill=shade(hexc(col), .75))
        if lantern:
            d.rectangle([X - 2, Y - 18 - r, X + 2, Y - 10 - r], fill=hexc(drum)); d.polygon([(X - 3, Y - 18 - r), (X, Y - 24 - r), (X + 3, Y - 18 - r)], fill=hexc(col))
            d.line([(X, Y - 24 - r), (X, Y - 28 - r)], fill=hexc('#E0C070'))
    return f
def flag_on(px_, py_, h, col1, col2='#FFFFFF'):
    def f(img):
        d = ImageDraw.Draw(img); X, Y = up(P(px_, py_), h)
        d.line([(X, Y), (X, Y - 18)], fill=hexc('#C8C8D0'))
        d.polygon([(X + 1, Y - 18), (X + 11, Y - 15), (X + 11, Y - 9), (X + 1, Y - 12)], fill=hexc(col1)); d.line([(X + 1, Y - 15), (X + 11, Y - 12)], fill=hexc(col2))
    return f
def clock_tower(cx_t, cy_t, base, s=1.2, h=26, wall='#D8D0C0', roof='#3A4048'):
    """옥상 위 시계탑: 사각 몸통 + 시계 + 뾰족 지붕"""
    def f(img):
        d = ImageDraw.Draw(img)
        box(d, cx_t - s / 2, cy_t - s / 2, cx_t + s / 2, cy_t + s / 2, h, shade(hexc(wall), .88), hexc(wall), hexc(wall), lift=base)
        X, Y = up(P(cx_t - s / 2, cy_t + s / 2), base + h - 14)
        d.ellipse([X + 2, Y - 6, X + 10, Y + 2], fill=hexc('#FFF8E8'), outline=hexc('#3A3040')); d.line([(X + 6, Y - 2), (X + 6, Y - 5)], fill=OUTL); d.line([(X + 6, Y - 2), (X + 8, Y - 1)], fill=OUTL)
        X2, Y2 = up(P(cx_t + s / 2, cy_t + s / 2), base + h - 14)
        d.ellipse([X2 + 2, Y2 - 10, X2 + 10, Y2 - 2], fill=hexc('#FFF8E8'), outline=hexc('#3A3040'))
        top = up(P(cx_t, cy_t), base + h + 22)
        Lp, Bp, Rp = up(P(cx_t - s / 2 - .1, cy_t + s / 2 + .1), base + h), up(P(cx_t + s / 2 + .1, cy_t + s / 2 + .1), base + h), up(P(cx_t + s / 2 + .1, cy_t - s / 2 - .1), base + h)
        poly(d, [Lp, Bp, top], hexc(roof)); poly(d, [Bp, Rp, top], shade(hexc(roof), 1.25))
        d.line([top, (top[0], top[1] - 6)], fill=hexc('#E0C070'))
    return f

# ---------------- 맵 연결 (tk_links.py) ----------------
exec(open('tk_links.py').read())
def _post(style):
    def f(img, x, y):
        d = ImageDraw.Draw(img); cx, cy = P(x + .5, y + .5)
        if style == 'euro':
            box(d, x + .2, y + .2, x + .8, y + .8, 26, '#C8C0B0', '#D8D0C0', '#E8E0D0'); X, Y = up(P(x + .5, y + .5), 26)
            d.rectangle([X - 3, Y - 9, X + 2, Y - 1], fill=hexc('#2E4A3E')); d.rectangle([X - 2, Y - 8, X + 1, Y - 2], fill=hexc('#FFE6A0'))
        elif style == 'wood':
            d.rectangle([cx - 1, cy - 22, cx + 1, cy], fill=hexc('#6A4A30'))
            d.polygon([(cx - 9, cy - 22), (cx + 8, cy - 18), (cx + 11, cy - 15), (cx + 8, cy - 12), (cx - 9, cy - 16)], fill=hexc('#9A6A44'))
            d.line([(cx - 6, cy - 18), (cx + 5, cy - 15)], fill=hexc('#F2E6CC'))
        else:   # 도쿄 길 안내 표지(파란 판 + 흰 화살표)
            d.rectangle([cx - 1, cy - 40, cx + 1, cy], fill=hexc('#B8B8BC'))
            d.polygon([(cx - 10, cy - 46), (cx + 10, cy - 40), (cx + 10, cy - 30), (cx - 10, cy - 36)], fill=hexc('#2E62C8'))
            d.line([(cx - 6, cy - 39), (cx + 5, cy - 35)], fill=hexc('#FFFFFF')); d.line([(cx + 5, cy - 35), (cx + 2, cy - 38)], fill=hexc('#FFFFFF')); d.line([(cx + 5, cy - 35), (cx + 1, cy - 34)], fill=hexc('#FFFFFF'))
    return f
def edge_exits(style='tokyo'):
    """tk_links.py의 출구를 달고, 역(tk_station)·트램 문을 열차로 바꿔요"""
    if 'post_' + style not in SPR: shared('post_' + style, _post(style))
    for (to, side, a0, a1) in EDGES.get(NAME, []):
        lab = LABELS[to] + ' 방면'
        if side in ('W', 'E'):
            fx = 0 if side == 'W' else NX - 1
            for yy in (a0 - 1, a1 + 1):
                if 0 <= yy < NY and (fx, yy) not in occupied: place('gate', 'post_' + style, fx, yy); occupied.add((fx, yy))
            door_ = dict(tile=[fx, (a0 + a1) // 2], to=to, spawn=edge_spawn(NAME, to), label=lab, walk=True, span=[a0, a1])
        else:
            fy = 0 if side == 'N' else NY - 1
            for xx in (a0 - 1, a1 + 1):
                if 0 <= xx < NX and (xx, fy) not in occupied: place('gate', 'post_' + style, xx, fy); occupied.add((xx, fy))
            door_ = dict(tile=[(a0 + a1) // 2, fy], to=to, spawn=edge_spawn(NAME, to), label=lab, walk=True, spanX=[a0, a1])
        objs.append(dict(name='exit', spr=objs[-1]['spr'], box=[0, 0, 0, 0], x=-9999, y=-9999, door=door_, solid=False, act=None))
        for t in range(a0, a1 + 1): occupied.discard((door_['tile'][0], t) if side in ('W', 'E') else (t, door_['tile'][1]))
    if NAME in TRAINS:
        lab, to, sp = TRAINS[NAME]
        for o in objs:
            if o['door'] and o['door'].get('to') in ('tk_station',) or (o['name'] in ('tram', 'station') and NAME in ('acca_badon', 'tk_inaka')):
                b = o['box']
                o['door'] = dict(tile=o['door']['tile'] if o['door'] else [(b[0] + b[2]) // 2, b[3]], to=to, spawn=sp, label=lab, train=True)
                break
