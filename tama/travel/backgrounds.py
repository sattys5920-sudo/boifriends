import sys, json, math, random
import numpy as np
from PIL import Image, ImageDraw
OUT = sys.argv[1]; W, H = 400, 150; GY = 118
INK = np.array([42, 32, 46])
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float)
class Scene:
    def __init__(s, sky, horizon, grass, path, seed):
        s.img = np.zeros((H, W, 3), float); s.r = random.Random(seed)
        a, b = hx(sky), hx(horizon)
        for y in range(GY):
            t = y / GY; c = a + (b - a) * t
            s.img[y] = c
            if (y % 6 == 5): s.img[y, ::2] = a + (b - a) * min(1, t + .04)   # 디더링 띠
        g, p = hx(grass), hx(path)
        s.img[GY:] = g
        for y in range(GY, H):
            for x in range(0, W, 3):
                if s.r.random() < .18: s.img[y, x] = g * .86
        s.img[GY + 12:GY + 24] = p
        for x in range(0, W, 10):
            for y in range(GY + 13, GY + 23, 5):
                xx = x + (y // 5 % 2) * 5; s.img[y, xx:xx + 8] = p * .9; s.img[y, xx] = p * .72
        s.img[GY + 12] = p * .7; s.img[GY + 24] = g * .75
        s.img[GY] = g * .72
        for _ in range(40):   # 풀 덤불
            x = s.r.randrange(0, W); s.img[GY - 1, x] = g * .8; s.img[GY - 2, x] = g * 1.05
    def clouds(s, n=5):
        for _ in range(n):
            cx, cy, w = s.r.randrange(0, W), s.r.randrange(8, 50), s.r.randrange(18, 34)
            m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
            d.ellipse([cx, cy, cx + w, cy + 9], fill=255); d.ellipse([cx + w // 4, cy - 6, cx + w * 3 // 4, cy + 7], fill=255)
            M = np.array(m) > 0; s.img[M] = [255, 255, 255]
            sh = M & ~np.roll(M, -2, 0); s.img[np.roll(sh, 0, 0) & M & (np.arange(H)[:, None] > cy + 5)] = [222, 232, 245]
    def obj(s, shapes, col, light=True, stripes=0, outline=True, windows=None, split=None):
        """shapes: [('poly', pts) | ('rect', box) | ('ell', box)] → 같은 색 덩어리 하나. 왼쪽 밝게/오른쪽 어둡게, 테두리, 줄무늬"""
        m = Image.new('L', (W, H)); d = ImageDraw.Draw(m)
        for kind, a in shapes:
            if kind == 'poly': d.polygon(a, fill=255)
            elif kind == 'rect': d.rectangle(a, fill=255)
            else: d.ellipse(a, fill=255)
        M = np.array(m) > 0
        if not M.any(): return M
        ys, xs = np.where(M); c = hx(col); cx = split if split is not None else (xs.min() + xs.max()) / 2
        X = np.arange(W)[None, :].repeat(H, 0)
        img = np.where((X < cx)[..., None], c * 1.06, c * .80) if light else np.broadcast_to(c, (H, W, 3))
        if stripes:
            Y = np.arange(H)[:, None].repeat(W, 1); st = (Y % stripes == 0)
            img = np.where(st[..., None], img * .86, img)
        top = M & ~np.roll(M, 1, 0)
        img = np.where(top[..., None], np.minimum(255, c * 1.25), img)
        s.img[M] = np.clip(img[M], 0, 255)
        if windows:
            wc, step, ww, wh = windows
            for y in range(ys.min() + 4, ys.max() - 4, step):
                for x in range(xs.min() + 3, xs.max() - 3, step):
                    if M[y:y + wh, x:x + ww].all(): s.img[y:y + wh, x:x + ww] = hx(wc) * (1 if x < cx else .82); s.img[y + wh - 1, x:x + ww] = hx(wc) * .7
        if outline:
            e = M & ~(np.roll(M, 1, 0) & np.roll(M, -1, 0) & np.roll(M, 1, 1) & np.roll(M, -1, 1)); s.img[e] = INK
        return M
    def tree(s, x, col='#5fa34d', h=22):
        s.obj([('rect', (x - 1, GY - 9, x + 1, GY))], '#7a4f2e')
        s.obj([('ell', (x - 8, GY - h, x + 8, GY - 6)), ('ell', (x - 5, GY - h - 5, x + 5, GY - h + 6))], col)
    def pine(s, x, h=30, col='#2f6b4f'):
        s.obj([('poly', [(x - 9, GY), (x, GY - h), (x + 9, GY)])], col, stripes=4)
    def palm(s, x):
        d = [('poly', [(x, GY), (x + 3, GY), (x + 6, GY - 30), (x + 3, GY - 30)])]; s.obj(d, '#9a6a3c', stripes=3)
        for dx, dy in [(-14, 6), (14, 6), (-11, -2), (11, -2), (0, -6)]:
            s.obj([('poly', [(x + 4, GY - 32), (x + 4 + dx, GY - 30 + dy), (x + 4 + dx * .6, GY - 33 + dy)])], '#3fa34d', light=False)
    def far(s, pts, col):   # 먼 산·언덕(테두리 없이 흐리게)
        s.obj([('poly', pts)], col, outline=False)
    def save(s, k): Image.fromarray(np.clip(s.img, 0, 255).astype(np.uint8)).save(f'{OUT}/{k}.png')
C = []
def country(k, n, price):
    def deco(fn): C.append((k, n, price, fn)); return fn
    return deco
@country('japan', '일본', 500)
def _():
    s = Scene('#a9d8f5', '#ffe3ee', '#9fd67a', '#d9c3a0', 1); s.clouds()
    s.far([(120, GY), (200, 30), (280, GY)], '#7f9fc7'); s.obj([('poly', [(178, 52), (200, 30), (222, 52), (212, 56), (200, 50), (188, 56)])], '#ffffff')
    for x0 in (40,):
        s.obj([('rect', (x0, 58, x0 + 70, 63))], '#d8483f'); s.obj([('rect', (x0 - 4, 52, x0 + 74, 57))], '#3a3238')
        s.obj([('rect', (x0 + 8, 68, x0 + 62, 71))], '#d8483f'); s.obj([('rect', (x0 + 10, 57, x0 + 16, GY)), ('rect', (x0 + 54, 57, x0 + 60, GY))], '#d8483f')
    s.obj([('rect', (300, 70, 360, GY))], '#f1e4c6', windows=('#7a4f2e', 10, 6, 8)); s.obj([('poly', [(292, 72), (330, 50), (368, 72)])], '#3d4a52', stripes=3)
    for x in (250, 380): s.tree(x, '#ffb3cc')
    s.save('japan')
@country('china', '중국', 600)
def _():
    s = Scene('#cfeaff', '#fff3c4', '#8fcf6a', '#d9c3a0', 2); s.clouds()
    s.far([(0, 80), (80, 46), (170, 70), (260, 40), (340, 66), (400, 55), (400, GY), (0, GY)], '#5fa34d')
    pts = [(0, 74), (80, 40), (170, 64), (260, 34), (340, 60), (400, 49)]
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        poly = [(x0, y0), (x1, y1), (x1, y1 + 8), (x0, y0 + 8)]; s.obj([('poly', poly)], '#c9a777', stripes=3, split=9999)
        for x in range(x0, x1, 7):
            y = int(y0 + (y1 - y0) * (x - x0) / (x1 - x0)); s.obj([('rect', (x, y - 4, x + 3, y))], '#b8956a', light=False)
    s.obj([('rect', (250, 18, 272, 36))], '#c9a777', windows=('#5a3a2a', 8, 4, 6)); s.obj([('poly', [(244, 20), (261, 8), (278, 20)])], '#b8403a', stripes=3)
    s.save('china')
@country('usa', '미국', 900)
def _():
    s = Scene('#8ccff5', '#e3f3ff', '#8fcf6a', '#9aa5b1', 3); s.clouds(4)
    for x, h, c in [(190, 50, '#6b7a8c'), (212, 78, '#56657a'), (236, 44, '#7a8798'), (256, 92, '#4a5870'), (282, 62, '#6b7a8c'), (306, 80, '#56657a'), (332, 52, '#7a8798'), (356, 70, '#4a5870')]:
        s.obj([('rect', (x, GY - h, x + 20, GY))], c, windows=('#ffe08a', 6, 3, 3))
    s.obj([('rect', (66, 92, 104, GY))], '#9a8a70', stripes=3)
    s.obj([('poly', [(74, 92), (78, 56), (92, 56), (96, 92)])], '#7fc7a8', stripes=4); s.obj([('ell', (77, 40, 93, 58))], '#7fc7a8')
    s.obj([('poly', [(76, 42), (79, 32), (82, 40), (85, 30), (88, 40), (91, 32), (94, 42)])], '#7fc7a8')
    s.obj([('poly', [(92, 52), (94, 50), (104, 24), (102, 22)])], '#7fc7a8'); s.obj([('ell', (99, 14, 108, 24))], '#ffd76a')
    s.save('usa')
@country('france', '프랑스', 900)
def _():
    s = Scene('#c4e3fb', '#ffd9c2', '#8fcf6a', '#d9c3a0', 4); s.clouds()
    s.obj([('poly', [(160, GY), (186, 70), (214, 70), (240, GY), (222, GY), (200, 92), (178, GY)])], '#8a6a4f', stripes=3)
    s.obj([('poly', [(186, 70), (193, 34), (207, 34), (214, 70)])], '#8a6a4f', stripes=3); s.obj([('poly', [(193, 34), (199, 10), (201, 10), (207, 34)])], '#8a6a4f')
    s.obj([('rect', (180, 80, 220, 85))], '#7a5a3f'); s.obj([('rect', (187, 58, 213, 62))], '#7a5a3f')
    for x in (300, 340): s.obj([('rect', (x, 76, x + 34, GY))], '#f1e4c6', windows=('#6b7fa8', 8, 4, 7)); s.obj([('poly', [(x - 3, 78), (x + 17, 64), (x + 37, 78)])], '#5b6672', stripes=3)
    for x in (40, 80, 120): s.tree(x)
    s.save('france')
@country('uk', '영국', 900)
def _():
    s = Scene('#b9cfe0', '#e8eef3', '#7fb35a', '#9aa5b1', 5); s.clouds(6)
    s.obj([('rect', (190, 40, 214, GY))], '#c9a46a', stripes=4); s.obj([('poly', [(186, 40), (202, 10), (218, 40)])], '#4a5560', stripes=3)
    s.obj([('ell', (194, 44, 210, 60))], '#fbf3df'); s.obj([('rect', (201, 47, 202, 52))], '#2a202e', light=False, outline=False)
    s.obj([('rect', (40, 78, 120, 108)), ('rect', (40, 64, 120, 78))], '#d63a34', windows=('#cfe6ff', 10, 7, 6))
    s.obj([('ell', (48, 104, 62, 118)), ('ell', (98, 104, 112, 118))], '#2a2a30')
    for x in (300, 340, 380): s.tree(x, '#4f8f3f')
    s.save('uk')
@country('italy', '이탈리아', 850)
def _():
    s = Scene('#a9d8f5', '#fff3c4', '#9fd67a', '#d9c3a0', 6); s.clouds()
    for i in range(8):
        y = GY - 9 * i; x = 220 + i * 2.2; s.obj([('rect', (x, y - 10, x + 26, y))], '#f4ecdc', stripes=0, windows=('#c9b89a', 5, 2, 5))
    s.obj([('rect', (40, 70, 140, GY))], '#e3cba8', stripes=5)
    for x in range(46, 136, 12): s.obj([('poly', [(x, GY), (x, 82), (x + 4, 76), (x + 8, 82), (x + 8, GY)])], '#b88a5a', light=False)
    for x in (320, 360): s.pine(x, 34, '#3f7a4f')
    s.save('italy')
@country('egypt', '이집트', 800)
def _():
    s = Scene('#ffc2a6', '#ffe9a3', '#e3cba8', '#c99a6a', 7)
    s.obj([('ell', (320, 16, 350, 46))], '#ff9a4d', light=False, outline=False)
    for x0, sz in [(90, 60), (190, 80), (300, 46)]:
        s.obj([('poly', [(x0 - sz, GY), (x0, GY - sz), (x0 + sz, GY)])], '#e2b33c', stripes=4, split=x0)
    s.palm(370); s.palm(20)
    s.save('egypt')
@country('korea', '한국', 500)
def _():
    s = Scene('#c4e3fb', '#ece6ff', '#8fcf6a', '#d9c3a0', 8); s.clouds()
    s.obj([('ell', (120, 56, 300, 190))], '#5fa34d', outline=False)
    s.obj([('rect', (205, 22, 213, 64))], '#f4f4f4', stripes=6); s.obj([('rect', (196, 28, 222, 36))], '#ff8fb3'); s.obj([('rect', (208, 6, 210, 22))], '#9aa5b1', light=False)
    s.obj([('rect', (40, 82, 120, GY))], '#f4ecdc', windows=('#8a5a3c', 10, 6, 10)); s.obj([('poly', [(30, 84), (80, 68), (130, 84)])], '#3a4a5a', stripes=3)
    for x in (330, 370): s.tree(x, '#ffb3cc')
    s.save('korea')
@country('australia', '호주', 1000)
def _():
    s = Scene('#8ccff5', '#d9efff', '#e3cba8', '#d9c3a0', 9); s.clouds(4)
    s.img[GY - 8:GY] = hx('#3f8fd8'); s.img[GY - 8:GY:3, ::4] = hx('#8ccff5')
    s.obj([('rect', (150, GY - 14, 270, GY - 8))], '#e3cba8')
    for x0, h in [(155, 44), (180, 56), (210, 42), (236, 34)]: s.obj([('poly', [(x0, GY - 14), (x0 + 20, GY - 14 - h), (x0 + 34, GY - 14)])], '#f7f7f2', stripes=3, split=x0 + 22)
    m = Image.new('L', (W, H)); ImageDraw.Draw(m).arc([290, 50, 410, 170], 180, 360, fill=255, width=4); M = np.array(m) > 0; s.img[M] = hx('#5b6672')
    for x in (30, 70): s.palm(x)
    s.save('australia')
@country('brazil', '브라질', 1000)
def _():
    s = Scene('#8fe3cc', '#fff3c4', '#ffe08a', '#e3cba8', 10); s.clouds(4)
    s.obj([('poly', [(100, GY), (150, 40), (190, 52), (210, GY)])], '#3f8f4f', stripes=5); s.obj([('poly', [(210, GY), (250, 58), (290, GY)])], '#3f8f4f', stripes=5)
    s.obj([('rect', (147, 22, 152, 42)), ('rect', (138, 26, 161, 30))], '#f4f4f4')
    s.img[GY + 4:GY + 10] = hx('#3fb5b0')
    for x in (30, 340, 380): s.palm(x)
    s.save('brazil')
@country('india', '인도', 800)
def _():
    s = Scene('#ffe0cc', '#ffc2e0', '#8fcf6a', '#d9c3a0', 11); s.clouds(3)
    s.obj([('rect', (140, 70, 260, GY))], '#f7f4ee', windows=('#d9d0e8', 14, 8, 14)); s.obj([('ell', (175, 34, 225, 80))], '#f7f4ee'); s.obj([('rect', (199, 22, 201, 34))], '#c9a777', light=False)
    for x in (128, 266): s.obj([('rect', (x, 34, x + 6, GY))], '#f7f4ee', stripes=6); s.obj([('ell', (x - 2, 28, x + 8, 38))], '#f7f4ee')
    s.obj([('poly', [(190, GY), (190, 92), (200, 82), (210, 92), (210, GY)])], '#c9d4e6')
    s.img[GY + 2:GY + 8, 150:250] = hx('#8ccff5')
    s.save('india')
@country('russia', '러시아', 850)
def _():
    s = Scene('#cfe6f7', '#ffffff', '#eef3f7', '#c9d4de', 12); s.clouds(4)
    for x, c, h in [(150, '#d8483f', 44), (185, '#4f8fe0', 62), (220, '#4fae6a', 52), (255, '#f0c040', 40)]:
        s.obj([('rect', (x - 9, GY - h, x + 9, GY))], '#f4ecdc', windows=('#8a5a3c', 6, 3, 6))
        s.obj([('ell', (x - 13, GY - h - 20, x + 13, GY - h + 2)), ('poly', [(x - 4, GY - h - 18), (x, GY - h - 30), (x + 4, GY - h - 18)])], c, stripes=3)
    for x in (40, 70, 340, 375): s.pine(x, 30, '#2c6b4f')
    s.save('russia')
@country('netherlands', '네덜란드', 750)
def _():
    s = Scene('#a9d8f5', '#e3f3ff', '#8fcf6a', '#8ccff5', 13); s.clouds(5)
    s.obj([('poly', [(180, GY), (188, 58), (212, 58), (220, GY)])], '#8a5a3c', stripes=4, windows=('#3a2a20', 12, 4, 6))
    s.obj([('poly', [(184, 58), (200, 44), (216, 58)])], '#5e3b28', stripes=3)
    for a in (20, 110, 200, 290):
        x = 200 + 36 * math.cos(math.radians(a)); y = 54 + 36 * math.sin(math.radians(a))
        px, py = -math.sin(math.radians(a)) * 4, math.cos(math.radians(a)) * 4
        s.obj([('poly', [(200, 54), (x, y), (x + px, y + py), (200 + px, 54 + py)])], '#f4ecdc', light=False)
    for x in range(8, W, 6):
        if not 160 < x < 240:
            c = ['#e5534b', '#ffe06b', '#ff8fb3', '#c6b5ff'][(x // 6) % 4]; s.img[GY - 6:GY, x] = hx('#3f8f4f'); s.img[GY - 10:GY - 6, x - 1:x + 2] = hx(c)
    s.save('netherlands')
@country('greece', '그리스', 750)
def _():
    s = Scene('#8ccff5', '#e3f3ff', '#f4f4f4', '#d9c3a0', 14); s.clouds(4)
    s.img[84:GY] = hx('#3f7fd8'); s.img[86:GY:4, ::5] = hx('#8ccff5')
    for x, w, h in [(110, 36, 30), (150, 30, 42), (184, 44, 26), (232, 32, 36), (270, 40, 24)]:
        s.obj([('rect', (x, GY - h, x + w, GY))], '#fbfbfb', windows=('#3f7fd8', 12, 5, 7))
    s.obj([('ell', (154, GY - 60, 176, GY - 38))], '#3f7fd8', stripes=3); s.obj([('rect', (164, GY - 66, 166, GY - 60))], '#2a202e', light=False)
    s.save('greece')
@country('spain', '스페인', 800)
def _():
    s = Scene('#ffe08a', '#ffc2a6', '#e3cba8', '#c99a6a', 15)
    for x, h in [(160, 56), (178, 72), (196, 80), (214, 72), (232, 56)]:
        s.obj([('rect', (x - 6, GY - h, x + 6, GY))], '#c99a6a', windows=('#6b4a2e', 6, 2, 3)); s.obj([('poly', [(x - 6, GY - h), (x, GY - h - 18), (x + 6, GY - h)])], '#a8784a', stripes=3)
    for x in (50, 90, 330, 370): s.tree(x, '#8f9a4f')
    s.save('spain')
@country('canada', '캐나다', 900)
def _():
    s = Scene('#a9d8f5', '#e6f9f2', '#5fa34d', '#d9c3a0', 16); s.clouds(4)
    s.obj([('poly', [(60, GY), (150, 28), (240, GY)])], '#7f9fc7', stripes=0, split=150); s.obj([('poly', [(128, 48), (150, 28), (172, 48), (160, 52), (150, 46), (140, 52)])], '#ffffff')
    s.obj([('poly', [(200, GY), (290, 40), (380, GY)])], '#6a8ab5', split=290); s.obj([('poly', [(272, 58), (290, 40), (308, 58), (298, 62), (290, 56), (282, 62)])], '#ffffff')
    for x in (20, 46, 330, 360, 388): s.pine(x, 34)
    s.obj([('poly', [(196, 92), (200, 82), (204, 88), (208, 78), (212, 88), (216, 82), (220, 92), (208, 98)])], '#d8483f')
    s.save('canada')
@country('mexico', '멕시코', 700)
def _():
    s = Scene('#ffc2a6', '#fff3c4', '#e3cba8', '#c99a6a', 17)
    for i in range(6): s.obj([('rect', (140 + i * 10, 52 + i * 11, 260 - i * 10, GY))], '#c9a777', stripes=3, split=200)
    s.obj([('rect', (188, 40, 212, 52))], '#a8784a', windows=('#4a3020', 8, 4, 6))
    for x in (60, 330, 370):
        s.obj([('rect', (x - 4, GY - 36, x + 4, GY)), ('rect', (x - 14, GY - 26, x - 4, GY - 21)), ('rect', (x - 14, GY - 34, x - 9, GY - 21)), ('rect', (x + 4, GY - 20, x + 13, GY - 15)), ('rect', (x + 8, GY - 30, x + 13, GY - 15))], '#3f9a4f', stripes=0)
    s.save('mexico')
@country('thailand', '태국', 600)
def _():
    s = Scene('#8fe3cc', '#ffe08a', '#8fcf6a', '#d9c3a0', 18); s.clouds(3)
    for i, w in enumerate([76, 58, 42, 26]): s.obj([('rect', (200 - w // 2, GY - 16 - i * 14, 200 + w // 2, GY - i * 14))], '#e2b33c', stripes=3, split=200)
    s.obj([('poly', [(190, 62), (200, 16), (210, 62)])], '#e2b33c', stripes=4, split=200)
    for x in (60, 110, 300, 350): s.palm(x)
    s.save('thailand')
@country('turkey', '튀르키예', 750)
def _():
    s = Scene('#ffc2a6', '#cfeaff', '#e3cba8', '#c99a6a', 19)
    for x, h in [(130, 40), (166, 56), (204, 36), (240, 48), (276, 32)]: s.obj([('poly', [(x - 16, GY), (x - 4, GY - h), (x + 4, GY - h), (x + 16, GY)])], '#e0b88a', stripes=4)
    for x, y, c in [(60, 36, '#d8483f'), (180, 20, '#f0c040'), (300, 42, '#4f8fe0'), (360, 24, '#ff8fb3')]:
        s.obj([('ell', (x - 11, y - 13, x + 11, y + 12))], c, stripes=4)
        s.obj([('rect', (x - 4, y + 18, x + 4, y + 23))], '#8a5a3c'); s.img[y + 11:y + 18, x - 5] = INK; s.img[y + 11:y + 18, x + 5] = INK
    s.save('turkey')
@country('switzerland', '스위스', 950)
def _():
    s = Scene('#a9d8f5', '#ffffff', '#8fcf6a', '#d9c3a0', 20); s.clouds(4)
    for x0, h in [(50, 56), (150, 84), (250, 70), (350, 56)]:
        s.obj([('poly', [(x0 - 70, GY), (x0, GY - h), (x0 + 70, GY)])], '#8f9aa8', split=x0)
        s.obj([('poly', [(x0 - 18, GY - h + 20), (x0, GY - h), (x0 + 18, GY - h + 20), (x0 + 8, GY - h + 24), (x0, GY - h + 18), (x0 - 8, GY - h + 24)])], '#ffffff', split=x0)
    s.obj([('rect', (190, 86, 230, GY))], '#c99a6a', stripes=3, windows=('#fbf3df', 12, 6, 6)); s.obj([('poly', [(182, 88), (210, 70), (238, 88)])], '#7a4f2e', stripes=3)
    s.obj([('rect', (40, 90, 54, 104))], '#d8483f'); s.img[95:100, 46:48] = 255; s.img[96:98, 43:51] = 255
    s.save('switzerland')
for k, n, p, fn in C: fn()
json.dump([dict(k=k, n=n, p=p) for k, n, p, _ in C], open(f'{OUT}/countries.json', 'w'), ensure_ascii=False)
sheet = Image.new('RGB', (W * 4 + 30, (H + 6) * 5))
for i, (k, *_) in enumerate(C): sheet.paste(Image.open(f'{OUT}/{k}.png'), ((i % 4) * (W + 10), (i // 4) * (H + 6)))
sheet.save(f'{OUT}/_sheet.png'); print(len(C))
