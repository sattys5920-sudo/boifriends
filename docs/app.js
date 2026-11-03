// 보이프렌즈 포켓 — 폰 다마고치
// 저장: Firebase 설정이 있으면 계정(서버)+이 기기, 없으면 이 기기에만.
const $ = s => document.querySelector(s);
const app = $('#app');
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clamp = v => Math.max(0, Math.min(100, Math.round(v)));
const today = () => { const d = new Date(); return `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`; };
const pick = a => a[Math.floor(Math.random() * a.length)];
function toast(t) { const el = $('#toast'); el.textContent = t; el.hidden = false; clearTimeout(toast.t); toast.t = setTimeout(() => el.hidden = true, 2200); }

// ---------- 데이터 ----------
const PAL = [['화이트', '#f7f9fb'], ['아이보리', '#fbf3df'], ['크림', '#f6e7c1'], ['연회색', '#d5dbe1'], ['회색', '#9aa5b1'], ['진회색', '#5b6672'], ['차콜', '#3a4049'], ['블랙', '#23262b'], ['베이지', '#e3cba8'], ['카멜', '#c99a6a'], ['브라운', '#8a5a3c'], ['초콜릿', '#5e3b28'], ['레드', '#e5534b'], ['코랄', '#ff8a75'], ['피치', '#ffc2a6'], ['오렌지', '#ffa04d'], ['머스타드', '#e2b33c'], ['레몬', '#ffe06b'], ['연두', '#c4e98a'], ['그린', '#6cc070'], ['올리브', '#8f9a4f'], ['민트', '#8fe3cc'], ['청록', '#3fb5b0'], ['하늘', '#8ccff5'], ['블루', '#4f8fe0'], ['네이비', '#2f4a7a'], ['라일락', '#c6b5ff'], ['보라', '#8b6bd6'], ['핑크', '#ff8fb3'], ['로즈', '#d9577f']];
const VAR = [['원래 색', 'conic-gradient(#ffd76a 0 25%,#8fe3cc 0 50%,#8ccff5 0 75%,#ff8fb3 0)']].concat(PAL);
const SHEET = { furn: { cw: 44, ch: 44, sw: 1364, sh: 440 }, deco: { cw: 44, ch: 24, sw: 1364, sh: 192 }, prop: { cw: 20, ch: 26, sw: 620, sh: 520 } };
const ITEMS = {
  wall: [['plain', '기본'], ['mintdot', '땡땡이'], ['skystripe', '줄무늬'], ['heart', '하트'], ['starnight', '별'], ['lemon', '체크'], ['cloud', '구름'], ['washi', '일본식'], ['plaid', '타탄'], ['lilac', '반짝이']],
  floor: [['plain', '기본'], ['wood', '원목 마루'], ['tatami', '다다미'], ['minttile', '타일'], ['pinkrug', '카펫'], ['checker', '체커'], ['grass', '잔디'], ['skytile', '큰 타일']],
  furn: [['bed', '침대', 44, 28], ['sofa', '소파', 40, 26], ['shelf', '책장', 26, 44], ['desk', '책상', 36, 30], ['kotatsu', '코타츠', 40, 22], ['fridge', '냉장고', 20, 38], ['tv', 'TV', 34, 32], ['wardrobe', '옷장', 28, 44], ['amp', '앰프·기타', 30, 34], ['lowtable', '좌식 밥상', 36, 24]],
  deco: [['window', '창문', 28, 24], ['clock', '벽시계', 16, 16], ['poster', '포스터', 18, 24], ['wallshelf', '선반', 30, 16], ['garland', '가랜드', 44, 10], ['mirror', '거울', 16, 22], ['frame', '액자', 24, 18], ['stars', '별 스티커', 20, 20]],
  prop: [['soba', '소바', 16, 12], ['strawmilk', '딸기우유', 10, 16], ['coffeejelly', '커피젤리', 14, 14], ['console', '게임기', 18, 10], ['guitar', '기타', 12, 26], ['baseball', '배트·공', 20, 18], ['manga', '만화책', 16, 14], ['jump', '점프', 14, 18], ['headphones', '헤드폰', 18, 14], ['cat', '고양이', 18, 14], ['plant', '화분', 14, 20], ['camera', '카메라', 18, 12], ['watermelon', '수박', 18, 14], ['milk', '우유병', 8, 16], ['curry', '카레', 18, 10], ['sketch', '스케치북', 16, 14], ['gi', '도복 띠', 18, 10], ['wing', '깃털', 12, 18], ['tobacco', '재떨이', 14, 8], ['glasses', '안경 케이스', 16, 8]]
};
const PRICE = { wall: 80, floor: 80, furn: 200, deco: 60, prop: 40 };
const STAGES = [['첫 만남', 'first', 0], ['친구', 'friend', 25], ['썸', 'crush', 50], ['연인', 'lover', 75]];
const stageOf = l => STAGES.filter(s => l >= s[2]).pop();
const MOODS = ['기분 최고', '설렘', '들뜸', '나른함', '심술', '시무룩', '멍함', '두근두근', '느긋함', '투덜투덜'];
function moodOf(id) { let h = 0; for (const ch of today() + id) h = (h * 31 + ch.charCodeAt(0)) >>> 0; return MOODS[h % MOODS.length]; }
function stateOf(o) { if (o.sleeping) return '쿨쿨'; const a = []; if (o.food < 35) a.push('배고픔'); if (o.energy < 30) a.push('졸림'); if (o.fun < 35) a.push('심심함'); if (o.clean < 35) a.push('꼬질꼬질'); return a.join(' · ') || '만족'; }
const JOB_NAME = { curly_suit: '어두운 세계', blue: '크로우 임무', blonde_student: '누나네 카페', mole: '학교 선생', punk: '공연', bartender: '바텐더', curly_coat: '사건 해결', mint: '잡지 모델', karate: '도장 사범 대리', baseball: '야구 연습', spiky: '탈환 의뢰', kyon: '편의점', ponytail: '수박 농장', chiro: '담배 가게 카운터', saiki: '라멘집 (몰래)', nozaki: '만화 어시스턴트', ahoge: '과외', blindfold: '퍼스컴 순찰', headphone: '영상 편집', gintoki: '해결사 의뢰', nifuji: '회사', usui: '메이드 카페 주방', izumi: '사신 업무', shima: '카페', hidden: '회사' };
// 알바 대신 다른 곳에 가는 캐릭터: [버튼, 방에 뜨는 글, 끝났을 때, 막힐 때]
const WORK = { hidden: ['회사', '회사 출근 중', '퇴근!', '회사에 가서'], blue: ['크로우 임무', '크로우 임무 하러 가는 중', '크로우 임무를 마치고 돌아왔다!', '크로우 임무 중이라'], punk: ['공연', '공연하러 가는 중', '공연을 마치고 돌아왔다!', '공연 중이라'], curly_coat: ['사건 해결', '사건 해결하러 가는 중', '사건을 해결하고 돌아왔다!', '사건 해결 중이라'], mole: ['학교', '학교 출근 중', '수업을 마치고 돌아왔다!', '학교에 가서'], baseball: ['야구 연습', '야구 연습하러 가는 중', '야구 연습을 마치고 돌아왔다!', '야구 연습 중이라'], blindfold: ['퍼스컴 순찰', '퍼스컴 순찰 중', '순찰을 마치고 돌아왔다!', '순찰 중이라'], nifuji: ['회사', '회사 출근 중', '퇴근!', '회사에 가서'], curly_suit: ['어두운 세계', '어두운 세계로 가는 중', '어두운 세계에서 돌아왔다!', '어두운 세계에 가서'] };
const JW = id => WORK[id] ? WORK[id][0] : '알바';
const JOBS = [['30 분', 30, 40], ['3 시간', 180, 150], ['8 시간', 480, 350]];
const DROP_MS = 5 * 60 * 1000;
const GACHA = 300, DUP = 150, TALK_MAX = 3, LOVE_DAY = 4;   // 애정은 하루 최대 4 → 한 단계(25)에 약 일주일
function addLove(o, n) { if (!o.lv || o.lv.day !== today()) o.lv = { day: today(), g: 0 }; const g = Math.max(0, Math.min(n, LOVE_DAY - o.lv.g)); const before = stageOf(o.love); o.lv.g += g; o.love = clamp(o.love + g); if (stageOf(o.love) !== before) { S.coins += 100; setTimeout(() => toast(`${stageOf(o.love)[0]}이(가) 됐어요! +100 코인`), 50); } return g; }
let CH = [], CHM = {}, TALK = {}, FR = {}, IT = [], ITM = {}, MUM = {}, CTRY = [], TRV = {}, GL = [], GLM = {}, SETS = [];
const SET_PAY = 300;
const hasP = id => !!(S.owned[id] || (S.girls || {})[id]);
const setDone = st => st.m.every(hasP);
const setReady = () => SETS.filter(st => setDone(st) && !(S.sets || {})[st.k]);
function setToast() { const r = setReady(); if (r.length) setTimeout(() => toast(`조합 완성! 「${r[0].n}」 도감에서 ${SET_PAY} 코인 받기`), 900); }
// 짝: 도감 25명을 다 모으면 열려요. 여자애는 방 하나에 한 명씩, 남자친구와 같이 행동해요
const allMet = () => CH.length && CH.every(c => S.owned[c.id]);
// 짝에 따라 말투가 바뀌면(voice) 그 짝 방에서는 그 대사 묶음을 써요
const GLX = g => { const gl = GLM[g], b = S.girls && S.girls[g] && S.girls[g].with, v = gl.pair && gl.pair[b] && gl.pair[b].voice; return v ? Object.assign({}, gl, v) : gl; };
const hisCall = g => { const b = S.girls[g].with, gl = GLM[g]; return S.girls[g].bc || (gl.pair && gl.pair[b] && gl.pair[b].his) || nameOf(g); };   // 남자애가 여자애를 부르는 이름
const herCall = g => { const b = S.girls[g].with, gl = GLM[g]; return S.girls[g].gc || (gl.pair && gl.pair[b] && gl.pair[b].call) || nameOf(b); };   // 여자애가 남자애를 부르는 이름
const BOY_HEART = ['{her}.', '{her}, 이리 와.', '{her}, 오늘 좀 예쁘네.', '....{her}, 좋아해.'], BOY_FIGHT = ['{her}, 왜 그래?', '....{her}, 내가 뭘 했는데.', '{her}, 미안해.'];
// 원작 커플 전용 대사(pair)는 절반쯤 섞여 나오고, 앞에 부르는 이름을 붙이지 않아요
const boyLine = (g, boy, k, def) => { const sp = GLM[g].pair && GLM[g].pair[boy] && GLM[g].pair[boy]['boy_' + k]; return (sp && Math.random() < .6 ? pick(sp) : pick(def)).split('{her}').join(hisCall(g)); };
const lineOf = (gl, boy, k) => { const sp = gl.pair && gl.pair[boy] && gl.pair[boy][k]; return sp && Math.random() < .5 ? '\u0001' + pick(sp) : pick(gl[k]); };
const withHim = (t, g) => {
  if (t[0] === '\u0001') return t.slice(1);
  if (t.includes('{him}')) return t.split('{him}').join(herCall(g));
  if (t[0] === '(' || Math.random() >= .45) return t;   // 말 없이 행동만 하는 줄은 이름을 안 붙여요
  const tag = t.match(/^\[[^\]]+\] /);   // [PDA] 같은 머리말은 앞에 두고 그 뒤에 이름
  return tag ? `${tag[0]}${herCall(g)}, ${t.slice(tag[0].length)}` : `${herCall(g)}, ${t}`;
};
const girlOf = boy => Object.keys(S.girls || {}).find(g => S.girls[g].with === boy);
const sub = (t, o, place) => t.split('{call}').join(o?.call || '너').split('{place}').join(place || '');
// 혼잣말: 지금 상태에 맞는 묶음에서, 다 쓸 때까지 겹치지 않게 섞어서 꺼내요
const BAG = {};
function mumbleOf(id, o) {
  const m = MUM[id]; if (!m) return pick(CHM[id].mumble);
  const h = new Date().getHours(), opts = [];
  if (o.food < 35) opts.push('hungry'); if (o.energy < 30) opts.push('sleepy'); if (o.fun < 35) opts.push('bored'); if (o.clean < 35) opts.push('dirty');
  if (o.fun > 75) opts.push('happy'); if (h >= 23 || h < 5) opts.push('night');
  const cat = opts.length && Math.random() < 0.6 ? pick(opts) : 'normal', key = id + cat;
  if (!BAG[key] || !BAG[key].length) BAG[key] = [...m[cat]].sort(() => Math.random() - 0.5);
  return BAG[key].pop().split('{call}').join(o.call || '너');
}

function spr(cat, k, col, sc) {
  const S = SHEET[cat], L = ITEMS[cat], i = Math.max(0, L.findIndex(x => x[0] === k)), it = L[i];
  return `<div class="clip" style="width:${it[2] * sc}px;height:${it[3] * sc}px;POS"><img class="px" src="assets/decor/${cat}.png" alt="" style="width:${S.sw * sc}px;height:${S.sh * sc}px;margin-left:${-col * S.cw * sc}px;margin-top:${-i * S.ch * sc}px"></div>`;
}
const icon = (k, sz) => `<span class="itm" style="width:${sz}px;height:${sz}px"><img class="px" src="assets/ui/items.png" alt="" style="width:${IT.length * sz}px;height:${sz}px;margin-left:${-ITM[k].i * sz}px"></span>`;
const face = (id, w) => { const s = w / 96; return `<img class="px" src="assets/ch/${id}.webp?v=35" alt="" style="position:absolute;width:${384 * s}px;height:${528 * s}px;left:${-(96 * s - w) / 2}px;top:0;max-width:none">`; };

// ---------- 저장 ----------
let fb = null, user = null, S = null, saveT = null;
async function initFirebase() {
  if (!window.FIREBASE_CONFIG) return;
  const V = '10.12.2', B = `https://www.gstatic.com/firebasejs/${V}/`;
  const [A, AU, FS] = await Promise.all([import(B + 'firebase-app.js'), import(B + 'firebase-auth.js'), import(B + 'firebase-firestore.js')]);
  const a = A.initializeApp(window.FIREBASE_CONFIG);
  fb = { auth: AU.getAuth(a), AU, db: FS.getFirestore(a), FS };
}
const emailOf = id => `${id.toLowerCase()}@boifriends.app`;
const localKey = () => `bp_save_${user.uid}`;
async function sha(t) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)); return [...new Uint8Array(b)].map(x => x.toString(16).padStart(2, '0')).join(''); }
function lsGet(k) { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } }
function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { } }

async function signUp(id, pw) {
  if (fb) { const c = await fb.AU.createUserWithEmailAndPassword(fb.auth, emailOf(id), pw); return { uid: c.user.uid, id }; }
  const users = lsGet('bp_users') || {}; if (users[id]) throw new Error('이미 있는 아이디예요.');
  users[id] = await sha(id + ':' + pw); lsSet('bp_users', users); lsSet('bp_session', id); return { uid: 'local_' + id, id };
}
async function logIn(id, pw) {
  if (fb) { const c = await fb.AU.signInWithEmailAndPassword(fb.auth, emailOf(id), pw); return { uid: c.user.uid, id }; }
  const users = lsGet('bp_users') || {}; if (!users[id] || users[id] !== await sha(id + ':' + pw)) throw new Error('아이디나 비밀번호가 맞지 않아요.');
  lsSet('bp_session', id); return { uid: 'local_' + id, id };
}
async function logOut() { if (fb) await fb.AU.signOut(fb.auth); localStorage.removeItem('bp_session'); user = null; S = null; render(); }
function fresh() { return { v: 1, at: Date.now(), coins: GACHA, owned: {}, cur: null, items: ['plain', 'bed'], day: today(), last: Date.now() }; }
async function loadSave() {
  let s = lsGet(localKey());
  if (fb) { try { const d = await fb.FS.getDoc(fb.FS.doc(fb.db, 'saves', user.uid)); if (d.exists()) { const r = JSON.parse(d.data().json); if (!s || r.at >= s.at) s = r; } } catch (e) { console.warn(e); } }
  S = s || fresh();
}
function save() {
  S.at = Date.now(); lsSet(localKey(), S);
  if (!fb) return; clearTimeout(saveT);
  saveT = setTimeout(() => fb.FS.setDoc(fb.FS.doc(fb.db, 'saves', user.uid), { json: JSON.stringify(S), at: S.at, id: user.id }).catch(e => console.warn(e)), 1500);
}

// ---------- 시간 흐름 ----------
function tickTime() {
  const now = Date.now(), h = Math.min(72, (now - S.last) / 3.6e6);
  for (const o of Object.values(S.owned)) {
    o.food = clamp(o.food - 6 * h); o.fun = clamp(o.fun - 4 * h); o.clean = clamp(o.clean - 3 * h);
    o.energy = clamp(o.energy + (o.sleeping ? 14 : -3) * h);
    if (o.sleeping && o.energy >= 100) o.sleeping = false;
    if (o.food < 10 && o.fun < 10) o.love = clamp(o.love - 2 * h / 24);
  }
  for (const [id, o] of Object.entries(S.owned)) if (o.job && now >= o.job.until) { S.coins += o.job.pay; o.food = clamp(o.food - 15); o.energy = clamp(o.energy - 20); setTimeout(() => toast(`${nameOf(id)} ${WORK[id] ? WORK[id][2] : '알바 끝!'} +${o.job.pay} 코인`), 300); o.job = null; }
  S.last = now;
  if (S.day !== today()) { S.day = today(); S.coins += 150; toast('출석 +150 코인'); S.mail = Object.keys(S.owned).map(id => ({ id, c: 10 + Math.floor(Math.random() * 31) })); }
}

// ---------- 화면 ----------
let panel = null, anim = { x: 0, dir: 1, mode: 'walk', t: 20, f: 0, mum: -1, heart: 0, tick: 0 }, sayText = null;
const cur = () => S.cur && S.owned[S.cur] ? S.cur : Object.keys(S.owned)[0];
const nameOf = id => id === 'hidden' ? (S.owned.hidden?.name || '???') : GLM[id] ? GLM[id].name : CHM[id].name;

const timeLeft = t => { const m = Math.max(0, Math.ceil((t - Date.now()) / 60000)); return m >= 60 ? `${Math.floor(m / 60)} 시간 ${m % 60} 분 남음` : `${m} 분 남음`; };
const wakeAt = o => Date.now() + Math.max(0, 100 - (o.energy + 14 * (Date.now() - S.last) / 3.6e6)) / 14 * 3.6e6;
const tileUrl = (cat, k) => k === 'plain' ? 'none' : `url(assets/decor/${cat}_${k}.png)`;
const slot = (cat, v, pos) => v ? spr(cat, v[0], v[1], 2).replace('POS', pos) : '';
// 잠: 침대에 뒷모습으로 눕히고 이불 덮기 (침대가 없으면 바닥에 이불)
function sleepHTML(id, r, dy) {
  const pos = r.a && r.a[0] === 'bed' ? 'left:3%;bottom:20%' : r.b && r.b[0] === 'bed' ? 'right:3%;bottom:20%' : 'left:calc(50% - 44px);bottom:6%';
  const s = 36 / 96;
  return `<div style="position:absolute;width:88px;height:56px;${pos};z-index:${dy ? 4 : 5};${dy ? `transform:translate(12px,${dy}px)` : ''}"><div style="position:absolute;inset:0;filter:brightness(.22)">
    <div style="position:absolute;left:11px;top:1px;width:36px;height:50px;overflow:hidden;transform:rotate(-90deg)"><img class="px" src="assets/ch/${id}.webp?v=35" alt="" style="width:${384 * s}px;height:${528 * s}px;max-width:none;margin-top:${-132 * s}px"></div>
    <div style="position:absolute;left:19px;top:19px;width:67px;height:29px;border:2px solid var(--ink);border-radius:8px 6px 4px 4px;background:#8ccff5;background-image:repeating-linear-gradient(90deg,transparent 0 10px,rgba(255,255,255,.5) 10px 13px)"></div></div>
    ${dy ? '' : '<span class="emo" style="left:8px;top:-22px;color:#5b6bd6">Z z z</span>'}</div>`;
}
function roomHTML(id, o, scale) {
  const r = o.room, g = id ? girlOf(id) : null, hideG = o.sleeping || o.job ? 'style="display:none"' : '';
  return `<div class="room" style="background-color:${PAL[r.wc][1]};background-image:${tileUrl('wall', r.wp)}">
    <div class="floor" style="background-color:${PAL[r.fc][1]};background-image:${tileUrl('floor', r.fl)}"></div>
    ${slot('deco', r.dc, 'left:6%;top:6%')}${slot('furn', r.a, 'left:3%;bottom:20%')}${slot('furn', r.b, 'right:3%;bottom:20%')}${slot('prop', r.pr, 'left:28%;bottom:4%;z-index:2')}
    ${id && o.sleeping && g ? sleepHTML(g, r, -16) : ''}${id && o.sleeping ? sleepHTML(id, r) : ''}${id && o.job ? `<div style="position:absolute;left:50%;top:38%;transform:translateX(-50%);z-index:5;background:#fff;border:3px solid var(--ink);border-radius:10px;padding:6px 10px;font-size:11px;text-align:center;line-height:1.5"><img src="assets/ui/ic_job.png" alt="" style="width:18px;vertical-align:-4px"> ${WORK[id] ? WORK[id][1] : esc(JOB_NAME[id]) + ' 알바 중'}${g ? `<br><small>${esc(nameOf(g))}도 같이</small>` : ''}<br><b id="jobleft">${timeLeft(o.job.until)}</b></div>` : ''}
    ${id ? `<div class="shadow" id="shd" ${o.sleeping || o.job ? 'style="display:none"' : ''}></div><div class="man" id="man" ${o.sleeping || o.job ? 'style="display:none"' : ''}><img class="px" src="assets/ch/${id}.webp?v=35" alt="${esc(nameOf(id))}"></div><span class="emo" id="emo" hidden></span><span class="mumble" id="mum" hidden></span>` : ''}
    ${g ? `<div class="shadow" id="gshd" ${hideG}></div><div class="man" id="gman" ${hideG}><img class="px" src="assets/ch/${g}.webp?v=35" alt="${esc(nameOf(g))}"></div><span class="emo" id="gemo" hidden></span><span class="mumble gmum" id="gmum" hidden></span>` : ''}
    ${o.sleeping ? `<div class="night"></div><div class="sleepleft">쿨쿨 · 일어나기까지 <b id="sleepleft">${timeLeft(wakeAt(o)).replace(' 남음', '')}</b></div>` : ''}
  </div>`;
}
function meterHTML(o) {
  const st = stageOf(o.love), nx = STAGES[STAGES.indexOf(st) + 1];
  const m = (l, v, c) => `<div class="meter"><div class="row"><span>${l}</span><span>${v}</span></div><div class="bar"><i style="width:${v}%;background-color:${v < 30 ? '#ff9a8a' : c}"></i></div></div>`;
  return `<div class="meters">${m('배부름', o.food, '#ffd76a')}${m('기분', o.fun, '#8fe3cc')}${m('청결', o.clean, '#8ccff5')}${m('체력', o.energy, '#c6b5ff')}
    <div class="meter wide"><div class="row"><span>애정</span><span>${st[0]}</span></div><div class="bar"><i style="width:${o.love}%;background-color:#ff8fb3"></i></div></div></div>`;
}
const ic = (act, img, label, pressed) => `<button class="ic" data-act="${act}" ${pressed ? 'aria-pressed="true"' : ''}><img src="assets/ui/ic_${img}.png?v=2" alt="">${label}</button>`;

let dropStyle = null; const cheat = {};
const APP_V = 107, COUPONS = { NINOGUYA: 3000 };
// 쿠폰 입력 정리: 한글 자판 상태로 친 글자(ㅜㅑㅜㅐ혀ㅛㅁ)도 영어 자판 글자로 바꾸고, 대소문자·띄어쓰기·마침표는 무시해요
const KEY = { ㄱ: 'r', ㄲ: 'R', ㄴ: 's', ㄷ: 'e', ㄸ: 'E', ㄹ: 'f', ㅁ: 'a', ㅂ: 'q', ㅃ: 'Q', ㅅ: 't', ㅆ: 'T', ㅇ: 'd', ㅈ: 'w', ㅉ: 'W', ㅊ: 'c', ㅋ: 'z', ㅌ: 'x', ㅍ: 'v', ㅎ: 'g',
  ㅏ: 'k', ㅐ: 'o', ㅑ: 'i', ㅒ: 'O', ㅓ: 'j', ㅔ: 'p', ㅕ: 'u', ㅖ: 'P', ㅗ: 'h', ㅘ: 'hk', ㅙ: 'ho', ㅚ: 'hl', ㅛ: 'y', ㅜ: 'n', ㅝ: 'nj', ㅞ: 'np', ㅟ: 'nl', ㅠ: 'b', ㅡ: 'm', ㅢ: 'ml', ㅣ: 'l',
  ㄳ: 'rt', ㄵ: 'sw', ㄶ: 'sg', ㄺ: 'fr', ㄻ: 'fa', ㄼ: 'fq', ㄽ: 'ft', ㄾ: 'fx', ㄿ: 'fv', ㅀ: 'fg', ㅄ: 'qt' };
const CHO = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ', JUNG = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ', JONG = ' ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ';
function normCode(t) {
  let out = '';
  for (const ch of String(t)) {
    const n = ch.charCodeAt(0) - 0xAC00;
    if (n >= 0 && n < 11172) { out += KEY[CHO[Math.floor(n / 588)]] + KEY[JUNG[Math.floor(n % 588 / 28)]] + (n % 28 ? KEY[JONG[n % 28]] : ''); }
    else out += KEY[ch] || ch;
  }
  return out.toUpperCase().replace(/[^A-Z0-9]/g, '');
}   // 쿠폰 코드는 몇 번이든 쓸 수 있어요
function placeDrop() { const r = document.querySelector('.lcd .room'); if (!r || !dropStyle || $('#drop')) return; const c = document.createElement('button'); c.id = 'drop'; c.dataset.act = 'coin'; c.setAttribute('aria-label', '동전 줍기'); c.style.cssText = dropStyle; r.appendChild(c); }
function render() { const y = window.scrollY; renderNow(); placeDrop(); animStep(false); window.scrollTo(0, y); }
function renderNow() {
  if (!user) return renderStart();
  if (!Object.keys(S.owned).length) { app.innerHTML = shellEmpty(); if (panel?.k !== 'gacha') openPanel('gacha'); return; }
  const id = cur(), o = S.owned[id], t = o.talk.day === today() ? o.talk.n : 0;
  app.innerHTML = `<div class="shell">
    <div class="brand"><img src="assets/ui/ic_heart.png" alt="">YEONIGOTCHI</div>
    <div class="topbar"><button class="who" data-act="who" aria-label="돌볼 사람 바꾸기"><span class="face">${face(id, 32)}</span><span>${esc(nameOf(id))}</span><img src="assets/ui/ic_back.png" alt="" style="width:14px;transform:rotate(-90deg)"></button>
      <span style="display:flex;gap:6px">${allMet() ? `<button class="pill pairbtn" data-act="pair" aria-label="짝 찾아 주기">♥ 짝</button>` : ''}${S.mail && S.mail.length ? `<button class="pill" data-act="mail" aria-label="편지 ${S.mail.length}통"><img src="assets/ui/ic_mail.png" alt="">${S.mail.length}</button>` : ''}<span class="pill coin"><img src="assets/ui/ic_coin.png" alt="">${S.coins.toLocaleString('ko-KR')}</span></span></div>
    <div class="icons">${ic('give', 'food', '주기')}${ic('play', 'play', '놀기')}${ic('wash', 'wash', '씻기')}${ic('sleep', 'sleep', o.sleeping ? '깨우기' : '재우기', o.sleeping)}${ic('talk', 'talk', '대화')}</div>
    <div class="lcd">${roomHTML(id, o)}</div>
    <div class="say"><b>${esc(nameOf(id))} · ${moodOf(id)} · ${stateOf(o)} <span>${'♥'.repeat(TALK_MAX - t)}</span></b><span id="say">${esc(sayText || defaultSay(id, o))}</span></div>
    ${meterHTML(o)}
    <div class="icons seven">${ic('profile', 'heart', '프로필')}${ic('decor', 'decor', '꾸미기')}${ic('job', 'job', JW(id))}${ic('travel', 'travel', '여행')}${ic('gacha', 'gacha', '가챠')}${ic('dex', 'dex', '도감')}${ic('menu', 'home', '메뉴')}</div>
    <div class="abc"><button class="round" data-act="prev" aria-label="이전 사람">◀</button><button class="round b" data-act="talk" aria-label="말 걸기">♥</button><button class="round" data-act="next" aria-label="다음 사람">▶</button></div>
  </div>`;
  if (panel) renderPanel();
}
function shellEmpty() {
  return `<div class="shell"><div class="brand"><img src="assets/ui/ic_heart.png" alt="">YEONIGOTCHI</div>
    <div class="lcd"><div class="room" style="background-color:#cfeaff"></div></div>
    <button class="btn yellow" data-act="gacha" style="width:100%"><img src="assets/ui/ic_gacha.png" alt="" style="width:20px;vertical-align:-4px"> 가챠</button></div>`;
}
function defaultSay(id, o) {
  if (o.sleeping) return '(쿨쿨....)';
  if (o.food < 30) return '(꼬르륵....)';
  return '';
}

// ---------- 시작 화면 ----------
let startMode = 'join';
function renderStart() {
  app.innerHTML = `<div class="start">
    <div class="egg"><div class="scr"><img src="assets/ui/ic_heart.png" alt="" style="width:40px;margin-bottom:18px"></div></div>
    <div style="text-align:center"><h1>여니고치</h1></div>
    <div class="card" style="width:100%;padding:0;overflow:hidden">
      <div style="display:grid;grid-template-columns:1fr 1fr;border-bottom:3px solid var(--ink)">
        <button data-act="mode-join" style="height:44px;border:0;font-weight:700;background:${startMode === 'join' ? 'var(--yellow)' : '#fff'}">가입하기</button>
        <button data-act="mode-login" style="height:44px;border:0;border-left:3px solid var(--ink);font-weight:700;background:${startMode === 'login' ? 'var(--yellow)' : '#fff'}">로그인</button></div>
      <form id="auth" style="padding:14px;display:flex;flex-direction:column;gap:8px">
        <label class="label" for="uid">아이디</label><input class="field" id="uid" name="uid" autocomplete="username" required minlength="4" maxlength="12" pattern="[A-Za-z0-9_]+" placeholder="영문·숫자 4~12자">
        <label class="label" for="pw">비밀번호</label><input class="field" id="pw" name="pw" type="password" autocomplete="${startMode === 'join' ? 'new-password' : 'current-password'}" required minlength="6" placeholder="6자 이상">
        <button class="btn" type="submit" style="margin-top:6px">${startMode === 'join' ? `가입하고 ${GACHA} 코인 받기` : '로그인'}</button>
      </form></div>
    ${fb ? '' : '<div class="note">오프라인 · 이 기기에만 저장</div>'}
  </div>`;
  $('#auth').onsubmit = async e => {
    e.preventDefault(); const id = $('#uid').value.trim(), pw = $('#pw').value;
    try { user = await (startMode === 'join' ? signUp(id, pw) : logIn(id, pw)); await enter(); }
    catch (err) { toast(authMsg(err)); }
  };
}
function authMsg(e) {
  const c = e.code || '';
  if (c.includes('email-already-in-use')) return '이미 있는 아이디예요.';
  if (c.includes('invalid-credential') || c.includes('wrong-password') || c.includes('user-not-found')) return '아이디나 비밀번호가 맞지 않아요.';
  if (c.includes('weak-password')) return '비밀번호는 6자 이상이에요.';
  return e.message || '잠시 후 다시 해 주세요.';
}
async function enter() { await loadSave(); tickTime(); save(); sayText = null; render(); }

// ---------- 패널 ----------
function openPanel(k, extra) { panel = Object.assign({ k }, extra || {}); renderPanel(); }
function closePanel() { if (!Object.keys(S.owned).length) return; panel = null; document.querySelector('.sheet')?.remove(); render(); }
function renderPanel() {
  const old = document.querySelector('.sheet .pbody'), keep = old && renderPanel.k === panel.k ? old.scrollTop : 0;   // 같은 창을 다시 그릴 때는 스크롤 위치를 지켜요
  renderPanel.k = panel.k;
  document.querySelector('.sheet')?.remove();
  const f = { travel: pTravel, who: pWho, profile: pProfile, decor: pDecor, gacha: pGacha, pair: pPair, place: pPlace, names: pNames, dex: pDex, menu: pMenu, give: pGive, job: pJob, mail: pMail }[panel.k];
  const [title, body] = f();
  const el = document.createElement('div'); el.className = 'sheet';
  el.innerHTML = `<div class="panel" role="dialog" aria-label="${esc(title)}"><div class="phead"><h2>${esc(title)}</h2>${Object.keys(S.owned).length ? '<button class="close" data-act="close" aria-label="닫기"><img src="assets/ui/ic_back.png" alt=""></button>' : `<span class="pill coin"><img src="assets/ui/ic_coin.png" alt="">${S.coins}</span>`}</div><div class="pbody">${body}</div></div>`;
  el.addEventListener('click', e => { if (e.target === el) closePanel(); });
  document.body.appendChild(el);
  if (keep) el.querySelector('.pbody').scrollTop = keep;
  if (panel.k === 'menu') { el.querySelector('#couponf').onsubmit = ev => { ev.preventDefault(); const c = normCode(el.querySelector('#coupon').value);
    if (COUPONS[c]) { S.coins += COUPONS[c]; save(); toast(`+${COUPONS[c]} 코인`); el.querySelector('#coupon').blur(); panel = null; document.querySelector('.sheet')?.remove(); render(); document.querySelectorAll('.pill.coin').forEach(p => { if (p.lastChild) p.lastChild.textContent = S.coins.toLocaleString('ko-KR'); }); } else toast('없는 코드예요.'); }; }
  if (panel.k === 'names') { const f3 = el.querySelector('#namef'); f3.onsubmit = ev => { ev.preventDefault(); const h = S.girls[panel.g]; h.bc = el.querySelector('#bc').value.trim(); h.gc = el.querySelector('#gc').value.trim(); save(); toast('저장했어요.'); GA.sayT = withHim(pick(GLX(panel.g).heart), panel.g); GA.sayUntil = anim.tick + 20; GA.heart = 14; closePanel(); }; }
  if (panel.k === 'profile') { const f2 = el.querySelector('#callf'); if (f2) f2.onsubmit = ev => { ev.preventDefault(); const o = S.owned[cur()]; o.call = el.querySelector('#call').value.trim() || '너'; const hn = el.querySelector('#hname'); if (hn) o.name = hn.value.trim() || '???'; save(); toast('저장했어요.'); render(); }; }
}
function pWho() {
  return ['돌볼 사람', Object.keys(S.owned).map(id => { const o = S.owned[id]; return `<button class="card" data-act="pick" data-id="${id}" style="display:flex;align-items:center;gap:10px;text-align:left;${id === cur() ? 'background:var(--yellow2)' : ''}">
    <span style="width:40px;height:40px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;position:relative;background:#bfe6ff;flex-shrink:0">${face(id, 40)}</span>
    <span style="flex:1;font-weight:700;font-size:13px">${esc(nameOf(id))}</span><span class="label">${stageOf(o.love)[0]}</span></button>`; }).join('') + `<button class="btn yellow" data-act="gacha">가챠로 새 사람 만나기</button>`];
}
function pProfile() {
  const id = cur(), o = S.owned[id], c = CHM[id];
  return [`프로필`, `<div class="card" style="padding:0;overflow:hidden"><div style="height:170px;position:relative;background:#bfe6ff;border-bottom:3px solid var(--ink)"><div style="position:absolute;left:50%;margin-left:-60px;bottom:4px;width:120px;height:165px;overflow:hidden">${face(id, 120)}</div></div>
      <div style="padding:10px 12px;display:flex;justify-content:space-between;align-items:center;gap:8px"><div><div style="font-size:16px;font-weight:700">${esc(nameOf(id))}</div><div class="label">오늘 기분 · ${moodOf(id)}<br>상태 · ${stateOf(o)}${girlOf(id) ? `<br>짝 · ${esc(nameOf(girlOf(id)))} <button class="pill" data-act="gnames" data-v="${girlOf(id)}" style="font-size:10px;padding:1px 6px">부르는 이름</button>` : ''}</div></div><span class="pill">${stageOf(o.love)[0]} · ${o.love}</span></div></div>
    <form id="callf" class="card" style="display:flex;flex-direction:column;gap:6px">
      ${id === 'hidden' ? `<label class="label" for="hname">이 사람의 이름</label><input class="field" id="hname" maxlength="8" value="${esc(o.name || '')}" placeholder="이름을 지어 주세요">` : ''}
      <label class="label" for="call">나를 부르는 이름</label><div style="display:flex;gap:8px"><input class="field" id="call" maxlength="8" value="${esc(o.call)}"><button class="btn" type="submit">저장</button></div></form>
    ${slots('좋아하는 것', c.li, (o.known || {}).l || [], 'var(--mint2)')}${slots('싫어하는 것', c.di, (o.known || {}).d || [], 'var(--pink2)')}`];
}
function slots(title, all, found, bg) {
  if (!all.length) return '';
  return `<div class="card" style="background:${bg}"><b style="font-size:11px">${title}</b><div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:6px">${all.map(k => found.includes(k)
    ? `<span style="display:flex;flex-direction:column;align-items:center;gap:2px;font-size:10px">${icon(k, 40)}${esc(ITM[k].n)}</span>`
    : `<span style="width:44px;height:44px;border:2px dashed var(--ink2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--ink2)">?</span>`).join('')}</div></div>`;
}
function pDecor() {
  const id = cur(), o = S.owned[id], tab = panel.tab || 'wall', slot = panel.slot || 'a';
  const pv = panel.pv && panel.pv.tab === tab ? panel.pv : null, r = JSON.parse(JSON.stringify(o.room));
  if (pv) { if (tab === 'wall' || tab === 'floor') r[pv.key] = pv.val; else r[pv.key] = [pv.val, pv.col]; if (tab === 'wall') r.wc = pv.col ?? r.wc; if (tab === 'floor') r.fc = pv.col ?? r.fc; }
  const key = tab === 'wall' ? 'wp' : tab === 'floor' ? 'fl' : tab === 'furn' ? slot : tab === 'deco' ? 'dc' : 'pr';
  const pal = tab === 'wall' || tab === 'floor' ? PAL : VAR, curCol = tab === 'wall' ? r.wc : tab === 'floor' ? r.fc : (r[key] ? r[key][1] : 0);
  const tabs = [['wall', '벽지'], ['floor', '바닥'], ['furn', '가구'], ['deco', '벽 장식'], ['prop', '소품']].map(t => `<button class="tab" role="tab" aria-selected="${t[0] === tab}" data-act="dtab" data-v="${t[0]}">${t[1]}</button>`).join('');
  const items = ITEMS[tab].map(it => {
    const k = it[0], on = tab === 'wall' ? r.wp === k : tab === 'floor' ? r.fl === k : !!r[key] && r[key][0] === k, have = S.items.includes(k);
    const th = tab === 'wall' || tab === 'floor' ? `<div class="th" style="background-color:${PAL[tab === 'wall' ? r.wc : r.fc][1]};background-image:${tileUrl(tab, k)}"></div>`
      : `<div class="th">${spr(tab, k, curCol, Math.max(it[2], it[3]) > 24 ? 1 : 2).replace('POS', 'position:relative')}</div>`;
    return `<button class="item" data-act="ditem" data-v="${k}" aria-pressed="${on}">${th}<span>${it[1]}</span><small style="color:${on && !(pv && pv.val === k) ? '#b8336a' : have ? '#1f7a60' : 'inherit'}">${pv && pv.val === k ? '미리 보기' : on ? '사용 중' : have ? '보유' : PRICE[tab] + ' 코인'}</small></button>`;
  }).join('');
  const none = tab === 'wall' || tab === 'floor' ? '' : `<button class="item" data-act="ditem" data-v="none" aria-pressed="${!r[key]}"><div class="th" style="font-size:20px;color:var(--ink2)">✕</div><span>없음</span><small></small></button>`;
  const nm = pv ? ITEMS[tab].find(x => x[0] === pv.val)[1] : '';
  const buy = pv ? `<div class="buybar"><span><b>${esc(nm)}</b> 미리 보는 중</span><button class="btn white" data-act="dcancel">취소</button><button class="btn yellow" data-act="dbuy" ${S.coins < PRICE[tab] ? 'disabled' : ''}>사기 · ${PRICE[tab]} 코인</button></div>` : '';
  return ['방 꾸미기', `<div class="lcd" style="padding:4px">${roomHTML(null, Object.assign({}, o, { room: r }))}</div>${buy}
    <div class="tabs" role="tablist">${tabs}</div>
    <div class="tabbody" style="display:flex;flex-direction:column;gap:8px">
      ${tab === 'furn' ? `<div style="display:flex;gap:6px;align-items:center"><span class="label">놓을 자리</span>${[['a', '왼쪽'], ['b', '오른쪽']].map(s => `<button class="pill" data-act="dslot" data-v="${s[0]}" style="${s[0] === slot ? 'background:var(--yellow)' : ''}">${s[1]}</button>`).join('')}</div>` : ''}
      <div class="label">색상 · ${pal[curCol][0]}</div>
      <div class="sw">${pal.map((c, i) => `<button data-act="dcol" data-v="${i}" aria-label="${c[0]}" title="${c[0]}" aria-pressed="${i === curCol}" style="background:${c[1]}"></button>`).join('')}</div>
      <div class="grid4">${none}${items}</div></div>`];
}
function pGacha() {
  const first = !Object.keys(S.owned).length;
  return [first ? '첫 남자친구 뽑기' : '남자친구 가챠', `
    <div class="machine" id="machine"><img class="m px" src="assets/ui/machine.png" alt="가챠 기계"><button class="knob" data-act="pull" aria-label="손잡이 돌리기"></button></div>
    <button class="btn yellow" data-act="pull" ${S.coins < GACHA ? 'disabled' : ''}><img src="assets/ui/ic_coin.png" alt="" style="width:16px;vertical-align:-3px"> ${GACHA}</button>`];
}
function pPair() {
  const mine = Object.keys(S.girls || {});
  return ['짝 찾아 주기', `
    <div class="machine pairm" id="machine"><img class="m px" src="assets/ui/machine.png" alt="가챠 기계"><button class="knob" data-act="gpull" aria-label="손잡이 돌리기"></button></div>
    <button class="btn yellow" data-act="gpull" ${S.coins < GACHA ? 'disabled' : ''}><img src="assets/ui/ic_coin.png" alt="" style="width:16px;vertical-align:-3px"> ${GACHA}</button>
    <div class="card"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700"><span>만난 여자애</span><span>${mine.length} / ${GL.length}</span></div></div>
    ${mine.map(g => { const w = S.girls[g].with; return `<div class="card" style="display:flex;align-items:center;gap:10px">
      <span style="width:40px;height:40px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;position:relative;background:#ffd9e6;flex-shrink:0">${face(g, 40)}</span>
      <span style="flex:1;font-size:12px;line-height:1.5"><b>${esc(nameOf(g))}</b><br>${w ? `${esc(nameOf(w))}의 방` : '아직 방이 없어요'}</span>
      <span style="display:flex;flex-direction:column;gap:4px"><button class="btn white" data-act="gplace" data-v="${g}" style="padding:6px 10px;font-size:12px">${w ? '방 바꾸기' : '방 고르기'}</button>${w ? `<button class="btn white" data-act="gnames" data-v="${g}" style="padding:6px 10px;font-size:12px">부르는 이름</button>` : ''}</span></div>`; }).join('')}`];
}
function pNames() {
  const g = panel.g, b = S.girls[g].with;
  return ['서로 부르는 이름', `<div class="card" style="display:flex;align-items:center;justify-content:center;gap:14px">
      <span style="width:48px;height:48px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;position:relative;background:#bfe6ff">${face(b, 48)}</span><b style="color:#e0457b">♥</b>
      <span style="width:48px;height:48px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;position:relative;background:#ffd9e6">${face(g, 48)}</span></div>
    <form id="namef" class="card" style="display:flex;flex-direction:column;gap:6px">
      <label class="label" for="bc">${esc(nameOf(b))} → ${esc(nameOf(g))}</label><input class="field" id="bc" maxlength="8" value="${esc(S.girls[g].bc || '')}" placeholder="${esc(nameOf(g))}">
      <label class="label" for="gc">${esc(nameOf(g))} → ${esc(nameOf(b))}</label><input class="field" id="gc" maxlength="8" value="${esc(S.girls[g].gc || '')}" placeholder="${esc(nameOf(b))}">
      <button class="btn yellow" type="submit">저장</button></form>`];
}
function pPlace() {
  const g = panel.g;
  return [`${nameOf(g)} · 방 고르기`, `<div class="card" style="font-size:12px;text-align:center">같이 지낼 방을 골라요. 한 방에 한 명씩만 들어가요.</div>` + Object.keys(S.owned).map(id => { const h = girlOf(id), mine = h === g, busy = h && !mine; return `<button class="card" data-act="${busy ? '' : 'gput'}" data-v="${id}" ${busy ? 'disabled' : ''} style="display:flex;align-items:center;gap:10px;text-align:left;${mine ? 'background:var(--yellow2)' : ''}${busy ? 'opacity:.45' : ''}">
    <span style="width:40px;height:40px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;position:relative;background:#bfe6ff;flex-shrink:0">${face(id, 40)}</span>
    <span style="flex:1;font-weight:700;font-size:13px">${esc(nameOf(id))}</span><span class="label">${mine ? '지금 방' : busy ? '짝 있음' : ''}</span></button>`; }).join('')];
}
function pSets() {
  const got = S.sets || {}, done = SETS.filter(st => got[st.k]).length;
  return `<div class="card"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700"><span>모은 조합</span><span>${done} / ${SETS.length}</span></div><div class="bar" style="margin-top:6px"><i style="width:${done / SETS.length * 100}%;background-color:var(--pink)"></i></div></div>
    ${SETS.map(st => { const n = st.m.filter(hasP).length, ok = n === st.m.length, take = got[st.k];
      return `<div class="card setcard${ok && !take ? ' ready' : ''}"><div style="display:flex;justify-content:space-between;align-items:center;gap:6px"><b style="font-size:13px">${esc(st.n)}</b>
        ${take ? '<span class="label">받음 ✓</span>' : ok ? `<button class="btn yellow" data-act="setget" data-v="${st.k}" style="padding:4px 10px;font-size:12px">${SET_PAY} 받기</button>` : `<span class="label">${n} / ${st.m.length} · ${SET_PAY} 코인</span>`}</div>
        <div class="setfaces">${st.m.map(id => `<span class="sf" title="${hasP(id) ? esc(nameOf(id)) : '???'}" style="background:${GLM[id] ? '#ffd9e6' : '#bfe6ff'}">${hasP(id) ? face(id, 34) : '<b>?</b>'}</span>`).join('')}</div></div>`; }).join('')}`;
}
function pDex() {
  const all = CH, met = all.filter(c => S.owned[c.id]).length, tab = panel.tab || 'ppl', ready = setReady().length;
  const tabs = `<div class="tabs" role="tablist"><button class="tab" role="tab" aria-selected="${tab === 'ppl'}" data-act="xtab" data-v="ppl">사람</button><button class="tab" role="tab" aria-selected="${tab === 'set'}" data-act="xtab" data-v="set">조합${ready ? ` <b style="color:#e0457b">● ${ready}</b>` : ''}</button></div>`;
  if (tab === 'set') return ['도감', tabs + pSets()];
  return ['도감', tabs + `<div class="card"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700"><span>만난 사람</span><span>${met} / ${all.length}</span></div><div class="bar" style="margin-top:6px"><i style="width:${met / all.length * 100}%;background-color:var(--mint)"></i></div></div>
    <div class="grid4">${all.map(c => { const o = S.owned[c.id]; return `<div class="tile"><div class="pic">${o ? `<div class="one">${face(c.id, 66)}</div>` : '<div class="sil"><i class="h"></i><i class="bd">?</i></div>'}</div><span class="nm" style="color:${o ? 'inherit' : 'var(--ink2)'}">${o ? esc(nameOf(c.id)) : '???'}</span></div>`; }).join('')}</div>
    ${allMet() ? `<div class="card"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700"><span>짝</span><span>${Object.keys(S.girls || {}).length} / ${GL.length}</span></div></div>
    <div class="grid4">${GL.map(c => { const h = (S.girls || {})[c.id]; return `<div class="tile"><div class="pic" style="background:#ffd9e6">${h ? `<div class="one">${face(c.id, 66)}</div>` : '<div class="sil"><i class="h"></i><i class="bd">?</i></div>'}</div><span class="nm" style="color:${h ? 'inherit' : 'var(--ink2)'}">${h ? esc(c.name) : '???'}</span></div>`; }).join('')}</div>` : ''}`];
}
function pGive() {
  const tab = panel.tab || 'food';
  const tabs = [['food', '먹을 것'], ['gift', '선물']].map(t => `<button class="tab" role="tab" aria-selected="${t[0] === tab}" data-act="gtab" data-v="${t[0]}">${t[1]}</button>`).join('');
  const base = tab === 'food' ? `<button class="item" data-act="feed"><div class="th"><img class="px" src="assets/ui/ic_food.png" alt="" style="width:40px"></div><span>밥</span><small>무료</small></button>` : '';
  const sel = panel.sel && ITM[panel.sel];
  const bar = sel ? `<div class="buybar"><span><b>${esc(sel.n)}</b></span><button class="btn white" data-act="gcancel">취소</button><button class="btn yellow" data-act="giveit" data-v="${sel.k}" ${S.coins < sel.p ? 'disabled' : ''}>주기 · ${sel.p} 코인</button></div>` : '';
  return ['주기', `${bar}<div class="tabs" role="tablist">${tabs}</div><div class="tabbody"><div class="grid4">${base}${IT.filter(x => x.t === tab).map(x => `<button class="item" data-act="givesel" data-v="${x.k}" aria-pressed="${panel.sel === x.k}"><div class="th">${icon(x.k, 40)}</div><span>${esc(x.n)}</span><small><img src="assets/ui/ic_coin.png" alt="" style="width:10px;vertical-align:-1px"> ${x.p}</small></button>`).join('')}</div></div>`];
}
function give(k) {
  const id = cur(), o = S.owned[id], it = ITM[k], c = CHM[id];
  if (o.sleeping) { panel = null; document.querySelector('.sheet')?.remove(); return toast('자는 중이라 못 해요. 깨우려면 깨우기를 눌러요.'); }
  if (o.job) { panel = null; document.querySelector('.sheet')?.remove(); return toast(`${WORK[cur()] ? WORK[cur()][3] : '알바 중이라'} 못 해요.`); }
  if (S.coins < it.p) return toast('코인이 부족해요.');
  if (o.food >= 95 && it.t === 'food') return toast('배불러서 못 먹겠대요.');
  S.coins -= it.p; o.known = o.known || { l: [], d: [] };
  if (it.t === 'food') o.food = clamp(o.food + 18); else o.fun = clamp(o.fun + 15);
  let msg;
  if (c.li.includes(k)) { addLove(o, 2); anim.heart = 16; if (!o.known.l.includes(k)) { o.known.l.push(k); S.coins += 30; } msg = `(${it.n}! 눈이 반짝였다 ♥)`; }
  else if (c.di.includes(k)) { o.love = clamp(o.love - 1); anim.angry = 16; if (!o.known.d.includes(k)) o.known.d.push(k); msg = `(${it.n}.... 표정이 굳었다)`; }
  else { addLove(o, 1); msg = `(${it.n}, 고마워)`; }
  sayText = msg; panel = null; document.querySelector('.sheet')?.remove(); if (it.t === 'food') girlEat(id); save(); render();
}
function girlEat(id) { const g = girlOf(id); if (!g) return; GA.heart = 12; GA.sayT = withHim(pick(GLX(g).eat), g); GA.sayUntil = anim.tick + 18; }
function pJob() {
  const id = cur(), o = S.owned[id];
  if (o.job) return [JW(id), `<div class="card" style="text-align:center;line-height:1.8"><img src="assets/ui/ic_job.png" alt="" style="width:32px"><br><b>${esc(JOB_NAME[id])}</b><br>${timeLeft(o.job.until)} · +${o.job.pay} 코인</div>`];
  return [JW(id), `<div class="card" style="text-align:center"><img src="assets/ui/ic_job.png" alt="" style="width:32px"><br><b>${esc(JOB_NAME[id])}</b></div>
    ${JOBS.map((j, i) => `<button class="btn ${i === 1 ? 'yellow' : 'white'}" data-act="dojob" data-v="${i}" ${o.sleeping ? 'disabled' : ''} style="display:flex;justify-content:space-between;align-items:center"><span>${j[0]}</span><span><img src="assets/ui/ic_coin.png" alt="" style="width:16px;vertical-align:-3px"> +${j[2]}</span></button>`).join('')}`];
}
function pMail() {
  return ['편지', (S.mail || []).map(m => `<div class="card" style="display:flex;align-items:center;gap:10px"><span style="width:40px;height:40px;border:2px solid var(--ink);border-radius:10px;overflow:hidden;position:relative;background:#bfe6ff;flex-shrink:0">${face(m.id, 40)}</span><span style="flex:1;font-size:12px;line-height:1.5"><b>${esc(nameOf(m.id))}</b><br>${esc(MUM[m.id] ? pick(MUM[m.id].normal) : pick(CHM[m.id].mumble))}</span><span class="pill coin"><img src="assets/ui/ic_coin.png" alt="">+${m.c}</span></div>`).join('') + `<button class="btn yellow" data-act="getmail">모두 받기</button>`];
}
function pTravel() {
  const id = cur(), o = S.owned[id], st = o.trips || {};
  const busy = o.job ? (WORK[id] ? WORK[id][3] + ' 못 가요.' : '알바 중이라 못 가요.') : o.sleeping ? '자는 중이라 못 가요.' : '';
  return ['여행', `${busy ? `<div class="card" style="text-align:center;font-size:12px">${busy}</div>` : ''}<div class="trips">${CTRY.map(c => `<button class="trip" data-act="gotrip" data-v="${c.k}" ${busy ? 'disabled' : ''}>
    <span class="tpic" style="background-image:url(assets/travel/${c.k}.png?v=2)"></span>
    <span class="tname">${esc(c.n)}${st[c.k] ? ` <small>✓${st[c.k]}</small>` : ''}</span>
    <span class="tprice"><img src="assets/ui/ic_coin.png" alt="" style="width:12px;vertical-align:-2px"> ${c.p}</span></button>`).join('')}</div>`];
}
function startTrip(k) {
  const id = cur(), o = S.owned[id], c = CTRY.find(x => x.k === k);
  if (!c || o.job || o.sleeping) return;
  if (S.coins < c.p) return toast('코인이 부족해요.');
  S.coins -= c.p; save(); panel = null; document.querySelector('.sheet')?.remove();
  const tg = girlOf(id);
  const lines = [...(TRV[id] || [])].sort(() => Math.random() - .5).slice(0, 3).map(l => l.split('{place}').join(c.n).split('{call}').join(o.call || '너'));
  if (tg) lines[1] = `${nameOf(tg)}: ${withHim(sub(pick(GLX(tg).trip), o, c.n), tg)}`;
  const n = (FR[id] || [4, 4, 4, 4])[3], el = document.createElement('div'); el.className = 'tripview';
  el.innerHTML = `<div class="tsay"> </div><div class="tstage" style="background-image:url(assets/travel/${k}.png?v=2)"><div class="tplace">${esc(c.n)}</div>
    <div class="twalker"><img class="px" src="assets/ch/${id}.webp?v=35" alt=""></div>${tg ? `<div class="twalker tgirl"><img class="px" src="assets/ch/${tg}.webp?v=35" alt=""></div>` : ''}<span class="emo tjoy">♪</span></div>
    <div class="tbar"><i></i></div><button class="btn white tskip" data-tskip="1">바로 돌아오기</button>`;
  document.body.appendChild(el);
  const gimg = el.querySelector('.tgirl img'), gn = tg ? (FR[tg] || [4, 4, 4, 4])[3] : 1;
  const img = el.querySelector('.twalker img'), say = el.querySelector('.tsay'), bar = el.querySelector('.tbar i'), joy = el.querySelector('.tjoy');
  const DUR = 21000, t0 = Date.now(); let f = 0, shown = -1;
  const tick = setInterval(() => {
    const t = Date.now() - t0; f++;
    img.style.marginLeft = -(f % n) * 66 + 'px'; img.style.marginTop = -3 * 91 + 'px';
    if (gimg) { gimg.style.marginLeft = -((f + 1) % gn) * 66 + 'px'; gimg.style.marginTop = -3 * 91 + 'px'; }
    el.querySelector('.tstage').style.backgroundPositionX = -(t / 30) + 'px';
    bar.style.width = Math.min(100, t / DUR * 100) + '%';
    const i = Math.floor((t - 1500) / 6500);
    if (i >= 0 && i < 3 && i !== shown && (t - 1500) % 6500 < 5000) { shown = i; say.textContent = lines[i] || ' '; say.style.visibility = lines[i] ? 'visible' : 'hidden'; }
    else if ((t - 1500) % 6500 >= 5000) say.style.visibility = 'hidden';
    joy.textContent = ['♪', '♥', '✦'][Math.floor(t / 1600) % 3];
    if (t >= DUR) done();
  }, 160);
  function done() {
    clearInterval(tick);
    o.fun = 100; o.clean = clamp(o.clean - 10); o.food = clamp(o.food - 10); addLove(o, 2); o.trips = Object.assign({}, o.trips); o.trips[k] = (o.trips[k] || 0) + 1;
    anim.heart = 20; sayText = `(${c.n} 여행 다녀왔다! 기분 최고)`; save(); el.remove(); render();
  }
  el.querySelector('[data-tskip]').onclick = done;
}
function pMenu() {
  return ['메뉴', `<div class="card" style="font-size:13px"><b>${esc(user.id)}</b></div>
    <form id="couponf" class="card" style="display:flex;flex-direction:column;gap:6px"><label class="label" for="coupon">쿠폰 코드</label>
      <div style="display:flex;gap:8px"><input class="field" id="coupon" maxlength="20" autocomplete="off" autocapitalize="characters" autocorrect="off" spellcheck="false" lang="en" inputmode="latin" placeholder="코드를 입력해요"><button class="btn yellow" type="submit">받기</button></div></form>
    <button class="btn white" data-act="logout">로그아웃</button>
    <div class="label" style="text-align:center">버전 ${APP_V}</div>`];
}

// ---------- 행동 ----------
function act(kind) {
  const id = cur(), o = S.owned[id]; if (!o) return;
  const say = t => { sayText = t; };
  if (o.job) { toast(`${WORK[cur()] ? WORK[cur()][3] : '알바 중이라'} 못 해요.`); return; }
  if (o.sleeping && kind !== 'sleep') { toast('자는 중이라 못 해요. 깨우려면 깨우기를 눌러요.'); return; }
  if (kind === 'feed') { if (o.food >= 95) say('(배불러....)'); else { o.food = clamp(o.food + 25); addLove(o, 1); S.coins += 15; anim.heart = 10; say('(냠냠)'); girlEat(id); } }
  if (kind === 'play') { if (o.energy < 15) say('(피곤해....)'); else { o.fun = clamp(o.fun + 22); o.energy = clamp(o.energy - 12); addLove(o, 1); S.coins += 15; anim.heart = 10; anim.mode = 'hop'; anim.t = 10; say('(신난다!)'); } }
  if (kind === 'wash') { if (o.clean >= 95) say('(반짝반짝)'); else { o.clean = clamp(o.clean + 35); S.coins += 10; say('(뽀득뽀득)'); } }
  if (kind === 'sleep') { o.sleeping = !o.sleeping; say(o.sleeping ? '(잘 자)' : '(좋은 아침)'); }
  if (kind === 'talk') {
    if (o.talk.day !== today()) o.talk = { day: today(), n: 0, i: o.talk.i };
    if (o.talk.n >= TALK_MAX) say('(내일 또 얘기하자.)');
    else {
      const lines = TALK[id][stageOf(o.love)[1]]; o.talk.i = (o.talk.i + 1) % lines.length; o.talk.n++;
      say(lines[o.talk.i].map(l => l.split('{call}').join(o.call)).join('\n'));
      addLove(o, 1); o.fun = clamp(o.fun + 3); S.coins += 20; anim.heart = 12;
    }
  }
  save(); render();
}
async function pull() {
  if (S.coins < GACHA || pull.busy) return;
  pull.busy = true; S.coins -= GACHA; save();
  $('#machine')?.classList.add('spin');
  const cap = document.createElement('div'); cap.className = 'drop';
  cap.style.cssText = `background:url(assets/ui/capsules.png) 0 ${-Math.floor(Math.random() * 5) * 36}px / 72px 180px no-repeat;image-rendering:pixelated`;
  setTimeout(() => $('#machine')?.appendChild(cap), 500);
  await new Promise(r => setTimeout(r, 1300));
  const pool = CH.filter(c => c.id !== 'hidden');
  const got = Math.random() < 0.02 ? 'hidden' : pick(pool).id, dup = !!S.owned[got];
  if (dup) S.coins += DUP;
  else { const c = CHM[got]; S.owned[got] = { love: 0, food: 70, fun: 60, clean: 80, energy: 80, call: '너', room: { wp: 'plain', wc: 1, fl: 'plain', fc: 8, a: ['bed', 0], b: null, dc: null, pr: null }, talk: { day: '', n: 0, i: -1 }, met: Date.now(), sleeping: false }; }
  S.cur = got; save(); pull.busy = false; reveal(got, dup); if (!dup) setToast();
  if (!dup && allMet()) setTimeout(() => toast('도감을 다 모았어요! 이제 ♥ 짝 버튼으로 짝을 찾아 줄 수 있어요.'), 600);
}
async function gpull() {
  if (S.coins < GACHA || pull.busy || !GL.length) return;
  pull.busy = true; S.coins -= GACHA; S.girls = S.girls || {}; save();
  $('#machine')?.classList.add('spin');
  await new Promise(r => setTimeout(r, 1300));
  const got = pick(GL).id, dup = !!S.girls[got];
  if (dup) S.coins += DUP; else S.girls[got] = { with: null, met: Date.now() };
  save(); pull.busy = false; reveal(got, dup); if (!dup) setToast();
}
function reveal(id, dup) {
  const c = CHM[id] || GLM[id], girl = !!GLM[id], hid = id === 'hidden', el = document.createElement('div'); el.className = 'reveal';
  el.innerHTML = `<div class="rcard"><div class="rstage ${hid ? 'hidden' : ''}" ${girl ? 'style="background:#ffd9e6"' : ''}><img class="tw px" src="assets/ui/ic_star.png" alt="" style="left:22px;top:20px"><img class="tw px" src="assets/ui/ic_star.png" alt="" style="right:26px;top:44px">
      <span class="badge" style="${dup ? 'background:#fff' : hid ? 'background:var(--yellow)' : ''}">${dup ? '또 만났다!' : hid ? 'HIDDEN ✦' : 'NEW!'}</span>
      <div style="width:120px;height:165px;margin-bottom:10px;overflow:hidden;position:relative">${face(id, 120)}</div></div>
    <div class="rbody"><div class="nm">${hid && !dup ? '???' : esc(nameOf(id))}</div><div style="font-size:13px;line-height:1.55">“${esc(c.gacha)}”</div>
      ${dup ? `<span class="pill coin"><img src="assets/ui/ic_coin.png" alt=""> +${DUP}</span>` : ''}
      ${hid && !dup ? `<label class="label" for="hn" style="align-self:flex-start">이 사람의 이름</label><input class="field" id="hn" maxlength="8" placeholder="이름을 지어 주세요">` : ''}
      ${girl && !dup ? `<button class="btn yellow" data-r="place" style="width:100%">같이 지낼 방 고르기</button>` : `<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;width:100%"><button class="btn white" data-r="again">한 번 더</button><button class="btn" data-r="go">${girl ? '닫기' : '방으로 가기'}</button></div>`}</div></div>`;
  document.body.appendChild(el);
  el.onclick = e => {
    const b = e.target.closest('[data-r]'); if (!b) return;
    const hn = el.querySelector('#hn'); if (hn) { S.owned.hidden.name = hn.value.trim() || '???'; save(); }
    el.remove();
    if (b.dataset.r === 'place') return openPanel('place', { g: id });
    if (b.dataset.r === 'go' && girl) return renderPanel();
    if (b.dataset.r === 'go') { panel = null; document.querySelector('.sheet')?.remove(); sayText = null; render(); }
    else renderPanel();
  };
}

// 치트: 도감 버튼 자리나 도감 창 제목·탭을 3초 안에 5번 누르면 3000 코인 (휴대폰 빠른 연타도 세려고 손가락이 닿는 순간을 세요)
document.addEventListener('pointerdown', e => {
  const ic = document.querySelector('.icons [data-act=dex]'), r = ic && ic.getBoundingClientRect();
  const onIcon = r && e.clientX > r.left - 12 && e.clientX < r.right + 12 && e.clientY > r.top - 12 && e.clientY < r.bottom + 12;   // 도감 버튼 자리(창이 덮고 있어도)
  if (!(e.target.closest('[data-act=dex]') || onIcon || (panel && panel.k === 'dex' && (e.target.closest('.phead') || e.target.closest('.tabs'))))) return;
  const now = Date.now(); cheat.t = (cheat.t || []).filter(x => now - x < 3000); cheat.t.push(now);
  if (cheat.t.length >= 5) { cheat.t = []; S.coins += 3000; save(); toast('+3000 코인'); render(); }
});
document.addEventListener('click', e => {
  const b = e.target.closest('[data-act]'); if (!b) return;
  const a = b.dataset.act, v = b.dataset.v;
  if (a === 'mode-join' || a === 'mode-login') { startMode = a.slice(5); return renderStart(); }
  if (['feed', 'play', 'wash', 'sleep', 'talk'].includes(a)) { if (a === 'feed') { panel = null; document.querySelector('.sheet')?.remove(); } return act(a); }
  if (a === 'prev' || a === 'next') { const ids = Object.keys(S.owned), i = ids.indexOf(cur()); S.cur = ids[(i + (a === 'next' ? 1 : ids.length - 1)) % ids.length]; sayText = null; save(); return render(); }
  if (['who', 'profile', 'decor', 'gacha', 'dex', 'menu', 'give', 'job', 'mail', 'travel'].includes(a)) return openPanel(a);
  if (a === 'gotrip') return startTrip(v);
  if (a === 'dojob') { const o = S.owned[cur()], j = JOBS[+v]; o.job = { until: Date.now() + j[1] * 60000, pay: j[2] }; o.sleeping = false; save(); panel = null; document.querySelector('.sheet')?.remove(); sayText = '(다녀올게)'; const jg = girlOf(cur()); if (jg) toast(`${nameOf(jg)}: ${GLX(jg).job}`); return render(); }
  if (a === 'getmail') { const n = (S.mail || []).reduce((t, m) => t + m.c, 0); S.coins += n; S.mail = []; save(); panel = null; document.querySelector('.sheet')?.remove(); toast(`+${n} 코인`); return render(); }
  if (a === 'gtab') { panel.tab = v; panel.sel = null; return renderPanel(); }
  if (a === 'givesel') { panel.sel = v; return renderPanel(); }
  if (a === 'gcancel') { panel.sel = null; return renderPanel(); }
  if (a === 'giveit') return give(v);
  if (a === 'close') return closePanel();
  if (a === 'pick') { S.cur = b.dataset.id; sayText = null; save(); panel = null; document.querySelector('.sheet')?.remove(); return render(); }
  if (a === 'logout') { panel = null; document.querySelector('.sheet')?.remove(); return logOut(); }
  if (a === 'pull') return pull();
  if (a === 'xtab') { panel.tab = v; return renderPanel(); }
  if (a === 'setget') { const st = SETS.find(x => x.k === v); if (!st || !setDone(st) || (S.sets || {})[v]) return; S.sets = Object.assign({}, S.sets, { [v]: true }); S.coins += SET_PAY; save(); toast(`「${st.n}」 조합 완성! +${SET_PAY} 코인`); render(); return renderPanel(); }
  if (a === 'pair') return openPanel('pair');
  if (a === 'gpull') return gpull();
  if (a === 'gplace') return openPanel('place', { g: v });
  if (a === 'gput') { const g = panel.g; S.girls[g].with = v; S.cur = v; save(); panel = null; document.querySelector('.sheet')?.remove(); sayText = null; GA.x = -anim.x || 0.4; GA.sayT = withHim(GLX(g).hello, g); GA.sayUntil = anim.tick + 22; GA.heart = 14; render(); return openPanel('names', { g }); }
  if (a === 'gnames') return openPanel('names', { g: v });
  if (a === 'coin') { const n = 10 + Math.floor(Math.random() * 21); S.coins += n; b.remove(); dropStyle = null; toast(`+${n} 코인`); save(); document.querySelector('.pill.coin').lastChild.textContent = S.coins.toLocaleString('ko-KR'); return; }
  if (a === 'dtab') { panel.tab = v; panel.pv = null; return renderPanel(); }
  if (a === 'dcancel') { panel.pv = null; return renderPanel(); }
  if (a === 'dslot') { panel.slot = v; panel.pv = null; return renderPanel(); }
  const o = S.owned[cur()]; if (!o) return;
  const tab = panel?.tab || 'wall', slot = panel?.slot || 'a', key = tab === 'wall' ? 'wp' : tab === 'floor' ? 'fl' : tab === 'furn' ? slot : tab === 'deco' ? 'dc' : 'pr';
  if (a === 'dcol' && panel.pv && panel.pv.tab === tab) { panel.pv.col = +v; return renderPanel(); }
  if (a === 'dcol') { const i = +v; if (tab === 'wall') o.room.wc = i; else if (tab === 'floor') o.room.fc = i; else if (o.room[key]) o.room[key] = [o.room[key][0], i]; save(); render(); return renderPanel(); }
  if (a === 'dbuy' && panel.pv) {
    const pv = panel.pv; if (S.coins < PRICE[tab]) return toast('코인이 부족해요.');
    S.coins -= PRICE[tab]; S.items.push(pv.val);
    if (tab === 'wall') { o.room.wp = pv.val; o.room.wc = pv.col; } else if (tab === 'floor') { o.room.fl = pv.val; o.room.fc = pv.col; } else o.room[pv.key] = [pv.val, pv.col];
    panel.pv = null; toast(`샀어요. -${PRICE[tab]} 코인`); save(); render(); return renderPanel();
  }
  if (a === 'ditem') {
    if (v === 'none') { o.room[key] = null; save(); render(); return renderPanel(); }
    if (!S.items.includes(v)) { const cc = tab === 'wall' ? o.room.wc : tab === 'floor' ? o.room.fc : (o.room[key] ? o.room[key][1] : 0); panel.pv = { tab, key, val: v, col: cc }; return renderPanel(); }
    panel.pv = null;
    if (tab === 'wall' || tab === 'floor') o.room[key] = v; else o.room[key] = [v, o.room[key] ? o.room[key][1] : 0];
    save(); render(); return renderPanel();
  }
});

// ---------- 움직임 ----------
const MODES = ['walk', 'walk', 'idle', 'back', 'hop', 'walk', 'idle'];
setInterval(() => animStep(true), 170);
function animStep(adv) {
  const man = $('#man'); if (!man || !S) return;
  const id = cur(), o = S.owned[id], A = anim, n = FR[id] || [4, 4, 4, 4];
  if (!adv) { paintMan(man, id, o, A, n); return paintGirl(id, o); }
  A.tick++; A.f++; A.t--;
  if (A.mode === 'walk') { A.x += A.dir * 0.025; if (Math.abs(A.x) > 0.9) { A.dir = -A.dir; A.x = Math.max(-0.9, Math.min(0.9, A.x)); } }
  if (A.t <= 0) { A.face = null; A.mode = pick(MODES); A.t = 12 + Math.floor(Math.random() * 18); if (Math.random() < .5) A.dir = -A.dir; }
  if (Date.now() - (S.lastDrop || 0) > DROP_MS && !$('#drop') && !o.job) { const r = document.querySelector('.lcd .room'); if (r) { dropStyle = `position:absolute;left:${10 + Math.random() * 75}%;bottom:${4 + Math.random() * 18}%;width:30px;height:30px;padding:0;border:0;background:url(assets/ui/ic_coin.png) center/24px no-repeat;z-index:3;animation:emo 1s ease-in-out infinite`; placeDrop(); S.lastDrop = Date.now(); } }
  const g = girlOf(id);
  if (!g) { if (A.tick % 45 === 0) A.mumT = mumbleOf(id, o); else if (A.tick % 45 === 20) A.mumT = ''; }
  else if (!o.sleeping && !o.job) pairStep(id, o, g);
  if (A.heart > 0) A.heart--;
  if (o.job) { man.style.display = 'none'; $('#shd').style.display = 'none'; $('#emo').hidden = true; $('#mum').hidden = true; const jl = $('#jobleft'); if (jl) jl.textContent = timeLeft(o.job.until); if (Date.now() >= o.job.until) { tickTime(); save(); render(); } return; }
  paintMan(man, id, o, A, n);
  paintGirl(id, o);
}
// 둘이 같이 있을 때: 따로 걷다가 가끔 대화, 하트, 다툼
const GA = { x: 0.4, dir: -1, mode: 'walk', t: 14, f: 0, heart: 0, angry: 0, face: null, sayT: '', sayUntil: 0, next: null };
function pairStep(id, o, g) {
  const A = anim, G = GA, gl = GLX(g), T = A.tick;
  G.f++; G.t--;
  if (G.mode === 'walk') { G.x += G.dir * 0.022; if (Math.abs(G.x) > 0.9) { G.dir = -G.dir; G.x = Math.max(-0.9, Math.min(0.9, G.x)); } }
  if (G.t <= 0) { G.face = null; G.mode = pick(['walk', 'walk', 'idle', 'back', 'walk']); G.t = 12 + Math.floor(Math.random() * 18); if (Math.random() < .5) G.dir = -G.dir; }
  if (G.heart > 0) G.heart--; if (G.angry > 0) G.angry--;
  if (A.mumT && T >= (A.mumUntil || 0)) A.mumT = '';
  if (G.sayT && T >= G.sayUntil) G.sayT = '';
  if (G.next && T >= G.next.at) { G.sayT = G.next.t; G.sayUntil = T + 20; if (G.next.fx === 'heart') G.heart = 14; G.next = null; }
  if (T % 60 !== 0) return;
  const r = Math.random(), side = A.x > 0 ? -1 : 1, meet = () => { G.x = Math.max(-0.9, Math.min(0.9, A.x + side * 0.62)); A.mode = G.mode = 'idle'; A.t = G.t = 26; };
  if (r < .5) { A.mumT = mumbleOf(id, o); A.mumUntil = T + 16; G.next = { at: T + 14, t: withHim(lineOf(gl, id, 'react'), g) }; }
  else if (r < .8) { meet(); A.face = side > 0 ? 3 : 2; G.face = side > 0 ? 2 : 3; A.heart = 18; G.heart = 18; A.mumT = boyLine(g, id, 'heart', BOY_HEART); A.mumUntil = T + 12; G.next = { at: T + 12, t: withHim(lineOf(gl, id, 'heart'), g), fx: 'heart' }; o.fun = clamp(o.fun + 2); }
  else { meet(); A.face = side > 0 ? 2 : 3; G.face = side > 0 ? 3 : 2; A.angry = 16; G.angry = 18; G.sayT = pick(gl.fight); G.sayUntil = T + 20; A.mumT = boyLine(g, id, 'fight', BOY_FIGHT); A.mumUntil = T + 34; G.next = { at: T + 36, t: withHim(pick(gl.makeup), g), fx: 'heart' }; }
}
function paintGirl(id, o) {
  const man = $('#gman'); if (!man) return;
  const g = girlOf(id), G = GA, n = FR[g] || [4, 4, 4, 4], hide = o.sleeping || o.job;
  man.style.display = hide ? 'none' : ''; $('#gshd').style.display = hide ? 'none' : '';
  const emo = $('#gemo'), mum = $('#gmum');
  if (hide) { emo.hidden = true; mum.hidden = true; return; }
  const row = G.face != null && G.mode === 'idle' ? G.face : G.mode === 'walk' ? (G.dir < 0 ? 2 : 3) : G.mode === 'back' ? 1 : 0;
  const col = G.mode === 'walk' ? G.f % n[row] : 0, img = man.firstElementChild;
  img.style.marginLeft = -col * 66 + 'px'; img.style.marginTop = -row * 91 + 'px';
  man.style.left = `calc(50% + ${G.x * 38}% - 33px)`; $('#gshd').style.left = `calc(50% + ${G.x * 38}% - 27px)`;
  const e = G.angry > 0 ? ['흥!', '#c0392b'] : G.heart > 0 ? ['♥', '#e0457b'] : null;
  emo.hidden = !e; if (e) { emo.textContent = e[0]; emo.style.color = e[1]; emo.style.left = `calc(50% + ${G.x * 38}% + 14px)`; emo.style.bottom = '52%'; }
  mum.hidden = !G.sayT; if (G.sayT) { mum.textContent = G.sayT; mum.style.left = `clamp(4px, calc(50% + ${G.x * 38}% - 70px), calc(100% - 64%))`; }
}
function paintMan(man, id, o, A, n) {
  const sl_ = $('#sleepleft'); if (o.sleeping && sl_) { sl_.textContent = timeLeft(wakeAt(o)).replace(' 남음', ''); if (Date.now() >= wakeAt(o)) { tickTime(); save(); return render(); } }
  if (o.job) { man.style.display = 'none'; return; }
  const sl = o.sleeping, row = sl ? 0 : A.face != null && A.mode === 'idle' ? A.face : A.mode === 'walk' ? (A.dir < 0 ? 2 : 3) : A.mode === 'back' ? 1 : 0;
  const col = A.mode === 'walk' && !sl ? A.f % n[row] : 0, x = sl ? 0 : A.x, left = `calc(50% + ${x * 38}% - 33px)`;
  const img = man.firstElementChild; img.style.marginLeft = -col * 66 + 'px'; img.style.marginTop = -row * 91 + 'px';
  man.style.left = left; man.style.display = sl ? 'none' : ''; $('#shd').style.display = sl ? 'none' : ''; man.classList.toggle('hop', A.mode === 'hop' && !sl);
  $('#shd').style.left = `calc(50% + ${x * 38}% - 27px)`;
  if (A.angry > 0) A.angry--;
  const emo = $('#emo'), e = sl ? null : A.angry > 0 ? ['....!?', '#c0392b'] : A.heart > 0 ? ['♥ ♥', '#e0457b'] : o.food < 40 ? ['꼬르륵....', '#c47a1a'] : o.clean < 35 ? ['킁킁....', '#5b8a3c'] : o.fun > 75 ? ['♪', '#2f8f73'] : null;
  emo.hidden = !e; if (e) { emo.textContent = e[0]; emo.style.color = e[1]; emo.style.left = `calc(50% + ${x * 38}% + 14px)`; emo.style.bottom = sl ? '30%' : '52%'; }
  const mum = $('#mum'), mt = !sl ? (A.mumT || '') : '';
  mum.hidden = !mt; if (mt) { mum.textContent = mt; mum.style.left = `clamp(4px, calc(50% + ${x * 38}% - 70px), calc(100% - 64%))`; }
}
setInterval(() => { if (S && user) { tickTime(); save(); } }, 60000);

// ---------- 시작 ----------
(async () => {
  // 새 버전 확인: version.json은 저장해 두지 않고 매번 새로 받아요. 더 새 버전이 있으면 주소를 바꿔 새로 불러와요
  try {
    const nv = (await fetch('version.json?t=' + Date.now(), { cache: 'no-store' }).then(r => r.json())).v;
    if (nv > APP_V && !location.search.includes('u=' + nv)) { location.replace(location.pathname + '?u=' + nv); return; }
  } catch { }
  app.innerHTML = '<div class="start"><div class="egg"><div class="scr"></div></div><div class="note">불러오는 중....</div></div>';
  const [c, t, f, it, mu, ct, tv, gl, sts] = await Promise.all(['data/chars.json', 'data/talk.json', 'data/frames.json', 'data/items.json', 'data/mumble.json', 'data/countries.json', 'data/travel.json', 'data/girls.json', 'data/sets.json'].map(u => fetch(u + '?v=107').then(r => r.ok ? r.json() : {})));
  CH = c; CHM = Object.fromEntries(c.map(x => [x.id, x])); TALK = t; FR = f; IT = it; ITM = Object.fromEntries(it.map(x => [x.k, x])); MUM = mu; CTRY = ct; TRV = tv; GL = Array.isArray(gl) ? gl : []; SETS = Array.isArray(sts) ? sts : []; GLM = Object.fromEntries(GL.map(x => [x.id, x]));
  try { await initFirebase(); } catch (e) { console.warn('Firebase 연결 실패, 기기 저장으로', e); fb = null; }
  if (fb) {
    fb.AU.onAuthStateChanged(fb.auth, async u => { if (u && !user) { user = { uid: u.uid, id: u.email.split('@')[0] }; await enter(); } else if (!u) { user = null; render(); } });
  } else {
    const id = lsGet('bp_session'); if (id) { user = { uid: 'local_' + id, id }; await enter(); } else render();
  }
})();
