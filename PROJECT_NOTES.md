# TRR Transport Portal — Project Notes

Last updated: 2026-05-22

---

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Single-file HTML SPA (Chart.js, XLSX.js, localStorage) |
| Backend | Google Apps Script (GAS) |
| Hosting | Netlify (static) + GAS (API) |
| Repo | GitHub → auto-deploy to Netlify |

---

## Branding

- Navy: `#1B2770`
- Gold: `#F5A623`
- Light navy (bg): `#EEF2FF`
- Company: **ธรารินทร์ 999 ขนส่ง จำกัด**
- Logo: `TRR999logo.png` (in project4 root)

---

## File Structure

```
project4/
├── index.html               ← Portal homepage (4 cards + sidebar)
├── TRR999logo.png
├── PROJECT_NOTES.md         ← this file
│
├── project1/
│   └── transport.html       ← Driver trip logging (GAS sync optional)
│
├── project2/
│   └── index.html           ← Fleet card employee list (fetches from Google Sheet)
│
├── project3/                ← (legacy, SQLite-based, data migrated)
│
├── dashboard/
│   └── index.html           ← Executive fuel dashboard (main focus)
│
├── dashboard_gas/
│   └── Code.gs              ← GAS backend for reading trip Sheet
│
└── project1_gas/
    └── Code.gs              ← GAS backend for driver data sync
```

---

## Google Sheet

- **Sheet ID**: `1HC2aGOvAUx-s82kBi2cMU-8U3k4POiqn7IXYeWr-C4c`
- **Tabs read**: `03`, `04`, `05`, `03tr`, `04tr`, `05tr`
- **Tab naming**: number = month (03=Mar, 04=Apr, 05=May), suffix `tr` = trailer

### Column Mapping (dashboard_gas/Code.gs)

```javascript
const C = { date:0, driver:1, plate:2, customer:3, route:4,
            dist:5, fuelType:6, fuelPrice:7, kmL:8, cost:9, cardNo:12 };
// A=0  B=1  C=2  D=3  E=4  F=5  G=6  H=7  I=8  J=9  K=10(blank)  L=11  M=12
```

**⚠️ UNVERIFIED** — column mapping may be wrong. See "Current Bug" below.

---

## Dashboard (dashboard/index.html)

### Data Sources

1. **Excel file** (TTB Fleet Card statement) → drag-drop import
   - Parsed by `parseStatement()` → extracts summary + transactions
   - Stored in `localStorage: trr_dashboard_excel`

2. **Google Sheet** (trip records) → loaded via GAS API
   - Stored in `localStorage: dash_trips`
   - GAS URL configured in dashboard Settings (⚙️ button)

### Charts

| Chart | Data |
|-------|------|
| Bar: Top 15 vehicles | Litres (blue) + Cost/100 (gold) |
| Line: Daily trend | Litres/day (blue) + Cost/day÷100 (gold) |
| Bar: Top 15 stations | Total litres by station |
| Bar: Variance | Calculated cost vs Actual per vehicle (navy vs gold) |

### Variance Calculation

```
variance = actualCost (from Excel statement) - calculatedCost (from Sheet trips)
calculatedCost = dist / kmL * fuelPrice   (per trip, then summed by plate)
```

Join key: `cardNo` (card number stripped to digits only)

---

## Current Bug — Data Corruption in Trip Data

**Symptom**: Calculated cost shows as ~3.5×10¹⁸ บาท (billions)

**Root cause**: Column mapping wrong — `cost` column index may be reading card number (16-digit) instead of รวมเงิน

**Sanity check added** in Code.gs:
```javascript
if (cost > 300000) return;  // skip rows where cost > 300k (corrupted)
```

**To diagnose**:
1. Deploy updated `dashboard_gas/Code.gs` (already updated in file)
2. Open in browser: `[GAS_URL]?action=debug&tab=04tr`
3. Read JSON → find which `colN` contains the actual รวมเงิน value
4. Update `const C = {...}` with correct index
5. Re-deploy

---

## GAS Deployments

| Script | Purpose | URL |
|--------|---------|-----|
| dashboard_gas/Code.gs | Trip data API | ⚠️ fill in after deploy |
| project1_gas/Code.gs | Driver sync | ⚠️ fill in after deploy |

### Deploy steps
1. script.google.com → open project
2. Paste updated code
3. Deploy → Manage deployments → Edit (existing) → New version → Deploy
4. **Do NOT create new deployment** (URL will change)

---

## project2/index.html

- Fetches employee/fleet card data from Google Sheet
- Sheet ID: `12o1drcocyTl51GnW6z5_nHvwQPtw3aoln67YHnWGcLI`
- Uses Google Visualization API (no GAS needed):
  ```
  https://docs.google.com/spreadsheets/d/{ID}/gviz/tq?tqx=out:json&gid={GID}
  ```
- Opens in same tab (no `target="_blank"`)

---

## project1/transport.html

- `DRIVER_GAS_URL` constant at top → leave empty or fill with project1_gas URL
- When empty → works with localStorage only (offline)
- When filled → syncs driver data to Sheet

---

## Pending Tasks

- [ ] Deploy `dashboard_gas/Code.gs`, get URL, insert into dashboard Settings
- [ ] Run `?action=debug&tab=04tr` → verify actual column mapping → fix `const C`
- [ ] Deploy `project1_gas/Code.gs`, get URL, insert into `transport.html`
- [ ] Push all to GitHub → Netlify auto-deploys
- [ ] End-to-end test: Upload Excel → load Sheet trips → check variance chart

---

## GitHub / Netlify

- Repo connected to Netlify
- Every push to `main` → auto-deploy
- Netlify URL: (fill in after first deploy)
