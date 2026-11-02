#!/bin/sh
# 전체 다시 만들기: 맵 → 캐릭터 → 게임 데이터 → 페이지(tk_world/index.html)
set -e
cd "$(dirname "$0")"
mkdir -p out
for f in maps/*.py; do python3 "$f"; done
python3 tk_npcs.py
python3 tk_chars.py
python3 tk_world_build.py
rm -rf tk_world/lpc && cp -r lpc_parts tk_world/lpc
python3 - <<'PY'
import base64
f = base64.b64encode(open('fonts/Galmuri11.full.woff2', 'rb').read()).decode()
open('tk_world/index.html', 'w').write(open('tk_world_tpl.html').read().replace('__GALMURI__', f))
PY
echo "done: tk_world/index.html"
