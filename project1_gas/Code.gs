// ─── TRR Transport — Driver Data GAS (สำหรับ project1/transport.html) ────────
//
// วิธี deploy:
//   1. script.google.com → New project → วางโค้ดนี้
//   2. Deploy → New deployment → Web app
//      Execute as : Me  |  Who has access : Anyone
//   3. Copy URL → วางใน transport.html บรรทัด DRIVER_GAS_URL = '...URL...'
//
// แหล่งข้อมูล:
//   GET  — อ่านจาก "รายชื่อคนขับ" tab (master sheet)
//          + merge phone/site/color จาก tab "transport_phones" (สร้างอัตโนมัติ)
//   POST — บันทึก phone supplement ลง "transport_phones" เท่านั้น
//          (ไม่แตะ "รายชื่อคนขับ" tab)
//
// คอลัมน์ใน "รายชื่อคนขับ":
//   A: ชื่อคนขับ   B: ทะเบียนรถ   C: เลขบัตร (ไม่ใช้)
//   D: เด็กรถ(ถ้ามี)   E-K: ข้อมูลอื่น (ไม่ใช้)
// ─────────────────────────────────────────────────────────────────────────────

const MASTER_SHEET_ID = '1HC2aGOvAUx-s82kBi2cMU-8U3k4POiqn7lXYeWr-C4c';
const DRIVERS_TAB     = 'รายชื่อคนขับ';
const PHONES_TAB      = 'transport_phones';   // สร้างอัตโนมัติถ้ายังไม่มี

// ── GET: return driver list ──────────────────────────────────────────────────
function doGet(e) {
  try {
    const ss = SpreadsheetApp.openById(MASTER_SHEET_ID);

    // 1. Read master driver list
    const driverSh = ss.getSheetByName(DRIVERS_TAB);
    if (!driverSh) return json({ ok: false, msg: 'ไม่พบ tab "' + DRIVERS_TAB + '"' });

    const vals = driverSh.getDataRange().getValues();
    const drivers = [];
    for (let i = 1; i < vals.length; i++) {
      const row = vals[i];
      const name  = String(row[0] || '').trim();
      const plate = String(row[1] || '').trim();
      const name2 = String(row[3] || '').trim();
      if (!name && !plate) continue;
      // Detect type from plate: trailer plates contain '/' or start with '700'
      const type = (plate.indexOf('/') >= 0 || plate.startsWith('700')) ? 'trailer' : '6wheel';
      drivers.push({ type, plate, province: 'ปทุมธานี', name, name2, phone: '', site: '', color: '' });
    }

    // 2. Merge phone/site/color from supplement tab
    const phoneSh = ss.getSheetByName(PHONES_TAB);
    if (phoneSh) {
      const pVals = phoneSh.getDataRange().getValues();
      const phoneMap = {};
      for (let i = 1; i < pVals.length; i++) {
        const pName = String(pVals[i][0] || '').trim();
        if (pName) phoneMap[pName] = { phone: String(pVals[i][1] || ''), site: String(pVals[i][2] || ''), color: String(pVals[i][3] || '') };
      }
      drivers.forEach(d => {
        if (phoneMap[d.name]) {
          d.phone = phoneMap[d.name].phone;
          d.site  = phoneMap[d.name].site;
          d.color = phoneMap[d.name].color;
        }
      });
    }

    return json({ ok: true, data: drivers });
  } catch (err) {
    return json({ ok: false, msg: err.message });
  }
}

// ── POST: save phone supplement only (does NOT touch "รายชื่อคนขับ") ─────────
function doPost(e) {
  try {
    const body    = JSON.parse(e.postData.contents);
    const drivers = body.drivers || [];

    const ss = SpreadsheetApp.openById(MASTER_SHEET_ID);
    let phoneSh = ss.getSheetByName(PHONES_TAB);
    if (!phoneSh) {
      phoneSh = ss.insertSheet(PHONES_TAB);
      phoneSh.getRange(1, 1, 1, 4).setValues([['name', 'phone', 'site', 'color']]);
      phoneSh.getRange(1, 1, 1, 4).setFontWeight('bold');
    }

    // Only save rows that have a phone/site/color value (skip empty)
    const rows = drivers.filter(d => d.phone || d.site || d.color)
                        .map(d => [d.name || '', d.phone || '', d.site || '', d.color || '']);

    // Clear and rewrite
    phoneSh.clearContents();
    phoneSh.getRange(1, 1, 1, 4).setValues([['name', 'phone', 'site', 'color']]);
    phoneSh.getRange(1, 1, 1, 4).setFontWeight('bold');
    if (rows.length) {
      phoneSh.getRange(2, 1, rows.length, 4).setValues(rows);
    }

    return json({ ok: true, saved: rows.length, ts: new Date().toISOString() });
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
