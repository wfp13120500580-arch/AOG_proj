from pathlib import Path
import re

p = Path('index_v3.0_minimal.html')
s = p.read_text(encoding='utf-8')

# -------------------- Monitor: true big-screen --------------------
monitor_start = s.find('  <!-- ==================== 监控看板 ==================== -->')
workbench_start = s.find('  <!-- ==================== 任务工作台 v2 ==================== -->', monitor_start)
if monitor_start < 0 or workbench_start < 0:
    raise SystemExit('monitor/workbench marker not found')

monitor_html = r'''  <!-- ==================== 监控看板 ==================== -->
  <div class="screen-monitor" v-if="activeTab==='monitor'">
    <div class="screen-map" id="aogMap"></div>
    <div class="screen-shade"></div>

    <div class="screen-head">
      <div>
        <div class="screen-title">AOG全球保障态势</div>
        <div class="screen-subtitle">GLOBAL AOG SUPPORT SITUATION</div>
      </div>
      <div class="screen-head-kpis">
        <div class="screen-kpi"><span>进行中</span><b>{{ tasksActive }}</b></div>
        <div class="screen-kpi urgent"><span>紧急</span><b>{{ tasksUrgent }}</b></div>
        <div class="screen-kpi"><span>本月完成</span><b>47</b></div>
        <div class="screen-kpi"><span>平均响应</span><b>4.2h</b></div>
      </div>
      <div class="screen-live"><i></i> 实时监控</div>
    </div>

    <div class="screen-panel screen-left">
      <div class="screen-panel-title"><span>在途 AOG 任务</span><em>{{ tasksActive }} ACTIVE</em></div>
      <div class="screen-task-list">
        <div class="screen-task-item" v-for="t in mockTasks.filter(x=>x.status==='进行中')" :key="t.id" :class="{selected:selectedTask===t,urgent:t.aogLevel===1}" @click="selectTask(t)">
          <div class="screen-task-line1"><b>{{ t.id }}</b><span>Lv{{ t.aogLevel }}</span></div>
          <div class="screen-task-line2"><strong>{{ t.airportCN }} · {{ t.iataCode }}</strong><em>{{ t.reg }}</em></div>
          <div class="screen-task-node">{{ t.currentNode }}</div>
        </div>
      </div>
    </div>

    <div class="screen-panel screen-right" v-if="selectedTask">
      <div class="screen-panel-title"><span>当前任务态势</span><em>{{ selectedTask.id }}</em></div>
      <div class="screen-current-top">
        <div><label>AOG等级</label><strong>Lv{{ selectedTask.aogLevel }}</strong></div>
        <div><label>保障地点</label><strong>{{ selectedTask.iataCode }}</strong></div>
        <div><label>需求时间</label><strong>{{ selectedTask.neededBy }}</strong></div>
      </div>
      <div class="screen-current-section">
        <label>当前节点</label>
        <div class="screen-node-highlight">{{ selectedTask.currentNode }}</div>
      </div>
      <div class="screen-current-section">
        <label>当前保障方案</label>
        <p>{{ selectedTask.plan }}</p>
      </div>
      <div class="screen-current-section">
        <label>保障进度</label>
        <div class="screen-mini-progress">
          <span v-for="n in selectedTask.checklistNodes" :key="n.name" :class="{done:n.done,current:n.active}" :title="n.name"></span>
        </div>
      </div>
      <button class="screen-enter-btn" @click="openWorkbench(selectedTask)">进入任务工作台 →</button>
    </div>

    <div class="screen-bottom">
      <div class="screen-bottom-card">
        <span class="screen-bottom-label">高风险任务</span>
        <b>{{ mockTasks.filter(t=>t.status==='进行中'&&t.aogLevel===1).length }}</b>
        <small>需持续关注保障窗口</small>
      </div>
      <div class="screen-bottom-card wide">
        <span class="screen-bottom-label">当前重点</span>
        <b class="screen-bottom-text">{{ selectedTask ? selectedTask.currentNode : '请选择任务' }}</b>
        <small>{{ selectedTask ? selectedTask.airportCN + ' · ' + selectedTask.faultType : '点击地图或左侧任务查看详情' }}</small>
      </div>
      <div class="screen-bottom-card">
        <span class="screen-bottom-label">保障成功率</span>
        <b>96%</b>
        <small>本月已完成 47 单</small>
      </div>
    </div>
  </div>

'''
s = s[:monitor_start] + monitor_html + s[workbench_start:]

# -------------------- Workbench: left task list + circle flow --------------------
wb_start = s.find('  <!-- ==================== 任务工作台 v2 ==================== -->')
knowledge_start = s.find('  <!-- ==================== 知识管理 ==================== -->', wb_start)
if wb_start < 0 or knowledge_start < 0:
    raise SystemExit('workbench/knowledge marker not found')

workbench_html = r'''  <!-- ==================== 任务工作台 v2 ==================== -->
  <div class="wb-layout-v3" v-if="activeTab==='workbench'">
    <!-- 左侧：任务列表切换 -->
    <aside class="wb-task-sidebar">
      <div class="wb-side-head">
        <div class="wb-side-title">AOG任务</div>
        <div class="wb-side-count">{{ mockTasks.length }} 个任务</div>
      </div>
      <div class="wb-side-list">
        <div class="wb-side-item" v-for="t in mockTasks" :key="t.id" :class="{active:wbTask&&wbTask.id===t.id,urgent:t.aogLevel===1}" @click="wbSelectedTaskId=t.id;onWbTaskChange(t.id)">
          <div class="wb-side-row"><b>{{ t.id }}</b><span class="wb-side-lv">Lv{{ t.aogLevel }}</span></div>
          <div class="wb-side-fault">{{ t.faultType }}</div>
          <div class="wb-side-meta"><span>{{ t.airportCN }} · {{ t.iataCode }}</span><em>{{ t.status }}</em></div>
          <div class="wb-side-node">{{ t.currentNode }}</div>
        </div>
      </div>
    </aside>

    <template v-if="wbTask">
      <!-- 中间：流程、明细、地图 -->
      <main class="wb-center-v3">
        <div class="wb-task-bar">
          <div class="wb-task-main-v3">
            <strong>{{ wbTask.id }} · {{ wbTask.reg }}</strong>
            <span>{{ wbTask.faultType }} · {{ wbTask.partNo }}</span>
          </div>
          <div class="wb-task-facts">
            <div><label>AOG等级</label><b>Lv{{ wbTask.aogLevel }}</b></div>
            <div><label>AOG地点</label><b>{{ wbTask.airportCN }}（{{ wbTask.iataCode }}）</b></div>
            <div><label>需求时间</label><b>{{ wbTask.neededBy }}</b></div>
            <div><label>下个航班</label><b>{{ formatNextFlight(wbTask.nextFlight) }}</b></div>
          </div>
        </div>

        <!-- 五阶段：仅圆形节点 + 连线 -->
        <div class="phase-circle-flow">
          <div class="phase-circle-unit" v-for="(p,pi) in wbPhases" :key="p.id">
            <div class="phase-circle-wrap" @click="selectPhase(p.id)">
              <div class="phase-circle" :class="{active:wbActivePhaseId===p.id,done:wbPhaseAllDone(p),partial:wbPhaseDoneCnt(p)>0&&!wbPhaseAllDone(p)}">
                <span v-if="wbPhaseAllDone(p)">✓</span><span v-else>{{ pi+1 }}</span>
              </div>
              <div class="phase-circle-title" :class="{active:wbActivePhaseId===p.id}">{{ p.title }}</div>
              <div class="phase-circle-count">{{ wbPhaseDoneCnt(p) }}/{{ p.nodes.length }}</div>
            </div>
            <div class="phase-circle-line" v-if="pi<wbPhases.length-1" :class="{done:wbPhaseAllDone(p)}"></div>
          </div>
        </div>

        <div class="wb-final-plan" :class="{ready:spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id}">
          <div class="wb-plan-left">
            <div class="wb-plan-title">最终保障方案 <span>{{ spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id ? '已生成' : '待生成' }}</span></div>
            <div class="wb-plan-desc" v-if="spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id&&spReport.schemes&&spReport.schemes.length">{{ spReport.schemes[0].name }} · {{ spReport.schemes[0].transport }} · ETA {{ spReport.schemes[0].eta }}</div>
            <div class="wb-plan-desc" v-else>询件、运输方案及合同确认完成后生成，作为运输监控执行基准。</div>
          </div>
          <button @click="openSupportPlanDialog">{{ spGenerated&&spReport.basic&&spReport.basic.id===wbTask.id ? '查看方案' : '生成方案' }}</button>
        </div>

        <div class="wb-stage-panel" v-if="activePhase">
          <div class="wb-stage-head">
            <div><strong>{{ activePhase.title }}</strong><span>当前环节</span></div>
            <em>{{ wbPhaseDoneCnt(activePhase) }}/{{ activePhase.nodes.length }} 完成</em>
          </div>
          <div class="wb-node-list">
            <div class="wb-node-row" v-for="node in activePhase.nodes" :key="node.id" :class="{done:wbDoneNodes.has(node.id),skip:wbSkippedNodes.has(node.id)}">
              <div class="wb-node-status-dot"></div>
              <div class="wb-node-content">
                <div class="wb-node-title"><span>{{ node.id }}</span><strong>{{ node.title }}</strong></div>
                <div class="wb-node-desc">{{ node.desc }}</div>
              </div>
              <div class="wb-node-actions">
                <span>{{ wbDoneNodes.has(node.id)?'已完成':(wbSkippedNodes.has(node.id)?'已跳过':'待处理') }}</span>
                <button v-if="!wbDoneNodes.has(node.id)" @click="markNodeDone(node.id)">完成</button>
                <button v-if="!wbDoneNodes.has(node.id)&&!wbSkippedNodes.has(node.id)" class="skip" @click="markNodeSkip(node.id)">跳过</button>
              </div>
            </div>
          </div>
        </div>

        <div class="wb-map-v3" id="recMap"></div>
      </main>

      <!-- 右侧：Agent -->
      <aside class="wb-agent-v3">
        <div class="agent-chat-panel">
          <div class="agent-chat-header">保障 Agent <span class="agent-status-badge">已启用</span></div>
          <div class="agent-chat-messages" ref="agentChatScroll">
            <div v-for="(m,i) in agentChatMessages" :key="i" class="msg" :class="[m.role,m.streaming?'streaming':'']"><div class="msg-content" v-html="m.html||m.content"></div></div>
            <div v-if="agentChatMessages.length===0" class="wb-agent-empty">向保障 Agent 发送指令</div>
          </div>
          <div class="agent-chat-input"><input v-model="agentChatInput" placeholder="输入指令，例如：更新运输方式、ETA、支援方..." @keyup.enter="sendAgentMessage" :disabled="agentChatLoading"><button @click="sendAgentMessage" :disabled="agentChatLoading||!agentChatInput.trim()">{{ agentChatLoading?'...':'发送' }}</button></div>
        </div>
      </aside>
    </template>

    <div class="wb-no-task" v-else>请从左侧选择一个 AOG 保障任务</div>
  </div>
'''
s = s[:wb_start] + workbench_html + '\n' + s[knowledge_start:]

# -------------------- CSS --------------------
css = r'''
/* ===== AOG Big Screen ===== */
.screen-monitor{height:calc(100vh - 50px);position:relative;overflow:hidden;background:#071421;color:#dbeafe}
.screen-map{position:absolute;inset:0;z-index:0}.screen-map.leaflet-container{background:#071421}
.screen-shade{position:absolute;inset:0;z-index:400;pointer-events:none;background:linear-gradient(90deg,rgba(4,16,29,.78) 0%,rgba(4,16,29,.18) 25%,rgba(4,16,29,.05) 50%,rgba(4,16,29,.22) 76%,rgba(4,16,29,.82) 100%),linear-gradient(180deg,rgba(4,16,29,.78) 0%,rgba(4,16,29,0) 20%,rgba(4,16,29,.45) 100%)}
.screen-head{position:absolute;z-index:500;left:20px;right:20px;top:16px;height:76px;display:flex;align-items:center;gap:28px;padding:0 20px;background:linear-gradient(90deg,rgba(7,25,43,.94),rgba(7,25,43,.72),rgba(7,25,43,.9));border:1px solid rgba(92,172,238,.28);box-shadow:0 10px 30px rgba(0,0,0,.18);backdrop-filter:blur(8px)}
.screen-title{font-size:22px;font-weight:700;color:#f4f9ff;letter-spacing:2px}.screen-subtitle{font-size:9px;color:#5ea7dc;letter-spacing:2px;margin-top:4px}
.screen-head-kpis{display:flex;gap:8px;flex:1;justify-content:center}.screen-kpi{min-width:105px;padding:8px 13px;border-left:1px solid rgba(95,166,218,.22)}.screen-kpi span{display:block;font-size:9px;color:#7fa5c2}.screen-kpi b{display:block;font-size:19px;color:#eaf6ff;margin-top:2px}.screen-kpi.urgent b{color:#ff867e}
.screen-live{font-size:10px;color:#9bc5df;display:flex;align-items:center;gap:7px}.screen-live i{width:7px;height:7px;border-radius:50%;background:#38d98b;box-shadow:0 0 10px #38d98b}
.screen-panel{position:absolute;z-index:500;top:108px;bottom:112px;width:275px;background:rgba(5,22,38,.88);border:1px solid rgba(81,158,217,.28);backdrop-filter:blur(7px);box-shadow:0 12px 30px rgba(0,0,0,.16)}.screen-left{left:20px}.screen-right{right:20px}
.screen-panel-title{height:44px;padding:0 13px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(83,152,203,.2);font-size:12px;font-weight:700;color:#e6f5ff}.screen-panel-title em{font-style:normal;font-size:8px;color:#5fa8db;font-weight:500}
.screen-task-list{padding:8px;overflow:auto;height:calc(100% - 44px)}.screen-task-item{padding:10px;border:1px solid rgba(79,142,188,.16);background:rgba(17,46,69,.55);margin-bottom:7px;cursor:pointer;transition:.15s}.screen-task-item:hover,.screen-task-item.selected{border-color:#4aa9e9;background:rgba(28,78,113,.72)}.screen-task-item.urgent{border-left:3px solid #f46e6e}
.screen-task-line1,.screen-task-line2{display:flex;justify-content:space-between;gap:8px;align-items:center}.screen-task-line1 b{font-size:10px;color:#d9efff}.screen-task-line1 span{font-size:9px;color:#ff9c92}.screen-task-line2{margin-top:5px}.screen-task-line2 strong{font-size:10px;color:#9fd2f1}.screen-task-line2 em{font-size:9px;color:#698ba5;font-style:normal}.screen-task-node{margin-top:7px;font-size:9px;color:#8caabd;padding-top:6px;border-top:1px dashed rgba(110,169,207,.16)}
.screen-current-top{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;padding:10px}.screen-current-top div{background:rgba(28,62,86,.65);padding:7px}.screen-current-top label,.screen-current-section label{display:block;font-size:8px;color:#7395ad;margin-bottom:4px}.screen-current-top strong{font-size:10px;color:#e4f4ff}.screen-current-section{padding:9px 11px;border-top:1px solid rgba(84,146,190,.16)}.screen-current-section p{font-size:9px;color:#abc4d5;line-height:1.65}.screen-node-highlight{font-size:11px;font-weight:700;color:#67c4ff;padding:7px 8px;background:rgba(42,114,162,.2);border-left:2px solid #55b9fa}.screen-mini-progress{display:flex;gap:5px}.screen-mini-progress span{height:5px;flex:1;background:#29475d}.screen-mini-progress span.done{background:#3dc587}.screen-mini-progress span.current{background:#5fbaff;box-shadow:0 0 7px rgba(95,186,255,.6)}.screen-enter-btn{position:absolute;left:10px;right:10px;bottom:10px;height:34px;background:#17689b;border:1px solid #42a8e5;color:#fff;font-size:10px;cursor:pointer}
.screen-bottom{position:absolute;z-index:500;left:315px;right:315px;bottom:18px;height:76px;display:grid;grid-template-columns:180px 1fr 180px;gap:10px}.screen-bottom-card{background:rgba(5,22,38,.9);border:1px solid rgba(80,155,210,.27);padding:11px 13px;backdrop-filter:blur(6px)}.screen-bottom-label{display:block;font-size:8px;color:#6f99b6}.screen-bottom-card b{display:block;font-size:17px;color:#e9f6ff;margin-top:4px}.screen-bottom-card small{display:block;font-size:8px;color:#6d8ca2;margin-top:3px}.screen-bottom-card .screen-bottom-text{font-size:12px;color:#68c5ff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

/* ===== Workbench v3 ===== */
.wb-layout-v3{height:calc(100vh - 50px);display:grid;grid-template-columns:250px minmax(0,1fr) 350px;background:#eef2f6;overflow:hidden}
.wb-task-sidebar{background:#f8fafc;border-right:1px solid #dfe5eb;display:flex;flex-direction:column;min-width:0}.wb-side-head{height:56px;padding:0 14px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #e2e7ec}.wb-side-title{font-size:14px;font-weight:700;color:#223f5c}.wb-side-count{font-size:9px;color:#91a0ad}.wb-side-list{flex:1;overflow:auto;padding:8px}.wb-side-item{background:#fff;border:1px solid #e5e9ee;border-radius:7px;padding:10px;margin-bottom:7px;cursor:pointer;transition:.15s}.wb-side-item:hover{border-color:#b6d4ec}.wb-side-item.active{border-color:#4a9ed8;background:#eef7ff;box-shadow:inset 3px 0 0 #378fca}.wb-side-item.urgent:not(.active){border-left:3px solid #ec7373}.wb-side-row{display:flex;justify-content:space-between;gap:6px}.wb-side-row b{font-size:10px;color:#2f506e}.wb-side-lv{font-size:9px;color:#b65b5b}.wb-side-fault{font-size:9px;color:#7e8e9d;margin-top:5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wb-side-meta{display:flex;justify-content:space-between;font-size:8px;color:#9aa6b1;margin-top:7px}.wb-side-meta em{font-style:normal;color:#4f88b4}.wb-side-node{font-size:8px;color:#66849c;margin-top:6px;padding-top:6px;border-top:1px dashed #edf0f3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wb-center-v3{min-width:0;display:flex;flex-direction:column;overflow:hidden;padding:10px;gap:9px}.wb-task-bar{background:linear-gradient(135deg,#143c60,#285e86);border-radius:8px;color:#fff;padding:10px 13px;display:flex;align-items:center;gap:20px;flex:none}.wb-task-main-v3{width:220px;min-width:0}.wb-task-main-v3 strong{display:block;font-size:12px}.wb-task-main-v3 span{display:block;font-size:9px;color:rgba(255,255,255,.62);margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wb-task-facts{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;flex:1}.wb-task-facts label{display:block;font-size:8px;color:rgba(255,255,255,.55)}.wb-task-facts b{display:block;font-size:10px;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.phase-circle-flow{height:78px;background:#fff;border:1px solid #e2e7ec;border-radius:8px;display:flex;align-items:flex-start;padding:10px 24px 7px;flex:none}.phase-circle-unit{display:flex;align-items:flex-start;flex:1;position:relative}.phase-circle-wrap{width:72px;text-align:center;cursor:pointer;position:relative;z-index:2}.phase-circle{width:28px;height:28px;border-radius:50%;margin:0 auto;border:2px solid #cbd5df;background:#fff;color:#8a98a5;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;transition:.15s}.phase-circle:hover{border-color:#6faed9}.phase-circle.active{border-color:#2f8fce;background:#2f8fce;color:#fff;box-shadow:0 0 0 5px rgba(47,143,206,.1)}.phase-circle.done{border-color:#42a66d;background:#42a66d;color:#fff}.phase-circle.partial:not(.active){border-color:#e1a64e;color:#bf7a16}.phase-circle-title{font-size:9px;color:#65788a;margin-top:6px;white-space:nowrap}.phase-circle-title.active{color:#247ab4;font-weight:700}.phase-circle-count{font-size:8px;color:#a2adb7;margin-top:1px}.phase-circle-line{height:2px;background:#dfe5eb;flex:1;margin-top:13px;margin-left:-5px;margin-right:-5px}.phase-circle-line.done{background:#79bd91}
.wb-final-plan{min-height:56px;background:#fff;border:1px solid #e2e7ec;border-radius:8px;padding:9px 12px;display:flex;justify-content:space-between;align-items:center;gap:12px;flex:none}.wb-final-plan.ready{border-color:#b9dfc5;background:#fbfffc}.wb-plan-title{font-size:11px;font-weight:700;color:#2b465f}.wb-plan-title span{font-size:8px;font-weight:500;margin-left:6px;color:#8996a3;background:#f1f4f7;border-radius:8px;padding:2px 6px}.wb-final-plan.ready .wb-plan-title span{background:#e4f7ea;color:#318458}.wb-plan-desc{font-size:9px;color:#8493a0;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.wb-plan-left{min-width:0}.wb-final-plan button{border:1px solid #8dc1e4;background:#eef8ff;color:#247bb5;border-radius:5px;padding:6px 10px;font-size:9px;cursor:pointer;white-space:nowrap}
.wb-stage-panel{background:#fff;border:1px solid #e2e7ec;border-radius:8px;display:flex;flex-direction:column;min-height:0;flex:1;overflow:hidden}.wb-stage-head{height:44px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;border-bottom:1px solid #edf0f3;flex:none}.wb-stage-head strong{font-size:12px;color:#2d4b66}.wb-stage-head span{font-size:8px;color:#2d83bd;background:#eaf5fc;padding:2px 6px;border-radius:8px;margin-left:6px}.wb-stage-head em{font-size:9px;color:#99a4ae;font-style:normal}.wb-node-list{overflow:auto;padding:8px}.wb-node-row{display:grid;grid-template-columns:12px 1fr auto;gap:8px;align-items:start;padding:9px;border-bottom:1px solid #eff2f5}.wb-node-row:last-child{border-bottom:0}.wb-node-status-dot{width:7px;height:7px;border-radius:50%;background:#cdd5dc;margin-top:4px}.wb-node-row.done .wb-node-status-dot{background:#42a66d}.wb-node-row.skip .wb-node-status-dot{background:#e4a13d}.wb-node-title{display:flex;gap:6px;align-items:center}.wb-node-title span{font-size:8px;color:#9aa6b0}.wb-node-title strong{font-size:10px;color:#324b60}.wb-node-desc{font-size:9px;color:#83919e;line-height:1.55;margin-top:4px}.wb-node-actions{display:flex;align-items:center;gap:5px}.wb-node-actions>span{font-size:8px;color:#9aa6b0}.wb-node-actions button{border:0;background:#eef5fa;color:#347eae;font-size:8px;padding:4px 7px;border-radius:4px;cursor:pointer}.wb-node-actions button.skip{background:#fff7e8;color:#bc7b1d}
.wb-map-v3{height:190px;border-radius:8px;overflow:hidden;border:1px solid #e2e7ec;flex:none}.wb-map-v3.leaflet-container{width:100%}
.wb-agent-v3{padding:10px 10px 10px 0;min-width:0}.wb-agent-v3 .agent-chat-panel{height:100%;border-radius:8px;border:1px solid #e1e6eb;overflow:hidden;background:#fff}.wb-agent-empty{text-align:center;color:#b6c0c9;padding:30px 0;font-size:10px}.wb-no-task{grid-column:2/4;display:flex;align-items:center;justify-content:center;color:#a1acb6;font-size:12px}
@media(max-width:1280px){.wb-layout-v3{grid-template-columns:220px minmax(0,1fr) 310px}.wb-task-main-v3{width:180px}.wb-task-facts{gap:7px}.screen-panel{width:245px}.screen-bottom{left:265px;right:265px}}
'''
s = s.replace('</style>', css + '\n</style>', 1)

# Monitor map must render immediately.
s = s.replace("const viewMode = ref('list');", "const viewMode = ref('map');", 1)
old_mount = "onMounted(() => { recalcAogLevels(); checkChatConfig(); });"
new_mount = "onMounted(() => { recalcAogLevels(); checkChatConfig(); nextTick(() => initMapIfNeeded()); });"
if old_mount in s:
    s = s.replace(old_mount, new_mount, 1)

# Workbench: selecting a task should default to first phase so the flow is immediately readable.
needle = "wbTask.value = mockTasks.value.find(t => t.id === taskId) || null;\n      wbActivePhaseId.value = null;"
if needle in s:
    s = s.replace(needle, "wbTask.value = mockTasks.value.find(t => t.id === taskId) || null;\n      wbActivePhaseId.value = 1;", 1)

p.write_text(s, encoding='utf-8')
print('layout v3 applied', len(s))
