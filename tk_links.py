# 맵 연결표: 맵 가장자리 출구(걸어서 넘어감) + 역/트램(눌러서 이동)
#   edge: (to, label, side, a0, a1)  side = 'W'(x=0) 'E'(x=NX-1) 'N'(y=0) 'S'(y=NY-1), a0~a1 = 지나갈 수 있는 칸 범위
#   상대 맵의 spawn은 그 맵에서 나를 가리키는 출구 안쪽 2칸으로 자동 계산해요
SIZES = {'tk_street': (48, 28), 'tk_school': (44, 36), 'tk_shibuya': (44, 34), 'tk_harajuku': (40, 36), 'tk_ikebukuro': (42, 36),
         'tk_asakusa': (40, 36), 'tk_ginza': (44, 34), 'tk_roppongi': (44, 34), 'tk_inaka': (46, 36), 'acca_badon': (44, 34), 'acca_dowa': (44, 36), 'tk_geofront': (44, 36)}
LABELS = {'tk_street': '우리 동네', 'tk_school': '학교', 'tk_shibuya': '시부야', 'tk_harajuku': '하라주쿠', 'tk_ikebukuro': '이케부쿠로', 'tk_asakusa': '아사쿠사',
          'tk_ginza': '긴자', 'tk_roppongi': '롯폰기', 'tk_inaka': '시골 마을', 'acca_badon': '바동', 'acca_dowa': '도와', 'tk_geofront': '지오프론트'}
EDGES = {
    'tk_street':    [('tk_school', 'W', 11, 17), ('tk_shibuya', 'E', 11, 17)],
    'tk_school':    [('tk_street', 'E', 31, 35)],
    'tk_shibuya':   [('tk_street', 'W', 13, 21), ('tk_roppongi', 'E', 13, 21), ('tk_harajuku', 'N', 17, 25)],
    'tk_harajuku':  [('tk_shibuya', 'S', 15, 21), ('tk_ikebukuro', 'N', 17, 21)],
    'tk_ikebukuro': [('tk_harajuku', 'W', 10, 18), ('tk_asakusa', 'E', 10, 18)],
    'tk_asakusa':   [('tk_ikebukuro', 'W', 31, 35), ('tk_ginza', 'E', 31, 35)],
    'tk_ginza':     [('tk_asakusa', 'N', 17, 25), ('tk_roppongi', 'W', 13, 20)],
    'tk_roppongi':  [('tk_shibuya', 'W', 13, 21), ('tk_ginza', 'E', 13, 21)],
    'tk_inaka':     [('tk_geofront', 'E', 10, 12)],
    'tk_geofront':  [('tk_inaka', 'W', 15, 19)],
    'acca_badon':   [('acca_dowa', 'E', 18, 21)],
    'acca_dowa':    [('acca_badon', 'S', 19, 24)],
}
# 역·트램: (맵, 문 이름표, 도착 맵, 도착 칸)
TRAINS = {
    'tk_shibuya':   ('시부야역 · 시골 마을행 열차', 'tk_inaka', [21, 12]),
    'tk_inaka':     ('역 · 시부야행 열차', 'tk_shibuya', [8, 10]),
    'tk_ikebukuro': ('이케부쿠로역 · 도와 왕국행 국제 열차', 'acca_badon', [35, 22]),
    'acca_badon':   ('트램 · 도쿄 이케부쿠로행', 'tk_ikebukuro', [8, 10]),
}
def edge_spawn(me, other):
    """other 맵에 들어갈 때 설 칸: other에서 me로 가는 출구 안쪽"""
    nx, ny = SIZES[other]
    for (to, side, a0, a1) in EDGES[other]:
        if to != me: continue
        m = (a0 + a1) // 2
        return {'W': [2, m], 'E': [nx - 3, m], 'N': [m, 2], 'S': [m, ny - 3]}[side]
    return None
