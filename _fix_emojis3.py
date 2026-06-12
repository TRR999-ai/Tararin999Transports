import sys, os
sys.stdout.reconfigure(encoding='utf-8')

# attendance/index.html
ATT = [
    ('<span class="mgr-nav-ic">📅</span>', '<span class="mgr-nav-ic"></span>'),
    ('<span class="mgr-nav-ic">📋</span>', '<span class="mgr-nav-ic"></span>'),
    ('<span class="mgr-nav-ic">📊</span>', '<span class="mgr-nav-ic"></span>'),
    ('<span class="mgr-nav-ic">⚙️</span>', '<span class="mgr-nav-ic"></span>'),
    ('<span class="mgr-nav-ic">⚙</span>', '<span class="mgr-nav-ic"></span>'),
    ('<span class="big-btn-icon" id="big-btn-icon">📍</span>', '<span class="big-btn-icon" id="big-btn-icon"></span>'),
    ('>🗑️ ล้างข้อมูลทั้งหมด<', '>ล้างข้อมูลทั้งหมด<'),
    ("'⚠️ localStorage เต็ม", "'localStorage เต็ม"),
    ("'<span class=\"log-dist\">📍 '+r.dist.toFixed(2)+' km</span>'", "'<span class=\"log-dist\">'+r.dist.toFixed(2)+' km</span>'"),
    ("return '<span style=\"font-size:'+(size*0.48)+'px;line-height:1;\">'+(pf?pf.avatar:'👤')+'</span>';",
     "return '<span style=\"font-size:'+(size*0.48)+'px;line-height:1;\">'+(pf?pf.avatar:'')+'</span>';"),
    ("+'<div class=\"att-kpi\"><div class=\"k-label\">👥 พนักงานทั้งหมด</div>",
     "+'<div class=\"att-kpi\"><div class=\"k-label\">พนักงานทั้งหมด</div>"),
    ("+'<div class=\"att-kpi green\"><div class=\"k-label\">✅ มาทำงาน</div>",
     "+'<div class=\"att-kpi green\"><div class=\"k-label\">มาทำงาน</div>"),
    ("+'<div class=\"att-kpi red\"><div class=\"k-label\">❌ ไม่มา / ยังไม่เช็ค</div>",
     "+'<div class=\"att-kpi red\"><div class=\"k-label\">ไม่มา / ยังไม่เช็ค</div>"),
    ("+'<div class=\"att-kpi amber\"><div class=\"k-label\">⚠️ มาสาย",
     "+'<div class=\"att-kpi amber\"><div class=\"k-label\">มาสาย"),
]

# fleet_view/index.html
FLEET = [
    ('>🔄 รีโหลด<', '>รีโหลด<'),
    ('"chart-title">💰 ค่าน้ำมัน', '"chart-title">ค่าน้ำมัน'),
    ('>⚙ จัดการทะเบียน</button>', '>จัดการทะเบียน</button>'),
    ('>⚙️ จัดการทะเบียน</button>', '>จัดการทะเบียน</button>'),
    ("'⬜ ยังไม่ระบุ'", "'ยังไม่ระบุ'"),
    ("'⚠️ หยุดนาน 7+ วัน'", "'หยุดนาน 7+ วัน'"),
    ('>☁️ ดึงจาก Sheets<', '>ดึงจาก Sheets<'),
    ('>📂 อัปโหลดไฟล์<', '>อัปโหลดไฟล์<'),
    ('"bar-title">⚙️ ตั้งค่า GAS Sync<', '"bar-title">ตั้งค่า GAS Sync<'),
    ("'c-idle','⚠️ หยุดนาน: '", "'c-idle','หยุดนาน: '"),
    ("r&&r.ok?'✅ เชื่อมต่อสำเร็จ':'❌ Error: '", "r&&r.ok?'เชื่อมต่อสำเร็จ':'Error: '"),
    ("setSyncStatus('err','❌ ไม่สามารถเชื่อมต่อได้')", "setSyncStatus('err','ไม่สามารถเชื่อมต่อได้')"),
    ("(hidden?'🚫':'👁')", "(hidden?'ซ่อน':'แสดง')"),
    ("'🗑</button>'", "'ลบ</button>'"),
    ('{v:\'fuel\',lbl:\'⛽ น้ำมัน\'', '{v:\'fuel\',lbl:\'น้ำมัน\''),
    ('{v:\'hub\', lbl:\'🏭 HUB\'', '{v:\'hub\', lbl:\'HUB\''),
    ('{v:\'khon\',lbl:\'🚚 ขนคืน\'', '{v:\'khon\',lbl:\'ขนคืน\''),
    ("'c-ready'+(bsf==='ready'?' active':'')+'\") onclick=\"setBoardStatusFilter(\\'ready\\')\"'>✅ พร้อม '",
     "'c-ready'+(bsf==='ready'?' active':'')+'\") onclick=\"setBoardStatusFilter(\\'ready\\')\"'>พร้อม '"),
    ("\">✅ พร้อม '", "\">พร้อม '"),
    ("\">❌ ไม่พร้อม '", "\">ไม่พร้อม '"),
    ("\">\U0001F3D6️ ลา '", "\">ลา '"),
    # chip labels
    (">✅ พร้อม '", ">พร้อม '"),
    (">❌ ไม่พร้อม '", ">ไม่พร้อม '"),
    (">🏖️ ลา '", ">ลา '"),
    ("'<div style=\"font-size:40px;margin-bottom:12px;\">🚗</div>'", "''"),
    ('\'กด "⚙ จัดการทะเบียน"', '\'กด "จัดการทะเบียน"'),
    ("'⚙ จัดการทะเบียน</button>'", "'จัดการทะเบียน</button>'"),
    ("'⚠️ หยุด '", "'หยุด '"),
    ("'📝 '+noteMap[plate]", "noteMap[plate]"),
    ("'🛣️ '+(tr.job||'—')", "(tr.job||'—')"),
    ("{v:'ready',lbl:'✅ พร้อมรับงาน'}", "{v:'ready',lbl:'พร้อมรับงาน'}"),
    ("{v:'busy',lbl:'❌ ไม่พร้อมรับงาน'}", "{v:'busy',lbl:'ไม่พร้อมรับงาน'}"),
    ("{v:'leave',lbl:'🏖️ ลา'}", "{v:'leave',lbl:'ลา'}"),
    ("'<span class=\"lbl\">📅</span> '", "'<span class=\"lbl\"></span>'"),
    ("'🛣️ '+(t.job||'—')", "(t.job||'—')"),
    ("'🏷️ ทุกประเภท'", "'ทุกประเภท'"),
    # stmt tabs
    ("switchStmtTab('plate'))\">🚗 รายคัน</bu", "switchStmtTab('plate'))\">รายคัน</bu"),
    ("switchStmtTab('station'))\">📍 สถานีน้ำมัน</bu", "switchStmtTab('station'))\">สถานีน้ำมัน</bu"),
    ("switchStmtTab('province'))\">🗺️ จังหวัด</bu", "switchStmtTab('province'))\">จังหวัด</bu"),
    ("switchStmtTab('daily'))\">📅 รายวัน</bu", "switchStmtTab('daily'))\">รายวัน</bu"),
    ("'✅ บันทึกแล้ว: '+v", "'บันทึกแล้ว: '+v"),
    ("'✅ พร้อมใช้: '+stmtSheetId", "'พร้อมใช้: '+stmtSheetId"),
    ("'<span class=\"file-chip\">☁️ '+tab", "'<span class=\"file-chip\">'+tab"),
    ("'<div class=\"bdm-plate\">📍 '+province", "'<div class=\"bdm-plate\">'+province"),
    ("'<div class=\"bdm-plate\" style=\"font-size:15px;\">⛽ '+station", "'<div class=\"bdm-plate\" style=\"font-size:15px;\">'+station"),
    ("'<div style=\"font-size:11px;color:var(--text2);margin-top:2px;\">📍 '+loc", "'<div style=\"font-size:11px;color:var(--text2);margin-top:2px;\">'+loc"),
    ("'<div class=\"bdm-plate\">🚗 '+plate", "'<div class=\"bdm-plate\">'+plate"),
    ("'<div class=\"bdm-plate\">📅 '+dateDisp", "'<div class=\"bdm-plate\">'+dateDisp"),
    ('"bdm-plate" style="font-size:16px;">⚙ จัดการทะเบียน</div>', '"bdm-plate" style="font-size:16px;">จัดการทะเบียน</div>'),
    # noMatch indicator in stmt table
    ("'<span title=\"ไม่พบทะเบียนนี้ใน Trip Sheet", "'<span title=\"ไม่พบทะเบียนนี้ใน Trip Sheet"),  # no-op placeholder, handled below
]

# portal index.html
PORTAL = [
    ("} else { _pfSyncMsg('⚠️ ไม่พบข้อมูลใน GAS'); }", "} else { _pfSyncMsg('ไม่พบข้อมูลใน GAS'); }"),
    ("+'<div class=\"pf-edit-badge\">✏️</div>'", "+'<div class=\"pf-edit-badge\">✎</div>'"),
    ("+(pf.pwHash?' 🔒':'')", "+(pf.pwHash?' ★':'')"),
]

# help.html
HELP = [
    ('<button class="mn-toggle"', '<button class="mn-toggle"'),  # no-op
    # ⚙ in step text content
    ('<b>⚙ จัดการทะเบียน</b>', '<b>จัดการทะเบียน</b>'),
    ('<b>⚙️ จัดการทะเบียน</b>', '<b>จัดการทะเบียน</b>'),
    ('ทะเบียนที่มี ⚠️ หมายถึง', 'ทะเบียนที่มี [!] หมายถึง'),
    ('<div class="step-group-title">⚙️ ตั้งค่า Markup', '<div class="step-group-title">ตั้งค่า Markup'),
    ('<b>⚙️ ตั้งค่า / Admin</b>', '<b>ตั้งค่า / Admin</b>'),
    ('<span class="sys-icon">⚙️</span>', '<span class="sys-icon"></span>'),
    ('— ถ้า ✅ แสดงว่า', '— ถ้าแสดง เชื่อมต่อสำเร็จ แสดงว่า'),
    ('Copy code ใหม่จาก Settings (กด 📋', 'Copy code ใหม่จาก Settings (กด ปุ่ม Copy'),
    ('<b>⚙️ ตั้งค่า', '<b>ตั้งค่า'),
    # ☰ hamburger ref in help
    ('>☰</button>', '>☰</button>'),  # keep hamburger in help
]

files = {
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/attendance/index.html': ATT,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/fleet_view/index.html': FLEET,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/index.html': PORTAL,
    'C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/help.html': HELP,
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
