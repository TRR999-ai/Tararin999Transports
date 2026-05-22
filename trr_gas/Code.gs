// ─── TRR Transport Web — Google Apps Script ──────────────────────────────────
//
// วิธี deploy:
//   1. สร้าง Google Apps Script project ใหม่
//   2. วาง Code.gs และ index.html ใส่ editor
//   3. Deploy → New deployment → Web app
//      Execute as  : Me
//      Who has access: Anyone  (หรือ Anyone with Google account ถ้าอยากจำกัด)
//   4. Copy deployment URL → ส่งให้ทีม
//
// Data storage:
//   ใช้ PropertiesService (Script Properties)
//   Key: 'trr_db'  Value: JSON string (format เดียวกับ localStorage ใน trr.html)
//   Limit: 500 KB per value, 9 MB total — รองรับข้อมูล TRR ได้สบาย
// ─────────────────────────────────────────────────────────────────────────────

const PROP_KEY = 'trr_db';

/** Serve the web app */
function doGet() {
  return HtmlService
    .createHtmlOutputFromFile('index')
    .setTitle('TRR Transport — ระบบต้นทุนน้ำมันขนส่ง')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/** Load DB → return JSON string (null ถ้ายังไม่มีข้อมูล) */
function loadDB() {
  return PropertiesService.getScriptProperties().getProperty(PROP_KEY);
}

/** Save DB ← รับ JSON string ทั้งก้อน */
function saveDB(jsonStr) {
  PropertiesService.getScriptProperties().setProperty(PROP_KEY, jsonStr);
  return true;
}

/** Reset DB — ลบข้อมูลทั้งหมด */
function resetDB() {
  PropertiesService.getScriptProperties().deleteProperty(PROP_KEY);
  return true;
}

/** Health check — ดูขนาด data ที่ store อยู่ */
function dbInfo() {
  const raw = PropertiesService.getScriptProperties().getProperty(PROP_KEY);
  if (!raw) return { empty: true, bytes: 0 };
  const d = JSON.parse(raw);
  return {
    empty:      false,
    bytes:      raw.length,
    locations:  d.locations?.length  || 0,
    distances:  d.distances?.length  || 0,
    backhaul:   d.backhaul?.length   || 0,
    multistop:  d.multistop?.length  || 0,
    calcs:      d.calcs?.length      || 0,
    fuel_price: d.settings?.fuel_price || 40,
  };
}
