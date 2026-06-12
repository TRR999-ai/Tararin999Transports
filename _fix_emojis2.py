import sys, os
sys.stdout.reconfigure(encoding='utf-8')

S16 = lambda path: f'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
IC_KPI    = S16('<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>')
IC_BOARD  = S16('<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>')
IC_LATEST = S16('<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>')
IC_PLATE  = S16('<rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/>')
IC_DRIVER = S16('<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>')
IC_FUEL   = S16('<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>')
IC_ANALYZE= S16('<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>')
IC_STMT   = S16('<rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>')
IC_SETTINGS=S16('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>')
IC_CAL    = S16('<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>')
IC_LIST   = S16('<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>')
IC_GEAR   = IC_SETTINGS

FLEET_NAV = [
    ('<span class="ic">📊</span>', f'<span class="ic">{IC_KPI}</span>'),
    ('<span class="ic">🚦</span>', f'<span class="ic">{IC_BOARD}</span>'),
    ('<span class="ic">🔍</span>', f'<span class="ic">{IC_LATEST}</span>'),
    ('<span class="ic">🚗</span>', f'<span class="ic">{IC_PLATE}</span>'),
    ('<span class="ic">👤</span>', f'<span class="ic">{IC_DRIVER}</span>'),
    ('<span class="ic">⛽</span>', f'<span class="ic">{IC_FUEL}</span>'),
    ('<span class="ic">📈</span>', f'<span class="ic">{IC_ANALYZE}</span>'),
    ('<span class="ic">🏦</span>', f'<span class="ic">{IC_STMT}</span>'),
    ('<span class="ic">⚙️</span>', f'<span class="ic">{IC_SETTINGS}</span>'),
    ('<span class="ic">⚙</span>',  f'<span class="ic">{IC_SETTINGS}</span>'),
]

FLEET_EXTRA = [
    # reload button
    ('<button class="btn-sm" style="margin-top:6px;width:100%;text-align:center;" oncl',
     '<button class="btn-sm" style="margin-top:6px;width:100%;text-align:center;" oncl'),
    # just strip 🔄 from reload
    ('>🔄</', '><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></'),
    # upload icon
    ('<div class="upload-icon">🏦</div>', '<div class="upload-icon"></div>'),
    # file chip
    ('📄 ', ''),
    # note placeholder
    ('placeholder="📝 Note..."', 'placeholder="Note..."'),
    # trip job icon
    ("'🛣️ '", "''"),
    # date icon
    ("'📅 '", "''"),
    # plate mgr
    ('👁/🚫 ซ่อน-แสดง', 'ซ่อน-แสดง'),
    ('>👁 แสดงทั้งหมด</button>', '>แสดงทั้งหมด</button>'),
    # sticker chip labels
    ("stLabels={ready:'พร้อมรับงาน',busy:'ไม่พร้อมรับงาน',", "stLabels={ready:'พร้อมรับงาน',busy:'ไม่พร้อมรับงาน',"),
    # status note icon
    ("'📝 '+noteMap[plate]", "noteMap[plate]"),
]

ATT_EXTRA = [
    # nav buttons
    ('>📅 วันนี้', '>วันนี้'),
    ('>📋 ประวัติ', '>ประวัติ'),
    ('>📊 รายงาน', '>รายงาน'),
    ('>⚙️ ตั้งค่า', '>ตั้งค่า'),
    ('>⚙ ตั้งค่า', '>ตั้งค่า'),
    # clear button
    ('"att-btn" style="background:#dc2626;" onclick="clearAllA', '"att-btn" style="background:#dc2626;" onclick="clearAllA'),
    ('>🗑️ ล้างข้อมูล<', '>ล้างข้อมูล<'),
    # sync toast
    ("showToast('✅ sync", "showToast('sync"),
    ("showToast('🌐 เชื่อม", "showToast('เชื่อม"),
    ("showToast('⚠️ sync", "showToast('sync"),
    # distance icon in log
    ("'📍 '+r.dist", "r.dist"),
    # confirm title
    ("showConfirm('🗑️'", "showConfirm('')"),
    # status emojis set via JS
    ("icon.textContent='✅'", "icon.textContent=''"),
    ("icon.textContent='🔴'", "icon.textContent=''"),
    ("icon.textContent='📍'", "icon.textContent=''"),
    ("icon.textContent='🚫'", "icon.textContent=''"),
    ("icon.textContent='🟢'", "icon.textContent=''"),
    ("statusEl.textContent='🟢", "statusEl.textContent='"),
    ("statusEl.textContent='✅", "statusEl.textContent='"),
    ("var icon=type==='in'?'🟢':'🔴'", "var icon=''"),
    ("showToast(type==='in'?'✅ บันทึกเวลาเข้างานแล้ว':'✅ บันทึกเวลาออกงานแล้ว')", "showToast(type==='in'?'บันทึกเวลาเข้างานแล้ว':'บันทึกเวลาออกงานแล้ว')"),
    ("'✅ บันทึกแล้ว'", "'บันทึกแล้ว'"),
    ("'✅ ได้ตำแหน่งแล้ว", "'ได้ตำแหน่งแล้ว"),
    ("r.ok===true?'✅ อยู่ในพื้นที่':r.ok===false?'⚠️ นอกพื้นที่'", "r.ok===true?'อยู่ในพื้นที่':r.ok===false?'นอกพื้นที่'"),
    ("r.ok===true?'✅':r.ok===false?'⚠️'", "r.ok===true?'✓':r.ok===false?'!'"),
]

HELP_EXTRA = [
    # step group titles
    ('🔐 ล็อกอินครั้งแรก', 'ล็อกอินครั้งแรก'),
    ('🔑 ล็อกอินปกติ', 'ล็อกอินปกติ'),
    ('🔄 เปลี่ยนรหัสผ่าน', 'เปลี่ยนรหัสผ่าน'),
    ('🚪 ออกจากระบบ', 'ออกจากระบบ'),
    ('🗂 การนำทาง', 'การนำทาง'),
    ('📊 ภาพรวม KPI', 'ภาพรวม KPI'),
    ('🚦 กำลังรถวันนี้ (Board)', 'กำลังรถวันนี้ (Board)'),
    ('🔍 งานล่าสุดแต่ละคัน', 'งานล่าสุดแต่ละคัน'),
    ('🚗 สรุปรายคัน + 👤 สรุปรายคนขับ', 'สรุปรายคัน + สรุปรายคนขับ'),
    ('📈 วิเคราะห์', 'วิเคราะห์'),
    ('🏦 Statement วิเคราะห์', 'Statement วิเคราะห์'),
    ('📋 ขั้นตอนการใช้งาน', 'ขั้นตอนการใช้งาน'),
    ('🗑️ ลบบัตร', 'ลบบัตร'),
    ('🧮 คำนวณต้นทุนน้ำมัน', 'คำนวณต้นทุนน้ำมัน'),
    ('📊 ตารางระยะทาง', 'ตารางระยะทาง'),
    ('📍 จัดการข้อมูล', 'จัดการข้อมูล'),
    ('📊 ดูตารางราคา', 'ดูตารางราคา'),
    ('📋 ดูรายการงาน', 'ดูรายการงาน'),
    ('✏️ บันทึกงานใหม่', 'บันทึกงานใหม่'),
    ('🔧 ขั้นตอนติดตั้ง GAS', 'ขั้นตอนติดตั้ง GAS'),
    ('🔄 Re-deploy', 'Re-deploy'),
    ('📁 เตรียม Google Sheet', 'เตรียม Google Sheet'),
    ('🔗 ตั้งค่าใน Fleet Dashboard', 'ตั้งค่าใน Fleet Dashboard'),
    # tip/note icons
    ('<span class="tip-icon">💡</span>', ''),
    ('<span class="note-icon">ℹ️</span>', ''),
    ('<span class="note-icon">⚠️</span>', ''),
    # inline nav items in tables
    ('🚚 ระบบจัดการงานขนส่ง', 'ระบบจัดการงานขนส่ง'),
    ('💳 Fleet Card Batch Update', 'Fleet Card Batch Update'),
    ('⛽ ต้นทุนน้ำมัน TRR', 'ต้นทุนน้ำมัน TRR'),
    ('💰 กระดานราคา', 'กระดานราคา'),
    ('🚦 Fleet Dashboard', 'Fleet Dashboard'),
    # step text references
    ('📋 วางวงเงิน</b>', 'วางวงเงิน</b>'),
    ('➕ เพิ่มบัตร</b>', 'เพิ่มบัตร</b>'),
    ('🗑 ลบที่เลือก</b>', 'ลบที่เลือก</b>'),
    ('🧮 คำนวณต้นทุน</b>', 'คำนวณต้นทุน</b>'),
    ('🏠 แดชบอร์ด</b>', 'แดชบอร์ด</b>'),
    ('🔌 Test</b>', 'Test</b>'),
    ('💾 บันทึก</b>', 'บันทึก</b>'),
    ('🏦 Statement</b>', 'Statement</b>'),
    ('👤 TARARIN 9', 'TARARIN 9'),
    ('⚙️ Settings</b>', 'Settings</b>'),
    ('🚗 รายคัน</b>', 'รายคัน</b>'),
    ('📍 สถานี</b>', 'สถานี</b>'),
    ('🗺️ จังหวัด</b>', 'จังหวัด</b>'),
    ('📅 รายวัน</b>', 'รายวัน</b>'),
    ('✅ เชื่อมต่อสำเร็จ', 'เชื่อมต่อสำเร็จ'),
    # step labels with emojis
    ('✅❌🏖️', 'พร้อม/ไม่พร้อม/ลา'),
    ('🚗 รายคัน', 'รายคัน'),
    ('📍 สถานีน้ำมัน', 'สถานีน้ำมัน'),
    ('🗺️ จังหวัด', 'จังหวัด'),
    ('📅 รายวัน', 'รายวัน'),
    ('⚙️ Settings</b>', 'Settings</b>'),
    ('<span class="ic">⚙️</span>', '<span class="ic"></span>'),
    ('<span class="ic">⚙</span>', '<span class="ic"></span>'),
    # misc
    ('📂', ''),
]

PORTAL_EXTRA = [
    ('>📷 อัปโหลดรูป</label>', '>อัปโหลดรูป</label>'),
    ('>💾 บันทึก</button>', '>บันทึก</button>'),
    ("'🔄 กำลัง sync โปรไฟล์...'", "'กำลัง sync โปรไฟล์...'"),
    ("'✅ sync แล้ว'", "'sync แล้ว'"),
    ("'✅ ข้อมูลตรงกัน'", "'ข้อมูลตรงกัน'"),
    ("showToast('⚠️ sync", "showToast('sync"),
    ("'⚠️ GAS connect f", "'GAS connect f"),
    ("'⚠️ parse error'", "'parse error'"),
]

TRR_EXTRA = [
    # remaining ➕
    ('>➕ เพิ่มระยะทางที่ขาด<', '>+ เพิ่มระยะทางที่ขาด<'),
]

TRANSPORT_EXTRA = [
    # reload
    ('" title="โหลดจาก Sheet">', '" title="โหลดจาก Sheet">'),
    ('>🔄</', '><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></'),
    # toast messages
    ("showToast('⚠️ ยังไม่ได้ใส่", "showToast('ยังไม่ได้ใส่"),
    ("showToast('⚠️ กรุณา", "showToast('กรุณา"),
    ("showToast('⚠️ วิเคราะห์", "showToast('วิเคราะห์"),
    ("showToast('⚠️ กรุณาใส่", "showToast('กรุณาใส่"),
]

PRICE_EXTRA = [
    ('>⚡ สร้างกระดานใหม่</button>', '>สร้างกระดานใหม่</button>'),
]

files = {
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/fleet_view/index.html': FLEET_NAV + FLEET_EXTRA,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/attendance/index.html': ATT_EXTRA,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/help.html': HELP_EXTRA,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/index.html': PORTAL_EXTRA,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/trr.html': TRR_EXTRA,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/project1/transport.html': TRANSPORT_EXTRA,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/priceboard/index.html': PRICE_EXTRA,
}

for fp, reps in files.items():
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    count = 0
    for old, new in reps:
        if old != new and old in s:
            s = s.replace(old, new)
            count += 1
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(s)
    name = os.path.basename(os.path.dirname(fp)) + '/' + os.path.basename(fp)
    print(f'Done: {name} ({count} replacements)')

print('All done')
