# boifriends

도쿄·도와 왕국을 걸으며 캐릭터에게 말을 걸고, 사귀거나 짝을 찾아주는 로그라이크 미연시.

- 게임 페이지: `tk_world/` (claude.ai 아티팩트로 게시. 세이브는 아티팩트 서버의 개인 칸에 저장)
- 전체 다시 만들기: `./build.sh` (Python 3 + Pillow, numpy, scipy)

## 폴더
| 경로 | 내용 |
|---|---|
| `maps/*.py` | 맵 13개 생성 코드 (`tk_lib.py` 공용 도구, `world.py` 그리기 기본기) |
| `tk_links.py` | 맵 연결(걸어서 넘어가는 길, 열차) |
| `chars_src/` | 캐릭터 시트 원본, `tk_chars.py`가 잘라서 4방향 걷기 그림으로 정리 |
| `tk_story.json` | 캐릭터 소개·짧은 장면·짝 |
| `story/<캐릭터id>/` | 10장짜리 긴 이야기. `*_src_N.txt`(대본 문법) → `python3 story_build.py <id> <love|match>` → `*_NN.json` |
| `story/SYNOPSIS.md` | 캐릭터별 이야기 뼈대 |
| `story/FORMAT.md` | 긴 이야기 데이터 형식, `story_check.py`로 검사 |
| `tk_world_tpl.html` | 게임 페이지 원본(엔진) |

글꼴: Galmuri11 (SIL OFL, `fonts/Galmuri-LICENSE.txt`)
