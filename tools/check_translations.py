import re, os, sys
print('check_translations running')
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
skip_dirs = {'.venv','venv', 'locale/en', 'templates/admin', 'node_modules', 'venv/Scripts'}
patterns = [
    re.compile(r"_\(\s*(['\"])(.*?)\1\s*\)"),
    re.compile(r"gettext_lazy\(\s*(['\"])(.*?)\1\s*\)"),
    re.compile(r"gettext\(\s*(['\"])(.*?)\1\s*\)"),
        re.compile(r'\{%\s*trans\s+([\'\"])(.*?)\1\s*%}'),
        re.compile(r'\{%\s*trans\s+([^%]+?)%}')
]
blockre = re.compile(r"\{%\s*blocktrans[^%]*%\}(.+?)\{%\s*endblocktrans\s*%\}", re.S)
msgs = set()
for dirpath, dirnames, filenames in os.walk(root):
    norm = dirpath.replace('\\','/')
    if any(sd in norm for sd in skip_dirs):
        continue
    for fname in filenames:
        if fname.endswith(('.py','.html','.txt')):
            path = os.path.join(dirpath,fname)
            try:
                with open(path,'r',encoding='utf-8') as f:
                    s=f.read()
            except Exception:
                continue
            for m in blockre.findall(s):
                txt=' '.join(line.strip() for line in m.splitlines())
                msgs.add(txt)
            for pat in patterns:
                for m in pat.findall(s):
                    if isinstance(m, tuple):
                        msgs.add(m[1].strip())
                    else:
                        msgs.add(m.strip())
# filter
msgs = {m for m in msgs if m and 'admin' not in m.lower()}
po_path = os.path.join(root,'locale','tr','LC_MESSAGES','django.po')
if not os.path.exists(po_path):
    print('Turkish PO file not found at', po_path, file=sys.stderr)
    sys.exit(2)
with open(po_path,'r',encoding='utf-8') as f:
    po_text=f.read()
missing=[]
for m in sorted(msgs):
    # check simple presence
    if ('msgid "'+m+'"') in po_text or ('"'+m+'"' in po_text):
        continue
    missing.append(m)
print('Root:', root)
print('Total translatable strings found (excluding admin paths):', len(msgs))
print('Missing in locale/tr:', len(missing))
for i,m in enumerate(missing,1):
    print(f'{i}. {m}')
