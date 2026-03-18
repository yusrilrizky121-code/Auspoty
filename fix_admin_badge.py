js_path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(js_path, encoding='utf-8') as f:
    js = f.read()

old = "return '<div style=\"display:flex;gap:10px;align-items:flex-start;\"><div style=\"width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#fff;flex-shrink:0;overflow:hidden;\">'+(d.picture?'<img src=\"'+d.picture+'\" style=\"width:100%;height:100%;object-fit:cover;\">':d.name.charAt(0).toUpperCase())+'</div><div style=\"flex:1;background:rgba(255,255,255,0.06);border-radius:12px;padding:10px 14px;\"><div style=\"display:flex;justify-content:space-between;margin-bottom:4px;\"><span style=\"font-size:13px;font-weight:700;color:var(--accent);\">'+d.name+'</span><span style=\"font-size:11px;color:var(--text-sub);\">'+time+'</span></div><p style=\"font-size:14px;color:white;line-height:1.5;margin:0;\">'+d.text+'</p></div></div>';"

new = """const isAdmin = d.email === 'yusrilrizky149@gmail.com';
            const badge = isAdmin ? '<span style=\"background:linear-gradient(135deg,#f59e0b,#ef4444);color:#fff;font-size:10px;font-weight:800;padding:2px 7px;border-radius:8px;margin-left:6px;letter-spacing:.5px;\">ADMIN</span>' : '<span style=\"background:rgba(255,255,255,0.1);color:var(--text-sub);font-size:10px;font-weight:600;padding:2px 7px;border-radius:8px;margin-left:6px;\">Pengguna</span>';
            return '<div style=\"display:flex;gap:10px;align-items:flex-start;\"><div style=\"width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700;color:#fff;flex-shrink:0;overflow:hidden;\">'+(d.picture?'<img src=\"'+d.picture+'\" style=\"width:100%;height:100%;object-fit:cover;\">':d.name.charAt(0).toUpperCase())+'</div><div style=\"flex:1;background:'+(isAdmin?'rgba(245,158,11,0.08)':'rgba(255,255,255,0.06)')+';border-radius:12px;padding:10px 14px;border:'+(isAdmin?'1px solid rgba(245,158,11,0.3)':'1px solid transparent')+'\"><div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;\"><div style=\"display:flex;align-items:center;\"><span style=\"font-size:13px;font-weight:700;color:'+(isAdmin?'#f59e0b':'var(--accent)')+';\">'+d.name+'</span>'+badge+'</div><span style=\"font-size:11px;color:var(--text-sub);\">'+time+'</span></div><p style=\"font-size:14px;color:white;line-height:1.5;margin:0;\">'+d.text+'</p></div></div>';"""

if old in js:
    js = js.replace(old, new)
    print("replaced OK")
else:
    # cari bagian render komentar
    idx = js.find("d.name+'</span><span style=")
    print("fallback idx:", idx)
    print("context:", repr(js[max(0,idx-30):idx+80]))

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("done")
