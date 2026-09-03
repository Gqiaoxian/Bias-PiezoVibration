import numpy as np
from AnalysisConst import *
def checkDataset(dataset):
        """
        检查每个进程计算的数据
        :param dataset:
        :return:
        """
        if not dataset:
            return False
        else:
            data_s_e = dataset[2]
            data_s_e = np.array(data_s_e)
            if data_s_e.shape[0] == 0 :
                return False
            return True


def data_axis_corr(log_segment, events,hover_rel_idx,d_start, fs,mode):
    """
    将单条 log_segment 的索引转化为以悬停起点为 0 的时间轴 (秒)
    """
    n = len(log_segment)
    hover_real_idx = int(hover_rel_idx[0])
    # 悬停起点需要调整
    
    event_idx = [ev[0] for ev in events]
    for i in event_idx:
        if i>hover_real_idx:
            if mode=='vibration_sine' or mode =='vibration_triangle':
                hover_real_idx = int(hover_real_idx - (i-hover_real_idx)/2)
                break
            elif mode == 'vibration_square':
                hover_real_idx = int(hover_real_idx - (i-hover_real_idx))
                break
    # 悬停起点在局部切片中的索引
    h_start_local = hover_real_idx-d_start
    # 生成局部索引序列 [0, 1, 2, ...] 并偏移，使 h_start_local 变为 0
    time_axis = (np.arange(n) - h_start_local) / fs
    return time_axis


def get_trough_peak(log_segment,piezo, segment_events, d_start,mode, min_peak_len, hover_amp,input_length=None):
    """
    log_segment: 切片后的电导数据
    segment_events: 原始全局索引拐点
    d_start: 切片起始全局索引
    min_peak_len: 预期的总拐点数 (例如 8 代表 4 peak + 4 trough)
    """
    log_G_peak = []
    log_G_trough = []
    max_G_peak = []
    min_G_trough = []
    # --- 1. 坐标映射与初步清洗 ---
    local_evs = [{'idx': ev[0] - d_start, 'type': ev[1]} for ev in segment_events]
    # --- 2. 数量处理：截断或补齐 ---
    actual_len = len(local_evs)
    
    if actual_len > min_peak_len:
        local_evs = local_evs[:min_peak_len]
        # 如果多了，直接截断
    elif actual_len < min_peak_len and actual_len >= 2:
        # 如果少了，进行末端推算补齐
        last_idx = local_evs[-1]['idx']
        prev_idx = local_evs[-2]['idx']
        avg_period = abs(last_idx - prev_idx) # 计算半周期步长
        
        last_type = local_evs[-1]['type']
        for _ in range(min_peak_len - actual_len):
            # 交替补齐类型
            new_type = 'trough' if last_type == 'peak' else 'peak'
            new_idx = last_idx + avg_period
            # 边界检查：补齐的点不能超出切片范围
            if new_idx >= len(log_segment):
                new_idx = len(log_segment) - 1
            if  mode == 'vibration_square':
                if abs(piezo[new_idx] - piezo[new_idx+int((last_idx-new_idx)/2)])> hover_amp*1.1:
                    new_idx = last_idx+1
            local_evs.append({'idx': int(new_idx), 'type': new_type})
            # 更新状态用于下一次循环
            last_idx = new_idx
            last_type = new_type
    def get_adaptive_len(curr_idx, i):
    # --- 3. 自适应长度计算 ---
        neighbors = []
        if i > 0: neighbors.append(abs(curr_idx - local_evs[i-1]['idx']))
        if i < len(local_evs) - 1: neighbors.append(abs(curr_idx - local_evs[i+1]['idx']))
        
        if not neighbors: return 50
        min_dist = min(neighbors)
        
        if mode == 'vibration_square':
            return min_dist
        else:
            return int(min_dist / 2)
    # --- 4. 提取数据 ---
    for i, curr in enumerate(local_evs):
        c_idx = curr['idx']
        c_type = curr['type']
        L = get_adaptive_len(c_idx, i)
        if mode == 'vibration_square':
            if input_length is not None and (int(input_length))>0:
                Lrange = int(input_length)
                start = max(0, int(c_idx-L/2-Lrange))
                end = min(c_idx, int(c_idx-L/2 + Lrange))
                chunk = log_segment[start : end]
            # 方波提取逻辑：取转折前稳定段
            else:
                start = max(0, c_idx - L)
                chunk = log_segment[start : c_idx]
            # if i== 7:
            #     print(f"s:{start},e:{c_idx},corr:{c_idx+d_start},L:{L},index:{c_idx},type:{c_type}")
            if c_type == 'peak': log_G_peak.extend(chunk)
            else: log_G_trough.extend(chunk)

        elif mode == 'vibration_triangle':
            if input_length is not None and (int(input_length))>0:
                L = int(input_length)
            # 三角波提取逻辑：中心对称窗口
            start = max(0, c_idx - L)
            end = min(len(log_segment), c_idx + L)
            # print(f"s:{start},e:{end},corr:{c_idx+d_start},L:{L},index:{c_idx},type:{c_type}")
            chunk = log_segment[start : end]
            if c_type == 'peak': log_G_peak.extend(chunk)
            else: log_G_trough.extend(chunk)

        elif mode == 'vibration_sine':
            if input_length is not None and (int(input_length))>0:
                L = int(input_length)
            # 正弦波提取逻辑：窗口内极值
            start = max(0, c_idx - L)
            end = min(len(log_segment), c_idx + L)
            # print(f"s:{start},e:{end},corr:{c_idx+d_start},L:{L},index:{c_idx},type:{c_type}")
            chunk = log_segment[start : end]
            if len(chunk) > 0:
                if c_type == 'peak': max_G_peak.append(np.max(chunk))
                else: min_G_trough.append(np.min(chunk))
    if mode == 'vibration_sine':
        log_G_peak.append(np.mean(max_G_peak))
        log_G_trough.append(np.mean(min_G_trough))
    return np.array(log_G_peak), np.array(log_G_trough)

def getDrawData(datasets, keyPara):
    all_times = []
    all_logs = []
    combined_peaks = []
    combined_troughs = []
    fs = float(keyPara['sample_frequence_lineEdit'])
    mode = keyPara['mode']
    hover_amp = float(keyPara['hoveramplitude_lineEdit'])
    compeaknum = int(keyPara['time_lineEdit']) *int(keyPara['hover_frequence_lineEdit'])/1000*2
    peaknum = int(keyPara['peaknum_lineEdit']) if keyPara['peaknum_lineEdit']!=0 else int(compeaknum)
    win_len = int(keyPara['length1dfit_lineEdit']) if keyPara['length1dfit_lineEdit']!=0 else None
    num = 0
    for data in datasets:
        log_seg = data['log_G']
        h_rel = data['hover_s_e'][0]
        d_start = int(data['data_s_e'][0][0])
        events = data['segment_events']
        piezo = data['piezo_segment']
        # print(f"hover:{h_rel},dsatr:{d_start}")
        # --- 1. 二维直方图数据 ---
        time_axis = data_axis_corr(log_seg, events,h_rel,d_start, fs,mode)
        all_times.append(time_axis)
        all_logs.append(log_seg)
        # --- 2. 一维直方图数据 (波峰波谷提取) ---
        if mode !='vibration_irregular':
            p_vals, t_vals = get_trough_peak(log_seg, piezo,events, d_start,mode, peaknum,hover_amp,input_length=win_len)
            combined_peaks.extend(p_vals)
            combined_troughs.extend(t_vals)
        if all_times:
            num += 1

    # 展开列表用于绘图
    
    if num == 0:
        return None, None, None, None, 0,False
    final_time = np.concatenate(all_times)
    final_log = np.concatenate(all_logs)
    return final_time, final_log, np.array(combined_peaks), np.array(combined_troughs),num,True