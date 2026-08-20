from pathlib import Path
import re

p = Path('index_v3.0_minimal.html')
s = p.read_text(encoding='utf-8')

# 1. Remove all legacy top task selector CSS remnants.
s = re.sub(r"\n?\.wb-selector\{[^}]*\}\n?\.wb-selector span\{[^}]*\}\n?\.wb-selector \.el-select\{[^}]*\}\n?", "\n", s, count=1)

# 2. Workbench tab should enter the left-tree workbench directly and select first task.
old_btn = "<button :class=\"{active:activeTab==='workbench'}\" @click=\"activeTab='workbench'\">任务工作台</button>"
new_btn = "<button :class=\"{active:activeTab==='workbench'}\" @click=\"enterWorkbench()\">任务工作台</button>"
if old_btn not in s:
    raise SystemExit('workbench header button marker not found')
s = s.replace(old_btn, new_btn, 1)

# 3. Add one canonical workbench-entry function beside openWorkbench.
old_fn = "function openWorkbench(task) { activeTab.value = 'workbench'; nextTick(() => { wbSelectedTaskId.value = task.id; onWbTaskChange(task.id); }); }"
new_fn = """function enterWorkbench() {
      activeTab.value = 'workbench';
      nextTick(() => {
        const task = wbTask.value || mockTasks.value[0];
        if (task) { wbSelectedTaskId.value = task.id; onWbTaskChange(task.id); }
      });
    }
    function openWorkbench(task) { activeTab.value = 'workbench'; nextTick(() => { wbSelectedTaskId.value = task.id; onWbTaskChange(task.id); }); }"""
if old_fn not in s:
    raise SystemExit('openWorkbench marker not found')
s = s.replace(old_fn, new_fn, 1)

# 4. Expose the entry function to the template.
old_return = "mapInstance, mapInitialized, initMapIfNeeded, selectTask, selectedTask, openWorkbench,"
new_return = "mapInstance, mapInitialized, initMapIfNeeded, selectTask, selectedTask, enterWorkbench, openWorkbench,"
if old_return not in s:
    raise SystemExit('return marker not found')
s = s.replace(old_return, new_return, 1)

# 5. Make the left side visually read as a task directory, not a card list.
css = r'''
/* ===== Workbench task directory refinement ===== */
.wb-task-sidebar{background:#f7f9fb}
.wb-side-head{background:#fff;height:52px;padding:0 14px}
.wb-side-title::before{content:'▤';font-size:12px;color:#4f83aa;margin-right:6px}
.wb-side-list{padding:6px 8px 12px}
.wb-side-item{border:0;border-bottom:1px solid #e8edf2;border-radius:0;margin:0;padding:10px 9px;background:transparent;box-shadow:none}
.wb-side-item:hover{background:#eef5fa;border-color:#e8edf2}
.wb-side-item.active{background:#e8f3fb;border:0;border-bottom:1px solid #dbe7ef;box-shadow:inset 3px 0 0 #2e83bd}
.wb-side-item.urgent:not(.active){border-left:3px solid #e87070;padding-left:7px}
.wb-side-row b{font-size:10px;color:#284965}
.wb-side-node{border-top:0;padding-top:4px;margin-top:3px;color:#7a92a5}
'''
s = s.replace('</style>', css + '\n</style>', 1)

# Safety: the legacy selector must not exist as HTML or CSS.
if 'class="wb-selector"' in s or '.wb-selector{' in s:
    raise SystemExit('legacy wb selector remains')
if 'wb-task-sidebar' not in s or 'enterWorkbench()' not in s:
    raise SystemExit('task tree workbench missing')

p.write_text(s, encoding='utf-8')
print('workbench task tree fix applied', len(s))
