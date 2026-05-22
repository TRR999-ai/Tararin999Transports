// ─── TRR Dashboard GAS — อ่านข้อมูลเที่ยวรถจาก Google Sheet ────────────────
//
// วิธี deploy:
//   1. script.google.com → New project → วางโค้ดนี้
//   2. Deploy → New deployment → Web app
//      Execute as : Me
//      Who has access : Anyone
//   3. Copy URL → ใส่ใน Dashboard → ⚙ GAS URL
//
// Sheet: 1HC2aGOvAUx-s82kBi2cMU-8U3k4POiqn7IXYeWr-C4c
// ─────────────────────────────────────────────────────────────────────────────

const SHEET_ID = '1HC2aGOvAUx-s82kBi2cMU-8U3k4POiqn7IXYeWr-C4c';

// ── Tabs ที่อ่าน (เพิ่ม/ลด tab ตรงนี้) ───────────────────────────────────
const TABS = [
  { name: '03',    month: '03/2026', type: '6wheel'  },
  { name: '04',    month: '04/2026', type: '6wheel'  },
  { name: '05',    month: '05/2026', type: '6wheel'  },
  { name: '03tr',  month: '03/2026', type: 'trailer' },
  { name: '04tr',  month: '04/2026', type: 'trailer' },
  { name: '05tr',  month: '05/2026', type: 'trailer' },
];

// ── Column index (A=0) ─────────────────────────────────────────────────────
//  A=วันที่  B=ชื่อคนขับ  C=ทะเบียน  D=ลูกค้า  E=ชื่องาน
//  F=ระยะทาง  G=ประเภทน้ำมัน  H=ราคาน้ำมัน  I=กม/ลิตร  J=รวมเงิน
//  K=(blank)  L=SMHUB_ID  M=เลขบัตร
const C = { date:0,driver:1,plate:2,customer:3,route:4,
            dist:5,fuelType:6,fuelPrice:7,kmL:8,cost:9,cardNo:12 };

// ── GET handler ─────────────────────────────────────────────────────────────
function doGet(e) {
  const action = (e.parameter.action || 'trips').toLowerCase();
  if (action === 'trips') return getTrips(e.parameter.month || '');
  if (action === 'info')  return json({ ok:true, tabs: TABS.map(t=>t.name) });
  if (action === 'debug') return debugCols(e.parameter.tab || TABS[0].name);
  return json({ ok:false, msg:'unknown action' });
}

// ── Read trip rows ───────────────────────────────────────────────────────────
function getTrips(filterMonth) {
  try {
    const ss    = SpreadsheetApp.openById(SHEET_ID);
    const trips = [];

    TABS.forEach(tab => {
      // Filter by month if specified (e.g. '04/2026')
      if (filterMonth && tab.month !== filterMonth) return;

      const sh = ss.getSheetByName(tab.name);
      if (!sh) return;

      const vals = sh.getDataRange().getValues();

      vals.forEach(row => {
        // Skip header/empty rows
        const rawDate = row[C.date];
        if (!rawDate) return;
        if (rawDate === 'วันที่' || rawDate === 'date') return;

        // Parse date
        let dateStr;
        if (rawDate instanceof Date) {
          dateStr = Utilities.formatDate(rawDate, 'Asia/Bangkok', 'dd/MM/yyyy');
        } else {
          const s = String(rawDate).trim();
          if (!s.match(/\d{1,2}\/\d{1,2}\/\d{4}/)) return;
          dateStr = s;
        }

        // Skip placeholder rows
        const plate = String(row[C.plate] || '').trim();
        if (!plate || plate === 'ไม่มี' || plate === '-' || plate === '') return;

        const cost = parseN(row[C.cost]);
        const dist = parseN(row[C.dist]);
        if (cost <= 0 && dist <= 0) return; // empty row

        // ── Sanity check: cost per trip ไม่ควรเกิน 300,000 บาท ────────────
        // ถ้าเกิน = อ่าน column ผิด (เช่น card number 16 หลัก)
        if (cost > 300000) return;

        // Normalize card number (digits only)
        const cardNo = String(row[C.cardNo] || '').replace(/[^0-9]/g, '');

        trips.push({
          date:      dateStr,
          driver:    String(row[C.driver]   || '').trim(),
          plate,
          customer:  String(row[C.customer] || '').trim(),
          route:     String(row[C.route]    || '').trim(),
          dist,
          fuelPrice: parseN(row[C.fuelPrice]),
          kmL:       parseN(row[C.kmL]),
          cost,
          cardNo,
          month:     tab.month,
          type:      tab.type,
        });
      });
    });

    return json({ ok:true, count:trips.length, data:trips });
  } catch (err) {
    return json({ ok:false, msg:err.message });
  }
}

// ── Debug: แสดง raw column values เพื่อตรวจ mapping ────────────────────────
function debugCols(tabName) {
  try {
    const ss  = SpreadsheetApp.openById(SHEET_ID);
    const sh  = ss.getSheetByName(tabName);
    if (!sh)  return json({ ok:false, msg: 'tab not found: ' + tabName });

    const vals = sh.getDataRange().getValues();
    const rows = [];
    let count  = 0;

    for (let i = 0; i < vals.length && count < 5; i++) {
      const row     = vals[i];
      const rawDate = row[0];
      if (!rawDate || rawDate === 'วันที่') continue;
      const plate   = String(row[2] || '').trim();
      if (!plate || plate === 'ไม่มี' || plate === '-') continue;

      // Show raw values at each index
      const rowData = {};
      for (let j = 0; j < row.length; j++) {
        const v = row[j];
        rowData['col' + j] = (v instanceof Date)
          ? 'DATE:' + Utilities.formatDate(v, 'Asia/Bangkok', 'dd/MM/yyyy')
          : String(v).substring(0, 40);
      }
      rows.push(rowData);
      count++;
    }

    return json({ ok:true, tab:tabName, cols:vals[0]?.length || 0, sample:rows });
  } catch (err) {
    return json({ ok:false, msg:err.message });
  }
}

// ── Helpers ──────────────────────────────────────────────────────────────────
function parseN(v) {
  if (!v && v !== 0) return 0;
  return parseFloat(String(v).replace(/,/g, '')) || 0;
}

function json(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
