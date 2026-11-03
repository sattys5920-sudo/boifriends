"""예전 그림체 남자애를 새 그림체 남자애들 크기·비율·외곽선에 맞춰요.
사용: python3 tk_fit_boy.py <id>   (기준: 새로 뽑은 남자애들의 평균 키·머리 비율)"""
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
import tk_match as T
FW, FH = 96, 132
REF = ['mole', 'blonde_student', 'blue', 'punk', 'mint', 'bartender']
def target():
    ms = [T.measure(T.load(i)[:FH, :FW]) for i in REF]
    fw, tw, c, h = [float(np.mean([m[k] for m in ms])) for k in range(4)]
    return fw, tw, c, h
def fit(cid):
    a = T.load(cid); fr = json.load(open('docs/data/frames.json'))[cid]
    fw, tw, c, h = target(); nfw, ntw, nc, nh = T.measure(a[:FH, :FW])
    sh = c / nc; sbh = (h - c) / max(nh - nc, 1); sbw = np.clip(tw / max(ntw, 1), .9, 1.4)
    sc = (sh, sbh, sbw, nc / nh); out = np.zeros_like(a)
    for r in range(4):
        for k in range(fr[r]):
            f = a[r * FH:(r + 1) * FH, k * FW:(k + 1) * FW]
            if not (f[..., 3] > 0).any(): continue
            _, fb, _, _ = T.bbox(f); out[r * FH:(r + 1) * FH, k * FW:(k + 1) * FW] = T.place(T.reshape(f, sc), fb)
    # 외곽선: 바깥 테두리의 새까만 픽셀을 새 그림체의 남보라(#382840)로
    al = out[..., 3] > 0; edge = al & ~ndimage.binary_erosion(al, iterations=2)
    dk = out[..., :3].max(2) < 70
    out[edge & dk, :3] = [56, 40, 64]
    Image.fromarray(out).save(f'docs/assets/ch/{cid}.webp', 'WEBP', lossless=True)
    return [round(float(x), 2) for x in sc]
if __name__ == '__main__':
    print(fit(sys.argv[1]))
