# story/<id>/<route>_src_N.txt (story_dsl 문법) → <route>_NN.json
#   python3 story_build.py curly_suit match
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from story_dsl import parse
cid, route = sys.argv[1], sys.argv[2]
d = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'story', cid)
for i in range(1, 11):
    fn = os.path.join(d, f'{route}_src_{i}.txt')
    if not os.path.exists(fn): continue
    t = open(fn).read(); head, rest = t.split('\n', 1)
    no, title = [x.strip() for x in head.strip('= ').split('|', 1)]
    ch = {'route': route, 'no': int(no), 'title': title}
    if '@need' in rest:
        need = rest.split('@need', 1)[1].split('\n', 1)[0].strip()
        wait = rest.split('@wait', 1)[1].split('@body', 1)[0]
        rest = rest.split('@body', 1)[1]
        ch['need'] = need; ch['wait'] = parse(wait)
    if '@night' in rest: ch['when'] = 'night'; rest = rest.replace('@night', '')
    ch['beats'] = parse(rest)
    json.dump(ch, open(os.path.join(d, f'{route}_{i:02d}.json'), 'w'), ensure_ascii=False, indent=1)
print('built')
