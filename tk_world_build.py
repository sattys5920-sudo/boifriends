# 도쿄·ACCA 맵 11개 + 캐릭터를 걷기 미리보기(tk_world/)용으로 묶어요
#   python3 tk_world_build.py  (먼저 maps/*.py, tk_npcs.py 실행) → tk_world/maps/*.png, tk_world/data.json
import json, os, shutil
os.chdir(os.path.dirname(os.path.abspath(__file__)))
exec(open('tk_links.py').read())
OUTD = 'tk_world'; os.makedirs(OUTD + '/maps', exist_ok=True)
maps = {}
for name in SIZES:
    j = json.load(open(f'out/{name}.json'))
    for k in ('bg', 'obj'): shutil.copy(f'out/{name}_{k}.png', f'{OUTD}/maps/{name}_{k}.png')
    objs = [dict(n=o['name'], b=o['box'], s=[o['sx'], o['sy'], o['sw'], o['sh']], p=[o['x'], o['y']], door=o['door'], solid=o['solid'], act=o['act']) for o in j['objs']]
    maps[name] = dict(label=LABELS[name], W=j['W'], H=j['H'], NX=j['NX'], NY=j['NY'], OX=j['OX'], OY=j['OY'], objs=objs, areas=j['areas'], water=j['water'], start=j['start'])
npcs = json.load(open('out/tk_chars.json')); shutil.copy('out/tk_chars.png', f'{OUTD}/chars.png')
if os.path.exists(f'{OUTD}/npcs.png'): os.remove(f'{OUTD}/npcs.png')
# 검사: 캐릭터 칸·출구 도착 칸이 막혀 있지 않은지
def blocked(m):
    s = {tuple(t) for t in m['water']}
    for o in m['objs']:
        if o['solid'] and o['b'][2] > o['b'][0]:
            for x in range(o['b'][0], o['b'][2]):
                for y in range(o['b'][1], o['b'][3]): s.add((x, y))
    return s
bad = []
for c in npcs['chars']:
    if c['map'] and tuple(c['tile']) in blocked(maps[c['map']]): bad.append(('npc', c['id'], c['map'], c['tile']))
for name, m in maps.items():
    for o in m['objs']:
        d = o['door']
        if d and (d.get('walk') or d.get('train')) and d.get('spawn') and tuple(d['spawn']) in blocked(maps[d['to']]): bad.append(('spawn', name, '->', d['to'], d['spawn']))
    if tuple(m['start']) in blocked(m): bad.append(('start', name, m['start']))
print('problems:', bad or 'none')
story = json.load(open('tk_story.json')); story.pop('_doc', None)
# story/<id>/ 폴더(긴 이야기 v2)가 있으면 그 캐릭터 데이터를 덮어써요
SD = 'story'
for cid in sorted(os.listdir(SD)) if os.path.isdir(SD) else []:
    d = os.path.join(SD, cid)
    if not os.path.isfile(os.path.join(d, 'meta.json')): continue
    meta = json.load(open(os.path.join(d, 'meta.json'))); routes = {}
    for rt in ('love', 'match'):
        chs = []
        for i in range(1, 11):
            fn = os.path.join(d, f'{rt}_{i:02d}.json')
            if os.path.exists(fn): chs.append(json.load(open(fn)))
        if chs: routes[rt] = dict(title=meta[rt]['title'], endings=meta[rt]['endings'], chapters=chs)
    done = {k: v for k, v in routes.items() if len(v['chapters']) == 10}   # 10장이 다 있는 갈래만(쓰는 중인 건 건너뜀)
    if done and cid in story['chars']:
        S = story['chars'][cid]
        S['story'] = done; S['pair'] = meta['pair']; S['pairProfile'] = meta.get('pairProfile', S.get('pairProfile', ''))
        S.setdefault('after', {}).update({k: v for k, v in meta.get('after', {}).items() if k in done})
        if 'routes' in S: S['routes'] = {k: v for k, v in S['routes'].items() if k not in done}
        print('story v2:', cid, {k: len(v['chapters']) for k, v in done.items()})
json.dump(dict(maps=maps, chars=npcs, story=story, home='tk_street', player='me'), open(f'{OUTD}/data.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('maps', len(maps), 'bytes', os.path.getsize(f'{OUTD}/data.json'))
