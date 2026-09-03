from scipy.signal import find_peaks
import numpy as np
from nptdms import TdmsFile
from gangLogger.myLog import MyLog
from AnalysisConst import *
from pathlib import Path

class DataProcessUtil:
    logger = MyLog("DataProcessUtil",BASEDIR)
    _file_cache = {}  # 文件缓存，避免重复加载
    @classmethod
    def loadTDMSFile(cls, filePath, use_cache=True):
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
    def cut(cls,log_G, HIGH_COND, LOW_COND, additional_length=0, STEP=50, LEN_HIGH=None, LEN_LOW=None):
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
    def find_square_wave_curves(cls,data_s_e, piezo_voltage, piezo_amplitude, piezo_frequency,time):
        data_square_wave = []
        start_point = []
        end_point = []
        pv = np.asarray(piezo_voltage).flatten()
        data_s_e1 = np.array(data_s_e)
        for i in range(len(data_s_e1)):
            s = int(float(data_s_e1[i,0])) 
            e = int(float(data_s_e1[i,1]))
            if e < len(piezo_voltage) and e > s:
                segment = pv[s:e]
                dseg = np.diff(segment)
                min_prom = piezo_amplitude * 1.8
                min_peak_num = max(1, int(time * piezo_frequency / 1000))
                peaks, _ = find_peaks(dseg, prominence=min_prom)
                peaks_trough, _ = find_peaks(-dseg, prominence=min_prom)
                if len(peaks) >= min_peak_num:
                    data_square_wave.append(data_s_e1[i,:].tolist())
                    start_point.append(int(min(peaks) + s - 10))
                    end_point.append(int(max(max(peaks), max(peaks_trough) + s + 10)))
        return data_square_wave, start_point, end_point


    @classmethod
    def VibProcessData(cls,filePath, keyPara):
        df_piezo,df_V = cls.loadTDMSFile(filePath)
        v0 = keyPara['V0_lineEdit']
        # g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        df_logG = cls.log_G_trans(data=df_V,V0=v0,a1=a1,b1=b1,a2=a2,b2=b2)
        high_cond = keyPara['highcond_lineEdit']
        low_cond = keyPara['lowcond_lineEdit']
        addtional_len = keyPara['additional_length_lineEdit']
        piezo_frequency = keyPara['hover_frequence_lineEdit']
        piezo_amplitude = keyPara['piezo_amplitude_lineEdit']
        time = keyPara['time_lineEdit']
        data_s_e, _ = cls.cut(df_logG, high_cond, low_cond,additional_length=addtional_len)
        num = 0
        if data_s_e is None:
            return np.array(df_logG), np.array(df_piezo),np.array(data_s_e),np.array(data_square_wave_s_e), np.array(start_point), np.array(end_point),num
        
        data_square_wave_s_e, start_point, end_point = cls.find_square_wave_curves(data_s_e, df_piezo, piezo_amplitude, piezo_frequency,time)
        if data_square_wave_s_e is not None:
            num = len(data_square_wave_s_e)
        return np.array(df_logG), np.array(df_piezo),np.array(data_s_e),np.array(data_square_wave_s_e), np.array(start_point), np.array(end_point),num
    
    @classmethod
    def CalProcessData(cls,filePath, keyPara):
        df_piezo,df_V = cls.loadTDMSFile(filePath)
        v0 = keyPara['V0_lineEdit']
        # g0 = keyPara['g0_lineEdit']
        a1 = keyPara['a1_lineEdit']
        a2 = keyPara['a2_lineEdit']
        b1 = keyPara['b1_lineEdit']
        b2 = keyPara['b2_lineEdit']
        df_logG = cls.log_G_trans(data=df_V,V0=v0,a1=a1,b1=b1,a2=a2,b2=b2)
        high_cond = keyPara['piezo_highcond_lineEdit']
        low_cond = keyPara['piezo_lowcond_lineEdit']
        low_len = keyPara['lenlow_lineEdit']
        high_len = keyPara['lenhigh_lineEdit']
        # addtional_len = keyPara['additional_length_lineEdit']
        data_s_e, len_s_e = cls.cut(df_logG, high_cond, low_cond,additional_length=0, LEN_HIGH=high_len, LEN_LOW=low_len)

        # Ensure returned segmentation arrays always have shape (N,2).
        if data_s_e is None:
            data_s_e_arr = np.empty((0, 2), dtype=int)
        else:
            data_s_e_arr = np.asarray(data_s_e)
            if data_s_e_arr.size == 0:
                data_s_e_arr = np.empty((0, 2), dtype=int)
            elif data_s_e_arr.ndim == 1:
                # single pair like [s, e] -> make it (1,2)
                data_s_e_arr = data_s_e_arr.reshape(1, -1)

        if len_s_e is None:
            len_s_e_arr = np.empty((0, 2), dtype=int)
        else:
            len_s_e_arr = np.asarray(len_s_e)
            if len_s_e_arr.size == 0:
                len_s_e_arr = np.empty((0, 2), dtype=int)
            elif len_s_e_arr.ndim == 1:
                # single pair -> reshape
                len_s_e_arr = len_s_e_arr.reshape(1, -1)

        # Compute delta piezo voltages for each (s,e) in len_s_e_arr
        delta_piezo_voltage = []
        if len_s_e_arr.size > 0:
            for i in range(len(len_s_e_arr)):
                s = int(len_s_e_arr[i, 0])
                e = int(len_s_e_arr[i, 1])
                # guard indices
                if 0 <= s < len(df_piezo) and 0 <= e < len(df_piezo):
                    delta_piezo_voltage.append(df_piezo[s] - df_piezo[e])
        num = len(len_s_e_arr)
        # print(len_s_e_arr)
        return np.asarray(delta_piezo_voltage), data_s_e_arr, len_s_e_arr, num

    
    

            


if __name__ == "__main__":
    keyPara = {}
    keyPara['v0_lineEdit'] = 0.1
    keyPara['g0_lineEdit'] = 12.9
    keyPara['a1_lineEdit'] = 4.1422
    keyPara['a2_lineEdit'] = -4.1044
    keyPara['b1_lineEdit'] = -13.196
    keyPara['b2_lineEdit'] = -13.135
    dataclass = DataProcessUtil()
    keyPara['highcond_lineEdit'] = 0.5
    keyPara['lowcond_lineEdit'] = -5.5
    keyPara['lenlow_lineEdit'] = -5
    keyPara['lenhigh_lineEdit'] = -3
    keyPara['additional_length_lineEdit'] = 7500
#     keyPara['piezo_frequence_lineEdit'] = 10
#     keyPara['piezo_amplitude_lineEdit'] = 0.0066
    DataProcessUtil.CalProcessData("./data/jz/0.1V-decane-20kHz-STM-3-1.tdms",keyPara)