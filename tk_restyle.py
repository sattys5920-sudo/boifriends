# 굵은 픽셀 그림체(큰 머리, 짧은 몸, 두꺼운 외곽선)에 맞춰 다시 만들어요. 사용: python3 tk_restyle.py <id> <머리배율> <몸배율> <픽셀> <left칸> <right칸> [mirror]
import sys; sys.path.insert(0,'/home/user/boifriends')
import numpy as np, tk_magenta as M, tk_chars as T, tk_whiten as W
from PIL import Image
from scipy import ndimage
# 메로코 원본 칸을 '머리 크게, 몸 짧게' 다시 짜고, 이즈미처럼 굵은 픽셀 + 두꺼운 외곽선으로
CID=sys.argv[1]; HEAD=float(sys.argv[2]); BODY=float(sys.argv[3]); PIX=int(sys.argv[4])
P=lambda t:[tuple(map(int,x.split(','))) for x in t.split(';')]
LP=P(sys.argv[5]); RP=P(sys.argv[6]); MIR=len(sys.argv)>7
def chin(f):
    # 목(가장 좁은 곳)을 머리/몸 경계로: 위 35~60% 구간에서 너비가 가장 좁은 줄
    # 피부(얼굴)가 끝나는 줄 = 턱. 머리카락·날개 때문에 너비로는 못 찾아서 피부색으로
    R,G,B=[f[...,i].astype(int) for i in range(3)]; al=f[...,3]>0; h=al.shape[0]
    sk=al&(R>215)&(G>175)&(B>145)&(R-B>15)&(R-G<60)
    rows=np.nonzero(sk[:int(h*.6)].sum(1)>3)[0]
    return int(rows.max())+2 if len(rows) else int(h*.45)
def reshape(f):
    c=chin(f); head=Image.fromarray(f[:c]); body=Image.fromarray(f[c:])
    hw,hh=head.size; bw,bh=body.size
    head=head.resize((int(hw*HEAD),int(hh*HEAD)),Image.LANCZOS); body=body.resize((bw,int(bh*BODY)),Image.LANCZOS)
    W_=max(head.width,body.width); out=Image.new('RGBA',(W_,head.height+body.height-2))
    out.alpha_composite(body,((W_-body.width)//2,head.height-2)); out.alpha_composite(head,((W_-head.width)//2,0))
    return np.array(out)
orig=M.cells
def cells2(path,cols=5,rows=4):
    return [[reshape(f) for f in r] for r in orig(path,cols,rows)]
M.cells=cells2
M.build(CID,f'chars_src/{CID}.png',pick={'down':[(0,k) for k in range(4)],'up':[(1,k) for k in range(4)],'left':LP,'right':RP})
fw,fh=96,132; a=np.array(Image.open(f'docs/assets/ch/{CID}.webp').convert('RGBA'))
if MIR:
    for k in range(len(RP)): a[2*fh:3*fh,k*fw:(k+1)*fw]=a[3*fh:4*fh,k*fw:(k+1)*fw][:, ::-1]
# 굵은 픽셀: 1/PIX로 줄였다가 NEAREST로 키우기 + 두꺼운 외곽선
im=Image.fromarray(a); sm=im.resize((im.width//PIX,im.height//PIX),Image.BOX); s=np.array(sm)
al=s[...,3]>110; s[...,3]=np.where(al,255,0)
edge=ndimage.binary_dilation(al)&~al
s[edge]=[40,26,40,255]
big=Image.fromarray(s).resize((im.width,im.height),Image.NEAREST)
big.save(f'docs/assets/ch/{CID}.webp','WEBP',lossless=True)
