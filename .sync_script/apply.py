from pathlib import Path
import hashlib

path = Path('index_v3.0_minimal.html')
expected_before = '26e4c70755de503537487f9202ce9ff15d2aa77231b89eb74e0b73b71d9bafad'
raw = path.read_bytes()
actual_before = hashlib.sha256(raw).hexdigest()
if actual_before != expected_before:
    raise SystemExit(f'Refusing to patch unexpected source: {actual_before}')
text = raw.decode('utf-8').replace('\r\n','\n')

css = r'''
/* ===== AOG 五阶段工作台布局覆盖 ===== */
.workbench{display:flex;gap:12px;height:calc(100vh - 106px);padding:10px 16px}
.rec-panel{flex:1;min-width:0;background:#fff;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.06);display:flex;flex-direction:column;overflow:hidden}
.rec-top{flex:1;overflow-y:auto;padding:12px 14px 14px}
.rec-map{height:238px;flex:none;position:relative;border-top:1px solid #e4e7ed;min-height:220px}
.right-panel{width:390px;flex-shrink:0;display:flex;flex-direction:column;overflow:hidden}
.agent-chat-panel{flex:1;min-height:0}
.wb-task-strip{display:flex;align-items:center;gap:18px;padding:9px 12px;background:linear-gradient(135deg,#0f2942,#244f76);color:#fff;border-radius:8px;margin-bottom:12px;overflow:hidden}
.wb-task-main{min-width:170px}.wb-task-id{font-size:13px;font-weight:700}.wb-task-fault{font-size:10px;color:rgba(255,255,255,.68);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px}
.wb-task-meta{display:flex;gap:18px;flex:1;min-width:0}.wb-task-meta-item{display:flex;flex-direction:column;gap:1px;min-width:72px}.wb-task-meta-item label{font-size:9px;color:rgba(255,255,255,.55)}.wb-task-meta-item span{font-size:11px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.phase-flow{display:flex;align-items:stretch;margin-bottom:12px;background:#f8fafc;border:1px solid #e7edf4;border-radius:8px;padding:8px 10px}.phase-flow-item{display:flex;align-items:center;flex:1;min-width:0}
.phase-step{display:flex;align-items:center;gap:7px;flex:1;min-width:0;padding:7px 8px;border-radius:6px;cursor:pointer;transition:all .15s}.phase-step:hover{background:#eef5ff}.phase-step.active{background:#eaf3ff;box-shadow:inset 0 0 0 1px #b8d5ff}.phase-step.done{background:#f0fdf4}.phase-step.partial:not(.active){background:#fffaf0}
.phase-step-index{width:22px;height:22px;border-radius:50%;background:#e5e7eb;color:#64748b;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0}.phase-step.active .phase-step-index{background:#1d4ed8;color:#fff}.phase-step.done .phase-step-index{background:#16a34a;color:#fff}.phase-step-copy{min-width:0}.phase-step-title{font-size:11px;font-weight:700;color:#334155;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.phase-step-progress{font-size:9px;color:#94a3b8;margin-top:1px}.phase-connector{width:18px;height:2px;background:#d8e0e8;flex-shrink:0}.phase-connector.done{background:#86c99b}
.final-plan-card{border:1px solid #dbe7f3;border-radius:8px;background:#fbfdff;margin-bottom:12px;overflow:hidden}.final-plan-card.ready{border-color:#b7dfc5;background:#fbfffc}.final-plan-head{display:flex;align-items:center;justify-content:space-between;padding:8px 10px;border-bottom:1px solid #edf2f7}.final-plan-title{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:700;color:#1f3c56}.final-plan-status{font-size:9px;padding:2px 7px;border-radius:8px;background:#f1f5f9;color:#64748b}.final-plan-status.ready{background:#dcfce7;color:#166534}.final-plan-body{padding:9px 10px}.final-plan-empty{display:flex;align-items:center;justify-content:space-between;gap:12px;color:#64748b;font-size:11px;line-height:1.5}.final-plan-grid{display:grid;grid-template-columns:1.1fr .9fr .9fr .9fr;gap:8px}.final-plan-item{background:#fff;border:1px solid #edf2f7;border-radius:6px;padding:6px 8px;min-width:0}.final-plan-item label{display:block;font-size:9px;color:#94a3b8;margin-bottom:2px}.final-plan-item strong{display:block;font-size:11px;color:#334155;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.final-plan-decision{font-size:10px;color:#64748b;line-height:1.5;margin-top:7px;padding-top:7px;border-top:1px dashed #e5e7eb}
.phase-head-main{display:flex;align-items:center;gap:8px}.phase-head-tag{font-size:9px;color:#1d4ed8;background:#dbeafe;padding:2px 6px;border-radius:8px}.task-card-status{font-size:9px;font-weight:600;padding:2px 7px;border-radius:8px;background:#f1f5f9;color:#64748b}.task-card-status.done{background:#dcfce7;color:#166534}.task-card-status.skip{background:#fff7ed;color:#9a3412}.task-card-desc{font-size:11px;color:#64748b;line-height:1.55;padding-top:2px}
@media(max-width:1180px){.right-panel{width:330px}.wb-task-meta{gap:10px}.final-plan-grid{grid-template-columns:1fr 1fr}}
'''
text = text.replace('</style>', css + '\n</style>', 1)

start = text.index('    <div class="workbench" v-if="wbTask">')
end = text.index('    <div v-else style="text-align:center;padding:60px;color:#c0c4cc">', start)
workbench = r'''    <div class="workbench" v-if="wbTask">
      <!-- 中间主区：五阶段流程 + 最终保障方案 + 小环节明细 + 地图 -->
      <div class="rec-panel" v-if="activePhase">
        <div class="rec-top">
          <div class="wb-task-strip">
            <div class="wb-task-main">
              <div class="wb-task-id">{{ wbTask.id }} · {{ wbTask.reg }}</div>
              <div class="wb-task-fault">{{ wbTask.faultType }} · {{ wbTask.partNo }}</div>
            </div>
            <div class="wb-task-meta">
              <div class="wb-task-meta-item"><label>AOG等级</label><span>Lv{{ wbTask.aogLevel }}</span></div>
              <div class="wb-task-meta-item"><label>AOG地点</label><span>{{ wbTask.airportCN }}（{{ wbTask.iataCode }}）</span></div>
              <div class="wb-task-meta-item"><label>需求时间</label><span>{{ wbTask.neededBy }}</span></div>
              <div class="wb-task-meta-item"><label>下个航班</label><span>{{ formatNextFlight(wbTask.nextFlight) }}</span></div>
            </div>
          </div>

          <div class="phase-flow">
            <div class="phase-flow-item" v-for="(p,pi) in wbPhases" :key="p.id">
              <div class="phase-step" :class="{active:wbActivePhaseId===p.id,done:wbPhaseAllDone(p),partial:wbPhaseDoneCnt(p)>0&&!wbPhaseAllDone(p)}" @click="selectPhase(p.id)">
                <span class="phase-step-index">{{ wbPhaseAllDone(p) ? '✓' : (pi+1) }}</span>
                <div class="phase-step-copy">
                  <div class="phase-step-title">{{ p.title }}</div>
                  <div class="phase-step-progress">{{ wbPhaseDoneCnt(p) }}/{{ p.nodes.length }} 已完成</div>
                </div>
              </div>
              <div v-if="pi < wbPhases.length-1" class="phase-connector" :class="{done:wbPhaseAllDone(p)}"></div>
            </div>
          </div>

          <div class="final-plan-card" :class="{ready:spGenerated && spReport.basic && spReport.basic.id===wbTask.id}">
            <div class="final-plan-head">
              <div class="final-plan-title"><span>最终保障方案</span><span class="final-plan-status" :class="{ready:spGenerated && spReport.basic && spReport.basic.id===wbTask.id}">{{ spGenerated && spReport.basic && spReport.basic.id===wbTask.id ? '已生成' : '待生成' }}</span></div>
              <el-button size="small" type="primary" plain @click="openSupportPlanDialog">{{ spGenerated && spReport.basic && spReport.basic.id===wbTask.id ? '查看完整方案' : '生成保障方案' }}</el-button>
            </div>
            <div class="final-plan-body">
              <template v-if="spGenerated && spReport.basic && spReport.basic.id===wbTask.id && spReport.schemes && spReport.schemes.length">
                <div class="final-plan-grid">
                  <div class="final-plan-item"><label>主方案</label><strong>{{ spReport.schemes[0].name }}</strong></div>
                  <div class="final-plan-item"><label>保障方式</label><strong>{{ spReport.schemes[0].method }}</strong></div>
                  <div class="final-plan-item"><label>运输方式</label><strong>{{ spReport.schemes[0].transport }}</strong></div>
                  <div class="final-plan-item"><label>预计到达</label><strong>{{ spReport.schemes[0].eta }}</strong></div>
                </div>
                <div class="final-plan-decision">{{ spReport.decision }}</div>
              </template>
              <div class="final-plan-empty" v-else><span>询件结果、运输信息和合同确认会持续汇总到这里；方案确认后作为运输监控的执行基准。</span><span style="white-space:nowrap;color:#94a3b8">建议在“运输方案”完成后生成</span></div>
            </div>
          </div>

          <div class="phase-head"><div class="phase-head-main"><h3>{{ activePhase.title }}</h3><span class="phase-head-tag">当前环节</span></div><span style="font-size:11px;color:#909399">{{ wbPhaseDoneCnt(activePhase) }}/{{ activePhase.nodes.length }} 项完成</span></div>
          <div class="task-card" v-for="node in activePhase.nodes" :key="node.id" :class="{card_done:wbDoneNodes.has(node.id), card_skip:wbSkippedNodes.has(node.id)}">
            <div class="task-card-header">
              <div class="task-card-title"><span class="task-card-dot" :class="wbDoneNodes.has(node.id)?'done':'pending'"></span><span style="font-size:10px;color:#909399">{{ node.id }}</span><span>{{ node.title }}</span></div>
              <div class="task-card-actions"><span class="task-card-status" :class="{done:wbDoneNodes.has(node.id),skip:wbSkippedNodes.has(node.id)}">{{ wbDoneNodes.has(node.id)?'已完成':(wbSkippedNodes.has(node.id)?'已跳过':'待处理') }}</span><el-button size="small" text @click="markNodeDone(node.id)" v-if="!wbDoneNodes.has(node.id)">完成</el-button><el-button size="small" text type="warning" @click="markNodeSkip(node.id)" v-if="!wbDoneNodes.has(node.id) && !wbSkippedNodes.has(node.id)">跳过</el-button></div>
            </div>
            <div class="task-card-body"><div class="task-card-desc">{{ node.desc }}</div></div>
          </div>
        </div>
        <div class="rec-map" id="recMap"></div>
      </div>

      <!-- 右侧只保留 Agent 对话 -->
      <div class="right-panel">
        <div class="agent-chat-panel">
          <div class="agent-chat-header">保障 Agent <span class="agent-status-badge">已启用</span></div>
          <div class="agent-chat-messages" ref="agentChatScroll">
            <div v-for="(m,i) in agentChatMessages" class="msg" :class="[m.role, m.streaming?'streaming':'']"><div class="msg-content" v-html="m.html||m.content"></div></div>
            <div v-if="agentChatMessages.length===0" style="text-align:center;color:#c0c4cc;padding:30px 0;font-size:11px">向保障 Agent 发送指令</div>
          </div>
          <div class="agent-chat-input"><input v-model="agentChatInput" placeholder="输入指令，例如：更新运输方式、ETA、支援方..." @keyup.enter="sendAgentMessage" :disabled="agentChatLoading"><button @click="sendAgentMessage" :disabled="agentChatLoading || !agentChatInput.trim()">{{ agentChatLoading ? '...' : '发送' }}</button></div>
        </div>
      </div>
    </div>
'''
text = text[:start] + workbench + text[end:]

cs = text.index('    const BUILTIN_CHECKLIST = [')
ce = text.index('    function openWorkbench(task)', cs)
checklist = r'''    const BUILTIN_CHECKLIST = [
      {id:1,title:'询件',_exp:true,nodes:[
        {id:'1.1',title:'核对询件需求',type:'manual',desc:'核对需求件号、数量、需求地点、需求时间、下次起飞时间及AOG等级，确保询件信息完整。'},
        {id:'1.2',title:'多渠道发起询件',type:'manual',desc:'向当地航司、KLM、汉莎、IATP、OEM等适用渠道同步发起AOG询件。'},
        {id:'1.3',title:'跟踪询件回复',type:'manual',desc:'持续跟踪各渠道可供数量、放件时效、价格及取件条件。'},
        {id:'1.4',title:'证书可用性审核',type:'audit',desc:'确认CAAC/FAA/EASA等适航证书可用于吉祥航空。',audit_steps:['质检确认','工程技术确认','PPC确认']},
        {id:'1.5',title:'确认支援方及取件信息',type:'manual',desc:'确认最终支援方、可供件号/数量、取件地址、联系人及联系方式。'},
        {id:'1.6',title:'锁定器材来源',type:'manual',desc:'比较各询件结果，锁定主来源和备选来源，作为运输方案输入。'},
      ]},
      {id:2,title:'运输方案',_exp:true,nodes:[
        {id:'2.1',title:'确认器材运输属性',type:'manual',desc:'确认尺寸、重量、货值、危险品属性及特殊包装要求。'},
        {id:'2.2',title:'确定运输方式',type:'manual',desc:'根据时效和器材属性选择手提货(OBC)、航空货运、专车或组合运输。'},
        {id:'2.3',title:'确认航班/运输班次',type:'manual',desc:'确认航班号或陆运班次、ETD/ETA、转机衔接和最晚交运时间。'},
        {id:'2.4',title:'确认提货人/承运人',type:'manual',desc:'确认提货人、承运人、证件信息、联系方式和抵达提货地时间。'},
        {id:'2.5',title:'确认接货人',type:'manual',desc:'确认外站接货人、接收地址、联系方式和末端交接要求。'},
        {id:'2.6',title:'确认出口报关',type:'manual',desc:'确认出口报关责任方、资料准备、申报状态和预计放行时间。'},
        {id:'2.7',title:'确认进口报关',type:'manual',desc:'确认进口清关责任方、资料准备、申报状态和预计放行时间。'},
        {id:'2.8',title:'锁定运输方案',type:'manual',desc:'汇总主运输方案、备选方案、关键时间点及风险项，形成可执行运输方案。'},
      ]},
      {id:3,title:'确认合同',_exp:true,nodes:[
        {id:'3.1',title:'确认支援价格及商务条款',type:'manual',desc:'确认借件/交换/采购价格、保障费用、运输费用及其他商务条件。'},
        {id:'3.2',title:'SAP合同制定',type:'manual',desc:'在SAP完成对应合同或订单制定，核对供应方、件号、数量及价格。'},
        {id:'3.3',title:'核对付款/归还/赔偿条款',type:'manual',desc:'核对付款方式、器材归还期限、交换件要求、损坏或延误责任。'},
        {id:'3.4',title:'合同确认生效',type:'manual',desc:'确认双方合同/订单已生效，支援方可正式放件并进入运输执行。'},
      ]},
      {id:4,title:'运输进度监控',_exp:true,nodes:[
        {id:'4.1',title:'物流抵达提货地',type:'manual',desc:'监控物流/承运人抵达支援方提货地点，并记录实际到达时间。'},
        {id:'4.2',title:'航材检查并提货',type:'manual',desc:'核对件号、数量、包装和证书，完成提货并留存照片/交接凭证。'},
        {id:'4.3',title:'承运人/物流出发',type:'manual',desc:'确认承运人已出发，更新实际出发时间及下一关键节点。'},
        {id:'4.4',title:'航班起飞/陆运在途',type:'manual',desc:'航空运输监控起飞与转机；陆运按固定频率更新位置和预计到达时间。'},
        {id:'4.5',title:'航班落地/到站',type:'manual',desc:'确认航班落地或陆运到站，关注行李/货物卸载、提取状态。'},
        {id:'4.6',title:'末端提货派送',type:'manual',desc:'确认末端物流或接货人完成提货，监控最后一公里派送。'},
        {id:'4.7',title:'航材到达并交接',type:'manual',desc:'确认航材到达AOG现场并完成交接，记录实际到达时间和签收凭证。'},
      ]},
      {id:5,title:'收尾',_exp:true,nodes:[
        {id:'5.1',title:'SAP收料/发料/差异处理',type:'manual',desc:'完成SAP收料、发料操作，如有数量或状态差异及时处理差异单。'},
        {id:'5.2',title:'确认器材归还方案',type:'manual',desc:'按借件/交换/跨境等场景确认归还责任、时间、运输和报关安排。'},
        {id:'5.3',title:'关闭保障任务并完成通报',type:'manual',desc:'确认航材保障完成、飞机恢复运行后关闭任务并完成最终通报。'},
        {id:'5.4',title:'生成复盘资料',type:'manual',desc:'沉淀关键时间线、方案变更、异常和经验，作为后续AOG案例复盘输入。'},
      ]},
    ];

'''
text = text[:cs] + checklist + text[ce:]

text = text.replace('deadline: t.deadline, nextFlight: formatNextFlight(t.nextFlight)', 'deadline: t.neededBy, nextFlight: formatNextFlight(t.nextFlight)')
text = text.replace("      spDialogVisible.value = true; spGenerated.value = false;\n      setTimeout(() => {", "      if (spGenerated.value && spReport.value?.basic?.id === wbTask.value.id) { spDialogVisible.value = true; return; }\n      spDialogVisible.value = true; spGenerated.value = false;\n      setTimeout(() => {")

old_load = '''        axios.get(`${API}/tasks`).then(r => {\n          wbPhases.value = r.data.phases || [];\n          generateAllAnswers();\n        }).catch(() => {\n          wbPhases.value = JSON.parse(JSON.stringify(BUILTIN_CHECKLIST));\n          // 加载内置检查单后生成智能体答案\n          nextTick(() => generateAllAnswers());\n        });'''
new_load = '''        wbPhases.value = JSON.parse(JSON.stringify(BUILTIN_CHECKLIST));\n        wbActivePhaseId.value = wbPhases.value[0]?.id || null;\n        nextTick(() => { generateAllAnswers(); initRecMap(); });'''
if old_load not in text:
    raise SystemExit('task loader marker not found')
text = text.replace(old_load, new_load, 1)
text = text.replace("      wbActivePhaseId.value = wbActivePhaseId.value === phaseId ? null : phaseId;", "      wbActivePhaseId.value = phaseId;")

out = text.encode('utf-8')
print('after', hashlib.sha256(out).hexdigest(), len(out))
path.write_bytes(out)
