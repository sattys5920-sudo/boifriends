"""피부색 픽셀만 밝게(미백). 쿄고쿠 마코토처럼 원래 까무잡잡한 캐릭터는 빼요.
사용: python3 tk_whiten.py id1,id2 (all = 전체)"""
import numpy as np, sys
from PIL import Image
def whiten(a, k=.22):
    a=a.copy(); R,G,B=[a[...,i].astype(float) for i in range(3)]; al=a[...,3]>0
    sk=al&(R>140)&(R>=G)&(G>=B)&((R-B)>18)&((R-B)<120)&((G-B)>6)&((R-G)<70)&(R+G+B>420)
    for i in range(3):
        c=a[...,i].astype(float); c=np.where(sk, c+(255-c)*k, c); a[...,i]=np.clip(c,0,255).astype(np.uint8)
    # 붉은 기 살짝 줄이기
    r=a[...,0].astype(float); g=a[...,1].astype(float); a[...,0]=np.where(sk, np.clip(r-(r-g)*.12,0,255), r).astype(np.uint8)
    return a, sk.sum()
SKIP = {'karate'}
def apply(id, k=.22):
    if id in SKIP: return
    p = f'docs/assets/ch/{id}.webp'; a = np.array(Image.open(p).convert('RGBA')); b, _ = whiten(a, k)
    Image.fromarray(b).save(p, 'WEBP', lossless=True)
if __name__ == '__main__':
    import json
    ids = sys.argv[1].split(',')
    if ids == ['all']: ids = list(json.load(open('docs/data/frames.json')))
    for i in ids: apply(i)
    print('whitened', len([i for i in ids if i not in SKIP]))
