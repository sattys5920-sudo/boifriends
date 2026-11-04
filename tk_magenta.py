"""단색 마젠타(#FF00FF) 배경 시트를 잘라 앱용 스프라이트(docs/assets/ch/<id>.webp)로 만들어요.
사용: python3 tk_magenta.py <id> <시트.png> [cols rows]
줄 순서: 1 앞, 2 뒤, 3 왼쪽, 4 오른쪽. 앞·뒤는 0~3칸, 옆은 걷는 1~4칸을 써요."""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
import tk_chars as T

def key_green(a):
    """초록(#00FF00) 배경용: 보라·분홍 캐릭터는 이쪽이 안전해요"""
    rgb = a[..., :3].astype(int); R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    fg = ~(G - np.maximum(R, B) > 70)
    lab, n = ndimage.label(fg)
    if n > 1:
        sz = ndimage.sum(fg, lab, range(1, n + 1)); fg &= np.isin(lab, 1 + np.where(sz >= max(40, sz.max() * .02))[0])
    for _ in range(2):
        edge = fg & ~ndimage.binary_erosion(fg); fg &= ~(edge & (G - np.maximum(R, B) > 35))
    near = ndimage.binary_dilation(~fg, iterations=3) & fg
    rgb = rgb.copy(); rgb[..., 1] = np.minimum(G, np.maximum(R, B) + 10 * ~near + 1000 * ~near)   # 테두리 초록기 빼기
    out = np.zeros(a.shape[:2] + (4,), np.uint8); out[..., :3] = np.clip(rgb, 0, 255); out[..., 3] = np.where(fg, 255, 0)
    return out

NO_DESPILL = False
def key(a):
    c = a[:4, :4, :3].reshape(-1, 3).astype(int).mean(0)
    if c[1] > 180 and c[0] < 100 and c[2] < 100: return key_green(a)
    rgb = a[..., :3].astype(int); R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mag = (np.minimum(R, B) - G > 70) & (np.abs(R - B) < 90)          # 배경과 거의 같은 색
    mag |= (np.minimum(R, B) - G > 45) & (np.abs(R - B) < 60) & (B > 90)   # 다리 사이에 낀 어두운 마젠타
    fg = ~mag
    dk = rgb.max(2) < 90   # 칸을 나누는 검은 격자선(가로·세로로 길게 이어진 선)은 배경으로
    for y in np.where(dk.mean(1) > .9)[0]: fg[max(0, y - 1):y + 2, :] = False
    for x in np.where(dk.mean(0) > .9)[0]: fg[:, max(0, x - 1):x + 2] = False
    lab, n = ndimage.label(fg)
    if n > 1:   # 작은 부스러기 버리기
        sz = ndimage.sum(fg, lab, range(1, n + 1)); fg &= np.isin(lab, 1 + np.where(sz >= max(40, sz.max() * .02))[0])
    near = ndimage.binary_dilation(~fg, iterations=3)   # 배경 바로 옆만 (눈 같은 안쪽 분홍은 그대로)
    fg &= ~(near & (np.minimum(R, B) - G > 55) & (R > 150) & (B > 150))   # 연기·반짝이에 남은 분홍 번짐
    # 가장자리 분홍 번짐 빼기: 테두리 1~2 px 중 마젠타 기운이 남은 픽셀
    for _ in range(2):
        edge = fg & ~ndimage.binary_erosion(fg)
        tint = (np.minimum(R, B) - G > 50) & (np.minimum(R, B) > 140)   # 라벤더 머리처럼 연한 보라는 남겨요
        fg &= ~(edge & tint)
    # 배경 근처에 남은 분홍기 빼기(despill): R·B가 G보다 넘치는 만큼 깎아요
    near = ndimage.binary_dilation(~fg, iterations=3) & fg
    ex = np.clip(np.minimum(R, B) - G, 0, None) * near
    if not NO_DESPILL: rgb = rgb.copy(); rgb[..., 0] -= ex; rgb[..., 2] -= ex
    out = np.zeros(a.shape[:2] + (4,), np.uint8); out[..., :3] = rgb; out[..., 3] = np.where(fg, 255, 0)
    return out

def strip_white(out):
    """캐릭터 둘레의 흰 테두리를 바깥부터 한 겹씩 깎아요 (안쪽 흰 셔츠·양말은 그대로)"""
    al = out[..., 3] > 0; rgb = out[..., :3].astype(int)
    white = (rgb.min(2) > 170) & ((rgb.max(2) - rgb.min(2)) < 60)   # 흰색·흰색에 분홍이 섞인 테두리까지
    for _ in range(8):
        edge = al & ~ndimage.binary_erosion(al); rm = edge & white
        if not rm.any(): break
        al &= ~rm
    out[..., 3] = np.where(al, 255, 0); return out

KEEP_PURPLE = {'nifuji'}   # 보라 넥타이처럼 분홍기 빼기에 지워지는 색이 있는 시트
STRIP = {'chiyo'}   # 흰 테두리가 있는 시트 (흰 테두리 덕분에 분홍기 빼기도 필요 없어요: 보라 눈이 지워지지 않게)
def cells(path, cols=5, rows=4):
    global NO_DESPILL
    st = any(k in path for k in STRIP); NO_DESPILL = st or any(k in path for k in KEEP_PURPLE)
    im = np.asarray(Image.open(path).convert('RGB')); H, W = im.shape[:2]; a = key(im); NO_DESPILL = False
    if any(k in path for k in KEEP_PURPLE):   # 몸 안쪽에 갇힌 구멍(보라 넥타이 등)은 원래 색으로 채워요
        al = a[..., 3] > 0; R, G, B = [im[..., i].astype(int) for i in range(3)]
        pure = (R > 200) & (B > 200) & (G < 70)   # 팔 사이로 보이는 진짜 배경은 채우지 않아요
        filled = ndimage.binary_fill_holes(al) & (al | ~pure)
        tie = (B - R > 10) & (B < 215) & (B > 90) & (G < 80) & ndimage.binary_dilation(al, iterations=3)   # 테두리에 붙은 진한 보라(넥타이)
        for _ in range(3): tie |= ndimage.binary_dilation(tie) & (B - R > 5) & (B < 220) & (G < 80) & ~pure
        filled |= tie
        a[..., :3] = np.where((filled & ~al)[..., None], im, a[..., :3]); a[..., 3] = np.where(filled, 255, 0)
    if st:   # 흰 테두리 시트: 보통처럼 자른 뒤, 캐릭터 안쪽에 갇힌 구멍(배경색과 비슷한 보라 눈 등)은 원래 색으로 채우고 흰 테두리를 깎아요
        al = a[..., 3] > 0; filled = ndimage.binary_fill_holes(al)
        a[..., :3] = np.where((filled & ~al)[..., None], im, a[..., :3]); a[..., 3] = np.where(filled, 255, 0)
        a = strip_white(a)
    def cuts(prof, n, L):   # 칸 경계는 그 근처에서 캐릭터가 가장 적게 걸치는 줄로 (시트가 격자에 딱 안 맞아도)
        out = [0]
        for k in range(1, n):
            b = int(k * L / n); w = int(L / n * .22); seg = prof[b - w:b + w]
            out.append(b - w + int(np.argmin(seg)))
        return out + [L]
    al = a[..., 3] > 0; YC = cuts(al.sum(1), rows, H); XC = cuts(al.sum(0), cols, W)
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            cell = a[YC[r]:YC[r + 1], XC[c]:XC[c + 1]]
            ys, xs = np.nonzero(cell[..., 3]); row.append(cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
        grid.append(row)
    return grid

def build(cid, path, cols=5, rows=4, pick=None):
    g = cells(path, cols, rows)
    pick = pick or {'down': [(0, k) for k in range(4)], 'up': [(1, k) for k in range(4)], 'left': [(2, k) for k in range(1, 5)], 'right': [(3, k) for k in range(1, 5)]}
    hmax = max(f.shape[0] for row in g for f in row); scale = T.TARGET * T.R / hmax
    fw, fh = T.FW * T.R, T.FH * T.R; block = np.zeros((fh * 4, fw * 4, 4), np.uint8)
    for di, d in enumerate(T.DIRS):
        for k, (r, c) in enumerate(pick[d][:4]):
            s = T.shrink(g[r][c], scale); h, w = s.shape[:2]
            if w > fw: s = s[:, (w - fw) // 2:(w - fw) // 2 + fw]; w = fw
            if h > fh - T.R: s = s[h - (fh - T.R):]; h = fh - T.R
            ox, oy = (fw - w) // 2, di * fh + fh - T.R - h
            dst = block[oy:oy + h, k * fw + ox:k * fw + ox + w]; dst[:] = np.where(s[..., 3:4] > 0, s, dst)
    import tk_whiten; block = block if cid in tk_whiten.SKIP else tk_whiten.whiten(block)[0]   # 피부 미백
    Image.fromarray(block).save(f'docs/assets/ch/{cid}.webp', 'WEBP', lossless=True)
    fr = json.load(open('docs/data/frames.json')); fr[cid] = [min(4, len(pick[d])) for d in T.DIRS]; json.dump(fr, open('docs/data/frames.json', 'w'))
    return block

if __name__ == '__main__':
    a = sys.argv; build(a[1], a[2], *(int(x) for x in a[3:5]))
    print('ok', a[1])
