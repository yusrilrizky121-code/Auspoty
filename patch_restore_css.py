import subprocess, os

base = r'C:\Users\Admin\Downloads\Auspoty'
css_path = os.path.join(base, 'public', 'style.css')

result = subprocess.run(
    ['git', '-C', base, 'show', '4684b89:public/style.css'],
    capture_output=True
)
content = result.stdout.decode('utf-8')
print("Lines:", content.count('\n'))

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("DONE")
