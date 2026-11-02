# 간단한 이야기 문법 → 장 JSON
#   c/p/n/me <문장>      대사 (c 캐릭터, p 짝, n 지문, me 주인공)
#   =이름 <문장>         그 밖의 인물
#   @choice / @opt 선택지 || match=10 hp=-1 || set=a,b / @end
#   @if 조건 / @else / @endif
#   # 로 시작하는 줄은 무시
import json, sys
def parse(text):
    root = []; stack = [root]; kinds = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith('#'): continue
        if s == '@choice':
            node = {'choice': []}; stack[-1].append(node); stack.append(node); kinds.append('choice'); continue
        if s.startswith('@opt'):
            if kinds[-1] == 'opt': stack.pop(); kinds.pop()
            parts = [x.strip() for x in s[4:].split('||')]
            o = {'t': parts[0], 'fx': {}, 'then': []}
            if len(parts) > 1 and parts[1]:
                for kv in parts[1].split(): k, v = kv.split('='); o['fx'][k] = int(v)
            if len(parts) > 2 and parts[2].startswith('set='): o['set'] = parts[2][4:].split(',')
            stack[-1]['choice'].append(o); stack.append(o['then']); kinds.append('opt'); continue
        if s == '@end':
            if kinds[-1] == 'opt': stack.pop(); kinds.pop()
            stack.pop(); kinds.pop(); continue
        if s.startswith('@if'):
            node = {'if': s[3:].strip(), 'then': [], 'else': []}; stack[-1].append(node); stack.append(node['then']); kinds.append(('if', node)); continue
        if s == '@else':
            stack.pop(); node = kinds[-1][1]; stack.append(node['else']); continue
        if s == '@endif':
            stack.pop(); kinds.pop(); continue
        if s.startswith('='):
            who, t = s[1:].split(' ', 1); stack[-1].append([who, t]); continue
        who, t = s.split(' ', 1); stack[-1].append([who, t])
    assert len(stack) == 1, 'unclosed block'
    return root
def chapter(route, no, title, body, when=None, need=None, wait=None):
    ch = {'route': route, 'no': no, 'title': title}
    if when: ch['when'] = when
    if need: ch['need'] = need; ch['wait'] = parse(wait)
    ch['beats'] = parse(body)
    return ch
