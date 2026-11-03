# 여행 대사 작성 지침

앱: 폰 다마고치. 플레이어가 캐릭터를 해외여행 보내면, 캐릭터가 그 나라 풍경 앞을 걸으면서 말풍선으로 혼잣말을 한다(한 여행에 3개 랜덤).
- 캐릭터마다 12줄. 각 줄은 짧은 한 문장(말풍선용, 26자 이내).
- 나라 이름 자리표시자 {place}를 12줄 중 6줄 이상에 넣는다(예: "{place}까지 왔네."). 조사는 받침 상관없이 자연스럽게 읽히도록 "{place}에서", "{place}까지", "{place}의" 같은 형태만 쓰고 "{place}은/는/이/가/을/를"은 쓰지 않는다.
- 여행이 즐겁고 신난 느낌. 원작 말투·말버릇·좋아하는 것(chars.json의 li, likes)을 살린다. 사이키는 모든 줄을 ( )로 감싼다. 성인으로 다룬다.
- 다른 캐릭터와 겹치는 문장 금지. 맞춤법은 표준국어대사전 기준, 숫자 뒤 명사는 띄어 쓴다, 말줄임표는 "...."(짧게) 또는 "......."(길게)만 쓴다.
- 말투 참고: /home/user/boifriends/tama/dialogue/<id>.json 의 voice와 대사.
- 히든(hidden)은 능글맞고 쿨하고 여유로운 여자 말투, 커피를 좋아하고 단것을 싫어함.

출력: /home/user/boifriends/tama/travel/<id>.json  형태: {"id":"<id>","lines":[12개]}
검증: python3 -c "import json,sys;d=json.load(open(sys.argv[1]));l=d['lines'];assert len(l)==12 and len(set(l))==12 and max(map(len,l))<=30 and sum('{place}' in x for x in l)>=6" <파일>
