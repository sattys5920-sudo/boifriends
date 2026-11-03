"""여자애 그림을 짝 남자애 그림체(키, 머리 비율, 픽셀 굵기, 외곽선)에 맞춰요.
원본은 git의 기준 커밋에서 읽어서, 몇 번 돌려도 결과가 같아요.
사용: python3 tk_match.py [girl_id ...]   (없으면 전체)"""
import sys, json, io, subprocess
import numpy as np
from PIL import Image
from scipy import ndimage
FW, FH = 96, 132
BASE = 'e0dc38f'   # 맞추기 전 그림이 있는 커밋
SKIP = {'meroko', 'kokomi'}   # 이미 손으로 맞춘 애들

def load(id, rev=None):
    if rev: return np.array(Image.open(io.BytesIO(subprocess.run(['git', 'show', f'{rev}:docs/assets/ch/{id}.webp'], capture_output=True).stdout)).convert('RGBA'))
    return np.array(Image.open(f'docs/assets/ch/{id}.webp').convert('RGBA'))

def bbox(f):
    ys, xs = np.nonzero(f[..., 3] > 0); return ys.min(), ys.max() + 1, xs.min(), xs.max() + 1

def chin(f):
    """얼굴 피부가 끝나는 줄(턱). 못 찾으면 키의 45%"""
    R, G, B = [f[..., i].astype(int) for i in range(3)]; al = f[..., 3] > 0; h = f.shape[0]
    sk = al & (R > 150) & (R > G) & (G > B) & (R - B > 20) & (R - B < 120)
    rows = np.nonzero(sk[:int(h * .62)].sum(1) > 2)[0]
    return int(rows.max()) + 1 if len(rows) and rows.max() > h * .2 else int(h * .45)

def pix_size(sheet):
    """그림의 실제 픽셀 굵기: k칸씩 묶었다 풀었을 때 거의 안 바뀌는 가장 큰 k"""
    f = sheet[:FH, :FW].astype(float); al = f[..., 3] > 0; best = 1
    for k in (2, 3):
        im = Image.fromarray(sheet[:FH, :FW]); s = im.resize((FW // k, FH // k), Image.BOX).resize((FW, FH), Image.NEAREST)
        err = np.abs(np.array(s).astype(float)[..., :3] - f[..., :3])[al].mean()
        if err < 22: best = k
    return best

def skin(f):
    R, G, B = [f[..., i].astype(int) for i in range(3)]; al = f[..., 3] > 0
    return al & (R > 150) & (R > G) & (G > B) & (R - B > 20) & (R - B < 120)

def measure(f):
    """[얼굴 폭, 몸통 폭, 턱 위치, 키] — 얼굴 폭은 피부가 가장 넓은 줄, 몸통 폭은 턱 아래 30% 지점"""
    t, b, l, r = bbox(f); f = f[t:b, l:r]; h = f.shape[0]; c = chin(f); sk = skin(f[:c])
    fw = int(sk.sum(1).max()) if sk.any() else int((f[:c, :, 3] > 0).any(0).sum() * .7)
    y = min(h - 1, c + int((h - c) * .3)); row = np.nonzero(f[y, :, 3] > 0)[0]
    tw = int(row.max() - row.min() + 1) if len(row) else f.shape[1]
    return fw, tw, c, h

def scales(gf, bf):
    gfw, gtw, gc, gh = measure(gf); bfw, btw, bc, bh = measure(bf)
    sh = np.clip(bfw * .95 / max(gfw, 1), .95, 1.3)          # 얼굴을 짝 남자애 얼굴 크기만큼
    sh = min(sh, max(.95, bc * 1.0 / max(gc, 1)))              # 머리 높이는 짝 남자애 머리보다 크지 않게
    Ht = bh * .95
    sbh = np.clip((Ht - gc * sh) / max(gh - gc, 1), .75, 1.1)  # 남은 키가 몸 (너무 짧아지지 않게)
    tot = gc * sh + (gh - gc) * sbh
    if tot > Ht * 1.02: k = Ht / tot; sh *= k; sbh *= k        # 전체 키가 넘치면 같이 줄여요
    sbw = np.clip(btw * .9 / max(gtw, 1), 1.0, 1.4)           # 몸통 폭을 짝 남자애 어깨만큼 넓게
    return sh, sbh, sbw, gc / gh

def reshape(f, sc):
    sh, sbh, sbw, cr = sc
    t, b, l, r = bbox(f); f = f[t:b, l:r]; h = f.shape[0]; c = max(1, round(h * cr))   # 모든 칸에 같은 배율·같은 턱 위치
    head, body = f[:c], f[c:]
    H = Image.fromarray(head).resize((max(1, round(head.shape[1] * sh)), max(1, round(c * sh))), Image.LANCZOS)
    Bd = Image.fromarray(body).resize((max(1, round(body.shape[1] * sbw)), max(1, round((h - c) * sbh))), Image.LANCZOS)
    w = max(H.width, Bd.width); out = Image.new('RGBA', (w, H.height + Bd.height - 1))
    out.alpha_composite(Bd, ((w - Bd.width) // 2, H.height - 1)); out.alpha_composite(H, ((w - H.width) // 2, 0))
    a = np.array(out); a[..., 3] = np.where(a[..., 3] > 110, 255, 0); return a

def place(a, bottom):
    cell = np.zeros((FH, FW, 4), np.uint8); h, w = a.shape[:2]
    if w > FW: a = a[:, (w - FW) // 2:(w - FW) // 2 + FW]; w = FW
    if h > bottom: a = a[h - bottom:]; h = bottom
    x = (FW - w) // 2; cell[bottom - h:bottom, x:x + w] = a; return cell

def pixelate(sheet, k):
    if k <= 1: k = 2   # 여자애들은 원래 픽셀이 잘아서 최소 2배로 굵게
    im = Image.fromarray(sheet); s = np.array(im.resize((im.width // k, im.height // k), Image.BOX))
    al = s[..., 3] > 110; s[..., 3] = np.where(al, 255, 0)
    edge = ndimage.binary_dilation(al) & ~al; s[edge] = [40, 26, 40, 255]   # 두꺼운 외곽선
    return np.array(Image.fromarray(s).resize((im.width, im.height), Image.NEAREST))

def match(g, b, fr):
    gs, bs = load(g, BASE), load(b, BASE if b != 'meroko' else None)
    bf = bs[:FH, :FW]
    out = np.zeros_like(gs); n = fr[g]; sc = scales(gs[:FH, :FW], bf)
    for r in range(4):
        for c in range(n[r]):
            f = gs[r * FH:(r + 1) * FH, c * FW:(c + 1) * FW]
            if not (f[..., 3] > 0).any(): continue
            _, fb, _, _ = bbox(f)
            out[r * FH:(r + 1) * FH, c * FW:(c + 1) * FW] = place(reshape(f, sc), fb)
    out = pixelate(out, 2)   # 남자애들 실제 굵기는 2배 정도 (3배는 얼굴이 뭉개져요)
    Image.fromarray(out).save(f'docs/assets/ch/{g}.webp', 'WEBP', lossless=True)
    return tuple(round(float(x), 2) for x in sc)

if __name__ == '__main__':
    G = json.load(open('docs/data/girls.json')); fr = json.load(open('docs/data/frames.json'))
    want = set(sys.argv[1:])
    for x in G:
        g = x['id']
        if g in SKIP or (want and g not in want) or not x.get('pair'): continue
        b = list(x['pair'])[0]; print(g, b, match(g, b, fr))
