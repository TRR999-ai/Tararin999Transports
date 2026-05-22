// ─── TRR Transport — GAS API Backend (สำหรับ Netlify deployment) ─────────────
//
// วิธี deploy:
//   1. ไปที่ script.google.com → New project
//   2. วางโค้ดนี้ใส่ Code.gs
//   3. Deploy → New deployment → Web app
//      Execute as  : Me
//      Who has access : Anyone
//   4. Copy "Web app URL"
//   5. เปิด project4/trr.html → หา GAS_URL = ''
//      ใส่ URL: GAS_URL = 'https://script.google.com/macros/s/ABC.../exec'
//   6. Push project4/ ขึ้น GitHub → Netlify deploy
//
// Data storage:
//   Primary  : Script Properties (fast, ~200ms) — key 'trr_db'
//   Secondary: Google Sheet (human-readable backup) — สร้างอัตโนมัติ
// ─────────────────────────────────────────────────────────────────────────────

const PROP_KEY   = 'trr_db';
const SHEET_NAME = 'TRR_Backup';   // Sheet สำหรับดู/แก้ข้อมูล (optional)

// ── GET handler ─────────────────────────────────────────────────────────────
function doGet(e) {
  const action = (e.parameter.action || '').toLowerCase();

  if (action === 'load') {
    const data = PropertiesService.getScriptProperties().getProperty(PROP_KEY);
    return json({ ok: true, data: data });
  }

  if (action === 'reset') {
    PropertiesService.getScriptProperties().deleteProperty(PROP_KEY);
    return json({ ok: true, msg: 'reset done' });
  }

  if (action === 'info') {
    const raw = PropertiesService.getScriptProperties().getProperty(PROP_KEY);
    if (!raw) return json({ ok: true, empty: true });
    const d = JSON.parse(raw);
    return json({
      ok:         true,
      bytes:      raw.length,
      locations:  d.locations?.length  || 0,
      distances:  d.distances?.length  || 0,
      backhaul:   d.backhaul?.length   || 0,
      multistop:  d.multistop?.length  || 0,
      calcs:      d.calcs?.length      || 0,
      fuel_price: d.settings?.fuel_price || 40,
    });
  }

  return json({ ok: false, msg: 'unknown action' });
}

// ── POST handler (รับ JSON string เป็น text/plain body) ─────────────────────
function doPost(e) {
  try {
    const jsonStr = e.postData.contents;
    if (!jsonStr) return json({ ok: false, msg: 'empty body' });

    // Validate JSON
    JSON.parse(jsonStr);

    // Save to Properties
    PropertiesService.getScriptProperties().setProperty(PROP_KEY, jsonStr);

    // Background sync to Sheet (non-blocking)
    try { syncToSheet_(jsonStr); } catch(err) { /* ไม่ให้ error กระทบ save หลัก */ }

    return json({ ok: true, ts: new Date().toISOString() });
  } catch(err) {
    return json({ ok: false, msg: err.message });
  }
}

// ── Helper: return JSON response ─────────────────────────────────────────────
function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

// ── Sync summary to Google Sheet (optional, for visibility) ─────────────────
function syncToSheet_(jsonStr) {
  const d = JSON.parse(jsonStr);

  let ss;
  try {
    ss = SpreadsheetApp.getActiveSpreadsheet();
  } catch(e) {
    // ถ้าไม่ได้ bind กับ Sheet → ข้ามไป
    return;
  }

  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) sh = ss.insertSheet(SHEET_NAME);
  sh.clearContents();

  // Header
  sh.getRange(1, 1, 1, 4).setValues([['ประเภท','ชื่อ','จังหวัด','ประเภทสถานที่']]);
  sh.getRange(1, 1, 1, 4).setFontWeight('bold');

  // Locations
  if (d.locations && d.locations.length) {
    const rows = d.locations.map(l => [l.type, l.name, l.province || '', l.type]);
    sh.getRange(2, 1, rows.length, 4).setValues(rows);
  }

  // Summary tab
  let sumSh = ss.getSheetByName('สรุป');
  if (!sumSh) sumSh = ss.insertSheet('สรุป');
  sumSh.clearContents();
  sumSh.getRange(1,1,6,2).setValues([
    ['อัปเดตล่าสุด', new Date().toLocaleString('th-TH')],
    ['สถานที่', d.locations?.length || 0],
    ['ระยะทาง', d.distances?.length || 0],
    ['Backhaul', d.backhaul?.length || 0],
    ['Multi-stop', d.multistop?.length || 0],
    ['ราคาน้ำมัน', d.settings?.fuel_price || 40],
  ]);
}
