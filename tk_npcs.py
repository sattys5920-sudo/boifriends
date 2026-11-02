# 도쿄·ACCA 맵에 세울 2등신 캐릭터 9명(+ 걷는 나) : out/tk_npcs.png (한 칸 24x36, 2프레임) + out/tk_npcs.json
#   그림은 사용자가 만든 캐릭터 설명(머리·안경·옷·소품)을 앱 크기에 맞춰 직접 찍은 도트예요
import json, os
from PIL import Image, ImageDraw
os.chdir(os.path.dirname(os.path.abspath(__file__)))
FW, FH = 24, 36
OUT = (28, 20, 32, 255)
def hx(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5)) + (255,)
def sh(c, k): return tuple(max(0, min(255, int(v * k))) for v in c[:3]) + (255,)

def draw_char(c, bob=0):
    img = Image.new('RGBA', (FW, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    R = lambda x0, y0, x1, y1, col: d.rectangle([x0, y0 - bob if y0 < 26 else y0, x1, y1 - bob if y1 < 26 else y1], fill=col)
    skin = hx(c.get('skin', '#F6DCC8'))
    # 다리·신발
    legs = hx(c['legs']); shoes = hx(c.get('shoes', '#2A2A30'))
    if c.get('long_coat'):
        R(8, 22, 15, 30, hx(c['top']))
    R(9, 26, 10, 32, legs); R(13, 26, 14, 32, legs)
    if c.get('rips'): d.point((9, 29), fill=skin); d.point((14, 29), fill=skin)
    if c.get('barefoot'): R(8, 33, 10, 34, skin); R(13, 33, 15, 34, skin)
    else: R(8, 33, 11, 34, shoes); R(12, 33, 15, 34, shoes)
    # 몸통
    top = hx(c['top'])
    R(7, 19, 16, 26, top); R(5, 20, 6, 25, top); R(17, 20, 18, 25, top)
    R(5, 26, 6, 26, skin); R(17, 26, 18, 26, skin)
    if c.get('band'): R(7, 24, 16, 26, hx(c['band']))
    if c.get('inner'):   # 열린 앞섶(셔츠·티)
        R(10, 19, 13, 25, hx(c['inner']))
        if c.get('stripes'):
            for x in (10, 12): R(x, 19, x, 25, hx(c['stripes']))
    if c.get('vest'): R(7, 21, 9, 26, hx(c['vest'])); R(14, 21, 16, 26, hx(c['vest'])); R(10, 23, 13, 26, hx(c['vest']))
    if c.get('tie'): R(11, 20, 12, 24, hx(c['tie']))
    if c.get('bowtie'): R(9, 19, 10, 20, hx(c['bowtie'])); R(13, 19, 14, 20, hx(c['bowtie'])); R(11, 19, 12, 20, sh(hx(c['bowtie']), 1.4))
    if c.get('belt'): R(7, 24, 16, 24, hx(c['belt'])); R(12, 25, 12, 27, hx(c['belt']))
    if c.get('chain'):
        for (x, y) in ((9, 20), (10, 21), (11, 22), (12, 22), (13, 21), (14, 20)): d.point((x, y - bob), fill=hx('#D8DCE4'))
        R(11, 23, 12, 24, hx('#C8CCD4'))
    if c.get('scarf'):
        R(7, 17, 16, 19, hx(c['scarf'])); R(13, 19, 14, 23, hx(c['scarf']))
        for x in range(7, 17, 3): d.point((x, 18 - bob), fill=hx('#C8302A'))
    if c.get('emblem'): d.point((14, 21 - bob), fill=hx(c['emblem']))
    if c.get('collar'): R(9, 18, 14, 19, hx(c['collar']))
    # 머리
    R(5, 6, 18, 18, skin)
    R(4, 9, 4, 14, skin); R(19, 9, 19, 14, skin)
    hair = hx(c['hair']); hl = sh(hair, 1.35); style = c['style']
    if style == 'spiky':
        R(4, 4, 19, 8, hair); R(4, 8, 5, 12, hair); R(18, 8, 19, 12, hair)
        for (x, y) in ((4, 2), (7, 1), (10, 0), (13, 1), (16, 1), (19, 3), (2, 6), (21, 6)): d.polygon([(x - 2, y + 4 - bob), (x, y - bob), (x + 2, y + 4 - bob)], fill=hair)
        R(7, 8, 10, 9, hair); R(12, 8, 15, 10, hair); d.point((9, 3 - bob), fill=hl); d.point((14, 3 - bob), fill=hl)
    elif style == 'buzz':
        R(5, 3, 18, 7, hair); R(4, 6, 5, 10, hair); R(18, 6, 19, 10, hair)
        for x in range(5, 19, 2): d.point((x, 2 - bob), fill=hair)
        R(10, 7, 11, 9, hair)
    elif style == 'curly':
        for (x, y, r) in ((5, 6, 3), (9, 3, 3), (14, 3, 3), (18, 6, 3), (4, 10, 2), (19, 10, 2), (7, 5, 2), (12, 4, 3), (16, 5, 2), (4, 13, 2), (19, 13, 2), (8, 8, 2), (15, 8, 2), (11, 8, 2)):
            d.ellipse([x - r, y - r - bob, x + r, y + r - bob], fill=hair)
        for (x, y) in ((8, 3), (13, 2), (17, 5), (5, 9), (11, 6)): d.point((x, y - bob), fill=hl)
    elif style == 'wavy':
        R(4, 3, 19, 8, hair); R(3, 6, 5, 15, hair); R(18, 6, 20, 15, hair)
        for (x, y) in ((3, 4), (8, 2), (14, 2), (20, 4), (2, 15), (21, 15)): d.ellipse([x - 2, y - 2 - bob, x + 2, y + 2 - bob], fill=hair)
        R(6, 8, 8, 9, hair); d.point((10, 4 - bob), fill=hl); d.point((15, 4 - bob), fill=hl)
    else:   # short / messy (앞머리)
        R(4, 3, 19, 8, hair); R(4, 8, 5, 13, hair); R(18, 8, 19, 13, hair)
        for x in range(5, 18, 3): R(x, 8, x + 1, 10 if style == 'messy' else 9, hair)
        d.point((3, 5 - bob), fill=hair); d.point((20, 5 - bob), fill=hair); d.point((9, 4 - bob), fill=hl); d.point((14, 4 - bob), fill=hl)
    # 눈
    eye = c.get('eyes', 'normal'); y = 12
    if eye == 'shades':
        R(6, y - 1, 17, y + 1, hx(c.get('lens', '#101018'))); d.point((8, y - 1 - bob), fill=hx('#FFFFFF')); d.point((15, y - 1 - bob), fill=hx('#FFFFFF'))
    elif eye == 'glasses':
        for x0 in (6, 12): d.rectangle([x0, y - 2 - bob, x0 + 5, y + 1 - bob], outline=OUT, fill=hx('#E8F0FF'))
        d.point((8, y - 1 - bob), fill=OUT); d.point((15, y - 1 - bob), fill=OUT)
    elif eye == 'sleepy':
        R(7, y, 9, y, OUT); R(14, y, 16, y, OUT); d.point((8, y + 1 - bob), fill=hx('#8A8E96')); d.point((15, y + 1 - bob), fill=hx('#8A8E96'))
    elif eye == 'smile':
        d.point((7, y - bob), fill=OUT); d.point((8, y - 1 - bob), fill=OUT); d.point((9, y - bob), fill=OUT)
        d.point((14, y - bob), fill=OUT); d.point((15, y - 1 - bob), fill=OUT); d.point((16, y - bob), fill=OUT)
    else:
        R(8, y - 1, 8, y + 1, hx(c.get('eyec', '#2A2228'))); R(15, y - 1, 15, y + 1, hx(c.get('eyec', '#2A2228')))
    if c.get('blush'): d.point((6, 14 - bob), fill=hx('#F4B4B0')); d.point((17, 14 - bob), fill=hx('#F4B4B0'))
    # 입
    m = c.get('mouth', 'flat')
    if m == 'smile': R(10, 15, 13, 15, OUT); d.point((9, 14 - bob), fill=OUT); d.point((14, 14 - bob), fill=OUT)
    elif m == 'smirk': R(11, 15, 13, 15, OUT); d.point((14, 14 - bob), fill=OUT)
    else: R(11, 15, 12, 15, OUT)
    if c.get('mole'): d.point((9, 15 - bob), fill=hx('#3A2420'))
    if c.get('bandage'): R(15, 7, 17, 8, hx('#F8E4C8')); d.point((16, 7 - bob), fill=hx('#C8A480'))
    if c.get('cig'): R(14, 15, 17, 15, hx('#FFFFFF')); d.point((18, 15 - bob), fill=hx('#FF6A30'))
    # 로봇 전용
    if c.get('robot'):
        img = Image.new('RGBA', (FW, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
        d.ellipse([3, 1 - bob, 20, 18 - bob], fill=hx('#F4F6FA')); d.ellipse([5, 2 - bob, 13, 8 - bob], fill=hx('#FFFFFF'))
        d.arc([4, 0 - bob, 19, 14 - bob], 200, 340, fill=hx('#3A5AD8'), width=2)
        d.ellipse([0, 6 - bob, 5, 13 - bob], fill=hx('#F2A020')); d.ellipse([18, 6 - bob, 23, 13 - bob], fill=hx('#F2A020'))
        d.rectangle([4, 10 - bob, 19, 13 - bob], fill=hx('#1A1A24')); d.rectangle([8, 11 - bob, 8, 12 - bob], fill=hx('#FFFFFF')); d.rectangle([15, 11 - bob, 15, 12 - bob], fill=hx('#FFFFFF'))
        d.rectangle([8, 19, 15, 26], fill=hx('#E8ECF4')); d.ellipse([10, 21, 13, 24], outline=hx('#5A5E6A'))
        d.ellipse([4, 20, 7, 24], fill=hx('#F4F6FA')); d.ellipse([16, 20, 19, 24], fill=hx('#F4F6FA'))
        d.rectangle([9, 27, 10, 30], fill=hx('#3A5AD8')); d.rectangle([13, 27, 14, 30], fill=hx('#3A5AD8'))
        d.ellipse([6, 30, 11, 34], fill=hx('#3A5AD8')); d.ellipse([12, 30, 17, 34], fill=hx('#3A5AD8'))
    # 테두리
    a = img.load(); add = []
    for yy in range(FH):
        for xx in range(FW):
            if a[xx, yy][3] == 0 and any(0 <= xx + dx < FW and 0 <= yy + dy < FH and a[xx + dx, yy + dy][3] > 200 and a[xx + dx, yy + dy][:3] != OUT[:3] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): add.append((xx, yy))
    for p in add: a[p] = OUT
    return img

CHARS = [
    dict(id='robot', name='로봇 마스코트', map='tk_street', tile=[21, 18], robot=True, style='short', hair='#FFFFFF', top='#FFFFFF', legs='#3A5AD8',
         lines=['삐빅! 어서 와, 여기는 우리 동네야.', '동쪽 길로 쭉 가면 시부야, 서쪽 길로 가면 학교가 나와.', '길 끝에 있는 파란 표지판 사이로 걸어가면 다음 동네로 넘어가. 삐빅!']),
    dict(id='blue', name='파란 머리 남자', map='acca_badon', tile=[6, 17], style='spiky', hair='#2E8FB5', eyes='shades', mouth='smirk', top='#1E1E26', collar='#2A2A34', legs='#2E3A66', shoes='#2A2A30',
         lines=['…운하 바람이 좋네.', '바동은 처음이야? 저 하얀 건물이 ACCA 본부야.', '도와 쪽으로 가려면 트램 길을 따라 동쪽 끝까지 가 봐.', '정류장 옆 가판대에서 담배 한 개비 사 오면 더 얘기해 줄게.']),
    dict(id='curly_suit', name='곱슬머리 정장 남자', map='tk_asakusa', tile=[32, 17], style='wavy', hair='#3A3532', eyes='sleepy', mouth='smirk', cig=True, top='#2A2A30', inner='#F0E6DC', stripes='#C8603C', tie='#C89048', legs='#2A2A30', shoes='#141418',
         lines=['강 보러 왔어? 여기 앉아서 멍하니 있기 좋지.', '나는 그냥… 일 쉬는 중이야. 비밀로 해 줘.', '참배길 노점 당고는 꼭 먹어 봐. 세 번째 가게가 제일이야.']),
    dict(id='blonde_student', name='금발 교복 남학생', map='tk_school', tile=[18, 10], style='messy', hair='#DCC488', mouth='flat', top='#343A4C', inner='#FFFFFF', tie='#D8404C', legs='#6A6A72', shoes='#FFFFFF', vest='#A8A8AC',
         lines=['……스읍.', '아, 책상 위에 뭐가 있었는데 누가 잘못 둔 것 같아서 옆으로 치워 뒀어.', '…수업 종 울리기 전에 들어가.']),
    dict(id='mole', name='점 있는 스웨터 청년', map='tk_harajuku', tile=[18, 24], style='short', hair='#22222E', eyes='smile', mouth='smile', mole=True, blush=True, top='#E8DCA0', band='#6A5444', collar='#F4C8D0', emblem='#8A2040', legs='#262E5A', shoes='#8A5A3A',
         lines=['어, 안녕! 여기 크레페 진짜 맛있어.', '다케시타 거리는 주말엔 사람이 너무 많아서 평일에 오는 게 좋아.', '북쪽 숲길 도리이 지나면 이케부쿠로로 가는 길이 나와.']),
    dict(id='punk', name='펑크 록커', map='tk_shibuya', tile=[8, 27], style='buzz', hair='#3A2A26', eyes='sleepy', mouth='smirk', cig=True, top='#33325A', inner='#FFFFFF', chain=True, legs='#8088C4', rips=True, shoes='#141418',
         lines=['…뭐야, 구경 왔어?', '오늘 밤에 이 근처 지하 라이브하우스에서 공연 있어. 기타는 내가 쳐.', '표는 없어. 그냥 와. 문 앞에서 내 이름 대면 돼.']),
    dict(id='bartender', name='금발 바텐더', map='tk_ikebukuro', tile=[18, 22], style='messy', hair='#E8D070', eyes='shades', lens='#3A3A90', mouth='flat', cig=True, top='#FFFFFF', vest='#42464E', bowtie='#101014', legs='#42464E', shoes='#141418',
         lines=['…이 동네에서 소란 피우지 마라. 피곤하니까.', '자판기? …아니, 던질 생각 없어. 마실 거야.', '동쪽으로 가면 아사쿠사. 서쪽 길은 하라주쿠야.']),
    dict(id='curly_coat', name='곱슬머리 코트 청년', map='tk_roppongi', tile=[8, 11], style='curly', hair='#22222E', eyes='normal', mouth='flat', top='#F0E6D0', long_coat=True, scarf='#F8A830', legs='#3A3A44', shoes='#8A5A3A',
         lines=['미술관에 들렀다 가는 길이에요.', '그림을 보면, 그린 사람이 무엇을 숨기고 싶었는지가 보일 때가 있어요.', '…아, 제가 또 혼자 너무 길게 얘기했네요.']),
    dict(id='karate', name='가라테 소년', map='tk_inaka', tile=[35, 19], style='buzz', hair='#22222E', skin='#C48C5C', eyes='glasses', mouth='flat', bandage=True, top='#FFFFFF', inner='#C48C5C', belt='#1C1C22', legs='#F4F4F0', barefoot=True,
         lines=['오스!', '이 신사 계단을 매일 아침 100번 오르내리는 게 수련이야.', '시골 공기가 좋아서 집중이 잘 돼. 너도 같이 뛸래?']),
]
PLAYER = dict(id='me', name='나', style='short', hair='#5A3E2E', eyes='normal', mouth='smile', top='#3E6A9A', inner='#FFFFFF', legs='#3A3A44', shoes='#E8E8E8')
if __name__ == '__main__':
    allc = CHARS + [PLAYER]
    sheet = Image.new('RGBA', (FW * 2, FH * len(allc)), (0, 0, 0, 0))
    for i, c in enumerate(allc):
        for f in range(2): sheet.paste(draw_char(c, f), (f * FW, i * FH))
    os.makedirs('out', exist_ok=True); sheet.save('out/tk_npcs.png')
    json.dump(dict(FW=FW, FH=FH, chars=[dict(id=c['id'], name=c['name'], map=c.get('map'), tile=c.get('tile'), row=i, lines=c.get('lines', [])) for i, c in enumerate(allc)]),
              open('out/tk_npcs.json', 'w'), ensure_ascii=False)
    sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST).save('out/tk_npcs_preview.png')
    print('npcs', len(allc))
