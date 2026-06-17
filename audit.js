/* ──────────────────────────────────────────────────────────────────────────
 * TRR Audit Log — shared helper
 * Usage (after firebase-app-compat + firebase-firestore-compat are loaded):
 *   TRRAudit.log('fleet_view', 'set_status', 'ทะเบียน 70-1234 → busy');
 *
 * Records who (active portal profile), what (module/action/detail), when (ts),
 * and device. Writes to Firestore collection `audit_log` (auto-id docs).
 * Works offline: Firestore queues the write locally and syncs on reconnect.
 * If Firestore is unavailable entirely, falls back to a localStorage queue
 * that is flushed on the next `online` event / page load.
 * ────────────────────────────────────────────────────────────────────────── */
(function(){
  var COL='audit_log';
  var QKEY='trr_audit_queue';

  function activeProfile(){
    try{
      var id=localStorage.getItem('portal_active_profile')||'';
      var profs=JSON.parse(localStorage.getItem('portal_profiles')||'[]');
      var p=profs.filter(function(x){return x.id===id;})[0];
      return {id:id||'unknown', name:(p&&p.name)||id||'ไม่ทราบ'};
    }catch(e){return {id:'unknown',name:'ไม่ทราบ'};}
  }

  function db(){
    try{ if(window.firebase&&firebase.apps&&firebase.apps.length)return firebase.firestore(); }catch(e){}
    return null;
  }

  function buildRec(module,action,detail){
    var who=activeProfile();
    return {
      ts: Date.now(),
      who: who.id,
      whoName: who.name,
      module: module||'',
      action: action||'',
      detail: (detail==null?'':String(detail)).slice(0,500),
      device: (navigator.userAgent||'').slice(0,140)
    };
  }

  function queuePush(rec){
    try{
      var q=JSON.parse(localStorage.getItem(QKEY)||'[]');
      q.push(rec);
      if(q.length>300)q=q.slice(-300);
      localStorage.setItem(QKEY,JSON.stringify(q));
    }catch(e){}
  }

  function log(module,action,detail){
    var rec=buildRec(module,action,detail);
    var d=db();
    if(!d){ queuePush(rec); return; }
    // Firestore handles offline queueing itself; only reaches catch on real errors.
    d.collection(COL).add(rec).catch(function(){ queuePush(rec); });
  }

  function flush(){
    var d=db(); if(!d)return;
    var q;
    try{ q=JSON.parse(localStorage.getItem(QKEY)||'[]'); }catch(e){ return; }
    if(!q.length)return;
    localStorage.removeItem(QKEY);
    q.forEach(function(rec){
      d.collection(COL).add(rec).catch(function(){ queuePush(rec); });
    });
  }

  window.TRRAudit={ log:log, flush:flush, activeProfile:activeProfile };
  try{ window.addEventListener('online',flush); }catch(e){}
  setTimeout(flush,4000);
})();
