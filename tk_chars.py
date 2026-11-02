# 사용자가 만든 캐릭터 시트(chars_src/*.png, 체크무늬·흰 배경이 그림에 박혀 있음)를 걷기 맵용으로 정리해요
#   1) 배경 지우기: 밝고 채도 낮은 넓은 영역(체크무늬·흰 바탕·옅은 얼룩)을 지우고, 격자선처럼 화면을 가로지르는 선도 버려요
#   2) 캐릭터 덩어리를 찾아 줄(y)·칸(x)으로 정렬
#   3) 방향 판단: 머리 부분의 피부 위치로 앞/왼쪽/오른쪽, 피부가 거의 없으면 뒤 (로봇은 줄 순서로)
#   4) 같은 비율로 줄여서 32x44 칸에 발을 맞춰 넣기 → out/tk_chars.png + out/tk_chars.json
#   python3 tk_chars.py  (그다음 tk_world_build.py)
import json, os
import numpy as np
from PIL import Image
from scipy import ndimage
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FW, FH, TARGET = 32, 44, 40          # 칸 크기, 캐릭터 키(px) — 게임 안 논리 크기
R = 3                                # 시트는 R배 해상도로 저장해요 (화면에서 부드럽게 줄여 그림)
DIRS = ['down', 'up', 'left', 'right']
# 옆모습은 시트마다 섞여 있어서 눈으로 보고 골랐어요: (줄, 칸). right가 None이면 왼쪽을 뒤집어 써요
SIDE = {
    'blue':           dict(left=[(2, 1), (2, 2), (2, 3), (3, 2)], right=None),
    'curly_suit':     dict(left=[(2, 1), (2, 2)], right=[(3, 0), (3, 1), (3, 2), (3, 3)]),
    'blonde_student': dict(left=[(3, 0), (3, 1), (3, 2), (3, 3)], right=None),
    'mole':           dict(left=[(3, 0), (3, 1), (3, 2), (3, 3)], right=None),
    'punk':           dict(left=[(2, 3), (2, 4), (2, 5), (3, 3)], right=None),
    'bartender':      dict(left=[(2, 0), (2, 1), (2, 2), (3, 1)], right=[(2, 3), (2, 4), (3, 3), (3, 4)]),
    'curly_coat':     dict(left=[(2, 0), (2, 1), (2, 2), (2, 3)], right=None),
    'baseball':       dict(left=[(3, 0), (3, 1), (3, 2), (2, 0)], right=[(2, 1), (2, 2), (2, 3), (2, 4)], trim_front=True, clean_front=True),
    'ume':            dict(left='mirror', right=[(2, 1), (2, 3), (2, 4), (2, 5)], down=[0, 1, 2, 3], up=[0, 1, 2, 3]),
    'kaguya':         dict(left='mirror', right=[(2, 1), (2, 3), (2, 4), (2, 5)], down=[0, 1, 2, 3], up=[0, 1, 2, 3]),
    'ahoge':          dict(left='mirror', right=[(2, 2), (2, 3), (2, 4), (3, 2)], down=[0, 1, 2], up=[0, 1, 2]),
    'blindfold':      dict(left=[(3, 1), (3, 2), (3, 3), (3, 4)], right=[(2, 0), (2, 2), (2, 3), (2, 4)], down=[0, 1, 2, 3], up=[0, 1, 2, 3]),
    'headphone':      dict(left='mirror', right=[(2, 1), (2, 2), (2, 3), (2, 4)]),
    'nifuji':         dict(left=[(3, 0), (3, 1)], right=[(2, 1), (2, 2)]),
    'gintoki':        dict(left=[(2, 1), (2, 2), (2, 3), (2, 4)], right='mirror', fill_inside=True, phase=False, nofill=True),
    'usui':           dict(left='mirror', right=[(2, 1), (2, 2), (2, 3), (2, 4)], up=[0, 1, 2, 4], down=[1, 2, 3, 4]),
    'izumi':          dict(left='mirror', right=[(2, 1), (2, 2), (3, 2), (3, 3)], fill_inside=True, phase=False, nofill=True),
    'ponytail':       dict(left=[(3, 0), (3, 1), (3, 2), (3, 3)], right=[(2, 1), (2, 2), (2, 3), (2, 4)]),
    'spiky':          dict(left=[(3, 0), (3, 1), (3, 2), (3, 3)], right=[(2, 1), (2, 2), (2, 3), (2, 4)], fill_frame=3),
    'kyon':           dict(left=[(3, 0), (3, 1), (3, 2), (3, 3)], right=[(2, 1), (2, 2), (2, 3), (2, 4)]),
    'chiro':          dict(left=[(2, 0), (2, 1), (3, 1), (3, 2)], right=[(2, 2), (2, 3), (2, 4), (3, 3)]),
    'saiki':          dict(left=[(2, 1), (2, 2), (2, 3), (2, 4)], right=None),
    'nozaki':         dict(left=[(3, 0), (3, 1), (3, 2)], right=[(2, 0), (2, 1), (2, 3), (2, 4)]),
    'shima':          dict(left=[(3, 1), (3, 2), (3, 3), (3, 4)], right=[(2, 1), (2, 2), (2, 3), (2, 4)]),
    'mint':           dict(left=[(2, 1), (2, 2), (2, 3), (2, 4)], right=None, outline=True),
    'karate':         dict(left=[(2, 1), (2, 2), (3, 1), (3, 2)], right=[(2, 4), (3, 3), (3, 4)], fill_inside=True),
}
PHASE_ALL = True
SHEETS = [  # id, 파일, 이름, 맵, 칸, 대사, 줄 순서 강제(로봇)
    ('blue', 'blue.png', '니노', 'acca_dowa', [16, 16], ['…운하 바람이 좋네.', '바동은 처음이야? 저 하얀 건물이 ACCA 본부야.', '도와 쪽으로 가려면 트램 길을 따라 동쪽 끝까지 가 봐.', '정류장 옆 가판대에서 담배 한 개비 사 오면 더 얘기해 줄게.'], None),
    ('curly_suit', 'curly_suit.png', '쿠지 치카이', 'tk_asakusa', [32, 17], ['강 보러 왔어? 여기 앉아서 멍하니 있기 좋지.', '나는 그냥… 일 쉬는 중이야. 비밀로 해 줘.', '참배길 노점 당고는 꼭 먹어 봐. 세 번째 가게가 제일이야.'], None),
    ('blonde_student', 'blonde_student.png', '후타미 슌', 'tk_school', [18, 10], ['……스읍.', '아, 책상 위에 뭐가 있었는데 누가 잘못 둔 것 같아서 옆으로 치워 뒀어.', '…수업 종 울리기 전에 들어가.'], None),
    ('mole', 'mole.png', '타나카 요이치', 'tk_school', [28, 9], ['어, 안녕! 여기 크레페 진짜 맛있어.', '다케시타 거리는 주말엔 사람이 너무 많아서 평일에 오는 게 좋아.', '북쪽 숲길 도리이 지나면 이케부쿠로로 가는 길이 나와.'], None),
    ('punk', 'punk.png', '혼죠 렌', 'tk_shibuya', [8, 27], ['…뭐야, 구경 왔어?', '오늘 밤에 이 근처 지하 라이브하우스에서 공연 있어. 기타는 내가 쳐.', '표는 없어. 그냥 와. 문 앞에서 내 이름 대면 돼.'], None),
    ('bartender', 'bartender.png', '헤이와지마 시즈오', 'tk_ikebukuro', [18, 22], ['…이 동네에서 소란 피우지 마라. 피곤하니까.', '자판기? …아니, 던질 생각 없어. 마실 거야.', '동쪽으로 가면 아사쿠사. 서쪽 길은 하라주쿠야.'], None),
    ('curly_coat', 'curly_coat.png', '쿠노우 토토노우', 'tk_roppongi', [8, 11], ['미술관에 들렀다 가는 길이에요.', '그림을 보면, 그린 사람이 무엇을 숨기고 싶었는지가 보일 때가 있어요.', '…아, 제가 또 혼자 너무 길게 얘기했네요.'], None),
    ('baseball', 'baseball.png', '타치바나 히데오', 'tk_school', [12, 26], ['…안녕.'], None),
    ('ume', 'ume.png', '쿠루미자와 우메', 'tk_asakusa', [20, 16], ['…'], None),
    ('kaguya', 'kaguya.png', '시노미야 카구야', 'acca_dowa', [27, 16], ['…'], None),
    ('ahoge', 'ahoge.png', '아라라기 코요미', 'tk_school', [30, 27], ['…'], None),
    ('blindfold', 'blindfold.png', '지마', 'acca_dowa', [9, 22], ['…'], None),
    ('headphone', 'headphone.png', '마가미 케이고', 'tk_ikebukuro', [29, 24], ['…'], None),
    ('nifuji', 'nifuji.png', '니후지 히로타카', 'tk_ginza', [33, 13], ['…'], None),
    ('gintoki', 'gintoki.png', '사카타 긴토키', 'tk_asakusa', [25, 21], ['…'], None),
    ('usui', 'usui.png', '우스이 타쿠미', 'tk_harajuku', [30, 30], ['…'], None),
    ('izumi', 'izumi.png', '이즈미 리오', 'tk_shibuya', [34, 31], ['…뭐야.'], None),
    ('ponytail', 'ponytail.png', '카지 료지', 'tk_geofront', [13, 26], ['…'], None),
    ('spiky', 'spiky.png', '미도 반', 'tk_roppongi', [38, 28], ['…'], None),
    ('kyon', 'kyon.png', '쿈', 'tk_street', [7, 11], ['…하아.'], None),
    ('chiro', 'chiro.png', '치로 하트', 'acca_badon', [31, 23], ['…담배 사러 왔나.'], None),
    ('saiki', 'saiki.png', '사이키 쿠스오', 'tk_shibuya', [36, 27], ['(…또 귀찮은 일이 생겼군.)'], None),
    ('nozaki', 'nozaki.png', '노자키 우메타로', 'tk_harajuku', [18, 24], ['…취재 중이야.'], None),
    ('shima', 'shima.png', '시마 소스케', 'tk_harajuku', [26, 30], ['음~ 안녕.'], None),
    ('mint', 'mint.png', '우고 카나토', 'tk_ginza', [32, 29], ['…아, 안녕.'], None),
    ('karate', 'karate.png', '쿄고쿠 마코토', 'tk_inaka', [35, 19], ['오스!', '이 신사 계단을 매일 아침 100번 오르내리는 게 수련이야.', '시골 공기가 좋아서 집중이 잘 돼. 너도 같이 뛸래?'], None),
]


def checker_phase_bg(im):
    """체크무늬가 일정한 칸 크기로 반복되면, 각 픽셀이 '그 자리의 체크 칸 색'과 같은지로 배경을 판단해요.
       흰 셔츠처럼 밝은 칸과 색이 비슷해도 어두운 칸 자리에서는 안 맞으니 캐릭터로 남아요."""
    Hh, Ww = im.shape[:2]
    def edges(line):
        lum = line.mean(1)
        if lum.max() - lum.min() < 15: return None
        b = lum > (lum.max() + lum.min()) / 2
        return np.where(np.diff(b.astype(int)) != 0)[0] + 1
    e = edges(im[2]); f = edges(im[:, 2])
    if e is None or f is None or len(e) < 6 or len(f) < 6: return None
    P = int(np.median(np.diff(e)))
    if P < 6 or np.mean(np.abs(np.diff(e)[:8] - P) <= 1) < .8: return None
    ox, oy = e[0] % P, f[0] % P
    yy, xx = np.mgrid[0:Hh, 0:Ww]
    par = (((xx - ox) // P) + ((yy - oy) // P)) % 2
    # 두 칸 색: 테두리에서 같은 parity끼리 평균
    band = np.zeros((Hh, Ww), bool); band[:6] = band[-6:] = True; band[:, :6] = band[:, -6:] = True
    c0 = np.median(im[band & (par == 0)], axis=0); c1 = np.median(im[band & (par == 1)], axis=0)
    exp = np.where(par[..., None] == 0, c0, c1)
    match = np.abs(im - exp).sum(2) < 26
    frac = ndimage.uniform_filter(match.astype(float), 7)
    return (match & (frac > .72)) | (frac > .9)

def extract(path, fill_inside=False, fill_frame=0, phase=False, nofill=False, outline=False):
    im = np.asarray(Image.open(path).convert('RGB')).astype(int); Hh, Ww = im.shape[:2]
    mx, mn = im.max(2), im.min(2)
    cand = (mx - mn < 30) & (mn > 135); S = max(Ww / 1152, Hh / 928)   # 시트 크기·비율이 달라도 같은 기준으로
    dark = mx < 90   # 칸을 나누는 검은 격자선(가로·세로로 길게 이어진 선)은 배경으로
    for y in np.where(dark.mean(1) > .97)[0]: cand[max(0, y - 1):y + 2, :] = True
    for x in np.where(dark.mean(0) > .97)[0]: cand[:, max(0, x - 1):x + 2] = True
    lab, n = ndimage.label(cand)
    # 배경 = 흰색·회색이 섞인 체크무늬 영역(어디 있든) + 시트 전체에 걸친 흰 바탕.
    #   테두리 안의 순백 영역(흰 날개·셔츠)은 체크무늬 회색이 없어서 남아요
    sl = ndimage.find_objects(lab)
    # 체크무늬의 두 색(밝은 칸·어두운 칸)을 시트 가장자리에서 찾아, 그 '어두운 칸' 색이 섞여 있는지로 판정
    brd = np.concatenate([im[:6].reshape(-1, 3), im[-6:].reshape(-1, 3), im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)])
    brd = brd[brd.min(1) > 150]; q = (brd // 8) * 8
    cols, cnt = np.unique(q, axis=0, return_counts=True); top = [c + 4 for c in cols[np.argsort(-cnt)[:3]]]   # 많이 나온 순
    hi = max(top, key=lambda c: int(c.sum()))
    lo = next((c for c in top if np.abs(c - hi).sum() >= 24), top[-1])   # 가장 밝은 칸 + (많이 나온 순으로) 확실히 어두운 칸
    grey = np.abs(im - lo).sum(2) < 18; white = np.abs(im - hi).sum(2) < 18
    if np.abs(lo - hi).sum() < 24: grey = np.zeros_like(grey)   # 체크무늬가 아닌 흰 바탕 시트
    wc = ndimage.sum(white, lab, range(1, n + 1)); gc = ndimage.sum(grey & cand, lab, range(1, n + 1)); tot = np.maximum(wc + gc, 1)
    keep_bg = []
    for i in range(n):
        hh, ww = sl[i][0].stop - sl[i][0].start, sl[i][1].stop - sl[i][1].start
        big = max(hh, ww) > 120 * S
        checker = gc[i] / tot[i] > .12 and wc[i] / tot[i] > .12
        pocket = gc[i] / tot[i] > .3 and wc[i] / tot[i] > .3 and tot[i] > 30 * S * S   # 캐릭터 사이에 갇힌 작은 체크무늬 조각은 더 엄격하게
        if (big and checker) or pocket or max(hh, ww) > 400 * S: keep_bg.append(i + 1)
    bg = np.isin(lab, keep_bg)
    # 체크무늬 밝은 칸보다 확실히 더 하얀 픽셀(흰 날개·셔츠 하이라이트)은 배경이 아님 → 되살리고,
    # 그 안에 갇힌 구멍 중 체크무늬 밝은 칸 색이 없는 것(날개 음영)은 함께 채워요
    if hi.min() < 236:
        bg &= ~(mn > hi.min() + 12)
        holes = ndimage.binary_fill_holes(~bg) & bg
        hl, hn = ndimage.label(holes)
        if hn:
            idx = range(1, hn + 1)
            has_light = ndimage.sum(white, hl, idx); has_dark = ndimage.sum(grey, hl, idx); size = ndimage.sum(np.ones_like(hl), hl, idx)
            fillids = [i + 1 for i in range(hn) if has_light[i] < 3 and has_dark[i] < size[i] * .4]
            bg &= ~np.isin(hl, fillids)
    fg = ~bg
    P = None
    if phase:
        e = np.where(np.diff((im[2].mean(1) > im[2].mean()).astype(int)) != 0)[0]
        if len(e) > 6: P = int(np.median(np.diff(e)))
        cL, cD = hi.astype(float), lo.astype(float)
    if fill_inside:   # 흰 머리처럼 배경색과 비슷한 부분: 테두리 틈을 메운 뒤 안쪽을 통째로 캐릭터로 채워요
        fg = ndimage.binary_fill_holes(ndimage.binary_closing(fg, iterations=4)) | fg
    lab2, n2 = ndimage.label(fg, structure=np.ones((3, 3)))
    sl2 = ndimage.find_objects(lab2); areas = ndimage.sum(np.ones_like(lab2), lab2, range(1, n2 + 1))
    bodies, bits = [], []
    for i, s in enumerate(sl2):
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
        if h > 400 * S or w > 400 * S or (min(h, w) < 6 * S and max(h, w) > 60 * S): continue   # 격자선
        if areas[i] > 2500 * S * S and h > 60 * S: bodies.append([i + 1, s])
        elif areas[i] > 12 * S * S: bits.append([i + 1, s])
    # 작은 조각(담배·머리끝)은 가까운 몸에 붙여요
    owner = {b[0]: b[0] for b in bodies}
    for (li, s) in bits:
        cy, cx = (s[0].start + s[0].stop) / 2, (s[1].start + s[1].stop) / 2
        for (bi, bs) in bodies:
            if bs[0].start - 8 <= cy <= bs[0].stop + 8 and bs[1].start - 10 <= cx <= bs[1].stop + 10: owner[li] = bi; break
    frames = []
    rgba = np.dstack([im, np.full((Hh, Ww), 255)]).astype(np.uint8)
    for (bi, s) in bodies:
        ids = [k for k, v in owner.items() if v == bi]
        m = np.isin(lab2, ids)
        # 흰 셔츠·날개처럼 배경으로 잘못 빠진 안쪽 부분을 프레임 하나 안에서 되살려요.
        #   틈을 살짝 메워서 생긴 '안쪽 구멍' 중, 체크무늬 어두운 칸이 거의 없는(=진짜 배경이 아닌) 덩어리만 채워요
        ys, xs = np.where(m); bb = (slice(max(0, ys.min() - 6), ys.max() + 7), slice(max(0, xs.min() - 6), xs.max() + 7))
        sub = m[bb] if not nofill else None; k = max(3, fill_frame, int(10 * S))
        hl, hn = ndimage.label(ndimage.binary_fill_holes(ndimage.binary_closing(sub, iterations=k)) & ~sub) if sub is not None else (None, 0)
        if hn:
            g = grey[bb]; w = white[bb]
            for i in range(1, hn + 1):
                r = hl == i; n = r.sum()
                if g[r].sum() < max(2, n * .04) and (w[r].sum() < n * .9 or n < 400 * S * S or fill_frame): sub = sub | r
            m = m.copy(); m[bb] = sub
        if P:   # 이 프레임 주변 배경으로 체크 격자 위치를 맞춘 뒤, 격자 색과 안 맞는 픽셀(흰 셔츠 등)을 되살려요
            ys, xs = np.where(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
            Y0, Y1, X0, X1 = max(0, y0 - 14), min(Hh, y1 + 14), max(0, x0 - 14), min(Ww, x1 + 14)
            ring = np.ones((Y1 - Y0, X1 - X0), bool); ring[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0] = False
            ry, rx = np.where(ring); sel = np.linspace(0, len(ry) - 1, min(600, len(ry))).astype(int); ry, rx = ry[sel] + Y0, rx[sel] + X0
            cols = im[ry, rx].astype(float); dL = np.abs(cols - cL).sum(1); dD = np.abs(cols - cD).sum(1)
            best, bo = -1, (0, 0)
            for oy in range(0, 2 * P, 2):
                for ox in range(0, 2 * P, 2):
                    par = (((rx + ox) // P) + ((ry + oy) // P)) % 2
                    sc = np.mean(np.where(par == 0, dL, dD) < 24)
                    if sc > best: best, bo = sc, (ox, oy)
            if best > .75:
                yy, xx = np.mgrid[y0:y1, x0:x1]; par = (((xx + bo[0]) // P) + ((yy + bo[1]) // P)) % 2
                exp = np.where(par[..., None] == 0, cL, cD); match = np.abs(im[y0:y1, x0:x1] - exp).sum(2) < 26
                frac = ndimage.uniform_filter(match.astype(float), 5)
                keep = ~(match & (frac > .5)) & ~dark[y0:y1, x0:x1]
                old = m[y0:y1, x0:x1]
                add = keep & ~old
                add = ndimage.binary_opening(add, iterations=max(2, int(2 * S)))        # 가는 선·잡티는 버리고 두툼한 덩어리만
                add &= ndimage.binary_dilation(old, iterations=2)                         # 원래 몸에 붙어 있는 것만
                add = ndimage.binary_propagation(add, mask=keep & ~old) & ndimage.binary_opening(keep & ~old, iterations=max(2, int(2 * S)))
                m = m.copy(); m[y0:y1, x0:x1] = old | add
                # 가장자리에 붙은 체크무늬 색 픽셀(흰 줄·점)은 두 번 깎아내요
                sub = m[y0:y1, x0:x1]; px_ = im[y0:y1, x0:x1].astype(float)
                bgcol = (np.abs(px_ - cL).sum(2) < 30) | (np.abs(px_ - cD).sum(2) < 30)
                for _ in range(2):
                    edge = sub & ~ndimage.binary_erosion(sub); sub = sub & ~(edge & bgcol & add)
                lab4, n4 = ndimage.label(sub)
                if n4 > 1: sz = ndimage.sum(sub, lab4, range(1, n4 + 1)); sub = (lab4 == (1 + int(np.argmax(sz)))) | (sub & np.isin(lab4, 1 + np.where(sz > sz.max() * .02)[0]))
                m[y0:y1, x0:x1] = sub
        if outline:   # 진한 외곽선으로 둘러싸인 안쪽(흰 신발 등)은 캐릭터로
            ys, xs = np.where(m); bb = (slice(max(0, ys.min() - 4), ys.max() + 5), slice(max(0, xs.min() - 4), xs.max() + 5))
            ol = (im[bb].max(2) < 110) & ndimage.binary_dilation(m[bb], iterations=6)
            enc = ndimage.binary_fill_holes(ndimage.binary_closing(ol | m[bb], iterations=1)) & ~m[bb]
            hl, hn = ndimage.label(enc)
            sub = m[bb].copy()
            for i in range(1, hn + 1):
                r = hl == i
                if r.sum() < 900 * S * S and grey[bb][r].mean() < .35: sub |= r
            m = m.copy(); m[bb] = sub
        ys, xs = np.where(m); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        crop = rgba[y0:y1, x0:x1].copy(); crop[..., 3] = np.where(m[y0:y1, x0:x1], 255, 0)
        frames.append(dict(img=crop, cx=(x0 + x1) / 2, cy=(y0 + y1) / 2, top=y0, bot=y1))
    # 줄 나누기: y 중심 정렬 후 큰 틈으로 4줄
    frames.sort(key=lambda f: f['cy'])
    gaps = sorted(range(1, len(frames)), key=lambda i: frames[i]['cy'] - frames[i - 1]['cy'], reverse=True)[:3]
    rows, start = [], 0
    for g in sorted(gaps) + [len(frames)]: rows.append(sorted(frames[start:g], key=lambda f: f['cx'])); start = g
    return rows

def skin_ref(front):
    a = front.astype(int); h, w = a.shape[:2]
    reg = a[int(h * .30):int(h * .40), int(w * .3):int(w * .7)].reshape(-1, 4)
    reg = reg[(reg[:, 3] > 0) & (reg[:, :3].sum(1) > 330)]
    return np.median(reg[:, :3], 0) if len(reg) else np.array([240, 210, 190])
def facing(img, ref):
    a = img.astype(int); h = a.shape[0]; head = a[int(h * .08): int(h * .45)]
    vis = head[..., 3] > 0
    skin = vis & (np.abs(head[..., :3] - ref).sum(2) < 60)
    if skin.sum() < vis.sum() * .05: return 'up'
    ys, xs = np.where(vis); cxb = (xs.min() + xs.max()) / 2; w = xs.max() - xs.min() + 1
    off = (np.where(skin)[1].mean() - cxb) / w
    return 'down' if abs(off) < .06 else ('left' if off < 0 else 'right')

def trim_side_hair(img, ref, clean=False):
    """앞모습 누끼: 모자챙 아래부터 턱까지 얼굴 윤곽만 남기고 옆머리를 지워요.
       윤곽은 위아래 줄과 이어지게 부드럽게 다듬어서(파인 곳은 피부로 메움) 테두리선을 다시 그려요"""
    a = img.copy(); h, w = a.shape[:2]; col = a[..., :3].astype(int)
    skin = (a[..., 3] > 0) & (np.abs(col - ref).sum(2) < 80)
    skin = ndimage.binary_closing(skin, iterations=2)
    rows = [y for y in range(int(h * .5)) if skin[y].sum() >= 3]
    if not rows: return a
    y0, y1 = rows[0], rows[-1]
    L, Rr = {}, {}
    for y in range(y0, y1 + 1):
        xs = np.where(skin[max(y0, y - 2):min(y1, y + 2) + 1].any(0))[0]
        if len(xs): L[y], Rr[y] = xs.min(), xs.max()
    ys = sorted(L)
    hair = np.array([30, 28, 40, 255], np.uint8)
    OL = np.array([26, 16, 36, 255], np.uint8); skc = np.array(list(ref.astype(np.uint8)) + [255], np.uint8)
    for y in ys:
        win = [k for k in ys if abs(k - y) <= 5]
        l = min(L[k] for k in win); r = max(Rr[k] for k in win)   # 위아래 5줄 중 가장 넓은 폭: 파인 데가 안 생김
        a[y, :max(0, l - 1), 3] = 0; a[y, r + 2:, 3] = 0
        hair = np.array([30, 28, 40, 255], np.uint8)
        for x in range(l, r + 1):   # 윤곽 안의 빈칸(파인 곳)은 검게 칠해 머리카락처럼
            if a[y, x, 3] == 0: a[y, x] = hair
        for x in (l - 1, r + 1):
            if 0 <= x < w: a[y, x] = OL
    # 모자챙 아래 ~ 얼굴 옆에 생긴 빈 틈: 챙 끝에서 얼굴선까지 부드럽게 머리카락으로 메워요
    if clean:   # 이마로 내려온 앞머리를 피부색으로: 얼굴 위쪽 30% 줄에서, 모자 바로 아래 붙어 있는 진한 픽셀만
        top = ys[:max(3, int(len(ys) * .3))]
        dark = (a[..., :3].astype(int).max(2) < 95) & (a[..., 3] > 0)
        reg = np.zeros(dark.shape, bool)
        for y in top: reg[y, L[y] + 1:Rr[y]] = True
        lab, n = ndimage.label(dark & reg)
        ids = set(lab[top[0]][lab[top[0]] > 0])
        for i in ids:
            r = lab == i
            a[r] = skc
        # 얼굴 옆으로 삐친 머리: 위쪽 60% 줄에서 그 줄의 실제 피부 폭 밖은 지우고 외곽선만
        col2 = a[..., :3].astype(int); skin2 = (a[..., 3] > 0) & (np.abs(col2 - ref).sum(2) < 80)
        skin2 = ndimage.binary_closing(skin2, iterations=1)
        for y in ys[:max(3, int(len(ys) * .6))]:
            xs_ = np.where(skin2[max(0, y - 2):y + 3].any(0))[0]
            if not len(xs_): continue
            lo_, hi_ = xs_.min(), xs_.max()
            a[y, :max(0, lo_ - 1), 3] = 0; a[y, hi_ + 2:, 3] = 0
            for x in (lo_ - 1, hi_ + 1):
                if 0 <= x < w: a[y, x] = OL
        # 모자챙 바로 아래 ~ 얼굴이 넓어지는 줄까지: 이마를 얼굴 폭으로 메워 틈을 없애요
        widths = {y: np.where(skin2[y])[0] for y in ys[:max(3, int(len(ys) * .6))]}
        wmax = max((len(v) and v.max() - v.min()) or 0 for v in widths.values())
        good = next((y for y in sorted(widths) if len(widths[y]) and widths[y].max() - widths[y].min() >= wmax * .85), None)
        if good is not None:
            lo_, hi_ = widths[good].min(), widths[good].max()
            yb = good
            while yb > 0 and not (a[yb - 1, lo_:hi_ + 1, 3] > 0).all() and good - yb < 12: yb -= 1
            for y in range(yb, good):
                row = a[y, lo_:hi_ + 1]; hole = row[:, 3] == 0; row[hole] = skc
                for x in (lo_ - 1, hi_ + 1):
                    if 0 <= x < w and a[y, x, 3] == 0: a[y, x] = OL
        return a
    above = [yy for yy in range(max(0, ys[0] - 4), ys[0]) if (a[yy, :, 3] > 0).any()]
    if above:
        yb = above[-1]; xs_b = np.where(a[yb, :, 3] > 0)[0]; bl, br = xs_b.min(), xs_b.max()
        n = max(4, int((ys[-1] - ys[0]) * .6)); pel, per = -1, 10 ** 6
        lf = min(L[k] for k in ys[:n]); rf = max(Rr[k] for k in ys[:n])   # 얼굴 폭은 고정값으로: 줄마다 들쭉날쭉하지 않게
        for i, y in enumerate(ys[:n]):
            t = (i / n) ** .8; win = [k for k in ys if abs(k - y) <= 5]; l = min(L[k] for k in win); r = max(Rr[k] for k in win)
            el = min(l - 1, max(pel, int(round(bl + (lf - bl) * t)))); er = max(r + 1, min(per, int(round(br + (rf - br) * t)))); pel, per = el, er
            for x in range(max(0, el), l - 1):
                if a[y, x, 3] == 0 or True: a[y, x] = hair
            for x in range(r + 2, min(w, er + 1)):
                a[y, x] = hair
            if el < l - 1 and el >= 0: a[y, el] = OL
            if er > r + 1 and er < w: a[y, er] = OL
    return a
def shrink(img, scale):
    img = img.copy(); m = img[..., 3] > 0
    # 누끼 테두리 정리: 바깥 1px(배경 잔여물)을 깎고, 작은 부스러기 덩어리는 버려요
    m = ndimage.binary_erosion(m, iterations=1)
    lab, nl = ndimage.label(m)
    if nl > 1:
        sz = ndimage.sum(m, lab, range(1, nl + 1)); keep = np.isin(lab, 1 + np.where(sz >= max(30, sz.max() * .01))[0]); m &= keep
    img[..., 3] = np.where(m, 255, 0)
    im = Image.fromarray(img, 'RGBA'); w, h = im.size
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    a = np.asarray(im).astype(float); pre = a.copy(); pre[..., :3] *= a[..., 3:4] / 255
    small = np.asarray(Image.fromarray(pre.astype(np.uint8), 'RGBA').resize((nw, nh), Image.LANCZOS)).astype(float)
    al = np.clip(small[..., 3], 0, 255); out = np.zeros_like(small)
    ok = al > 24; out[ok, :3] = np.clip(small[ok, :3] * 255 / np.maximum(al[ok, None], 1), 0, 255); out[ok, 3] = al[ok]
    return out.astype(np.uint8)

def build():
    sheet_rows, meta = [], []
    for (cid, fn, name, mp, tile, lines, force) in SHEETS:
        rows = extract('chars_src/' + fn, fill_inside=SIDE.get(cid, {}).get('fill_inside', False), fill_frame=SIDE.get(cid, {}).get('fill_frame', 0), phase=SIDE.get(cid, {}).get('phase', PHASE_ALL), nofill=SIDE.get(cid, {}).get('nofill', False), outline=SIDE.get(cid, {}).get('outline', False))
        allf = [(ri, f) for ri, row in enumerate(rows) for f in row]
        hmax = max(f['img'].shape[0] for _, f in allf); scale = TARGET * R / hmax
        groups = {d: [] for d in DIRS}
        if force:
            for ri, row in enumerate(rows): groups[force[ri]] += row
        else:
            groups['down'] = [rows[0][k] for k in SIDE[cid].get('down', range(len(rows[0])))]; groups['up'] = [rows[1][k] for k in SIDE[cid].get('up', range(len(rows[1])))]
            if SIDE[cid].get('trim_front'): ref = skin_ref(rows[0][0]['img']); groups['down'] = [dict(f, img=trim_side_hair(f['img'], ref, SIDE[cid].get('clean_front', False))) for f in rows[0]]
            sd = SIDE[cid]
            groups['left'] = [rows[r][k] for r, k in sd['left']] if sd['left'] != 'mirror' else [dict(rows[r][k], img=rows[r][k]['img'][:, ::-1]) for r, k in sd['right']]
            groups['right'] = [rows[r][k] for r, k in sd['right']] if sd['right'] and sd['right'] != 'mirror' else [dict(f, img=f['img'][:, ::-1]) for f in groups['left']]
            if len(groups['left']) < 3 and sd['right']: groups['left'] = [dict(f, img=f['img'][:, ::-1]) for f in groups['right']]
        # 한쪽 옆모습이 모자라면 반대쪽을 뒤집어 써요
        for a_, b_ in (('left', 'right'), ('right', 'left')):
            if len(groups[a_]) < 2 and len(groups[b_]) >= 2: groups[a_] = [dict(f, img=f['img'][:, ::-1]) for f in groups[b_]]
        block = np.zeros((FH * R * 4, FW * R * 4, 4), np.uint8); counts = {}; fw, fh = FW * R, FH * R
        for di, d in enumerate(DIRS):
            fs = groups[d][:4] or groups['down'][:1]
            counts[d] = len(fs)
            for k, f in enumerate(fs):
                s = shrink(f['img'], scale); h, w = s.shape[:2]
                if w > fw: s = s[:, (w - fw) // 2:(w - fw) // 2 + fw]; w = fw
                if h > fh - R: s = s[h - (fh - R):]; h = fh - R
                ox, oy = (fw - w) // 2, di * fh + fh - R - h
                dst = block[oy:oy + h, k * fw + ox:k * fw + ox + w]
                dst[:] = np.where(s[..., 3:4] > 0, s, dst)
        meta.append(dict(id=cid, name=name, map=mp, tile=tile, lines=lines, base=len(sheet_rows) * 4, n=counts,
                         found={d: len(groups[d]) for d in DIRS}))
        a = block[..., 3] > 0; rgb = block[..., :3].astype(int)
        light = (rgb.min(2) > 150) & ((rgb.max(2) - rgb.min(2)) < 28)
        for _ in range(2):
            edge = a & ~ndimage.binary_erosion(a); a &= ~(edge & light)
        lab, n = ndimage.label(a)
        if n: sz = ndimage.sum(a, lab, range(1, n + 1)); a &= ~np.isin(lab, 1 + np.where(sz < 8)[0])
        block[..., 3] = np.where(a, block[..., 3], 0)
        sheet_rows.append(block)
        print(cid, 'rows', [len(r) for r in rows], {d: len(groups[d]) for d in DIRS})
    return sheet_rows, meta

if __name__ == '__main__':
    blocks, meta = build()
    # 코트 청년과 '나'는 아직 시트가 없어서 tk_npcs.py의 그림(앞모습 2프레임)을 칸에 맞춰 넣어요
    npc = Image.open('out/tk_npcs.png'); nj = json.load(open('out/tk_npcs.json'))
    for c in nj['chars']:
        if c['id'] != 'me': continue
        block = Image.new('RGBA', (FW * R * 4, FH * R * 4), (0, 0, 0, 0))
        for di in range(4):
            for k in range(2):
                fr = npc.crop((k * 24, c['row'] * 36, k * 24 + 24, c['row'] * 36 + 36)).resize((26 * R, 39 * R), Image.NEAREST)
                if di == 3: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
                block.paste(fr, ((k * FW + 3) * R, (di * FH + FH - 40) * R), fr)
        meta.append(dict(id=c['id'], name=c['name'], map=c['map'], tile=c['tile'], lines=c['lines'], base=len(blocks) * 4, n={d: 2 for d in DIRS}, found={}))
        blocks.append(np.asarray(block))
    sheet = np.concatenate(blocks, 0)
    Image.fromarray(sheet, 'RGBA').save('out/tk_chars.png')
    json.dump(dict(FW=FW, FH=FH, R=R, dirs=DIRS, chars=meta), open('out/tk_chars.json', 'w'), ensure_ascii=False)
    prev = Image.fromarray(sheet, 'RGBA'); bgp = Image.new('RGBA', prev.size, (60, 56, 80, 255)); bgp.alpha_composite(prev)
    bgp.save('out/tk_chars_preview.png')
    print('sheet', sheet.shape)
