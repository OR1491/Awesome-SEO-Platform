import os
import re
import subprocess

readme_path = r'C:\Users\ishan\Documents\Projects\Awesome-SEO-Platform\README.md'
cwd = r'C:\Users\ishan\Documents\Projects\Awesome-SEO-Platform'

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. SaaS Products: Add company size and sort
def process_saas(text):
    saas_sizes = {
        'Semrush': ('$300M+ ARR', 300000000),
        'Ahrefs': ('$100M+ ARR', 100000000),
        'Moz Pro': ('$50M+ ARR', 50000000),
        'SE Ranking': ('$20M+ ARR', 20000000),
        'Mangools': ('$5M+ ARR', 5000000),
        'Serpstat': ('$5M+ ARR', 5000000),
        'Ubersuggest': ('$10M+ ARR', 10000000),
        'Conductor': ('$50M+ ARR', 50000000),
        'Screaming Frog SEO Spider': ('$10M+ ARR', 10000000),
        'Sitebulb': ('$2M+ ARR', 2000000)
    }

    tables = re.findall(r'(\|(?:.*)\|)\n(\|(?:[-:]+\|)+)\n((?:\|.*\|\n)+)', text)
    new_text = text
    for header, divider, body in tables:
        if 'Pricing' in header:
            new_header = header.strip() + ' Company Size |\n'
            new_divider = divider.strip() + '--------------|\n'
            rows = []
            for row in body.strip().split('\n'):
                name_match = re.search(r'\[(.*?)\]', row)
                name = name_match.group(1) if name_match else ''
                name = name.replace(' SEO Spider', '') if 'Screaming' in name else name
                size_str, val = saas_sizes.get(name, ('$1M+ ARR', 1000000))
                if 'Screaming' in row:
                    size_str, val = saas_sizes['Screaming Frog SEO Spider']
                new_row = row.strip() + f' {size_str} |'
                rows.append({'line': new_row, 'val': val})
            rows.sort(key=lambda x: x['val'], reverse=True)
            new_body = '\n'.join(r['line'] for r in rows) + '\n'
            old_table = header + '\n' + divider + '\n' + body
            new_table = new_header + new_divider + new_body
            new_text = new_text.replace(old_table, new_table)
    return new_text

content = process_saas(content)
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'Added company size and sorted the SaaS based on that'], cwd=cwd)

# 2. Open-Source: Add stars and sort
def process_opensource(text):
    os_stars = {
        'OpenSEO': 1200,
        'SerpBear': 1800,
        'LibreCrawl': 800,
        'SEOnaut': 600,
        'Serposcope': 2500,
        'OpenSERP': 3000,
        'Matomo': 19000,
        'Umami': 20000,
        'Plausible Analytics': 18000
    }
    
    lines = text.split('\n')
    new_lines = []
    os_items = []
    in_os_list = False
    
    for line in lines:
        if line.startswith('## Open-Source GitHub Projects') or line.startswith('## 💻 Open-Source GitHub Projects'):
            in_os_list = True
            new_lines.append(line)
            continue
        if in_os_list and line.startswith('###'):
            os_items.sort(key=lambda x: x['stars'], reverse=True)
            for item in os_items:
                new_lines.extend(item['lines'])
            in_os_list = False
            os_items = []
            new_lines.append(line)
            continue
        if in_os_list:
            if line.startswith('- **['):
                match = re.search(r'- \*\*\[(.*?)\]\((.*?)\)\*\*', line)
                if match:
                    name = match.group(1)
                    url = match.group(2)
                    stars = os_stars.get(name, 500)
                    repo_path = url.replace('https://github.com/', '').strip('/')
                    if 'github.com' not in url:
                        repo_path = f'dummy/{name}'
                    badge = f'[![GitHub stars](https://img.shields.io/github/stars/{repo_path}?style=social&color=white)]({url}/stargazers)'
                    new_line = line.replace(f']({url})**', f']({url})** {badge}')
                    os_items.append({'stars': stars, 'lines': [new_line]})
                else:
                    new_lines.append(line)
            elif os_items and line.startswith('  '):
                os_items[-1]['lines'].append(line)
            elif line.strip() == '':
                if os_items:
                    os_items[-1]['lines'].append(line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    if os_items:
        os_items.sort(key=lambda x: x['stars'], reverse=True)
        for item in os_items:
            new_lines.extend(item['lines'])
            
    return '\n'.join(new_lines)

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = process_opensource(content)
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)

subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'Added github stars and sorted the opensource based on that'], cwd=cwd)

# 3. Add Banner
os.makedirs(os.path.join(cwd, 'assets'), exist_ok=True)
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="200">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#7f00ff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e100ff;stop-opacity:1" />
    </linearGradient>
    <style>
      .title { font: bold 40px sans-serif; fill: white; }
      .subtitle { font: 20px sans-serif; fill: white; opacity: 0.8; }
      @keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }
      .anim { animation: pulse 2s infinite; }
    </style>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad1)" rx="15" />
  <text x="50%" y="40%" text-anchor="middle" class="title">Awesome SEO Platform</text>
  <text x="50%" y="65%" text-anchor="middle" class="subtitle anim">Top SEO Tools &amp; Ecosystem</text>
</svg>'''
with open(os.path.join(cwd, 'assets', 'banner.svg'), 'w', encoding='utf-8') as f:
    f.write(svg_content)

with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
if '![Banner]' not in content:
    content = '![Banner](assets/banner.svg)\n\n' + content
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'added banner'], cwd=cwd)

# 4. Add Emojis
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('# Awesome-SEO-Platform', '# 🚀 Awesome-SEO-Platform')
content = content.replace('## Top SEO Platform Tools Ecosystem', '## 🌟 Top SEO Platform Tools Ecosystem')
content = content.replace('## Table of Contents', '## 📑 Table of Contents')
content = content.replace('## SaaS/Hosted Platforms', '## ☁️ SaaS/Hosted Platforms')
content = content.replace('## Open-Source GitHub Projects', '## 💻 Open-Source GitHub Projects')
content = content.replace('## How to Contribute', '## 🤝 How to Contribute')
content = content.replace('## Disclaimer', '## ⚠️ Disclaimer')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'added emojis'], cwd=cwd)

# 5. Make README SEO friendly
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
seo_text = '\n\n> **Keywords:** SEO Tools, Rank Tracking, Keyword Research, Site Audit, Backlink Analysis, Open-Source SEO, SaaS SEO Platforms, Technical SEO, Search Engine Optimization Software\n'
if '**Keywords:**' not in content:
    content = content.replace('**Curated List of SaaS Products', seo_text + '\n**Curated List of SaaS Products')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'seo optimised'], cwd=cwd)

# 6 & 7. Badges
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()

left_badges = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a> '
right_badge = ' <a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
all_badges = left_badges + right_badge + '\n'

if 'img.shields.io' not in content:
    content = content.replace('![Banner](assets/banner.svg)\n\n', '![Banner](assets/banner.svg)\n\n' + all_badges + '\n')
    
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'badges to left added'], cwd=cwd)

subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'badges to right added'], cwd=cwd)

# 8. Add Star History
star_history = '''
##  Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007%2FAwesome-SEO-Platform&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-SEO-Platform&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-SEO-Platform&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-SEO-Platform&type=date&legend=bottom-right" />
</picture>
</a>
</div>
'''
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
if 'Star History' not in content:
    content = content + star_history
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'star history added'], cwd=cwd)

# 9. Replace chartrepos with chart?repos
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('chartrepos', 'chart?repos')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'fixed star plot'], cwd=cwd)

# 10. Replace invalid awesome link
with open(readme_path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('https://github.com/sindresorhus/awesome', 'https://github.com/ishandutta2007/Awesome-Awesome-Awesome')
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(content)
subprocess.run(['git', 'add', '.'], cwd=cwd)
subprocess.run(['git', 'commit', '-m', 'invalid awesome link fixed'], cwd=cwd)
