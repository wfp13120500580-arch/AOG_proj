from pathlib import Path
p=Path('index_v3.0_minimal.html')
s=p.read_text(encoding='utf-8')
# remove system overview nav
s=s.replace("<button :class=\"{active:activeTab==='overview'}\" @click=\"activeTab='overview';if(!stats)loadStats()\">系统概览</button>","")
# replace label only; detailed structural changes are injected by CSS overrides
css='''
/* monitor redesign */
.monitor-container{background:#f5f7fa}
.stats-row{padding:12px 20px;background:#fff}
.stat-card{background:#fff;border-radius:12px;padding:14px 18px;border:1px solid #edf0f4}
.view-toolbar{height:48px}
.task-list-wrap{padding:14px 20px}
.task-table{border-radius:12px}
.detail-panel{width:360px;background:#f8fafc}
.detail-card{border-radius:12px;padding:14px}
.detail-card:first-child{border-left:3px solid #2563eb}
/* hide unused overview */
.overview{display:none!important}
'''
s=s.replace('</style>',css+'</style>',1)
s=s.replace('AOG 保障任务','AOG保障监控')
p.write_text(s,encoding='utf-8')
