from pathlib import Path
import re

p = Path('index_v3.0_minimal.html')
s = p.read_text(encoding='utf-8')

# 1) 删除“系统概览”导航入口
s = re.sub(
    r'\s*<button\s+:class="\{active:activeTab===\'overview\'\}"\s+@click="activeTab=\'overview\';if\(!stats\)loadStats\(\)"\s*>系统概览</button>',
    '',
    s,
    count=1,
)

# 2) 删除“系统概览”页面本体
ov_start = s.find('  <!-- ==================== 系统概览 ==================== -->')
ov_end_marker = '  <!-- 智能评估功能已集成至工作台中，不再需要独立Tab -->'
if ov_start != -1:
    ov_end = s.find(ov_end_marker, ov_start)
    if ov_end == -1:
        raise SystemExit('overview end marker not found')
    s = s[:ov_start] + s[ov_end:]

# 3) 整体替换监控看板
monitor_start_marker = '  <!-- ==================== 监控看板 ==================== -->'
workbench_marker = '  <!-- ==================== 任务工作台 v2 ==================== -->'
monitor_start = s.find(monitor_start_marker)
monitor_end = s.find(workbench_marker, monitor_start)
if monitor_start == -1 or monitor_end == -1:
    raise SystemExit('monitor/workbench markers not found')

monitor_html = r'''  <!-- ==================== 监控看板 ==================== -->
  <div class="monitor-container monitor-v2" v-if="activeTab==='monitor'">
    <div class="monitor-shell">
      <div class="monitor-page-head">
        <div>
          <div class="monitor-page-title">AOG保障监控</div>
          <div class="monitor-page-sub">聚焦在途AOG任务、关键保障节点与风险时限</div>
        </div>
        <div class="monitor-head-status"><span class="monitor-live-dot"></span>保障态势实时更新</div>
      </div>

      <div class="monitor-summary">
        <div class="monitor-kpi critical">
          <div class="monitor-kpi-top"><span>进行中任务</span><span class="monitor-kpi-icon">01</span></div>
          <div class="monitor-kpi-value">{{ tasksActive }}</div>
          <div class="monitor-kpi-foot"><b>{{ tasksUrgent }}</b> 个紧急任务需重点关注</div>
        </div>
        <div class="monitor-kpi">
          <div class="monitor-kpi-top"><span>今日新增</span><span class="monitor-kpi-icon">02</span></div>
          <div class="monitor-kpi-value">3</div>
          <div class="monitor-kpi-foot">较昨日 <b>+1</b></div>
        </div>
        <div class="monitor-kpi success">
          <div class="monitor-kpi-top"><span>本月完成</span><span class="monitor-kpi-icon">03</span></div>
          <div class="monitor-kpi-value">47</div>
          <div class="monitor-kpi-foot">保障成功率 <b>96%</b></div>
        </div>
        <div class="monitor-kpi">
          <div class="monitor-kpi-top"><span>平均响应</span><span class="monitor-kpi-icon">04</span></div>
          <div class="monitor-kpi-value">4.2<span class="monitor-kpi-unit">h</span></div>
          <div class="monitor-kpi-foot">同比缩短 <b>0.8h</b></div>
        </div>
      </div>

      <div class="monitor-grid">
        <section class="monitor-card monitor-task-panel">
          <div class="monitor-card-head">
            <div>
              <div class="monitor-card-title">保障任务态势</div>
              <div class="monitor-card-sub">按任务查看当前保障节点、时限和处置状态</div>
            </div>
            <div class="monitor-toolbar-actions">
              <div class="monitor-segment">
                <button :class="{active:listFilter==='all'}" @click="listFilter='all'">全部</button>
                <button :class="{active:listFilter==='urgent'}" @click="listFilter='urgent'">紧急</button>
                <button :class="{active:listFilter==='active'}" @click="listFilter='active'">进行中</button>
              </div>
              <div class="monitor-segment view-segment">
                <button :class="{active:viewMode==='list'}" @click="viewMode='list'">列表</button>
                <button :class="{active:viewMode==='map'}" @click="viewMode='map';initMapIfNeeded()">地图</button>
              </div>
            </div>
          </div>

          <div class="monitor-table-wrap" v-show="viewMode==='list'">
            <table class="monitor-task-table">
              <thead>
                <tr><th>任务</th><th>飞机/航班</th><th>AOG等级</th><th>保障地点</th><th>当前节点</th><th>需求时间</th><th>状态</th></tr>
              </thead>
              <tbody>
                <tr v-for="t in filteredTasks" :key="t.id" :class="{selected:selectedTask===t}" @click="selectTask(t)">
                  <td>
                    <div class="monitor-task-id">{{ t.id }}</div>
                    <div class="monitor-task-fault">{{ t.faultType }}</div>
                  </td>
                  <td><div class="monitor-primary-text">{{ t.reg }}</div><div class="monitor-secondary-text">{{ t.flight }}</div></td>
                  <td><span class="badge" :class="'aog-lv'+t.aogLevel">Lv{{ t.aogLevel }}</span></td>
                  <td><div class="monitor-primary-text">{{ t.airportCN }}</div><div class="monitor-secondary-text">{{ t.iataCode }}</div></td>
                  <td><span class="monitor-node-pill">{{ t.currentNode }}</span></td>
                  <td><div class="monitor-primary-text">{{ t.neededBy }}</div><div class="monitor-secondary-text">下班 {{ t.nextFlight }}</div></td>
                  <td><span class="monitor-status-pill" :class="t.status==='进行中'?'active':'done'">{{ t.status }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="monitor-map-wrap" v-show="viewMode==='map'">
            <div id="aogMap"></div>
          </div>
        </section>

        <aside class="monitor-side-panel" v-if="selectedTask">
          <div class="monitor-card monitor-detail-card">
            <div class="monitor-detail-top">
              <div>
                <div class="monitor-detail-label">任务监控详情</div>
                <div class="monitor-detail-id">{{ selectedTask.id }}</div>
              </div>
              <div class="monitor-detail-badges">
                <span class="badge" :class="'aog-lv'+selectedTask.aogLevel">Lv{{ selectedTask.aogLevel }}</span>
                <span class="monitor-status-pill" :class="selectedTask.status==='进行中'?'active':'done'">{{ selectedTask.status }}</span>
              </div>
            </div>

            <div class="monitor-detail-grid">
              <div class="monitor-detail-item"><label>飞机 / 航班</label><strong>{{ selectedTask.reg }} · {{ selectedTask.flight }}</strong></div>
              <div class="monitor-detail-item"><label>AOG地点</label><strong>{{ selectedTask.airportCN }}（{{ selectedTask.iataCode }}）</strong></div>
              <div class="monitor-detail-item"><label>需求时间</label><strong>{{ selectedTask.neededBy }}</strong></div>
              <div class="monitor-detail-item"><label>下个航班</label><strong>{{ selectedTask.nextFlight }}</strong></div>
            </div>

            <div class="monitor-focus-card" :class="{'high-risk':selectedTask.aogLevel===1}">
              <div class="monitor-section-title">风险与时限</div>
              <div class="monitor-focus-row"><span>当前风险</span><b>{{ selectedTask.aogLevel===1 ? '高风险' : (selectedTask.aogLevel===2 ? '重点关注' : '常规监控') }}</b></div>
              <div class="monitor-focus-text" v-if="selectedTask.aogLevel===1">保障窗口紧，需持续关注备件来源、运输衔接和需求时间前的交付余量。</div>
              <div class="monitor-focus-text" v-else>按当前保障节点推进，重点关注需求时间、下一航班及异常节点变化。</div>
            </div>

            <div class="monitor-detail-section">
              <div class="monitor-section-title">当前保障方案</div>
              <div class="monitor-plan-text">{{ selectedTask.plan }}</div>
            </div>

            <div class="monitor-detail-section progress-section">
              <div class="monitor-section-title">保障进度</div>
              <div class="monitor-progress-list">
                <div class="monitor-progress-item" v-for="n in selectedTask.checklistNodes" :key="n.name" :class="{current:n.active,done:n.done}">
                  <span class="monitor-progress-dot"></span>
                  <span class="monitor-progress-name">{{ n.name }}</span>
                  <span class="monitor-progress-state">{{ n.done?'已完成':(n.active?'进行中':'待处理') }}</span>
                </div>
              </div>
            </div>

            <button class="monitor-workbench-btn" @click="openWorkbench(selectedTask)">进入任务工作台 <span>→</span></button>
          </div>
        </aside>

        <aside class="monitor-side-panel" v-else>
          <div class="monitor-card monitor-detail-empty">
            <div class="monitor-empty-icon">AOG</div>
            <div class="monitor-empty-title">选择任务查看保障态势</div>
            <div class="monitor-empty-desc">点击左侧任务，查看当前节点、风险时限与保障进度。</div>
          </div>
        </aside>
      </div>
    </div>
  </div>

'''

s = s[:monitor_start] + monitor_html + s[monitor_end:]

# 4) 注入新版监控看板样式
css = r'''
/* ===== Monitor Dashboard v2 ===== */
.monitor-v2{display:block;height:calc(100vh - 50px);overflow:auto;background:#f4f6f9}
.monitor-shell{padding:18px 20px 24px;min-width:1080px}
.monitor-page-head{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:14px}
.monitor-page-title{font-size:20px;font-weight:700;color:#172b4d;letter-spacing:.2px}
.monitor-page-sub{font-size:11px;color:#8a98a8;margin-top:4px}
.monitor-head-status{font-size:11px;color:#65758b;display:flex;align-items:center;gap:6px}
.monitor-live-dot{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 0 4px rgba(34,197,94,.1)}
.monitor-summary{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}
.monitor-kpi{background:#fff;border:1px solid #e7ebf0;border-radius:10px;padding:14px 16px;box-shadow:0 1px 2px rgba(15,23,42,.02);position:relative;overflow:hidden}
.monitor-kpi::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:#9fb4c8}
.monitor-kpi.critical::before{background:#e85d5d}.monitor-kpi.success::before{background:#42a66d}
.monitor-kpi-top{display:flex;justify-content:space-between;align-items:center;font-size:11px;color:#718096}
.monitor-kpi-icon{font-size:9px;color:#b5c0cd;border:1px solid #edf0f3;border-radius:5px;padding:2px 5px}
.monitor-kpi-value{font-size:26px;line-height:1.1;font-weight:700;color:#173b63;margin-top:8px}
.monitor-kpi-unit{font-size:13px;margin-left:2px;color:#60758a}
.monitor-kpi-foot{font-size:10px;color:#9aa6b2;margin-top:6px}.monitor-kpi-foot b{color:#52677b;font-weight:600}
.monitor-grid{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:14px;align-items:start}
.monitor-card{background:#fff;border:1px solid #e5e9ee;border-radius:10px;box-shadow:0 1px 3px rgba(15,23,42,.03)}
.monitor-task-panel{min-width:0;overflow:hidden}
.monitor-card-head{height:62px;padding:0 16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #edf0f3}
.monitor-card-title{font-size:14px;font-weight:700;color:#233a55}.monitor-card-sub{font-size:10px;color:#9aa5b1;margin-top:3px}
.monitor-toolbar-actions{display:flex;align-items:center;gap:8px}
.monitor-segment{display:flex;background:#f4f6f8;border-radius:7px;padding:2px}
.monitor-segment button{border:0;background:transparent;color:#718096;font-size:10px;padding:5px 10px;border-radius:5px;cursor:pointer}
.monitor-segment button.active{background:#fff;color:#173b63;font-weight:600;box-shadow:0 1px 2px rgba(15,23,42,.08)}
.monitor-table-wrap{overflow:auto;padding:0 14px 14px}
.monitor-task-table{width:100%;border-collapse:separate;border-spacing:0;font-size:11px}
.monitor-task-table th{text-align:left;padding:10px 9px;color:#8c98a6;font-size:10px;font-weight:500;border-bottom:1px solid #e9edf2;white-space:nowrap;background:#fafbfc}
.monitor-task-table td{padding:10px 9px;border-bottom:1px solid #eef1f4;color:#34485e;vertical-align:middle}
.monitor-task-table tbody tr{cursor:pointer;transition:.12s}.monitor-task-table tbody tr:hover{background:#f8fbff}.monitor-task-table tbody tr.selected{background:#eef6ff}
.monitor-task-id{font-weight:700;color:#234e78;font-size:11px;white-space:nowrap}.monitor-task-fault{font-size:9px;color:#9aa5b1;margin-top:2px;max-width:150px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.monitor-primary-text{font-size:11px;font-weight:600;color:#34485e;white-space:nowrap}.monitor-secondary-text{font-size:9px;color:#9aa5b1;margin-top:2px;white-space:nowrap;max-width:160px;overflow:hidden;text-overflow:ellipsis}
.monitor-node-pill{display:inline-block;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:#f2f6fa;color:#516a82;padding:4px 7px;border-radius:6px;font-size:9px}
.monitor-status-pill{display:inline-flex;align-items:center;border-radius:10px;padding:3px 8px;font-size:9px;font-weight:600;white-space:nowrap}.monitor-status-pill.active{background:#e8f2ff;color:#2f6fb1}.monitor-status-pill.done{background:#eaf8ef;color:#288554}
.monitor-map-wrap{height:520px;padding:12px}.monitor-map-wrap #aogMap{height:100%;width:100%;border-radius:8px;overflow:hidden}
.monitor-side-panel{min-width:0}
.monitor-detail-card{padding:16px;position:sticky;top:0}
.monitor-detail-top{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;padding-bottom:13px;border-bottom:1px solid #edf0f3}
.monitor-detail-label{font-size:10px;color:#9aa5b1}.monitor-detail-id{font-size:15px;font-weight:700;color:#1f3d5b;margin-top:3px}
.monitor-detail-badges{display:flex;gap:5px;align-items:center}
.monitor-detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
.monitor-detail-item{background:#f8fafc;border:1px solid #edf0f3;border-radius:7px;padding:8px 9px;min-width:0}.monitor-detail-item label{display:block;font-size:9px;color:#9aa5b1;margin-bottom:3px}.monitor-detail-item strong{display:block;font-size:10px;color:#34485e;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.monitor-focus-card{border:1px solid #f1dfc0;background:#fffbf3;border-radius:8px;padding:10px 11px;margin-bottom:12px}.monitor-focus-card.high-risk{border-color:#f1c5c5;background:#fff7f7}
.monitor-section-title{font-size:11px;font-weight:700;color:#3d5368;margin-bottom:7px}.monitor-focus-row{display:flex;justify-content:space-between;font-size:10px;color:#7a8998}.monitor-focus-row b{color:#b26a19}.monitor-focus-card.high-risk .monitor-focus-row b{color:#c44242}.monitor-focus-text{font-size:9px;color:#8b98a6;line-height:1.55;margin-top:5px}
.monitor-detail-section{padding:11px 0;border-top:1px solid #edf0f3}.monitor-plan-text{font-size:10px;color:#66788a;line-height:1.7;background:#f8fafc;border-radius:7px;padding:8px 9px}
.monitor-progress-list{display:flex;flex-direction:column}.monitor-progress-item{display:grid;grid-template-columns:14px 1fr auto;align-items:center;gap:6px;min-height:25px;position:relative;font-size:10px;color:#738496}.monitor-progress-item::before{content:'';position:absolute;left:5px;top:17px;bottom:-8px;width:1px;background:#e4e8ed}.monitor-progress-item:last-child::before{display:none}
.monitor-progress-dot{width:10px;height:10px;border-radius:50%;background:#d5dce4;border:2px solid #fff;box-shadow:0 0 0 1px #d5dce4;z-index:1}.monitor-progress-item.done .monitor-progress-dot{background:#42a66d;box-shadow:0 0 0 1px #42a66d}.monitor-progress-item.current .monitor-progress-dot{background:#3b82c4;box-shadow:0 0 0 3px rgba(59,130,196,.12)}
.monitor-progress-item.current .monitor-progress-name{font-weight:700;color:#286da8}.monitor-progress-state{font-size:9px;color:#a0aab5}.monitor-progress-item.current .monitor-progress-state{color:#3b82c4}.monitor-progress-item.done .monitor-progress-state{color:#42a66d}
.monitor-workbench-btn{width:100%;height:36px;border:0;border-radius:7px;background:#1d466d;color:#fff;font-size:11px;font-weight:600;cursor:pointer;margin-top:4px}.monitor-workbench-btn:hover{background:#173b5d}.monitor-workbench-btn span{margin-left:5px}
.monitor-detail-empty{height:310px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:30px}.monitor-empty-icon{width:46px;height:46px;border-radius:50%;background:#eef4fa;color:#6d88a2;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;margin-bottom:12px}.monitor-empty-title{font-size:12px;font-weight:700;color:#4c6074}.monitor-empty-desc{font-size:10px;color:#9aa5b1;line-height:1.6;margin-top:5px;max-width:230px}
@media(max-width:1280px){.monitor-grid{grid-template-columns:minmax(0,1fr) 320px}.monitor-shell{min-width:1020px}.monitor-summary{gap:9px}.monitor-kpi{padding:12px 13px}}
'''
s = s.replace('</style>', css + '\n</style>', 1)

p.write_text(s, encoding='utf-8')
print('monitor redesign applied', len(s))
