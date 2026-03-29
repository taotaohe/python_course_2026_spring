from psychopy import visual, core, event

# ==========================================
# 1. 实验基本参数与设计
# ==========================================
TRIGGER_KEY = '5'
TR = 2.0
DUMMY_VOLUMES = 3
DUMMY_DURATION = TR * DUMMY_VOLUMES  # 前置空扫时间：6.0秒

# 定义实验序列（列表形式）
# 注意：我们稍后会为每个字典动态添加 'planned_onset' 键
trialList = [
    {'name': 'Stim_A', 'stim_dur': 2.0, 'iti_dur': 3.0},
    {'name': 'Stim_B', 'stim_dur': 2.0, 'iti_dur': 4.0},
    {'name': 'Stim_C', 'stim_dur': 2.0, 'iti_dur': 3.0}
]

# ==========================================
# 2. 提前计算每个 Trial 的绝对起始时间
# ==========================================
# 第一个 Trial 的起始时间就是 Dummy Scans 结束的时间
current_trial_time = DUMMY_DURATION 

for trial in trialList:
    # 记录该 Trial 应该在全局时钟的哪一秒开始
    trial['planned_onset'] = current_trial_time
    # 下一个 Trial 的起始时间 = 当前起始时间 + 刺激时长 + ITI时长
    current_trial_time += trial['stim_dur'] + trial['iti_dur']
print(trialList)

# ==========================================
# 3. 初始化窗口和视觉刺激
# ==========================================
win = visual.Window(size=(800, 600), color='black')
msg = visual.TextStim(win, text="等待扫描仪脉冲...\n(请按键盘 '5')", font='Arial Unicode MS', color='white')
fixation = visual.TextStim(win, text="+", height=0.2, color='white')
stimulus = visual.TextStim(win, text="", height=0.2, color='green')

# ==========================================
# 4. 触发与同步阶段
# ==========================================
msg.draw()
win.flip()
print("--- 等待扫描仪启动 ---")

event.waitKeys(keyList=[TRIGGER_KEY])

# 收到 Trigger，重置全局时钟 
global_clock = core.Clock() 
print("--- 收到 Trigger！时钟已重置为 0.00 秒 ---")

# ==========================================
# 5. Dummy Scans 阶段
# ==========================================
fixation.draw()
win.flip() 
print(f"进入 Dummy Scans 阶段，呈现注视点 {DUMMY_DURATION} 秒...")

# ==========================================
# 6. 正式实验 Trial 循环
# ==========================================
for i, trial in enumerate(trialList):
    
    # 计算距离计划开始时间还有多久
    time_to_wait = trial['planned_onset'] - global_clock.getTime()
    if time_to_wait > 0:
        core.wait(time_to_wait) # 等待时间差，确保绝对对齐
    
    # --- 阶段 A：呈现刺激 ---
    stimulus.text = trial['name']
    stimulus.draw()
    win.flip()
    
    # 记录真实的 Onset（示例需要）
    actual_onset = global_clock.getTime()
    print(f"Trial {i+1} [{trial['name']}] 真实Onset: {actual_onset:.3f} 秒 (计划: {trial['planned_onset']:.3f})")
    
    # Trial内部计时相对灵活：直接用 core.wait
    core.wait(trial['stim_dur'])
    
    # --- 阶段 B：呈现 ITI (注视点) ---
    fixation.draw()
    win.flip()
    
    # 注意：这里我们不需要写 core.wait(trial['iti_dur'])
    # 因为在下一次循环开始时，time_to_wait 会自动处理 ITI 期间的等待！
    # 这样如果有任何误差，都会在这个隐形的 ITI 等待期被自动消化掉。

# 实验结束后，再额外呈现几秒注视点（让血流动力学响应HRF落回基线）
core.wait(6.0)

print(f"\n--- 实验结束，总耗时: {global_clock.getTime():.3f} 秒 ---")
win.close()
core.quit()
