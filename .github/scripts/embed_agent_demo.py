from pathlib import Path
import re

p = Path('index_v3.0_minimal.html')
s = p.read_text(encoding='utf-8')

css = '''
/* ===== Embedded interactive Agent demo ===== */
.agent-demo-frame-wrap{height:100%;width:100%;background:#fff;border:1px solid #e1e6eb;border-radius:8px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.05)}
.agent-demo-frame{display:block;width:100%;height:100%;border:0;background:#fff}
'''
if 'Embedded interactive Agent demo' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)

replacement = '''      <!-- 右侧：完整交互 Agent Demo -->
      <aside class="wb-agent-v3">
        <div class="agent-demo-frame-wrap">
          <iframe class="agent-demo-frame" src="agent_chat_demo.html" title="AOG保障Agent完整交互Demo"></iframe>
        </div>
      </aside>'''

pattern = re.compile(r'      <!-- 右侧：Agent -->\s*<aside class="wb-agent-v3">.*?</aside>', re.S)
s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    # compatible with already-renamed marker
    pattern = re.compile(r'      <!-- 右侧：.*?Agent.*?-->\s*<aside class="wb-agent-v3">.*?</aside>', re.S)
    s, n = pattern.subn(replacement, s, count=1)
if n != 1:
    raise SystemExit('Could not locate the right Agent panel')

p.write_text(s, encoding='utf-8')
print('Embedded agent_chat_demo.html into main workbench right panel')
