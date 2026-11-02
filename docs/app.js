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
  wall: [['mintdot', '땡땡이'], ['skystripe', '줄무늬'], ['heart', '하트'], ['starnight', '별'], ['lemon', '체크'], ['cloud', '구름'], ['washi', '일본식'], ['plaid', '타탄'], ['lilac', '반짝이']],
  floor: [['wood', '원목 마루'], ['tatami', '다다미'], ['minttile', '타일'], ['pinkrug', '카펫'], ['checker', '체커'], ['grass', '잔디'], ['skytile', '큰 타일']],
  furn: [['bed', '침대', 44, 28], ['sofa', '소파', 40, 26], ['shelf', '책장', 26, 44], ['desk', '책상', 36, 30], ['kotatsu', '코타츠', 40, 22], ['fridge', '냉장고', 20, 38], ['tv', 'TV', 34, 32], ['wardrobe', '옷장', 28, 44], ['amp', '앰프·기타', 30, 34], ['lowtable', '좌식 밥상', 36, 24]],
  deco: [['window', '창문', 28, 24], ['clock', '벽시계', 16, 16], ['poster', '포스터', 18, 24], ['wallshelf', '선반', 30, 16], ['garland', '가랜드', 44, 10], ['mirror', '거울', 16, 22], ['frame', '액자', 24, 18], ['stars', '별 스티커', 20, 20]],
  prop: [['soba', '소바', 16, 12], ['strawmilk', '딸기우유', 10, 16], ['coffeejelly', '커피젤리', 14, 14], ['console', '게임기', 18, 10], ['guitar', '기타', 12, 26], ['baseball', '배트·공', 20, 18], ['manga', '만화책', 16, 14], ['jump', '점프', 14, 18], ['headphones', '헤드폰', 18, 14], ['cat', '고양이', 18, 14], ['plant', '화분', 14, 20], ['camera', '카메라', 18, 12], ['watermelon', '수박', 18, 14], ['milk', '우유병', 8, 16], ['curry', '카레', 18, 10], ['sketch', '스케치북', 16, 14], ['gi', '도복 띠', 18, 10], ['wing', '깃털', 12, 18], ['tobacco', '재떨이', 14, 8], ['glasses', '안경 케이스', 16, 8]]
};
const PRICE = { wall: 80, floor: 80, furn: 200, deco: 60, prop: 40 };
const STAGES = [['첫 만남', 'first', 0], ['친구', 'friend', 25], ['썸', 'crush', 50], ['연인', 'lover', 75]];
const stageOf = l => STAGES.filter(s => l >= s[2]).pop();
const GACHA = 300, DUP = 150, TALK_MAX = 3, LOVE_DAY = 4;   // 애정은 하루 최대 4 → 한 단계(25)에 약 일주일
function addLove(o, n) { if (!o.lv || o.lv.day !== today()) o.lv = { day: today(), g: 0 }; const g = Math.max(0, Math.min(n, LOVE_DAY - o.lv.g)); o.lv.g += g; o.love = clamp(o.love + g); return g; }
let CH = [], CHM = {}, TALK = {}, FR = {};

function spr(cat, k, col, sc) {
  const S = SHEET[cat], L = ITEMS[cat], i = Math.max(0, L.findIndex(x => x[0] === k)), it = L[i];
  return `<div class="clip" style="width:${it[2] * sc}px;height:${it[3] * sc}px;POS"><img class="px" src="assets/decor/${cat}.png" alt="" style="width:${S.sw * sc}px;height:${S.sh * sc}px;margin-left:${-col * S.cw * sc}px;margin-top:${-i * S.ch * sc}px"></div>`;
}
const face = (id, w) => { const s = w / 96; return `<img class="px" src="assets/ch/${id}.webp" alt="" style="position:absolute;width:${384 * s}px;height:${528 * s}px;left:${-(96 * s - w) / 2}px;top:0;max-width:none">`; };

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
function fresh() { return { v: 1, at: Date.now(), coins: GACHA, owned: {}, cur: null, items: ['mintdot', 'cloud', 'wood', 'checker', 'bed', 'window', 'plant'], day: today(), last: Date.now() }; }
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
  S.last = now;
  if (S.day !== today()) { S.day = today(); S.coins += 100; toast('오늘의 출석 보너스 +100코인'); }
}

// ---------- 화면 ----------
let panel = null, anim = { x: 0, dir: 1, mode: 'walk', t: 20, f: 0, mum: -1, heart: 0, tick: 0 }, sayText = null;
const cur = () => S.cur && S.owned[S.cur] ? S.cur : Object.keys(S.owned)[0];
const nameOf = id => id === 'hidden' ? (S.owned.hidden?.name || '???') : CHM[id].name;

function roomHTML(id, o, scale) {
  const r = o.room;
  return `<div class="room pw-${r.wp}" style="background-color:${PAL[r.wc][1]};background-image:url(assets/decor/wall_${r.wp}.png)">
    <div class="floor" style="background-color:${PAL[r.fc][1]};background-image:url(assets/decor/floor_${r.fl}.png)"></div>
    ${spr('deco', r.dc[0], r.dc[1], 2).replace('POS', 'left:6%;top:6%')}
    ${spr('furn', r.a[0], r.a[1], 2).replace('POS', 'left:3%;bottom:20%')}
    ${spr('furn', r.b[0], r.b[1], 2).replace('POS', 'right:3%;bottom:20%')}
    ${spr('prop', r.pr[0], r.pr[1], 2).replace('POS', 'left:28%;bottom:4%;z-index:2')}
    ${id ? `<div class="shadow" id="shd"></div><div class="man" id="man"><img class="px" src="assets/ch/${id}.webp" alt="${esc(nameOf(id))}"></div><span class="emo" id="emo" hidden></span><span class="mumble" id="mum" hidden></span>` : ''}
    ${o.sleeping ? '<div class="night"></div>' : ''}
  </div>`;
}
function meterHTML(o) {
  const st = stageOf(o.love), nx = STAGES[STAGES.indexOf(st) + 1];
  const m = (l, v, c) => `<div class="meter"><div class="row"><span>${l}</span><span>${v}</span></div><div class="bar"><i style="width:${v}%;background-color:${v < 30 ? '#ff9a8a' : c}"></i></div></div>`;
  return `<div class="meters">${m('배부름', o.food, '#ffd76a')}${m('기분', o.fun, '#8fe3cc')}${m('청결', o.clean, '#8ccff5')}${m('체력', o.energy, '#c6b5ff')}
    <div class="meter wide"><div class="row"><span>애정 · ${st[0]}</span><span>${nx ? `다음 단계까지 ${nx[2] - o.love} · 오늘 +${o.lv && o.lv.day === today() ? o.lv.g : 0}/${LOVE_DAY}` : '최고 단계'}</span></div><div class="bar"><i style="width:${o.love}%;background-color:#ff8fb3"></i></div></div></div>`;
}
const ic = (act, img, label, pressed) => `<button class="ic" data-act="${act}" ${pressed ? 'aria-pressed="true"' : ''}><img src="assets/ui/ic_${img}.png" alt="">${label}</button>`;

function render() {
  if (!user) return renderStart();
  if (!Object.keys(S.owned).length) { app.innerHTML = shellEmpty(); if (panel?.k !== 'gacha') openPanel('gacha'); return; }
  const id = cur(), o = S.owned[id], t = o.talk.day === today() ? o.talk.n : 0;
  app.innerHTML = `<div class="shell">
    <div class="brand"><img src="assets/ui/ic_heart.png" alt="">BOIFRIENDS POCKET</div>
    <div class="topbar"><button class="who" data-act="who" aria-label="돌볼 사람 바꾸기"><span class="face">${face(id, 32)}</span><span>${esc(nameOf(id))}</span><img src="assets/ui/ic_back.png" alt="" style="width:14px;transform:rotate(-90deg)"></button>
      <span class="pill coin"><img src="assets/ui/ic_coin.png" alt="">${S.coins.toLocaleString('ko-KR')}</span></div>
    <div class="icons">${ic('feed', 'food', '밥')}${ic('play', 'play', '놀기')}${ic('wash', 'wash', '씻기')}${ic('sleep', 'sleep', o.sleeping ? '깨우기' : '재우기', o.sleeping)}${ic('talk', 'talk', '대화')}</div>
    <div class="lcd">${roomHTML(id, o)}</div>
    <div class="say"><b>${esc(nameOf(id))} <span>오늘 대화 ${t}/${TALK_MAX} · 나를 “${esc(o.call)}”(이)라고 불러요</span></b><span id="say">${esc(sayText || defaultSay(id, o))}</span></div>
    ${meterHTML(o)}
    <div class="icons">${ic('profile', 'heart', '프로필')}${ic('decor', 'decor', '꾸미기')}${ic('gacha', 'gacha', '가챠')}${ic('dex', 'dex', '도감')}${ic('menu', 'home', '메뉴')}</div>
    <div class="abc"><button class="round" data-act="prev" aria-label="이전 사람">◀</button><button class="round b" data-act="talk" aria-label="말 걸기">♥</button><button class="round" data-act="next" aria-label="다음 사람">▶</button></div>
  </div>`;
  if (panel) renderPanel();
}
function shellEmpty() {
  return `<div class="shell"><div class="brand"><img src="assets/ui/ic_heart.png" alt="">BOIFRIENDS POCKET</div>
    <div class="lcd"><div class="room" style="background-color:#cfeaff;display:flex;align-items:center;justify-content:center"><span style="background:#fff;border:3px solid var(--ink);border-radius:12px;padding:8px 12px;font-size:12px;text-align:center;line-height:1.6">아직 아무도 없어요.<br>가챠를 돌려 첫 남자친구를 만나요!</span></div></div>
    <button class="btn yellow" data-act="gacha" style="width:100%">첫 가챠 돌리기</button></div>`;
}
function defaultSay(id, o) {
  if (o.sleeping) return '(쿨쿨 자고 있어요. 체력이 차는 중.)';
  if (o.food < 30) return '(배가 고파 보여요. 밥을 주세요.)';
  if (o.clean < 30) return '(좀 씻겨야 할 것 같아요.)';
  return id === 'hidden' ? '(말 걸어 볼까요? ♥ 버튼이나 대화를 눌러요.)' : `(${CHM[id].tag}. 말 걸어 볼까요?)`;
}

// ---------- 시작 화면 ----------
let startMode = 'join';
function renderStart() {
  app.innerHTML = `<div class="start">
    <div class="egg"><div class="scr"><img src="assets/ui/ic_heart.png" alt="" style="width:40px;margin-bottom:18px"></div></div>
    <div style="text-align:center"><h1>보이프렌즈 포켓</h1><div class="note">주머니 속 남자친구를 키워 보세요</div></div>
    <div class="card" style="width:100%;padding:0;overflow:hidden">
      <div style="display:grid;grid-template-columns:1fr 1fr;border-bottom:3px solid var(--ink)">
        <button data-act="mode-join" style="height:44px;border:0;font-weight:700;background:${startMode === 'join' ? 'var(--yellow)' : '#fff'}">가입하기</button>
        <button data-act="mode-login" style="height:44px;border:0;border-left:3px solid var(--ink);font-weight:700;background:${startMode === 'login' ? 'var(--yellow)' : '#fff'}">로그인</button></div>
      <form id="auth" style="padding:14px;display:flex;flex-direction:column;gap:8px">
        <label class="label" for="uid">아이디</label><input class="field" id="uid" name="uid" autocomplete="username" required minlength="4" maxlength="12" pattern="[A-Za-z0-9_]+" placeholder="영문·숫자 4~12자">
        <label class="label" for="pw">비밀번호</label><input class="field" id="pw" name="pw" type="password" autocomplete="${startMode === 'join' ? 'new-password' : 'current-password'}" required minlength="6" placeholder="6자 이상">
        <button class="btn" type="submit" style="margin-top:6px">${startMode === 'join' ? `가입하고 ${GACHA}코인 받기` : '로그인'}</button>
      </form></div>
    <div class="note">${fb ? '로그인하면 이 기기와 계정 모두에 저장돼요.<br>폰을 바꿔도 같은 아이디로 이어서 할 수 있어요.' : (window.FIREBASE_CONFIG ? '서버에 연결하지 못해서 지금은 이 기기에만 저장돼요. 잠시 후 새로고침해 보세요.' : '지금은 서버 설정 전이라 이 기기에만 저장돼요.')}</div>
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
  document.querySelector('.sheet')?.remove();
  const f = { who: pWho, profile: pProfile, decor: pDecor, gacha: pGacha, dex: pDex, menu: pMenu }[panel.k];
  const [title, body] = f();
  const el = document.createElement('div'); el.className = 'sheet';
  el.innerHTML = `<div class="panel" role="dialog" aria-label="${esc(title)}"><div class="phead"><h2>${esc(title)}</h2>${Object.keys(S.owned).length ? '<button class="close" data-act="close" aria-label="닫기"><img src="assets/ui/ic_back.png" alt=""></button>' : `<span class="pill coin"><img src="assets/ui/ic_coin.png" alt="">${S.coins}</span>`}</div><div class="pbody">${body}</div></div>`;
  el.addEventListener('click', e => { if (e.target === el) closePanel(); });
  document.body.appendChild(el);
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
      <div style="padding:10px 12px;display:flex;justify-content:space-between;align-items:center;gap:8px"><div><div style="font-size:16px;font-weight:700">${esc(nameOf(id))}</div><div class="label">${esc(c.work)} · ${esc(c.tag)}</div></div><span class="pill">${stageOf(o.love)[0]} · ${o.love}</span></div></div>
    <form id="callf" class="card" style="display:flex;flex-direction:column;gap:6px">
      ${id === 'hidden' ? `<label class="label" for="hname">이 사람의 이름</label><input class="field" id="hname" maxlength="8" value="${esc(o.name || '')}" placeholder="이름을 지어 주세요">` : ''}
      <label class="label" for="call">나를 부르는 이름</label><div style="display:flex;gap:8px"><input class="field" id="call" maxlength="8" value="${esc(o.call)}"><button class="btn" type="submit">저장</button></div>
      <span class="label">사람마다 따로 정할 수 있어요. 대사 속 호칭이 이 이름으로 바뀌어요.</span></form>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div class="card" style="background:var(--mint2)"><b style="font-size:11px">좋아하는 것</b><div style="font-size:12px;line-height:1.7;margin-top:4px">${c.likes.map(esc).join('<br>')}</div></div>
      <div class="card" style="background:var(--pink2)"><b style="font-size:11px">싫어하는 것</b><div style="font-size:12px;line-height:1.7;margin-top:4px">${c.dislikes.map(esc).join('<br>')}</div></div></div>`];
}
function pDecor() {
  const id = cur(), o = S.owned[id], r = o.room, tab = panel.tab || 'wall', slot = panel.slot || 'a';
  const key = tab === 'wall' ? 'wp' : tab === 'floor' ? 'fl' : tab === 'furn' ? slot : tab === 'deco' ? 'dc' : 'pr';
  const pal = tab === 'wall' || tab === 'floor' ? PAL : VAR, curCol = tab === 'wall' ? r.wc : tab === 'floor' ? r.fc : r[key][1];
  const tabs = [['wall', '벽지'], ['floor', '바닥'], ['furn', '가구'], ['deco', '벽 장식'], ['prop', '소품']].map(t => `<button class="tab" role="tab" aria-selected="${t[0] === tab}" data-act="dtab" data-v="${t[0]}">${t[1]}</button>`).join('');
  const items = ITEMS[tab].map(it => {
    const k = it[0], on = tab === 'wall' ? r.wp === k : tab === 'floor' ? r.fl === k : r[key][0] === k, have = S.items.includes(k);
    const th = tab === 'wall' || tab === 'floor' ? `<div class="th" style="background-color:${PAL[tab === 'wall' ? r.wc : r.fc][1]};background-image:url(assets/decor/${tab}_${k}.png)"></div>`
      : `<div class="th">${spr(tab, k, curCol, Math.max(it[2], it[3]) > 24 ? 1 : 2).replace('POS', 'position:relative')}</div>`;
    return `<button class="item" data-act="ditem" data-v="${k}" aria-pressed="${on}">${th}<span>${it[1]}</span><small style="color:${on ? '#b8336a' : have ? '#1f7a60' : 'inherit'}">${on ? '사용 중' : have ? '보유' : PRICE[tab] + '코인'}</small></button>`;
  }).join('');
  return ['방 꾸미기', `<div class="lcd" style="padding:4px">${roomHTML(null, o)}</div>
    <div class="tabs" role="tablist">${tabs}</div>
    <div class="tabbody" style="display:flex;flex-direction:column;gap:8px">
      ${tab === 'furn' ? `<div style="display:flex;gap:6px;align-items:center"><span class="label">놓을 자리</span>${[['a', '왼쪽'], ['b', '오른쪽']].map(s => `<button class="pill" data-act="dslot" data-v="${s[0]}" style="${s[0] === slot ? 'background:var(--yellow)' : ''}">${s[1]}</button>`).join('')}</div>` : ''}
      <div class="label">색상 · ${pal[curCol][0]}</div>
      <div class="sw">${pal.map((c, i) => `<button data-act="dcol" data-v="${i}" aria-label="${c[0]}" title="${c[0]}" aria-pressed="${i === curCol}" style="background:${c[1]}"></button>`).join('')}</div>
      <div class="grid4">${items}</div></div>`];
}
function pGacha() {
  const first = !Object.keys(S.owned).length;
  return [first ? '첫 남자친구 뽑기' : '남자친구 가챠', `
    ${first ? `<div class="card" style="text-align:center;font-size:12px;line-height:1.6">처음 받은 ${GACHA}코인으로 한 번 돌려 보세요.<br>나온 사람이 첫 번째 남자친구가 돼요.</div>` : ''}
    <div class="machine" id="machine"><img class="m px" src="assets/ui/machine.png" alt="가챠 기계"><button class="knob" data-act="pull" aria-label="손잡이 돌리기"></button></div>
    <button class="btn yellow" data-act="pull" ${S.coins < GACHA ? 'disabled' : ''}>손잡이 돌리기 · ${GACHA}코인</button>
    <div class="card label" style="line-height:1.7">25명 중 한 명이 나와요. 이미 만난 사람이 또 나오면 ${DUP}코인을 돌려받아요.<br>아주 낮은 확률로 히든 캐릭터가 나와요. 이름은 직접 지어 줄 수 있어요.<br>코인은 돌보기·대화와 매일 출석으로 모여요.</div>`];
}
function pDex() {
  const all = CH, met = all.filter(c => S.owned[c.id]).length;
  return ['도감', `<div class="card"><div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700"><span>만난 사람</span><span>${met} / ${all.length}</span></div><div class="bar" style="margin-top:6px"><i style="width:${met / all.length * 100}%;background-color:var(--mint)"></i></div></div>
    <div class="grid4">${all.map(c => { const o = S.owned[c.id]; return `<div class="tile"><div class="pic">${o ? face(c.id, 72).replace('position:absolute;', 'position:absolute;') : '<div class="sil"><i class="h"></i><i class="bd">?</i></div>'}</div><span style="color:${o ? 'inherit' : 'var(--ink2)'}">${o ? esc(nameOf(c.id)) : '???'}</span>${o ? `<span class="label">${stageOf(o.love)[0]}</span>` : ''}</div>`; }).join('')}</div>`];
}
function pMenu() {
  return ['메뉴', `<div class="card" style="font-size:12px;line-height:1.8">아이디: <b>${esc(user.id)}</b><br>저장: ${fb ? '계정(서버) + 이 기기' : '이 기기에만'}</div>
    <div class="card label" style="line-height:1.7">· 시간이 지나면 배부름·기분·청결·체력이 줄어요.<br>· 재우면 체력이 차요.<br>· 대화는 사람마다 하루 ${TALK_MAX}번. 애정 단계마다 대답이 달라져요.<br>· 애정은 하루 최대 +${LOVE_DAY}. 꾸준히 돌보면 일주일에 한 단계쯤 올라요.<br>· 너무 오래 굶기고 방치하면 애정이 조금 줄어요.<br>· 돌보면 코인이 모여요. 매일 처음 들어오면 +100코인.</div>
    <button class="btn white" data-act="logout">로그아웃</button>`];
}

// ---------- 행동 ----------
function act(kind) {
  const id = cur(), o = S.owned[id]; if (!o) return;
  const say = t => { sayText = t; };
  if (o.sleeping && kind !== 'sleep') { say('(자는 중이에요. 깨우려면 깨우기를 눌러요.)'); return render(); }
  if (kind === 'feed') { if (o.food >= 95) say('(배불러서 더는 못 먹겠대요.)'); else { o.food = clamp(o.food + 25); addLove(o, 1); S.coins += 10; anim.heart = 10; say('(밥을 줬다. 배부름 +25 · 코인 +10)'); } }
  if (kind === 'play') { if (o.energy < 15) say('(너무 지쳐서 못 놀겠대요. 재워 주세요.)'); else { o.fun = clamp(o.fun + 22); o.energy = clamp(o.energy - 12); addLove(o, 1); S.coins += 10; anim.heart = 10; anim.mode = 'hop'; anim.t = 10; say('(같이 놀았다. 기분 +22 · 코인 +10)'); } }
  if (kind === 'wash') { if (o.clean >= 95) say('(이미 반짝반짝해요.)'); else { o.clean = clamp(o.clean + 35); S.coins += 5; say('(깨끗해졌다. 청결 +35 · 코인 +5)'); } }
  if (kind === 'sleep') { o.sleeping = !o.sleeping; say(o.sleeping ? '(불을 껐다. 잘 자.)' : '(일어났다. 좋은 아침.)'); }
  if (kind === 'talk') {
    if (o.talk.day !== today()) o.talk = { day: today(), n: 0, i: o.talk.i };
    if (o.talk.n >= TALK_MAX) say('(오늘은 충분히 이야기했어요. 내일 또 말 걸어 봐요.)');
    else {
      const lines = TALK[id][stageOf(o.love)[1]]; o.talk.i = (o.talk.i + 1) % lines.length; o.talk.n++;
      say(lines[o.talk.i].map(l => l.split('{call}').join(o.call)).join('\n'));
      addLove(o, 1); o.fun = clamp(o.fun + 3); S.coins += 15; anim.heart = 12;
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
  else { const c = CHM[got]; S.owned[got] = { love: 0, food: 70, fun: 60, clean: 80, energy: 80, call: '너', room: JSON.parse(JSON.stringify(c.room)), talk: { day: '', n: 0, i: -1 }, met: Date.now(), sleeping: false }; }
  S.cur = got; save(); pull.busy = false; reveal(got, dup);
}
function reveal(id, dup) {
  const c = CHM[id], hid = id === 'hidden', el = document.createElement('div'); el.className = 'reveal';
  el.innerHTML = `<div class="rcard"><div class="rstage ${hid ? 'hidden' : ''}"><img class="tw px" src="assets/ui/ic_star.png" alt="" style="left:22px;top:20px"><img class="tw px" src="assets/ui/ic_star.png" alt="" style="right:26px;top:44px">
      <span class="badge" style="${dup ? 'background:#fff' : hid ? 'background:var(--yellow)' : ''}">${dup ? '또 만났다!' : hid ? 'HIDDEN ✦' : 'NEW!'}</span>
      <div style="width:120px;height:165px;margin-bottom:10px;overflow:hidden;position:relative">${face(id, 120)}</div></div>
    <div class="rbody"><div class="nm">${hid && !dup ? '???' : esc(nameOf(id))}</div><div class="label">${esc(c.work)}</div><div style="font-size:13px;line-height:1.55">“${esc(c.gacha)}”</div>
      ${dup ? `<span class="pill coin">이미 만난 사람 · 코인 +${DUP}</span>` : ''}
      ${hid && !dup ? `<label class="label" for="hn" style="align-self:flex-start">이 사람의 이름</label><input class="field" id="hn" maxlength="8" placeholder="이름을 지어 주세요">` : ''}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;width:100%"><button class="btn white" data-r="again">한 번 더</button><button class="btn" data-r="go">방으로 가기</button></div></div></div>`;
  document.body.appendChild(el);
  el.onclick = e => {
    const b = e.target.closest('[data-r]'); if (!b) return;
    const hn = el.querySelector('#hn'); if (hn) { S.owned.hidden.name = hn.value.trim() || '???'; save(); }
    el.remove();
    if (b.dataset.r === 'go') { panel = null; document.querySelector('.sheet')?.remove(); sayText = null; render(); }
    else renderPanel();
  };
}

document.addEventListener('click', e => {
  const b = e.target.closest('[data-act]'); if (!b) return;
  const a = b.dataset.act, v = b.dataset.v;
  if (a === 'mode-join' || a === 'mode-login') { startMode = a.slice(5); return renderStart(); }
  if (['feed', 'play', 'wash', 'sleep', 'talk'].includes(a)) return act(a);
  if (a === 'prev' || a === 'next') { const ids = Object.keys(S.owned), i = ids.indexOf(cur()); S.cur = ids[(i + (a === 'next' ? 1 : ids.length - 1)) % ids.length]; sayText = null; save(); return render(); }
  if (['who', 'profile', 'decor', 'gacha', 'dex', 'menu'].includes(a)) return openPanel(a);
  if (a === 'close') return closePanel();
  if (a === 'pick') { S.cur = b.dataset.id; sayText = null; save(); panel = null; document.querySelector('.sheet')?.remove(); return render(); }
  if (a === 'logout') { panel = null; document.querySelector('.sheet')?.remove(); return logOut(); }
  if (a === 'pull') return pull();
  if (a === 'dtab') { panel.tab = v; return renderPanel(); }
  if (a === 'dslot') { panel.slot = v; return renderPanel(); }
  const o = S.owned[cur()]; if (!o) return;
  const tab = panel?.tab || 'wall', slot = panel?.slot || 'a', key = tab === 'wall' ? 'wp' : tab === 'floor' ? 'fl' : tab === 'furn' ? slot : tab === 'deco' ? 'dc' : 'pr';
  if (a === 'dcol') { const i = +v; if (tab === 'wall') o.room.wc = i; else if (tab === 'floor') o.room.fc = i; else o.room[key] = [o.room[key][0], i]; save(); render(); return renderPanel(); }
  if (a === 'ditem') {
    if (!S.items.includes(v)) { if (S.coins < PRICE[tab]) return toast('코인이 부족해요.'); S.coins -= PRICE[tab]; S.items.push(v); toast(`구매했어요. -${PRICE[tab]}코인`); }
    if (tab === 'wall' || tab === 'floor') o.room[key] = v; else o.room[key] = [v, o.room[key][1]];
    save(); render(); return renderPanel();
  }
});

// ---------- 움직임 ----------
const MODES = ['walk', 'walk', 'idle', 'back', 'hop', 'walk', 'idle'];
setInterval(() => {
  const man = $('#man'); if (!man || !S) return;
  const id = cur(), o = S.owned[id], A = anim, n = FR[id] || [4, 4, 4, 4];
  A.tick++; A.f++; A.t--;
  if (A.mode === 'walk') { A.x += A.dir * 0.025; if (Math.abs(A.x) > 0.9) { A.dir = -A.dir; A.x = Math.max(-0.9, Math.min(0.9, A.x)); } }
  if (A.t <= 0) { A.mode = pick(MODES); A.t = 12 + Math.floor(Math.random() * 18); if (Math.random() < .5) A.dir = -A.dir; }
  if (A.tick % 45 === 0) A.mum = Math.floor(Math.random() * 3); else if (A.tick % 45 === 20) A.mum = -1;
  if (A.heart > 0) A.heart--;
  const sl = o.sleeping, row = sl ? 0 : A.mode === 'walk' ? (A.dir < 0 ? 2 : 3) : A.mode === 'back' ? 1 : 0;
  const col = A.mode === 'walk' && !sl ? A.f % n[row] : 0, x = sl ? 0 : A.x, left = `calc(50% + ${x * 38}% - 33px)`;
  const img = man.firstElementChild; img.style.marginLeft = -col * 66 + 'px'; img.style.marginTop = -row * 91 + 'px';
  man.style.left = left; man.style.transform = sl ? 'rotate(-90deg) translateX(-14px)' : ''; man.classList.toggle('hop', A.mode === 'hop' && !sl);
  $('#shd').style.left = `calc(50% + ${x * 38}% - 27px)`;
  const emo = $('#emo'), e = sl ? ['Z z z', '#5b6bd6'] : A.heart > 0 ? ['♥ ♥', '#e0457b'] : o.food < 40 ? ['꼬르륵…', '#c47a1a'] : o.clean < 35 ? ['킁킁…', '#5b8a3c'] : o.fun > 75 ? ['♪', '#2f8f73'] : null;
  emo.hidden = !e; if (e) { emo.textContent = e[0]; emo.style.color = e[1]; emo.style.left = `calc(50% + ${x * 38}% + 14px)`; emo.style.bottom = sl ? '30%' : '52%'; }
  const mum = $('#mum'), mt = !sl && A.mum >= 0 ? CHM[id].mumble[A.mum] : '';
  mum.hidden = !mt; if (mt) { mum.textContent = mt; mum.style.left = `clamp(4px, calc(50% + ${x * 38}% - 70px), calc(100% - 64%))`; }
}, 170);
setInterval(() => { if (S && user) { tickTime(); save(); } }, 60000);

// ---------- 시작 ----------
(async () => {
  app.innerHTML = '<div class="start"><div class="egg"><div class="scr"></div></div><div class="note">불러오는 중…</div></div>';
  const [c, t, f] = await Promise.all(['data/chars.json', 'data/talk.json', 'data/frames.json'].map(u => fetch(u).then(r => r.json())));
  CH = c; CHM = Object.fromEntries(c.map(x => [x.id, x])); TALK = t; FR = f;
  try { await initFirebase(); } catch (e) { console.warn('Firebase 연결 실패, 기기 저장으로', e); fb = null; }
  if (fb) {
    fb.AU.onAuthStateChanged(fb.auth, async u => { if (u && !user) { user = { uid: u.uid, id: u.email.split('@')[0] }; await enter(); } else if (!u) { user = null; render(); } });
  } else {
    const id = lsGet('bp_session'); if (id) { user = { uid: 'local_' + id, id }; await enter(); } else render();
  }
})();
