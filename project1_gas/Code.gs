// ─── TRR Transport — Driver Data GAS (สำหรับ project1/transport.html) ────────
//
// วิธี deploy:
//   1. script.google.com → New project → วางโค้ดนี้
//   2. แก้ SHEET_ID และ TAB_NAME ให้ตรงกับ Sheet จริง
//   3. Deploy → New deployment → Web app
//      Execute as : Me
//      Who has access : Anyone
//   4. Copy URL → วางใน transport.html บรรทัด DRIVER_GAS_URL = '...URL...'
//   5. Commit + push → Netlify auto-deploy
//
// Sheet format (แถว 1 = header):
//   A: type (6wheel / trailer)
//   B: plate      C: province  D: name   E: name2
//   F: phone      G: site      H: color
// ─────────────────────────────────────────────────────────────────────────────

const SHEET_ID = '1aKYH07A-4CR17PlhIIPiiN9EGangvaeeDyDUHnRAqzc';
const TAB_NAME = 'Sheet1'; // ← เปลี่ยนให้ตรงกับชื่อ tab ที่มีข้อมูลพนักงาน

const DRIVER_COLS = ['type','plate','province','name','name2','phone','site','color'];

// ── GET: return driver list ──────────────────────────────────────────────────
function doGet(e) {
  try {
    const sh   = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_NAME);
    const vals = sh.getDataRange().getValues();
    const drivers = [];
    for (let i = 1; i < vals.length; i++) {          // skip header row
      if (!vals[i][1]) continue;                      // skip empty plate
      const d = {};
      DRIVER_COLS.forEach((col, j) => d[col] = String(vals[i][j] || ''));
      drivers.push(d);
    }
    return json({ ok: true, data: drivers });
  } catch (err) {
    return json({ ok: false, msg: err.message });
  }
}

// ── POST: save driver list ───────────────────────────────────────────────────
function doPost(e) {
  try {
    const body    = JSON.parse(e.postData.contents);
    const drivers = body.drivers || [];

    const sh = SpreadsheetApp.openById(SHEET_ID).getSheetByName(TAB_NAME);
    sh.clearContents();

    // Write header
    sh.getRange(1, 1, 1, DRIVER_COLS.length).setValues([DRIVER_COLS]);
    sh.getRange(1, 1, 1, DRIVER_COLS.length).setFontWeight('bold');

    // Write data
    if (drivers.length) {
      const rows = drivers.map(d => DRIVER_COLS.map(c => d[c] || ''));
      sh.getRange(2, 1, rows.length, DRIVER_COLS.length).setValues(rows);
    }

    return json({ ok: true, saved: drivers.length, ts: new Date().toISOString() });
  } catch (err) {
    return json({ ok: false, msg: err.message });
  }
}

// ── Helper ───────────────────────────────────────────────────────────────────
function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
