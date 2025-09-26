let all = [];
let filtered = [];
let page = 1;
let pageSize = 25;

const $ = sel => document.querySelector(sel);
const byId = id => document.getElementById(id);

async function loadData(){
  setStatus('Loading…');
  try{
    const res = await fetch('/transcripts?limit=500', {headers:{'Accept':'application/json'}});
    if(!res.ok) throw new Error('HTTP '+res.status);
    all = await res.json();
    applyFilters();
    setStatus(`Loaded ${all.length} records`);
  }catch(err){
    setStatus('Failed to load');
  }
}

function setStatus(t){ byId('status').textContent = t; }

function applyFilters(){
  const q = byId('q').value.trim().toLowerCase();
  const sort = byId('sort').value;

  filtered = all.filter(it=>{
    const txt = ((it.speech_result||'') + ' ' + (it.call_sid||'') + ' ' + (it.from_||'') + ' ' + (it.to||'')).toLowerCase();
    return !q || txt.includes(q);
  });

  const getTime = it => Date.parse(it.created_at || 0) || 0;
  const getConf = it => (it.confidence==null ? -1 : Number(it.confidence));
  if(sort==='time-desc') filtered.sort((a,b)=> getTime(b)-getTime(a));
  if(sort==='time-asc')  filtered.sort((a,b)=> getTime(a)-getTime(b));
  if(sort==='conf-desc') filtered.sort((a,b)=> getConf(b)-getConf(a));
  if(sort==='conf-asc')  filtered.sort((a,b)=> getConf(a)-getConf(b));

  page = 1;
  render();
}

function render(){
  pageSize = parseInt(byId('pagesize').value,10) || 25;
  const start = (page-1)*pageSize;
  const end = Math.min(start+pageSize, filtered.length);
  const view = filtered.slice(start,end);

  const rows = byId('rows');
  rows.innerHTML = '';

  byId('empty').style.display = (view.length===0) ? 'block' : 'none';

  for(const it of view){
    const tr = document.createElement('tr');
    const time = (it.created_at||'').replace('T',' ').replace('Z','');
    const conf = it.confidence!=null ? Number(it.confidence).toFixed(3) : '—';
    tr.innerHTML = `
      <td class="mono">${escapeHtml(time)}</td>
      <td class="mono wrap">${escapeHtml(it.call_sid||'')}</td>
      <td class="mono">${escapeHtml(it.from_||'')}</td>
      <td class="mono">${escapeHtml(it.to||'')}</td>
      <td>${it.confidence!=null?'<span class="badge ok">'+conf+'</span>':'<span class="badge">—</span>'}</td>
      <td class="wrap">${escapeHtml(it.speech_result||'')}</td>
      <td>
        <a class="link mono" href="/transcripts/${encodeURIComponent(it.id||it.call_sid||'')}" target="_blank">JSON</a>
        &nbsp;·&nbsp;
        <a class="link mono" href="#" onclick="copyText('${b64((it.speech_result||''))}');return false;">Copy</a>
      </td>
    `;
    rows.appendChild(tr);
  }
  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  byId('pager').textContent = `Page ${page} of ${totalPages}`;
  byId('prev').disabled = page<=1;
  byId('next').disabled = page>=totalPages;
}

function nextPage(){ const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize)); if(page<totalPages){ page++; render(); } }
function prevPage(){ if(page>1){ page--; render(); } }

function downloadCSV(){
  const header = ['created_at','call_sid','from','to','confidence','speech_result'];
  const rows = filtered.map(it=>[
    it.created_at||'', it.call_sid||'', it.from_||'', it.to||'',
    (it.confidence!=null? it.confidence : ''), (it.speech_result||'').replace(/\n/g,' ')
  ]);
  const csv = [header].concat(rows).map(r=>r.map(csvEscape).join(',')).join('\n');
  const blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'transcripts.csv'; a.click();
  URL.revokeObjectURL(url);
}

function csvEscape(v){
  const s = String(v??'');
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g,'""') + '"' : s;
}

function copyText(b64text){
  const text = atob(b64text);
  navigator.clipboard.writeText(text).then(()=>{
    setStatus('Copied to clipboard');
    setTimeout(()=>setStatus(`Loaded ${all.length} records`), 1200);
  });
}

function escapeHtml(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function b64(s){ return btoa(unescape(encodeURIComponent(s))); }

byId('refresh').addEventListener('click', loadData);
byId('download').addEventListener('click', downloadCSV);
byId('q').addEventListener('input', applyFilters);
byId('sort').addEventListener('change', applyFilters);
byId('pagesize').addEventListener('change', render);
byId('prev').addEventListener('click', prevPage);
byId('next').addEventListener('click', nextPage);

loadData();
