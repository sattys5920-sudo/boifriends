# 이야기 폴더 검사: python3 tools/iso/story_check.py <id> [<id>...]   (형식은 story/FORMAT.md)
import json, os, re, sys
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'story')
COND = re.compile(r'^(!?flag:[a-z0-9_]+|score>=\d+|day>=\d+)$')
def lines_in(beats, path, errs, flags_set, flags_used):
    n = 0
    for b in beats:
        if isinstance(b, list):
            if len(b) != 2 or not all(isinstance(x, str) for x in b) or not b[1].strip(): errs.append(f'{path}: 잘못된 대사 {b}')
            n += 1
        elif isinstance(b, dict) and 'choice' in b:
            if not (2 <= len(b['choice']) <= 4): errs.append(f'{path}: 선택지는 2~4개')
            for o in b['choice']:
                if not o.get('t'): errs.append(f'{path}: 선택지 문장 없음')
                for k in (o.get('fx') or {}):
                    if k not in ('love', 'match', 'hp', 'yen', 'gift'): errs.append(f'{path}: fx 키 {k}')
                for f in o.get('set', []): flags_set.add(f)
                n += lines_in(o.get('then', []), path, errs, flags_set, flags_used)
        elif isinstance(b, dict) and 'if' in b:
            if not COND.match(b['if']): errs.append(f'{path}: 조건 형식 {b["if"]}')
            if 'flag:' in b['if']: flags_used.add(b['if'].split(':')[1])
            n += max(lines_in(b.get('then', []), path, errs, flags_set, flags_used), lines_in(b.get('else', []), path, errs, flags_set, flags_used))
        else: errs.append(f'{path}: 알 수 없는 비트 {str(b)[:60]}')
    return n
def check(cid):
    errs, d = [], os.path.join(BASE, cid)
    try: meta = json.load(open(os.path.join(d, 'meta.json')))
    except Exception as e: return [f'meta.json: {e}'], {}
    for k in ('pair', 'pairProfile', 'intro', 'love', 'match', 'after'):
        if k not in meta: errs.append(f'meta: {k} 없음')
    stats = {}
    flags_set, flags_used = set(), set()
    for route in ('love', 'match'):
        tot = []
        for i in range(1, 11):
            fn = os.path.join(d, f'{route}_{i:02d}.json')
            try: ch = json.load(open(fn))
            except Exception as e: errs.append(f'{route}_{i:02d}: {e}'); continue
            if ch.get('route') != route or ch.get('no') != i: errs.append(f'{route}_{i:02d}: route/no 불일치')
            if ch.get('need'):
                if not COND.match(ch['need']): errs.append(f'{route}_{i:02d}: need 형식')
                if not ch.get('wait'): errs.append(f'{route}_{i:02d}: wait 없음')
            n = lines_in(ch.get('beats', []), f'{route}_{i:02d}', errs, flags_set, flags_used)
            nch = json.dumps(ch.get('beats', []), ensure_ascii=False).count('"choice"')
            if n < 85: errs.append(f'{route}_{i:02d}: 대사 {n}줄 (90줄 이상 필요)')
            if nch < 2: errs.append(f'{route}_{i:02d}: 선택지 {nch}번 (2번 이상 필요)')
            tot.append(n)
        ends = (meta.get(route) or {}).get('endings', [])
        if len(ends) < 3: errs.append(f'meta.{route}: 결말 3개 이상 필요')
        if ends and ends[-1].get('cond'): errs.append(f'meta.{route}: 마지막 결말 cond는 []')
        for e in ends:
            for c in e.get('cond', []):
                if not COND.match(c): errs.append(f'meta.{route} 결말 조건 {c}')
                if c.startswith('flag:') or c.startswith('!flag:'): flags_used.add(c.split(':')[1])
        stats[route] = tot
    for f in flags_used - flags_set: errs.append(f'플래그 {f}를 쓰는데 set하는 곳이 없음')
    return errs, stats
if __name__ == '__main__':
    ok = True
    for cid in sys.argv[1:]:
        errs, stats = check(cid)
        if errs: ok = False; print(cid, 'FAIL'); [print('  -', e) for e in errs[:40]]
        else: print(cid, 'OK', {k: sum(v) for k, v in stats.items()}, '줄')
    sys.exit(0 if ok else 1)
