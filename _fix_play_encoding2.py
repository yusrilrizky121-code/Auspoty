import os, re

BASE = r'C:\Users\Admin\Downloads\Auspoty'
JS = os.path.join(BASE, 'public', 'script.js')

with open(JS, 'r', encoding='utf-8') as f:
    content = f.read()

# Cek isi renderVItem dan renderHCard
idx_v = content.find('function renderVItem')
idx_h = content.find('function renderHCard')
print('renderVItem at index:', idx_v)
print('renderHCard at index:', idx_h)
print()
print('=== renderVItem ===')
print(repr(content[idx_v:idx_v+300]))
print()
print('=== renderHCard ===')
print(repr(content[idx_h:idx_h+300]))
print()
print('=== makeTrackData ===')
idx_m = content.find('function makeTrackData')
print(repr(content[idx_m:idx_m+250]))
