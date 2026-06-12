import sys, os
sys.stdout.reconfigure(encoding='utf-8')

S_HOME  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'
S_TRUCK = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>'
S_CARD  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>'
S_FUEL  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>'
S_CHART = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
S_EYE   = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'
S_USER  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
S_BOOK  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

QN_REPS = [
    ('<span class="qn-ic">\U0001f3e0</span>', f'<span class="qn-ic">{S_HOME}</span>'),
    ('<span class="qn-ic">\U0001f69b</span>', f'<span class="qn-ic">{S_TRUCK}</span>'),
    ('<span class="qn-ic">\U0001f69a</span>', f'<span class="qn-ic">{S_TRUCK}</span>'),
    ('<span class="qn-ic">\U0001f4b3</span>', f'<span class="qn-ic">{S_CARD}</span>'),
    ('<span class="qn-ic">⛽</span>',         f'<span class="qn-ic">{S_FUEL}</span>'),
    ('<span class="qn-ic">\U0001f4b0</span>', f'<span class="qn-ic">{S_CHART}</span>'),
    ('<span class="qn-ic">\U0001f6a6</span>', f'<span class="qn-ic">{S_EYE}</span>'),
    ('<span class="qn-ic">\U0001f550</span>', f'<span class="qn-ic">{S_USER}</span>'),
    ('<span class="qn-ic">\U0001f4d6</span>', f'<span class="qn-ic">{S_BOOK}</span>'),
]

EXTRA = {
    'project2/index.html': [
        ('>🗑 ลบที่เลือก<', '>ลบที่เลือก<'),
        ('>📋 วางวงเงิน</button>', '>วางวงเงิน</button>'),
        ('<h3>➕ เพิ่มบัตรใหม่</h3>', '<h3>เพิ่มบัตรใหม่</h3>'),
        ('<h3>📋 วางวงเงิน</h3>', '<h3>วางวงเงิน</h3>'),
        ("'🗑 ลบบัตรนี้'", "'ลบบัตรนี้'"),
        ('💡 <b>คอมพิวเตอร์:</b>', '<b>คอมพิวเตอร์:</b>'),
        ('📱 <b>มือถือ:</b> กดปุ่ม 📋 <b>วางวงเงิน</b>', 'มือถือ: กดปุ่ม <b>วางวงเงิน</b>'),
    ],
    'priceboard/index.html': [
        ('>⛽ ราคาน้ำมันวันนี้:<', '>ราคาน้ำมันวันนี้:<'),
        ('>📈 ปรับราคาเพิ่ม:<', '>ปรับราคาเพิ่ม:<'),
        ('>📊 กระดานต้นฉบับ</button>', '>กระดานต้นฉบับ</button>'),
        ('>📋 กระดานราคาใหม่', '>กระดานราคาใหม่'),
        ('>🔍 เปรียบเทียบราคา', '>เปรียบเทียบราคา'),
        ('>📥 บันทึก Excel</button>', '>บันทึก Excel</button>'),
        ('>🖨 บันทึก PDF</button>', '>บันทึก PDF</button>'),
        ('>🔍 วิเคราะห์</button>', '>วิเคราะห์</button>'),
        ('>🗑 ล้างค่า</button>', '>ล้างค่า</button>'),
        ('>📥 ส่งออก Excel</but', '>ส่งออก Excel</but'),
    ],
    'fleet_view/index.html': [
        ('🚚 Fleet Dashboard', 'Fleet Dashboard'),
        ('📅 สรุปรายเดือน', 'สรุปรายเดือน'),
        ('🗂️ สายงาน', 'สายงาน'),
        ('🏆 Top 10 รถ', 'Top 10 รถ'),
        ('🏆 Top 10 คนขับ', 'Top 10 คนขับ'),
        ('🚦 กำลังรถวันนี้', 'กำลังรถวันนี้'),
        ('⛶ เต็มจอ', 'เต็มจอ'),
        ('"📈 วิเคราะห์"', '"วิเคราะห์"'),
        ('📈 วิเคราะห์</div>', 'วิเคราะห์</div>'),
        ('📅 เปรียบเทียบเดือนนี้', 'เปรียบเทียบเดือนนี้'),
        ('🛣️ Top Routes', 'Top Routes'),
        ('📈 บาท/km รายคัน', 'บาท/km รายคัน'),
        ('🏦 Statement วิเคราะห์', 'Statement วิเคราะห์'),
        ('🔗 Google Apps Script URL', 'Google Apps Script URL'),
        ('>💾 บันทึก</button>', '>บันทึก</button>'),
        ('>🔌 Test</button>', '>Test</button>'),
        ('📋 GAS Script', 'GAS Script'),
        ('>📋 Copy Code', '>Copy Code'),
        ('🏦 Transaction Report', 'Transaction Report'),
        ('🗑️ จัดการข้อมูล Local', 'จัดการข้อมูล Local'),
        ('>📥 Export สถานะ (JSON)</button>', '>Export สถานะ (JSON)</button>'),
        ('>🗑️ ล้าง status ทั้งหมด</button>', '>ล้าง status ทั้งหมด</button>'),
        ('value="ready">✅ พร้อมรับงาน', 'value="ready">พร้อมรับงาน'),
        ('value="busy">❌ ไม่พร้อมรับงาน', 'value="busy">ไม่พร้อมรับงาน'),
        ("value=\"leave\">\U0001f3d6️ ลา", 'value="leave">ลา'),
        ("'✅ พร้อม: '", "'พร้อม: '"),
        ("'❌ ไม่พร้อม: '", "'ไม่พร้อม: '"),
        ("'\U0001f3d6️ ลา: '", "'ลา: '"),
        ("ready:'✅ พร้อมรับงาน'", "ready:'พร้อมรับงาน'"),
        ("busy:'❌ ไม่พร้อมรับงาน'", "busy:'ไม่พร้อมรับงาน'"),
        ("leave:'\U0001f3d6️ ลา'", "leave:'ลา'"),
        ("lbl:'✅ พร้อม'", "lbl:'พร้อม'"),
        ("lbl:'❌ ไม่พร้อม'", "lbl:'ไม่พร้อม'"),
        ("lbl:'\U0001f3d6️ ลา'", "lbl:'ลา'"),
        ('⛽ ลิตรรวม', 'ลิตรรวม'),
        ('💰 ยอดรวม', 'ยอดรวม'),
        ('📊 ฿/ลิตรเฉลี่ย', '฿/ลิตรเฉลี่ย'),
        ('📍 จังหวัดที่เติม', 'จังหวัดที่เติม'),
        ("'\U0001f697 รายคัน'", "'รายคัน'"),
        ("'\U0001f4cd สถานี'", "'สถานี'"),
        ("'\U0001f5fa️ จังหวัด'", "'จังหวัด'"),
        ("'\U0001f4c5 รายวัน'", "'รายวัน'"),
        ('🚗 สรุปน้ำมันรายคัน', 'สรุปน้ำมันรายคัน'),
        ('📍 Top สถานีน้ำมัน', 'Top สถานีน้ำมัน'),
        ('🗺️ สรุปรายจังหวัด', 'สรุปรายจังหวัด'),
        ('📅 ยอดเติมน้ำมันรายวัน', 'ยอดเติมน้ำมันรายวัน'),
        ('🚗 รถทั้งหมด', 'รถทั้งหมด'),
        ('⛽ ลิตรรวม', 'ลิตรรวม'),
        ('💰 ยอดรวม', 'ยอดรวม'),
    ],
    'attendance/index.html': [
        ('>🏠 Portal</a>', '>Portal</a>'),
        ('>🏠 กลับ Portal</a>', '>กลับ Portal</a>'),
        ('>🔄 รีเฟรช<', '>รีเฟรช<'),
        ('>👥 สถานะพนักงานวันนี้<', '>สถานะพนักงานวันนี้<'),
        ('>🕐 บันทึกทั้งหมดวันนี้<', '>บันทึกทั้งหมดวันนี้<'),
        ('>📋 บันทึกการเข้างาน<', '>บันทึกการเข้างาน<'),
        ('>📊 สรุปรายคน<', '>สรุปรายคน<'),
        ('>📅 รายละเอียดรายวัน<', '>รายละเอียดรายวัน<'),
        ('>📍 สถานที่ทำงาน (GPS)<', '>สถานที่ทำงาน (GPS)<'),
        ('>📍 ใช้ตำแหน่งปัจจุบัน</button>', '>ใช้ตำแหน่งปัจจุบัน</button>'),
        ('>💾 บันทึก</button>', '>บันทึก</button>'),
        ('>🗑️ จัดการข้อมูล<', '>จัดการข้อมูล<'),
        ('>📥 Export JSON</button>', '>Export JSON</button>'),
        ("'👥 พนักงานทั้งหมด'", "'พนักงานทั้งหมด'"),
        ("'✅ มาทำงาน'", "'มาทำงาน'"),
        ("'❌ ไม่มา / ยังไม่เช็ค'", "'ไม่มา / ยังไม่เช็ค'"),
    ],
    'help.html': [
        ('<span class="mn-title">📖 คู่มือการใช้งาน</span>', '<span class="mn-title">คู่มือการใช้งาน</span>'),
        ('<h1>📖 คู่มือการใช้งาน</h1>', '<h1>คู่มือการใช้งาน</h1>'),
        ('<span class="sys-icon">🏠</span>', '<span class="sys-icon"></span>'),
        ('<span class="sys-icon">🚦</span>', '<span class="sys-icon"></span>'),
        ('<span class="sys-icon">💳</span>', '<span class="sys-icon"></span>'),
        ('<span class="sys-icon">⛽</span>', '<span class="sys-icon"></span>'),
        ('<span class="sys-icon">💰</span>', '<span class="sys-icon"></span>'),
        ('<span class="sys-icon">🚚</span>', '<span class="sys-icon"></span>'),
        ('<span class="sys-icon">🏦</span>', '<span class="sys-icon"></span>'),
        ('<span class="ic">🏠</span>', '<span class="ic"></span>'),
        ('<span class="ic">🚦</span>', '<span class="ic"></span>'),
        ('<span class="ic">💳</span>', '<span class="ic"></span>'),
        ('<span class="ic">⛽</span>', '<span class="ic"></span>'),
        ('<span class="ic">💰</span>', '<span class="ic"></span>'),
        ('<span class="ic">🚚</span>', '<span class="ic"></span>'),
        ('<span class="ic">🏦</span>', '<span class="ic"></span>'),
        ('📋 วางวงเงิน</b>', 'วางวงเงิน</b>'),
        ('➕ เพิ่มบัตร</b>', 'เพิ่มบัตร</b>'),
        ('🗑 ลบที่เลือก</b>', 'ลบที่เลือก</b>'),
        ('🧮 คำนวณต้นทุน</b>', 'คำนวณต้นทุน</b>'),
        ('🏠 แดชบอร์ด</b>', 'แดชบอร์ด</b>'),
        ('🔌 Test</b>', 'Test</b>'),
        ('💾 บันทึก</b>', 'บันทึก</b>'),
        ('🏦 Statement</b>', 'Statement</b>'),
        ('👤 TARARIN 9', 'TARARIN 9'),
        ('⚙️ Settings', 'Settings'),
    ],
    'transport.html': [
        ("showToast('🙈 ซ่อน", "showToast('ซ่อน"),
        ("showToast('✅ โหลด", "showToast('โหลด"),
        ("showToast('❌ โหลด", "showToast('โหลดไม่สำเร็จ: "),
        ("showToast('❌ เชื่อมต่อ", "showToast('เชื่อมต่อ"),
        ("showToast('✅ พบ ", "showToast('พบ "),
        ("showToast('❌ เกิด", "showToast('เกิด"),
        ("showToast('✅ คัดลอก", "showToast('คัดลอก"),
        ("showToast('✅ เพิ่ม", "showToast('เพิ่ม"),
        ("showToast('✅ จัด", "showToast('จัด"),
        ("showToast('🎨 รีเซ็ต", "showToast('รีเซ็ต"),
        ("'🚛 ทุกประเภท ", "'ทุกประเภท "),
        ("'🚛 ' + esc(s)", "esc(s)"),
        ("'📋 ไม่ระบุ ", "'ไม่ระบุ "),
    ],
}

files = [
    ('C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/project1/transport.html', False),
    ('C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/project2/index.html', False),
    ('C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/priceboard/index.html', False),
    ('C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/fleet_view/index.html', False),
    ('C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/attendance/index.html', False),
    ('C:/Users/chait/OneDrive/Desktop/CLAUDE/project4/help.html', True),
]

for fp, is_root in files:
    with open(fp, 'r', encoding='utf-8') as f:
        s = f.read()
    for old, new in QN_REPS:
        s = s.replace(old, new)
    name = os.path.basename(os.path.dirname(fp)) + '/' + os.path.basename(fp)
    for k, v in EXTRA.items():
        if fp.endswith(k):
            for old, new in v:
                s = s.replace(old, new)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(s)
    print(f'Done: {name}')

print('All done')
