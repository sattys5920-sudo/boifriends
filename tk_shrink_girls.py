"""여자애들을 남자애 평균 키의 RATIO 배로 줄여요 (발 위치 유지, 칸마다 같은 배율). 사용: python3 tk_shrink_girls.py [ratio]"""
import sys, json, numpy as np
from PIL import Image
FW, FH = 96, 132
RATIO = float(sys.argv[1]) if len(sys.argv) > 1 else .93
G = [g['id'] for g in json.load(open('docs/data/girls.json'))]; B = [c['id'] for c in json.load(open('docs/data/chars.json'))]
fr = json.load(open('docs/data/frames.json'))
def h(i):
    a = np.array(Image.open(f'docs/assets/ch/{i}.webp').convert('RGBA'))[:FH, :FW, 3] > 0; ys = np.nonzero(a)[0]; return ys.max() - ys.min() + 1
target = np.mean([h(i) for i in B]) * RATIO
for g in G:
    s = target / h(g)
    if s >= .995: print(g, 'skip'); continue
    p = f'docs/assets/ch/{g}.webp'; a = np.array(Image.open(p).convert('RGBA')); out = np.zeros_like(a)
    for r in range(4):
        for k in range(fr[g][r]):
            c = a[r*FH:(r+1)*FH, k*FW:(k+1)*FW]; al = c[..., 3] > 0
            if not al.any(): continue
            ys, xs = np.nonzero(al); bot = ys.max() + 1
            im = Image.fromarray(c[ys.min():bot, xs.min():xs.max()+1])
            sm = np.array(im.resize((max(1, round(im.width*s)), max(1, round(im.height*s))), Image.NEAREST))
            hh, ww = sm.shape[:2]; cx = (xs.min() + xs.max()) // 2; x0 = max(0, min(FW-ww, cx - ww//2))
            out[r*FH+bot-hh:r*FH+bot, k*FW+x0:k*FW+x0+ww] = sm
    Image.fromarray(out).save(p, 'WEBP', lossless=True); print(g, round(s, 3))
