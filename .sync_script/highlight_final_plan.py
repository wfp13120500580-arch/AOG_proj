from pathlib import Path

p = Path('index_v3.0_minimal.html')
s = p.read_text(encoding='utf-8')

old = '''        <div class="wb-final-plan" :class="{ready:spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id}">
          <div class="wb-plan-left">
            <div class="wb-plan-title">最终保障方案 <span>{{ spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id ? '已生成' : '待生成' }}</span></div>
            <div class="wb-plan-desc" v-if="spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id&&spReport.schemes&&spReport.schemes.length">{{ spReport.schemes[0].name }} · {{ spReport.schemes[0].transport }} · ETA {{ spReport.schemes[0].eta }}</div>
            <div class="wb-plan-desc" v-else>询件、运输方案及合同确认完成后生成，作为运输监控执行基准。</div>
          </div>
          <button @click="openSupportPlanDialog">{{ spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id ? '查看方案' : '生成方案' }}</button>
        </div>'''

new = '''        <div class="wb-plan-hero" :class="{ready:spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id}">
          <div class="wb-plan-hero-accent"></div>
          <div class="wb-plan-hero-main">
            <div class="wb-plan-hero-head">
              <div>
                <div class="wb-plan-kicker">核心决策</div>
                <div class="wb-plan-hero-title">最终保障方案
                  <span :class="{ready:spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id}">{{ spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id ? '已生成' : '待生成' }}</span>
                </div>
              </div>
              <button class="wb-plan-hero-btn" @click="openSupportPlanDialog">{{ spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id ? '查看完整方案 →' : '生成保障方案 →' }}</button>
            </div>

            <template v-if="spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id&&spReport.schemes&&spReport.schemes.length">
              <div class="wb-plan-primary">{{ spReport.schemes[0].name }}</div>
              <div class="wb-plan-metrics">
                <div><label>保障方式</label><strong>{{ spReport.schemes[0].method || '待确认' }}</strong></div>
                <div><label>运输方式</label><strong>{{ spReport.schemes[0].transport || '待确认' }}</strong></div>
                <div><label>预计到达</label><strong>{{ spReport.schemes[0].eta || '待确认' }}</strong></div>
                <div><label>执行状态</label><strong>作为当前执行基准</strong></div>
              </div>
              <div class="wb-plan-reason" v-if="spReport.decision">{{ spReport.decision }}</div>
            </template>
            <div class="wb-plan-await" v-else>
              <strong>等待形成最终保障决策</strong>
              <span>询件、运输方案及合同确认完成后生成；生成后作为运输进度监控和异常处置的执行基准。</span>
            </div>
          </div>
        </div>'''

if old not in s:
    raise SystemExit('final plan block not found')
s = s.replace(old, new, 1)

s = s.replace('title="AOG 保障方案"', 'title="最终保障方案"', 1)

css = r'''
/* ===== Final support plan hero ===== */
.wb-plan-hero{position:relative;display:flex;min-height:88px;background:linear-gradient(135deg,#f8fbff 0%,#eef6ff 100%);border:1px solid #b9d7ef;border-radius:10px;overflow:hidden;flex:none;box-shadow:0 3px 10px rgba(42,102,150,.08)}
.wb-plan-hero.ready{background:linear-gradient(135deg,#f8fffb 0%,#eefaf3 100%);border-color:#8fc8a4;box-shadow:0 4px 12px rgba(53,132,82,.1)}
.wb-plan-hero-accent{width:5px;background:#2f8fce;flex:none}.wb-plan-hero.ready .wb-plan-hero-accent{background:#35a464}
.wb-plan-hero-main{flex:1;min-width:0;padding:11px 14px 12px}.wb-plan-hero-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}
.wb-plan-kicker{font-size:8px;letter-spacing:1px;color:#2f82ba;font-weight:700;margin-bottom:2px}.wb-plan-hero.ready .wb-plan-kicker{color:#2f8b57}
.wb-plan-hero-title{font-size:14px;font-weight:800;color:#183c5a}.wb-plan-hero-title span{display:inline-block;margin-left:7px;font-size:8px;font-weight:600;color:#8a98a6;background:#edf1f5;border-radius:10px;padding:2px 7px;vertical-align:2px}.wb-plan-hero-title span.ready{background:#dcf5e5;color:#25814d}
.wb-plan-hero-btn{border:0;background:#247fb9;color:#fff;border-radius:6px;padding:7px 11px;font-size:9px;font-weight:600;cursor:pointer;white-space:nowrap}.wb-plan-hero.ready .wb-plan-hero-btn{background:#2d9258}.wb-plan-hero-btn:hover{filter:brightness(.96)}
.wb-plan-primary{font-size:12px;font-weight:800;color:#234d6b;margin-top:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wb-plan-hero.ready .wb-plan-primary{color:#22613e}
.wb-plan-metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:8px}.wb-plan-metrics>div{background:rgba(255,255,255,.75);border:1px solid rgba(170,199,219,.45);border-radius:6px;padding:6px 8px;min-width:0}.wb-plan-hero.ready .wb-plan-metrics>div{border-color:rgba(149,199,165,.5)}.wb-plan-metrics label{display:block;font-size:8px;color:#8a99a7}.wb-plan-metrics strong{display:block;font-size:9px;color:#334f64;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wb-plan-reason{font-size:9px;color:#657989;line-height:1.5;margin-top:7px;padding-top:7px;border-top:1px dashed rgba(115,156,185,.28)}
.wb-plan-await{display:flex;align-items:center;gap:12px;margin-top:9px;padding:8px 10px;background:rgba(255,255,255,.65);border:1px dashed #bdd3e4;border-radius:6px}.wb-plan-await strong{font-size:10px;color:#395d78;white-space:nowrap}.wb-plan-await span{font-size:9px;color:#8798a7;line-height:1.45}
'''
s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
print('final plan highlighted', len(s))
