import numpy as np
def getAggregateDrawData(keyPara,datasets):
    """
    获取多进程计算结果的聚合
    :param datasets: 多线程的结果
    :return:
    """         # Bias_Square模块

    all_times, all_logs = [], []
    combined_peaks, combined_troughs = [], []
    num = 0
    mode = keyPara.get('mode')
    try:
        sample_rate = float(keyPara.get('sample_rate_lineEdit', 1.0))
    except Exception:
        sample_rate = 1.0

    # 防御性编程：如果 datasets 为 None 或不是可迭代，直接返回失败状态
    if not datasets:
        return np.array([]), np.array([]), np.array([]), np.array([]), 0, False

    for data in datasets:
        if data is None:
            continue
        # 支持 dict-like 或对象属性的访问
        try:
            log_seg = data.get('log_G') if isinstance(data, dict) else data['log_G']
        except Exception:
            # 最后尝试索引访问（例如元组）
            try:
                log_seg = data["log_G"]
            except Exception:
                continue

        if log_seg is None:
            continue

        # 提取 hover 与 data start，若缺失则跳过该条目
        try:
            h_rel = int(data.get('hover_s_e')[0]) if isinstance(data, dict) else int(data['hover_s_e'][0])
            d_start = int(data.get('data_s_e')[0]) if isinstance(data, dict) else int(data['data_s_e'][0])
        except Exception:
            continue

        # --- 1. 二维直方图数据 ---
        try:
            time_axis = data_axis_corr(log_seg, h_rel, d_start, sample_rate)
        except Exception:
            continue

        all_times.append(time_axis)
        all_logs.append(np.asarray(log_seg))

        # --- 2. 一维直方图数据 (波峰波谷提取) ---
        if mode not in ('Bias_Irregular_Vabration', 'RE_Irregular_Vabration'):
            p_vals = None
            t_vals = None
            try:
                p_vals = data.get('log_G_peak') if isinstance(data, dict) else data['log_G_peak']
            except Exception:
                p_vals = None
            try:
                t_vals = data.get('log_G_trough') if isinstance(data, dict) else data['log_G_trough']
            except Exception:
                t_vals = None

            if p_vals is None:
                p_vals = []
            if t_vals is None:
                t_vals = []

            # 确保是可迭代
            try:
                combined_peaks.extend(list(p_vals))
            except Exception:
                pass
            try:
                combined_troughs.extend(list(t_vals))
            except Exception:
                pass

        if all_times:
            num += 1

    # 展开列表用于绘图
    if num == 0 or not all_times:
        return np.array([]), np.array([]), np.array([]), np.array([]), 0, False

    try:
        final_time = np.concatenate(all_times)
        final_log = np.concatenate(all_logs)
    except Exception:
        return np.array([]), np.array([]), np.array([]), np.array([]), 0, False

    return final_time, final_log, np.array(combined_peaks), np.array(combined_troughs), num, True
            

def data_axis_corr(log_G,h_rel,d_start,sample_rate):
    n = len(log_G)
    h_start_local = h_rel-d_start
    # 生成局部索引序列 [0, 1, 2, ...] 并偏移，使 h_start_local 变为 0
    time_axis = (np.arange(n) - h_start_local) / sample_rate
    return time_axis
