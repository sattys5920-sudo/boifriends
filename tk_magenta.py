"""단색 마젠타(#FF00FF) 배경 시트를 잘라 앱용 스프라이트(docs/assets/ch/<id>.webp)로 만들어요.
사용: python3 tk_magenta.py <id> <시트.png> [cols rows]
줄 순서: 1 앞, 2 뒤, 3 왼쪽, 4 오른쪽. 앞·뒤는 0~3칸, 옆은 걷는 1~4칸을 써요."""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage
import tk_chars as T

def key(a):
    rgb = a[..., :3].astype(int); R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mag = (np.minimum(R, B) - G > 70) & (np.abs(R - B) < 90)          # 배경과 거의 같은 색
    fg = ~mag
    lab, n = ndimage.label(fg)
    if n > 1:   # 작은 부스러기 버리기
        sz = ndimage.sum(fg, lab, range(1, n + 1)); fg &= np.isin(lab, 1 + np.where(sz >= max(40, sz.max() * .02))[0])
    fg = ndimage.binary_fill_holes(fg)
    # 가장자리 분홍 번짐 빼기: 테두리 1~2 px 중 마젠타 기운이 남은 픽셀
    for _ in range(2):
        edge = fg & ~ndimage.binary_erosion(fg)
        tint = (np.minimum(R, B) - G > 35)
        fg &= ~(edge & tint)
    out = np.zeros(a.shape[:2] + (4,), np.uint8); out[..., :3] = rgb; out[..., 3] = np.where(fg, 255, 0)
    return out

def cells(path, cols=5, rows=4):
    im = np.asarray(Image.open(path).convert('RGB')); H, W = im.shape[:2]; a = key(im)
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            cell = a[int(r * H / rows):int((r + 1) * H / rows), int(c * W / cols):int((c + 1) * W / cols)]
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
    Image.fromarray(block).save(f'docs/assets/ch/{cid}.webp', 'WEBP', lossless=True)
    fr = json.load(open('docs/data/frames.json')); fr[cid] = [min(4, len(pick[d])) for d in T.DIRS]; json.dump(fr, open('docs/data/frames.json', 'w'))
    return block

if __name__ == '__main__':
    a = sys.argv; build(a[1], a[2], *(int(x) for x in a[3:5]))
    print('ok', a[1])
