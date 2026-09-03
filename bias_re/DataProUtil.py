from scipy.signal import find_peaks
import numpy as np
import pandas as pd
from nptdms import TdmsFile
from gangLogger.myLog import MyLog
from AnalysisConst import *
import matplotlib.pyplot as plt

class DataProcessUtil:
    logger = MyLog("DataProcessUtil",BASEDIR)

    @classmethod
    def loadTDMSFile(cls, filePath,mode):
        """
        读取单个tdms文件
        """
        with TdmsFile.open(filePath) as tdmsFile:
            group = tdmsFile.groups()[0]
            channels = group.channels()
            
            df_bias = None
            df_v = None
            state = 'v'
            # 动态寻找通道
            for chan in channels:
                name_upper = chan.name.upper()
                if mode == 'RE_Irregular_Vabration':
                    if 'RE' in name_upper:
                        df_bias = chan[:]
                else:
                    if 'BIAS' in name_upper:
                        # 直接获取底层 numpy 数组，避免过多的 pandas 封装开销
                        df_bias = chan[:]
                if 'AI0' in name_upper:
                    df_v = chan[:]
                elif 'LOG(G/G0)' in name_upper:
                    df_v = chan[:]
                    state = 'log_G'
                # 如果都找到了就提前退出循环
                if df_bias is not None and df_v is not None:
                    break
            if df_bias is None or df_v is None:
                cls.logger.debug(f"newvibration:在文件 {filePath} 中未找到匹配 Bias 或 AI0 的通道")
        return df_bias, df_v,state
        # df = load_tdms_files(folder_selected)
        # df_V = df.iloc[:, 1]  # 电压
        # df_bias = df.iloc[:, 0]  # piezo
        # return df_V, df_bias
    
    @classmethod
    def log_G_trans(cls, data, df_bias, G0=12.9, a1=4.1422, b1=-13.196, a2=-4.1044, b2=-13.135):
        """
        对数放大器当中的电导转化（按点对应的 bias）
        原先的 V0 为常数电压，现在改为传入 `df_bias`，对每个点使用对应的 bias 值参与计算。
        Returns: Log(G/G0)
        """
        log_G = []
        x = np.asarray(data).astype(float)
        bias_arr = np.asarray(df_bias).astype(float).flatten() if df_bias is not None else np.array([])
        n_bias = bias_arr.size
        for i in range(len(x)):
            # 获取对应点的 bias；若长度不匹配则使用最后一个可用值或 0
            if n_bias == 0:
                bias_i = 0.0
            elif i < n_bias:
                bias_i = bias_arr[i]
            else:
                bias_i = bias_arr[-1]

            if x[i] > 0:
                G = 10 ** (x[i] * a1 + b1)
            else:
                G = 10 ** (x[i] * a2 + b2)

            # 避免除零与非法值
            try:
                denom = (bias_i / 1000.0) / G
                if denom == 0 or not np.isfinite(denom):
                    log_G.append(np.nan)
                else:
                    log_G_s = np.log10(abs(G0 / denom))
                    log_G.append(log_G_s)
            except Exception:
                log_G.append(np.nan)
        return log_G

    @classmethod
    def cut(cls,log_G, HIGH_COND, LOW_COND, additional_length=0, STEP=50, LEN_HIGH=None, LEN_LOW=None):
        """_
        按照指定的电导值，进行单条电导拆分
        Returns:data_s_e,
                len_data:len_data是为了有时候要计算电导在len_low和len_high之间的长度，目前没用到
        """
        log_G = np.asarray(log_G).astype(float)
        data_s_e = []
        len_data = []
        start_point = {}
        end_point = {}
        len_s = {}
        len_e = {}
        i_start = STEP * 10 - 1
        if log_G is not None:
            i_end = len(log_G) - STEP * 10
            cur_index = 0
            for i in range(i_start, i_end, STEP):
                i_left = log_G[i - STEP * 10 + 1:i].mean() 
                i_right = log_G[i:i + STEP * 10].mean()
                if i_left > i_right:
                    left_small = log_G[i - STEP + 1:i].mean()
                    right_small = log_G[i:i + STEP].mean()
                    if left_small >= HIGH_COND and right_small <= HIGH_COND:
                        start_point[cur_index] = i
                    if left_small >= LOW_COND and right_small <= LOW_COND:
                        end_point[cur_index] = i
                    if (LEN_HIGH is not None) and (left_small >= LEN_HIGH and right_small <= LEN_HIGH):
                        len_s[cur_index] = i
                    if (LEN_LOW is not None) and (left_small >= LEN_LOW and right_small <= LEN_LOW):
                        len_e[cur_index] = i
                elif log_G[i - STEP + 1:i].mean() <= LOW_COND and log_G[i:i + STEP].mean() >= LOW_COND:
                    cur_index += 1
            if LEN_HIGH is not None and LEN_LOW is not None:
                for i in len_s:
                    if i in len_e:
                        if len_s[i] != 0 and len_e[i] != 0 and len_s[i] < len_e[i]:
                            len_data.append([len_s[i], len_e[i]])
            for i in start_point:
                if i in end_point:
                    if start_point[i] != 0 and end_point[i] != 0 and start_point[i] < end_point[i]:
                        if additional_length == 0:
                            data_s_e.append([start_point[i], end_point[i]])
                        elif additional_length != 0 and end_point[i] + additional_length * 0.5 - start_point[i] > additional_length:
                            data_s_e.append([start_point[i], start_point[i] + additional_length])
        return data_s_e, len_data

    @classmethod
    def find_square_wave_curves(cls,data_s_e, log_G,df_bias, bias_frequency,time,threshold,fs):
        """
        根据bias的方波特征，找到符合条件的单条数据
        Returns:
            data_square_wave:bias符合方波条件的数据其实点
            start_point:整个单条根据bias拐点确定的单条起始点
            end_point:整个单条根据bias拐点确定的单条终点
        """
        # data_square_wave = []
        all_result = []
        pv = np.asarray(df_bias).flatten()
        data_s_e1 = np.array(data_s_e)
        for i in range(len(data_s_e1)):
            s = int(float(data_s_e1[i,0])) 
            e = int(float(data_s_e1[i,1]))
            log_G_peak = []
            log_G_trough = []
            start_point,end_point = 0,0
            if e < len(df_bias) and e > s:
                segment = pv[s:e]
                dseg = np.diff(segment)
                dseg = np.diff(segment)
                # min_prom = Vpp
                min_peak_num = max(1, int(time * bias_frequency / 1000))
                peaks, _ = find_peaks(dseg)
                peaks_trough, _ = find_peaks(-dseg)
                # print(peaks,peaks_trough)
                if len(peaks) >= min_peak_num:
                    # data_square_wave.append(data_s_e1[i,:].tolist())
                    start_point= (int(min(min(peaks),min(peaks_trough)) + s - 1))
                    end_point = (int(max(max(peaks), max(peaks_trough) + s + 1)))
                    switch_point = np.sort(np.concatenate((peaks, peaks_trough)))
                    if len(peaks) > 0 and len(peaks_trough) > 0 and min(switch_point) == min(peaks):
                        for j in range(0, len(switch_point) - 1, 2):
                            start_idx = int(float(s)) + int(float(switch_point[j])) 
                            end_idx = int(float(s)) + int(float(switch_point[j + 1])) 
                            log_G_peak.extend(log_G[start_idx:end_idx])
                            # print(start_idx,end_idx)
                        for j in range(1, len(switch_point) - 1, 2):
                            start_idx = int(float(s)) + int(float(switch_point[j])) 
                            end_idx = int(float(s)) + int(float(switch_point[j + 1])) 
                            log_G_trough.extend(log_G[start_idx:end_idx])
                            # print(start_idx,end_idx)
                    elif len(peaks) > 0 and len(peaks_trough) > 0 and min(switch_point) == min(peaks_trough):
                        for j in range(0, len(switch_point) - 1, 2):
                            start_idx = int(float(s)) + int(float(switch_point[j])) 
                            end_idx = int(float(s)) + int(float(switch_point[j + 1])) 
                            log_G_trough.extend(log_G[start_idx:end_idx])
                            # print(start_idx,end_idx)
                        for j in range(1, len(switch_point) - 1, 2):
                            start_idx = int(float(s)) + int(float(switch_point[j])) 
                            end_idx = int(float(s)) + int(float(switch_point[j + 1])) 
                            log_G_peak.extend(log_G[start_idx:end_idx])
            if len(log_G_peak) > 0:
                # print(data_s_e1[i,0],data_s_e1[i,1])
                segment_info = {
                    "data_s_e":(int(data_s_e1[i,0]),int(data_s_e1[i,1])),
                    "hover_s_e":(int(start_point),int(end_point)),
                    "log_G_peak":log_G_peak,
                    "log_G_trough":log_G_trough,
                    "bias_segment":pv[int(data_s_e1[i,0]):int(data_s_e1[i,1])].copy(),
                    "log_G":log_G[int(data_s_e1[i,0]):int(data_s_e1[i,1])].copy(),
                }
                # print(start_point,end_point)
                all_result.append(segment_info)
                            # print(start_idx,end_idx)
        return all_result
    @classmethod
    def find_sine_wave_curves(cls,data_s_e, log_G,df_bias,bias_frequency,time,threshold,fs):
        # data_square_wave = []
        all_result = []
        pv = np.asarray(df_bias).flatten()
        data_s_e1 = np.array(data_s_e)
        for i in range(len(data_s_e1)):
            s = int(float(data_s_e1[i,0])) 
            e = int(float(data_s_e1[i,1]))
            max_log_peak = []
            max_log_though = []
            log_G_peak = []
            log_G_trough = []
            hover_peak = []
            if e < len(df_bias) and e > s:
                segment = pv[s:e]
                min_peak_num = max(1, int(time * bias_frequency / 1000))*2
                peak = cls.find_switch_points(segment,threshold)
                if len(peak) < min_peak_num:
                    continue
                num_found = len(peak)
                limitpoint = fs*time/1000/min_peak_num
                adjustnum = 0
                for j in range(num_found):
                    curr_idx, curr_type = peak[j]
                    # --- 计算自适应窗口长度 (L) ---
                    # 寻找相邻点来计算半周期步长
                    distances = []
                    if j > 0:
                        distances.append(abs(curr_idx - peak[j-1][0]))
                    if j < num_found - 1:
                        distances.append(abs(curr_idx - peak[j+1][0]))
                    if distances:
                        # 窗口半径设为相邻极值点间距的 1/2
                        L = int(min(distances) / 2)
                        if L*2 < limitpoint*0.6:
                            continue
                        else:
                            hover_peak.append(curr_idx+s)
                    else:
                        continue
                    # --- 定义搜索区间 ---
                    # 这里的索引是相对于 segment 的，转换到 log_segment 中提取
                    win_start = max(0, curr_idx - L + s)
                    win_end = min(len(log_G), curr_idx + L+s)
                    search_chunk = log_G[win_start : win_end]
                    if len(search_chunk) > 0:
                        if curr_type == 'peak':
                            # 提取正弦波顶部的最大值
                            adjustnum += 1
                            max_log_peak.append(np.max(search_chunk))
                        else:
                            # 提取正弦波底部的最小值
                            adjustnum += 1
                            max_log_though.append(np.min(search_chunk))
                    if adjustnum >= min_peak_num:
                                break
            # 仅在找到有效峰/谷时计算均值，避免对空列表求均值导致警告/NaN
            log_peak_mean = None
            log_trough_mean = None
            if len(max_log_peak) > 0:
                try:
                    log_peak_mean = float(np.mean(max_log_peak))
                except Exception:
                    log_peak_mean = None
            if len(max_log_though) > 0:
                try:
                    log_trough_mean = float(np.mean(max_log_though))
                except Exception:
                    log_trough_mean = None

            # 如果既没有 hover_peak 也没有有效的均值，则跳过该段
            if not hover_peak and log_peak_mean is None and log_trough_mean is None:
                continue

            # 安全地构造返回结构，hover 范围若不存在则回退到 data_s_e 段
            hover_start = int(hover_peak[0]) if hover_peak else int(data_s_e1[i,0])
            hover_end = int(hover_peak[-1]) if hover_peak else int(data_s_e1[i,1])

            segment_info = {
                "data_s_e":(int(data_s_e1[i,0]),int(data_s_e1[i,1])),
                "hover_s_e":(hover_start, hover_end),
                "log_G_peak":[log_peak_mean] if log_peak_mean is not None else [],
                "log_G_trough":[log_trough_mean] if log_trough_mean is not None else [],
                "bias_segment":pv[int(data_s_e1[i,0]):int(data_s_e1[i,1])].copy(),
                "log_G":log_G[int(data_s_e1[i,0]):int(data_s_e1[i,1])].copy(),
            }
            all_result.append(segment_info)
        # print(log_G_peak) 
        return all_result

    @classmethod
    def find_switch_points(cls, series,tolerance=0.01, min_trend_len=1):
        series = np.asarray(series)
        N = len(series)
        # ---------- 方向序列 ----------
        dp = np.diff(series)
        sign = np.sign(dp)
        for i in range(1,len(sign)-1):
                if sign[i]!=0 and sign[i-1]==0 and sign[i+1]==0:
                    # print(f"111:i:{i}")
                    # 判断平稳的时候的抖动
                    if abs(dp[i]) < tolerance:
                        # print(f"pingwen:{i},{dp[i]}")
                        sign[i] = 0
        for i in range(1, len(sign)):
            if sign[i] == 0:
                sign[i] = sign[i - 1]
        sign[sign == 0] = 1  # 极端情况下全 0，随便给一个方向
        # ---------- 趋势压缩 ----------
        trends = []   # [(dir, start_idx, length)]
        cur_dir = sign[0]
        start = 0
        length = 1
        for i in range(1, len(sign)):
            if sign[i] == cur_dir:
                length += 1
            else:
                if length >= min_trend_len:
                    trends.append((cur_dir, start, length))
                cur_dir = sign[i]
                start = i
                length = 1
        if length >= min_trend_len:
            trends.append((cur_dir, start, length))
        # ----------  找主拐点 ----------
        extrema = {}  # (type, index)
        peak = []
        for i in range(len(trends) - 1):
            d0, s0, l0 = trends[i]
            d1, s1, l1 = trends[i + 1]

            if d0 == 1 and d1 == -1:
                # 波峰，取交界点
                extrema[s1] = "max"
                peak.append((s1,'peak'))
            elif d0 == -1 and d1 == 1:
                # 波谷
                extrema[s1] = "min"
                peak.append((s1,'trough'))
        if len(extrema) < 3:
            return []
        peak.sort(key=lambda x: x[0])
        return peak
    
    @classmethod
    def BiasSquareProcessData(cls,filePath, keyPara):
        df_bias,df_V,state = cls.loadTDMSFile(filePath,'biassquare')
        v0 = keyPara['v0_lineEdit']
        g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        if state == 'v':
            df_logG = cls.log_G_trans(df_V, df_bias, g0, a1, b1, a2, b2)
        elif state == 'log_G':
            df_logG = df_V
        high_cond = keyPara['highcond_lineEdit']
        low_cond = keyPara['lowcond_lineEdit']
        addtional_len = int(keyPara['additional_length_lineEdit'])
        square_frequency = float(keyPara['square_frequence_lineEdit'])
        samplerate = float(keyPara['sample_rate_lineEdit'])
        # Vpp = keyPara['Vpp_lineEdit']
        time = int(keyPara['time_lineEdit'])
        step = int(time*samplerate/50000)
        if keyPara.get('use_generic_bias_cut', False):
            data_s_e = cls.find_bias_trigger_points(
                df_bias,
                samplerate,
                time,
                additional_length=addtional_len,
                level_threshold=keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', None)),
                cut_offset=keyPara.get('cut_offset_lineEdit', 0),
            )
        else:
            data_s_e, _ = cls.cut(df_logG, high_cond, low_cond,additional_length=addtional_len,STEP=step)
        log_G_peak = []
        log_G_trough = []
        data_square_wave_s_e = []
        start_point = []
        end_point = []
        switch_points = []
        num = 0
        if data_s_e is None:
            return np.array(df_logG), np.array(df_bias),np.array(log_G_peak),np.array(log_G_trough),np.array(data_s_e),np.array(data_square_wave_s_e), np.array(start_point), np.array(end_point),num, np.asarray(switch_points, dtype=object)
        threshold = keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', 0.1))
        all_result = cls.find_square_wave_curves(data_s_e,df_logG, df_bias,square_frequency,time,threshold,samplerate)
        return all_result
    
    @classmethod
    def BiasSineProcessData(cls,filePath, keyPara):
        df_bias,df_V,state = cls.loadTDMSFile(filePath,'biassine')
        v0 = keyPara['v0_lineEdit']
        g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        if state == 'v':
            df_logG = cls.log_G_trans(df_V, df_bias, g0, a1, b1, a2, b2)
        elif state == 'log_G':
            df_logG = df_V
        # print(df_logG)
        # df_bias = df_bias[:10000]
        # df_logG = df_logG[:10000]
        high_cond = keyPara['highcond_lineEdit']
        low_cond = keyPara['lowcond_lineEdit']
        addtional_len = keyPara['additional_length_lineEdit']
        sine_frequency = keyPara['sine_frequence_lineEdit_sine']
        samplerate = keyPara['sample_rate_lineEdit']
        # Vpp = keyPara['Vpp_lineEdit_sine']
        time = keyPara['time_lineEdit']
        step = int(time*samplerate/50000)
        if keyPara.get('use_generic_bias_cut', False):
            data_s_e = cls.find_bias_trigger_points(
                df_bias,
                samplerate,
                time,
                additional_length=addtional_len,
                level_threshold=keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', None)),
                cut_offset=keyPara.get('cut_offset_lineEdit', 0),
            )
        else:
            data_s_e, _ = cls.cut(df_logG, high_cond, low_cond,additional_length=addtional_len,STEP=50)
        threshold = keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', 0.1))
        all_result = cls.find_sine_wave_curves(data_s_e,df_logG, df_bias,sine_frequency,time,threshold,samplerate)
        return all_result
    
    @classmethod
    def filter_irregular_segments(cls, data_s_e, df_bias, time_val=0, sample_rate=10000, bias_ptp_threshold=0.02):
        """
        对切分后的数据段进行筛选
        1. 排除掉比悬停长度短的段
        2. 排除掉Bias变化过小的段 (直线)
        """
        filtered_data_s_e = []
        if data_s_e is None:
            return []
            
        try:
            time_val = float(time_val)
        except Exception:
            time_val = 0.0
        try:
            sample_rate = float(sample_rate)
        except Exception:
            sample_rate = 0.0

        min_points = (time_val / 1000.0) * sample_rate
        
        for segment in data_s_e:
            start = int(segment[0])
            end = int(segment[1])
            
            # 1. 长度筛选
            if (end - start) < min_points:
                continue
       
            if end <= len(df_bias):
                seg_bias = df_bias[start:end]
                if np.ptp(seg_bias) < bias_ptp_threshold:
                    continue
            filtered_data_s_e.append(segment)
        return filtered_data_s_e

    @classmethod
    def find_bias_trigger_points(cls, df_bias, sample_rate, time_ms, additional_length=0, level_threshold=None, cut_offset=0):
        bias = np.asarray(df_bias).astype(float).flatten()
        n = bias.size
        if n <= 1:
            return np.array([])

        try:
            sample_rate = float(sample_rate)
        except Exception:
            sample_rate = 0

        if sample_rate <= 0:
            return np.array([])

        try:
            time_ms = float(time_ms)
        except Exception:
            time_ms = 0

        try:
            additional_length = int(float(additional_length))
        except Exception:
            additional_length = 0
        try:
            cut_offset = int(float(cut_offset))
        except Exception:
            cut_offset = 0
        cut_offset = max(0, cut_offset)

        # 窗口长度逻辑重构：
        # 1. 如果是通用切割模式 (提供了 level_threshold)，直接使用 additional_length 作为窗口点数
        # 2. 如果是非通用切割模式，由 time_ms 决定基础长度，并与 additional_length 取大值（兼容旧逻辑）
        if level_threshold is not None:
            window_points = max(1, additional_length)
        else:
            base_window_points = int(round(time_ms * sample_rate / 1000.0))
            window_points = max(1, base_window_points, additional_length)

        baseline_n = min(n, max(50, int(round(n * 0.01))))
        baseline = float(np.nanmedian(bias[:baseline_n]))
        bias_range = float(np.nanmax(bias) - np.nanmin(bias))
        if not np.isfinite(bias_range) or bias_range <= 0:
            return np.array([])

        try:
            level_threshold = float(level_threshold) if level_threshold is not None else None
        except Exception:
            level_threshold = None
        user_level_th = level_threshold is not None and level_threshold > 0
        level_th = max(1e-7, bias_range * 0.001) if not user_level_th else level_threshold

        d_bias = np.abs(np.diff(bias, prepend=bias[0]))
        smooth_w = max(1, int(round(sample_rate * 0.0005)))
        if smooth_w > 1:
            kernel = np.ones(smooth_w, dtype=float) / float(smooth_w)
            d_smooth = np.convolve(d_bias, kernel, mode="same")
        else:
            d_smooth = d_bias

        d_max = float(np.nanmax(d_smooth))
        d_th = max(1e-9, d_max * 0.05)

        if user_level_th:
            active = (np.abs(bias - baseline) > level_th)
        else:
            active = (d_smooth > d_th) | (np.abs(bias - baseline) > level_th)
        if active.size == 0:
            return np.array([])

        rise = np.flatnonzero(active[1:] & (~active[:-1])) + 1
        if active[0]:
            rise = np.concatenate((np.array([0], dtype=int), rise))

        data_s_e = []
        last_end = -1
        for start in rise.tolist():
            if start < last_end:
                continue
            start_adj = max(0, int(start) - cut_offset)
            end_adj = min(n, start_adj + window_points)
            if end_adj - start_adj <= 1:
                continue
            s0 = max(0, int(start_adj) - 5)
            e0 = min(n, int(end_adj) + 5)
            if e0 - s0 <= 1:
                continue
            data_s_e.append([s0, e0])
            last_end = e0

        return np.asarray(data_s_e, dtype=int)

    @classmethod
    def BiasIrregularProcessData(cls,filePath, keyPara):
        """
        不规则波形的数据处理
        1. 读取数据并转化为LogG
        2. 利用cut函数基于电导阈值进行切分
        3. 直接提取切分后的数据段，不做额外的波形校验
        :param filePath: 文件路径
        :param keyPara: 参数字典
        :return: 
            df_logG: 原始LogG数据
            df_bias: 原始Bias数据
            data_s_e: 切分后的起止点列表
            num: 有效曲线数量
        """
        # 1. 加载数据 (通道0为Bias，通道1为电流/电压响应)
        df_bias, df_V, state = cls.loadTDMSFile(filePath,'biasirregular')
        
        # 2. 参数获取与LogG转换
        v0 = keyPara['v0_lineEdit']
        g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        sample_rate = keyPara['sample_rate_lineEdit']
        if state == 'v':
            df_logG = cls.log_G_trans(df_V, df_bias, g0, a1, b1, a2, b2)
        elif state == 'log_G':
            df_logG = df_V
        
        # 3. 获取切分参数
        high_cond = keyPara['highcond_lineEdit']
        low_cond = keyPara['lowcond_lineEdit']
        addtional_len = keyPara['additional_length_lineEdit']
        
        try:
            time_val = float(keyPara.get('time_lineEdit', 0)) # ms
        except:
            time_val = 0

        if keyPara.get('use_generic_bias_cut', False):
            data_s_e = cls.find_bias_trigger_points(
                df_bias,
                sample_rate,
                time_val,
                additional_length=addtional_len,
                level_threshold=keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', None)),
                cut_offset=keyPara.get('cut_offset_lineEdit', 0),
            )
        else:
            data_s_e, _ = cls.cut(df_logG, high_cond, low_cond, additional_length=addtional_len)
            data_s_e = cls.filter_irregular_segments(data_s_e, df_bias, time_val,sample_rate=sample_rate)
        
        num = 0
        if data_s_e is not None:
            num = len(data_s_e)
        all_result = []
        for s,e in data_s_e:
            seg = df_bias[s:e]
            diff = np.diff(seg)
            sign = np.sign(diff)
            hover_start = np.where(sign[:-1] != sign[1:])[0] 
            segment_info = {
                "data_s_e":(s,e),
                "hover_s_e":(int(hover_start[0]+s),int(hover_start[-1]+s)),
                "log_G_peak":None,
                "log_G_trough":None,
                "bias_segment":df_bias[s:e].copy(),
                "log_G":df_logG[s:e].copy(),
            }
            all_result.append(segment_info)    
        # 6. 返回结果
        # 注意：为了保持接口一致性，不需要的返回值用None填充
        # 返回顺序需与 BiasSquareProcessData 对应的接收端匹配，或者并在聚合端做适配
        # 这里返回核心数据：全量LogG, 全量Bias, 切分点列表, 有效数量
        return all_result

    @classmethod
    def BiasGenericProcessData(cls, filePath, keyPara):
        df_bias, df_V,state = cls.loadTDMSFile(filePath,'biasgeneric')

        v0 = keyPara['v0_lineEdit']
        g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        if state == 'v':
            df_logG = cls.log_G_trans(df_V, df_bias, g0, a1, b1, a2, b2)
        elif state == 'log_G':
            df_logG = df_V

        sample_rate = keyPara.get('sample_rate_lineEdit', 0)
        time_ms = keyPara.get('time_lineEdit', 0)
        additional_length = keyPara.get('additional_length_lineEdit', 0)

        data_s_e = cls.find_bias_trigger_points(
            df_bias,
            sample_rate,
            time_ms,
            additional_length=additional_length,
            level_threshold=keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', None)),
            cut_offset=keyPara.get('cut_offset_lineEdit', 0),
        )
        num = int(len(data_s_e)) if data_s_e is not None else 0

        return np.array(df_logG), np.array(df_bias), np.array(data_s_e), num
    
    @classmethod
    def REIrregularProcessData(cls, filePath, keyPara):
        """
        RE不规则波形的数据处理
        1. 读取数据并转化为LogG
           注意：RE模式下，通道0(AI0)为响应信号(用于计算LogG)，通道1(RE)为控制信号(类似Bias，用于切分)
        2. 利用cut函数基于电导阈值进行切分
        3. 直接提取切分后的数据段，不做额外的波形校验
        :param filePath: 文件路径
        :param keyPara: 参数字典
        :return: 
            df_logG: 原始LogG数据
            df_bias: 原始Bias数据(其实是RE信号)
            data_s_e: 切分后的起止点列表
            num: 有效曲线数量
        """
        # 1. 加载数据 
        # loadTDMSFile返回 [Ch0, Ch1]
        # RE模式: Ch0 = AI0 (Response/LogG source), Ch1 = RE (Signal/Bias source)
        df_bias, df_V ,state= cls.loadTDMSFile(filePath,'RE_Irregular_Vabration')
        
        # 2. 参数获取与LogG转换
        v0 = keyPara['v0_lineEdit']
        g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        if state == 'v':
            df_logG = cls.log_G_trans(df_V, v0, g0, a1, b1, a2, b2)
        elif state == 'log_G':
            df_logG = df_V
        sample_rate = keyPara['sample_rate_lineEdit']
        
        # 3. 获取切分参数
        high_cond = keyPara['highcond_lineEdit']
        low_cond = keyPara['lowcond_lineEdit']
        addtional_len = keyPara['additional_length_lineEdit']
        
        try:
            time_val = float(keyPara.get('time_lineEdit', 0)) # ms
        except:
            time_val = 0

        if keyPara.get('use_generic_bias_cut', False):
            data_s_e = cls.find_bias_trigger_points(
                df_bias,
                sample_rate,
                time_val,
                additional_length=addtional_len,
                level_threshold=keyPara.get('threshold_lineEdit', keyPara.get('bias_trigger_threshold', None)),
                cut_offset=keyPara.get('cut_offset_lineEdit', 0),
            )
        else:
            data_s_e, _ = cls.cut(df_logG, high_cond, low_cond, additional_length=addtional_len)
            data_s_e = cls.filter_irregular_segments(data_s_e, df_bias, time_val,sample_rate=sample_rate)
        
        num = 0
        if data_s_e is not None:
            num = len(data_s_e)
        all_result = []
        for s,e in data_s_e:
            seg = df_bias[s:e]
            diff = np.diff(seg)
            sign = np.sign(diff)
            hover_start = np.where(sign[:-1] != sign[1:])[0] 
            segment_info = {
                "data_s_e":(s,e),
                "hover_s_e":(int(hover_start[0]+s),int(hover_start[-1]+s)),
                "log_G_peak":None,
                "log_G_trough":None,
                "bias_segment":df_bias[s:e].copy(),
                "log_G":df_logG[s:e].copy(),
            }
            all_result.append(segment_info)  
        # 6. 返回结果
        # 注意：为了保持接口一致性，不需要的返回值用None填充
        # 返回顺序需与 BiasSquareProcessData 对应的接收端匹配，或者并在聚合端做适配
        # 这里返回核心数据：全量LogG, 全量Bias, 切分点列表, 有效数量
        return all_result

    
    
    
    
if __name__ == "__main__":
    keyPara = {}
    keyPara['v0_lineEdit'] = 0.1
    keyPara['g0_lineEdit'] = 12.9
    keyPara['a1_lineEdit'] = 4.0789                                                                                                                         
    keyPara['a2_lineEdit'] = -4.0492
    keyPara['b1_lineEdit'] = -13.175
    keyPara['b2_lineEdit'] = -13.139
    dataclass = DataProcessUtil()
    keyPara['highcond_lineEdit'] = -1
    keyPara['lowcond_lineEdit'] = -7
    keyPara['Vpp_lineEdit'] = 0.4
    keyPara['square_frequence_lineEdit'] = 20
    keyPara['time_lineEdit'] = 200
    # keyPara['lenlow_lineEdit'] = -5
    # keyPara['lenhigh_lineEdit'] = -3
    keyPara['additional_length_lineEdit_sine'] = 0
    keyPara['highcond_lineEdit_sine'] = 1
    keyPara['lowcond_lineEdit_sine'] = -7
    keyPara['Vpp_lineEdit_sine'] = 0.2
    keyPara['sine_frequence_lineEdit_sine'] = 2000
    keyPara['time_lineEdit_sine'] = 200
    # keyPara['lenlow_lineEdit'] = -5
    # keyPara['lenhigh_lineEdit'] = -3
    keyPara['additional_length_lineEdit'] = 0
    keyPara['sample_rate_lineEdit'] = 20000
        # Vpp = keyPara['Vpp_lineEdit_sine']
#     keyPara['piezo_frequence_lineEdit'] = 10
#     keyPara['piezo_amplitude_lineEdit'] = 0.0066
    DataProcessUtil.BiasSineProcessData("H:/A-GQX/Aproject/qt/A-two_vibration/biasdata/py2-piezo-2Khz-0.0012V-1震荡测试正弦波-bias - 0000.tdms",keyPara)
