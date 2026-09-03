import numpy as np
from gangLogger.myLog import MyLog
from AnalysisConst import *
class NewDataProcessUtil:
    logger = MyLog("New_DataProcessUtil",BASEDIR)
    _file_cache = {}  # 文件缓存，避免重复加载

    @classmethod
    def loadTDMSFile(cls, filePath, use_cache=True):
        from nptdms import TdmsFile
        from pathlib import Path
        file_key = str(Path(filePath).resolve())
        # 1. 内存缓存 (优先)
        if use_cache and file_key in cls._file_cache:
            return cls._file_cache[file_key]
        # 2. 磁盘高速缓存层 (.npz 文件)
        cache_file = filePath + ".cache.npz"
        if use_cache and os.path.exists(cache_file):
            try:
                data = np.load(cache_file)
                df_piezo, df_v = data['piezo'], data['v']
                cls._file_cache[file_key] = (df_piezo, df_v)
                return df_piezo, df_v
            except Exception as e:
                cls.logger.debug(f"读取本地缓存失败，重新解析TDMS: {e}")

        # 3. 如果没有缓存，解析 TDMS
        with TdmsFile.open(filePath) as tdmsFile:
            group = tdmsFile.groups()[0]
            channels = group.channels()
            
            df_piezo = None
            df_v = None
            # 优化：提前转换为大写并直接匹配，减少不必要的操作
            for chan in channels:
                name_upper = chan.name.upper()
                if 'PIEZO' in name_upper and df_piezo is None:
                    df_piezo = chan[:]
                elif 'AI0' in name_upper and df_v is None:
                    df_v = chan[:]
                
                if df_piezo is not None and df_v is not None:
                    break
                    
            if df_piezo is None or df_v is None:
                cls.logger.debug(f"在文件 {filePath} 中未找到匹配的通道")

        # 4. 写入磁盘高速缓存 (耗时一次，后续瞬间加载)
        if use_cache and df_piezo is not None and df_v is not None:
            np.savez_compressed(cache_file, piezo=df_piezo, v=df_v) # 或者直接用 np.savez 更快但体积大
            cls._file_cache[file_key] = (df_piezo, df_v)
            
        return df_piezo, df_v
    
    
    @classmethod
    def log_G_trans(cls, data, V0=0.1, G0=12.9, a1=4.1422, b1=-13.196, a2=-4.1044, b2=-13.135):
        x = np.asarray(data).astype(float)
        
        # 使用numpy向量化操作避免Python循环
        G = np.where(x > 0, 10**(x*a1+b1), 10**(x*a2+b2))
        log_G = np.log10(np.abs(G0 / ((V0/1000) / G)))
        
        return log_G.tolist()  # 如果需要列表格式，返回列表；否则可以直接返回numpy数组
    @classmethod
    def get_all_hover_segments(cls,events, piezo,log_G, hover_amplitude, peak_num_expected,threshold,square_len,mode):
        """
        扫描整段数据的所有拐点，提取所有符合特征的悬停段。
        
        返回:
            list of dict: 每个 dict 包含 {scan_s_e, hover_s_e, segment_events}
        """
        all_results = []
        if mode == 'vibration_square':
            for i in range(1,len(events)):
                seg = piezo[events[i-1][0]:events[i][0]]
                dp = np.diff(seg)
                square_hovernum = np.sum(dp==0)
                if square_hovernum > square_len*1.5:
                    idx = np.isclose(dp,hover_amplitude,atol=0.0001)
                    idx = np.where(idx)[0]
                    # 说明两个中间是有悬停的
                    if idx.size > 0:
                        if events[i-1][1] == 'peak':
                            peak_idx = int(events[i-1][0]+idx[0])
                            events.append((peak_idx,'peak'))
                        else:
                            trough_idx = int(events[i-1][0]+idx[0])
                            events.append((trough_idx,'trough'))
            events.sort(key=lambda x: x[0])
        # 1. 判定单次波动是否符合悬停振幅 (峰峰值)
        def is_hover_swing(p1_idx, p2_idx):
            amp = abs(piezo[p1_idx] - piezo[p2_idx])
            # print(amp,log_G[p1_idx],log_G[p2_idx])
            # 允许 threshold% 的振幅波动
            if hover_amplitude * (1-float(threshold)) <= amp <= hover_amplitude * (1+float(threshold)):
                # 处理刚开始多出来的方波
                if mode == 'vibration_square':
                    if p1_idx > square_len:
                        square_seg = piezo[p1_idx-square_len:p1_idx]
                        dp = np.diff(square_seg)
                        square_hovernum = np.sum(dp==0)
                        # print(square_hovernum,square_len)
                        if square_hovernum < square_len*0.5:
                            return False
                        else:
                            return True
                else:
                    return True
            else:
                return False
                # 处理方波长度的问题
            return hover_amplitude * (1-float(threshold)) <= amp <= hover_amplitude * (1+float(threshold))
        i = 0
        while i < len(events) - 1:
            current_segment = []
            j = i
            # --- 步骤 1: 寻找满足平稳振幅的连续区间 ---
            while j < len(events) - 1:
                # if j<15:
                #     print(j,events[j][0],events[j+1][0],is_hover_swing(events[j][0], events[j+1][0]))
                if is_hover_swing(events[j][0], events[j+1][0]):
                    if not current_segment:
                        current_segment.append(events[j])
                    current_segment.append(events[j+1])
                    j += 1
                else:
                    break
            # print(current_segment[:10],len(current_segment))
            # --- 步骤 2: 基础过滤 (拐点数) ---
            if current_segment and len(current_segment) >= peak_num_expected-1 and len(current_segment) <= peak_num_expected+1:
                mid_vals = [piezo[ev[0]] for ev in current_segment]
                hover_max = max(mid_vals)
                hover_min = min(mid_vals)
                # --- 步骤 3: 寻找真正的扫描段大跳变 (回溯逻辑) ---
                # 向前找显著高于悬停段的大波峰
                scan_peak_node = None
                for k in range(i - 1, -1, -1):
                    val = piezo[events[k][0]]
                    # 设定缓冲区，跨过切换瞬间的小抖动
                    if val > hover_max + (hover_amplitude * 0.2):
                        scan_peak_node = events[k]
                        break
                # 向后找显著低于悬停段的大波谷
                scan_trough_node = None
                for k in range(j + 1, len(events)):
                    val = piezo[events[k][0]]
                    if val < hover_min - (hover_amplitude * 0.2):
                        scan_trough_node = events[k]
                        break

                # --- 步骤 4: 最终校验并保存结果 ---
                if scan_peak_node and scan_trough_node:
                    segment_info = {
                        # 扫描段的起止点 (大波峰和大波谷)
                        "data_s_e": (scan_peak_node, scan_trough_node),
                        # 悬停段的起止拐点
                        "hover_s_e": (current_segment[0], current_segment[-1]),
                        # 悬停段内的所有拐点 (用于后续找波峰波谷)
                        "segment_events": current_segment,
                        "piezo_segment":piezo[scan_peak_node[0]:scan_trough_node[0]].copy(),
                        "log_G":log_G[scan_peak_node[0]:scan_trough_node[0]].copy()
                    }
                    all_results.append(segment_info)
                    # print(all_results[0]['hover_s_e'])
                    # 性能优化：找到一段后，将 i 移动到 j 之后继续寻找下一段
                    i = j 
            i += 1

        return all_results
    @classmethod
    def get_all_hover_segments_irregular(cls,piezo,log_G,events,irregular_stable_len,hover_amplitude):
        all_results = []
        zero_runs_origin = []
        sign = np.sign(np.diff(piezo))
        is_zero = (sign == 0)
        start_f = -1
        for idx, val in enumerate(is_zero):
            if val and start_f == -1:
                start_f = idx
            elif not val and start_f != -1:
                run_len = idx - start_f
                # 只有长度达到设定要求的才记录为有效的“稳定台阶”
                if run_len > 1: # 这里可以根据实际噪声情况调大
                    zero_runs_origin.append((start_f, idx, run_len,piezo[int(start_f+(idx-start_f)/2)]))
                start_f = -1
        # 过滤掉长度太小的,用中位数过滤
        lengths = np.array([run[2] for run in zero_runs_origin])
        median_len = np.median(lengths)
        zero_runs = [run for run in zero_runs_origin if run[2] >= median_len*0.3]
        # 2. 在 zero_runs 中寻找符合数量要求的连续组合
        # 目标：找到连续的 N 个台阶，且它们被包裹在扫描段内
        k = 0
        while k <= len(zero_runs) - irregular_stable_len:
            # 这一组台阶的范围
            current_group = zero_runs[k : k + irregular_stable_len]
            hover_start_idx = current_group[0][0]  # 第一个0的起点
            hover_end_idx = current_group[-1][1]    # 最后一个0的终点
            # 第一个条件：这里悬停段必须是相接的，不能有间隔
            continuous = True
            for i in range(len(current_group) - 1):
                prev_end = current_group[i][1]
                next_start = current_group[i + 1][0]
                if next_start-prev_end > 2:
                    continuous = False
                    break
            if not continuous:
                k += 1
                continue
            # 找这里面的平稳段的最大值和最小值
            maxvalue = max([run[3] for run in current_group])
            minvalue = min([run[3] for run in current_group])
                # 3. 寻找扫描段大边界 (回溯 events 列表)
            if all_results and hover_start_idx<all_results[-1]['data_s_e'][1][0]:
            # print(f"k={k},hover_start_idx={hover_start_idx},hover_end_idx={hover_end_idx},{all_results[-1]['data_s_e'][1][0]}")
                k += 1
                continue
            scan_peak_node = None
            scan_trough_node = None
            # 往前找第一个比悬停起点高的大波峰
            for ev in reversed(events):
                if ev[0] < hover_start_idx and piezo[ev[0]] >maxvalue + hover_amplitude*0.2 :
                    scan_peak_node = ev
                    break
            # 往后找第一个比悬停终点低的大波谷
            for ev in events:
                if ev[0] > hover_end_idx and  piezo[ev[0]]<minvalue - hover_amplitude*0.2:
                    scan_trough_node = ev
                    break
            if scan_peak_node and scan_trough_node:
                all_results.append({
                    "data_s_e": (scan_peak_node, scan_trough_node),
                    "hover_s_e": ((hover_start_idx, 'irregular_start'), (hover_end_idx, 'irregular_end')),
                    "segment_events": [(r[0], 'step_start') for r in current_group],
                    "piezo_segment":piezo[scan_peak_node[0]:scan_trough_node[0]].copy(),
                    "log_G":log_G[scan_peak_node[0]:scan_trough_node[0]].copy()
                })
                # 找到了就跳过这一组
                k += (irregular_stable_len-1) 
            k += 1
        return all_results
    @classmethod
    def segment_piezo_cycles(cls,piezo,log_G,hover_amplitude,threshold,hover_len,mode,min_trend_len=1,min_peak_len=3):
        """
        使用「方向累计位移 + 趋势压缩」切分 piezo 周期

        参数
        ----
        piezo : 1D array-like
            piezo 原始数据
        min_trend_len : int
            最小趋势长度，用于抑制单点抖动（不是窗口，不依赖尺度）
        threshold：阈值为了防止hover_amplitude的抖动
        min_peak_len:time*悬停波的频率/1000*2
        sine_1d_fit:int,是为了找波峰最高值的时候的范围，因为边界可能会掉所以给用户这么一个参数设置，三角波的凸起那部分的范围为[l,r]，那找波峰最高值的时候的范围为[l-sine_1d_fit,r+sine_1d_fit]
        返回
        ----
        all_results 
        """
        tolerance = hover_amplitude * 0.1
        piezo = np.asarray(piezo)

        # ---------- 方向序列 ----------
        dp = np.diff(piezo)
        sign = np.sign(dp)
        square_len = int(hover_len/min_peak_len)
        # print(square_len,mode,tolerance)
        if mode == 'vibration_square' or mode == 'vibration_irregular':
            for i in range(1,len(sign)-1):
                if sign[i]!=0 and sign[i-1]==0 and sign[i+1]==0:
                    # 判断方波平稳的时候的抖动，因为方波稳定那部分也会有很微小的抖动
                    if abs(dp[i]) < tolerance:
                        sign[i] = 0
                        
        # sign(dp): 只取方向，0 直接继承前一个方向
        # sign = np.sign(dp)
        # 利用这个找到不规则方波的悬停位置
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
        if len(trends) < 3:
            return []
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
        if mode == 'vibration_irregular':
            allresult = cls.get_all_hover_segments_irregular(piezo,log_G,peak,min_peak_len,hover_amplitude)
        else:
            allresult = cls.get_all_hover_segments(peak,piezo,log_G,hover_amplitude,min_peak_len,threshold,square_len,mode)
        return allresult

    @classmethod
    def _filter_by_conductance_range(cls, all_results, df_logG, mode, low_cond, high_cond):
        """
        根据电导范围过滤悬停段

        Parameters:
        -----------
        all_results : list
            从 segment_piezo_cycles() 返回的所有候选段
        df_logG : array-like
            完整的原始 log_G 数据（全文件）
        mode : str
            波形模式 ('vibration_square', 'vibration_sine', 'vibration_triangle', 'vibration_irregular')
        low_cond : float
            电导下限
        high_cond : float
            电导上限

        Returns:
        --------
        list : 过滤后的候选段
        """
        filtered_results = []
        df_logG = np.asarray(df_logG)
        for segment in all_results:
            hover_s_e = segment['hover_s_e']
            segment_events = segment['segment_events']
            start_idx = hover_s_e[0][0]
            end_idx = hover_s_e[1][0]

            # 计算真实的悬停段起点
            if mode == 'vibration_irregular':
                # 不规则波形不调整
                real_start_idx = start_idx
                real_end_idx = end_idx
            else:
                # 标准波形：查找第一个在起点之后的拐点，应用调整公式
                real_start_idx = start_idx
                for ev in segment_events:
                    if ev[0] > start_idx:
                        if mode in ['vibration_sine', 'vibration_triangle']:
                            real_start_idx = int(start_idx - (ev[0] - start_idx) / 2)
                            real_end_idx = int(end_idx + (ev[0] - start_idx) / 2)
                        elif mode == 'vibration_square':
                            real_start_idx = int(start_idx - (ev[0] - start_idx))
                            real_end_idx = int(end_idx + (ev[0] - start_idx))
                        break

            # 提取悬停段 log_G 数据
            hover_log_G = df_logG[real_start_idx:real_end_idx-1]
    
            # 检查所有值是否在范围内
            if len(hover_log_G) > 0:
                # 过滤无效值
                valid_vals = hover_log_G[(~np.isnan(hover_log_G)) & (~np.isinf(hover_log_G))]
                if len(valid_vals) > 0:
                    # 检查是否所有有效值都在范围内
                    if np.all(valid_vals >= low_cond) and np.all(valid_vals <= high_cond):
                        filtered_results.append(segment)
                        
                    # 否则跳过此段

        return filtered_results

    @classmethod
    def NewVibProcessData(cls, filePath, keyPara):
        df_piezo, df_log = cls.loadTDMSFile(filePath)
        v0 = float(keyPara['V0_lineEdit'])
        a1 = float(keyPara['a1_lineEdit'])
        a2 = float(keyPara['a2_lineEdit'])
        b1 = float(keyPara['b1_lineEdit'])
        b2 = float(keyPara['b2_lineEdit'])
        df_logG = cls.log_G_trans(df_log, V0=v0, a1=a1, b1=b1, a2=a2, b2=b2)

        # addtional_l = int(keyPara['additional_length_lineEdit'])
        piezo_frequency = float(keyPara['hover_frequence_lineEdit'])
        # piezo_amplitude = keyPara['piezo_amplitude_lineEdit']
        fs = float(keyPara['sample_frequence_lineEdit'])
        hover_time = int(keyPara['time_lineEdit'])
        # min_trend_len = int(keyPara['mintrendlen_lineEdit'])
        min_peak_len = int(keyPara['peaknum_lineEdit'])
        threshold = float(keyPara['threshold_lineEdit'])
        hover_amplitude = float(keyPara['hoveramplitude_lineEdit'])
        mode = keyPara['mode']
        high_cond = keyPara['highcond_lineEdit']
        low_cond = keyPara['lowcond_lineEdit']
        hover_len = fs*hover_time/1000
        if mode == 'vibration_sine' or mode == 'vibration_triangle':
            hover_amplitude = hover_amplitude*2
        # print(hover_len)
        # 计算峰的数量
        if min_peak_len == -1 or min_peak_len == 0:
            min_peak_len = int((hover_time*piezo_frequency/1000)*2)
        # print(min_peak_len)
        all_results = cls.segment_piezo_cycles(df_piezo,df_logG,hover_amplitude,threshold,hover_len,mode,min_peak_len=min_peak_len)

        # 如果启用了电导范围检查，进行过滤
        if keyPara.get('conda_range_check', False):  # 默认为 False，保向后兼容
            try:
                high_cond = float(high_cond) if high_cond is not None else 999
                low_cond = float(low_cond) if low_cond is not None else -999
                all_results = cls._filter_by_conductance_range(all_results, df_logG, mode, low_cond, high_cond)
            except (ValueError, KeyError, TypeError) as e:
                cls.logger.error(f"电导范围检查失败: {e}，将返回所有结果")
                # 如果出错，继续返回原结果

        return all_results
if __name__ == "__main__":
    keyPara = {}
    keyPara['v0_lineEdit'] = 0.1
    keyPara['g0_lineEdit'] = 12.9 
    # keyPara['a1_lineEdit'] = 3.888
    # keyPara['a2_lineEdit'] = -4.026
    # keyPara['b1_lineEdit'] = -12.964
    # keyPara['b2_lineEdit'] = -12.978
    keyPara['a1_lineEdit'] = 4.1422
    keyPara['a2_lineEdit'] = -4.1044
    keyPara['b1_lineEdit'] = -13.196
    keyPara['b2_lineEdit'] = -13.135
    dataclass = NewDataProcessUtil()
    keyPara['highcond_lineEdit'] = 0.5
    keyPara['lowcond_lineEdit'] = -5.5
    keyPara['lenlow_lineEdit'] = -5
    keyPara['lenhigh_lineEdit'] = -3
    keyPara['additional_length_lineEdit'] = 0
    keyPara['sample_frequence_lineEdit'] = 20000
    keyPara['hoveramplitude_lineEdit'] = 0.02
    keyPara['time_lineEdit'] = 200
    keyPara['threshold_lineEdit'] = 0.01
    keyPara['peaknum_lineEdit'] = 3
    keyPara['sine1dfit_lineEdit'] = 1
    keyPara['mode'] = "vibration_irregular"
    keyPara['hover_frequence_lineEdit'] = 10
    keyPara['mintrendlen_lineEdit'] = 1
#     keyPara['piezo_frequence_lineEdit'] = 10
#     keyPara['piezo_amplitude_lineEdit'] = 0.0066
    dataclass.NewVibProcessData("./testdata/py2-多段 - 0000.tdms",keyPara)
        