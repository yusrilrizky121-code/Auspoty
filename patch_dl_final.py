import re

path = r'C:\Users\Admin\Downloads\Auspoty\public\script.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the entire downloadMusic function
# Match from "// DOWNLOAD" or "async function downloadMusic" to closing brace
old_pattern = re.compile(
    r'(// DOWNLOAD\s*\n)?async function downloadMusic\(\).*?(?=\n// |\n\n// |\Z)',
    re.DOTALL
)

new_func = '''// DOWNLOAD
function downloadMusic() {
    if (!currentTrack) { showToast('Putar lagu dulu!'); return; }
    var dlUrl = 'https://id.ytmp3.mobi/v1/#' + currentTrack.videoId;
    window.open(dlUrl, '_blank');
    showToast('Halaman download dibuka. Klik Konversi lalu Unduh MP3');
}'''

if old_pattern.search(content):
    new_content = old_pattern.sub(new_func + '\n', content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('OK - replaced downloadMusic')
else:
    # Fallback: find by line
    lines = content.split('\n')
    start = None
    end = None
    brace_count = 0
    in_func = False
    for i, line in enumerate(lines):
        if 'function downloadMusic' in line or ('async function downloadMusic' in line):
            start = i
            # go back to find comment
            if i > 0 and '// DOWNLOAD' in lines[i-1]:
                start = i - 1
            in_func = True
        if in_func:
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0 and start is not None and i > start:
                end = i
                break

    if start is not None and end is not None:
        new_lines = lines[:start] + new_func.split('\n') + lines[end+1:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f'OK - replaced lines {start}-{end}')
    else:
        print('ERROR: could not find downloadMusic function')
        print('Searching...')
        for i, line in enumerate(lines):
            if 'download' in line.lower():
                print(f'  Line {i}: {line[:80]}')
