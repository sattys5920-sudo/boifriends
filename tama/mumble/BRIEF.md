# 혼잣말 작성 지침

폰 다마고치 앱에서 남자 캐릭터가 방 안을 돌아다니며 말풍선으로 중얼거리는 혼잣말이다. 플레이어에게 하는 말이 아니라 혼자 하는 말.
- 한 줄 = 짧은 한 문장 (말풍선에 들어가게 20자 안팎, 최대 26자).
- 원작 말투·말버릇·1인칭·어미를 최대한 살린다. 원작 대사를 길게 베끼지 말고 그 말투로 새로 쓴다.
- 좋아하는 것/싫어하는 것, 원작 설정(가족·친구·직업·취미)을 자연스럽게 녹인다.
- 모든 캐릭터는 성인(20대 이상)으로 다룬다. 학생 캐릭터는 학창 시절을 추억으로.
- 같은 캐릭터 안에서 문장·표현이 겹치지 않게. 다른 캐릭터와도 비슷한 문장 금지.
- 사이키 쿠스오는 텔레파시라 모든 줄을 ( )로 감싼다.

카테고리와 개수 (캐릭터마다):
- normal: 평소 혼잣말 16줄
- hungry: 배고플 때 4줄
- sleepy: 졸릴 때 4줄
- bored: 심심할 때 4줄
- dirty: 씻어야 할 때(꼬질꼬질) 3줄
- happy: 기분 좋을 때 4줄
- night: 밤(자기 전·새벽) 3줄

출력: /home/user/boifriends/tama/mumble/<id>.json 하나씩, 정확히 이 형태:
{"id":"<id>","normal":[16개],"hungry":[4],"sleepy":[4],"bored":[4],"dirty":[3],"happy":[4],"night":[3]}
작성 후 검증:
python3 -c "import json,sys;d=json.load(open(sys.argv[1]));n={'normal':16,'hungry':4,'sleepy':4,'bored':4,'dirty':3,'happy':4,'night':3};assert all(len(d[k])==v for k,v in n.items());a=sum((d[k] for k in n),[]);assert len(set(a))==len(a);assert max(map(len,a))<=26,max(a,key=len)" <파일>
