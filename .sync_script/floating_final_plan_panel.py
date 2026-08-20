from pathlib import Path
import re

p = Path('index_v3.0_minimal.html')
s = p.read_text(encoding='utf-8')

start = s.find('  <!-- 保障方案对话框 -->')
end = s.find('  <el-dialog v-model="fullDialogVisible"', start)
if start == -1 or end == -1:
    raise SystemExit('final plan dialog markers not found')

replacement = '''  <!-- 最终保障方案悬浮面板 -->
  <transition name="fade">
    <div v-if="spDialogVisible" class="sp-floating-shell">
      <section class="sp-floating-panel">
        <div class="sp-floating-head">
          <div>
            <div class="sp-floating-kicker">AOG 保障决策</div>
            <div class="sp-floating-title">最终保障方案</div>
            <div class="sp-floating-sub" v-if="spGenerated && spReport.basic">{{ spReport.basic.id }} · {{ spReport.basic.site }}</div>
          </div>
          <button class="sp-floating-close" @click="spDialogVisible=false">×</button>
        </div>
        <div class="sp-floating-body">
          <div class="sp-dialog-hero" v-if="spReport.schemes && spReport.schemes.length">
            <span class="sp-scheme-badge recommended">推荐执行</span>
            <strong>{{ spReport.schemes[0].name }}</strong>
          </div>
          <div class="pm-section"><h4>保障方案明细</h4>
            <div v-for="(sch,si) in spReport.schemes" :key="si" class="sp-scheme-card">
              <b>方案{{si+1}}：{{sch.name}}</b>
              <table class="pm-table"><tr><td>{{sch.parts}}</td><td>{{sch.transport}}</td><td>{{sch.eta}}</td></tr></table>
            </div>
          </div>
          <div class="sp-decision-box" v-if="spReport.decision">AI决策建议：{{spReport.decision}}</div>
        </div>
        <div class="sp-floating-footer"><el-button @click="spDialogVisible=false">关闭</el-button><el-button type="primary" @click="spExport">导出方案</el-button></div>
      </section>
    </div>
  </transition>
'''

s = s[:start] + replacement + s[end:]

css = r'''
.sp-floating-shell{position:fixed;right:18px;top:65px;bottom:18px;width:620px;z-index:3000}
.sp-floating-panel{height:100%;background:#fff;border-radius:14px;box-shadow:0 18px 50px rgba(0,0,0,.25);display:flex;flex-direction:column;overflow:hidden}
.sp-floating-head{background:#173b63;color:#fff;padding:18px;display:flex;justify-content:space-between}.sp-floating-title{font-size:22px;font-weight:800}.sp-floating-close{background:none;border:0;color:#fff;font-size:24px}
.sp-floating-body{flex:1;overflow:auto;padding:16px}.sp-dialog-hero{background:#edf6ff;border:1px solid #b7d8f2;padding:16px;border-radius:10px}.sp-scheme-badge.recommended{background:#409eff;color:#fff;padding:4px 10px;border-radius:20px}.sp-scheme-card{background:#fff;border:1px solid #dce8f3;padding:12px;margin-top:10px;border-radius:8px}.sp-decision-box{background:#fff5dd;padding:12px;border-radius:8px}.sp-floating-footer{padding:12px;text-align:right;border-top:1px solid #eee}
'''
s = s.replace('</style>', css + '</style>', 1)

p.write_text(s, encoding='utf-8')
