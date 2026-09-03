from PySide6.QtCore import QObject, Signal
import os
import numpy as np
import time
from gangLogger.myLog import MyLog
from gangUtils.generalUtils import GeneralUtils
from AnalysisConst import *

class SaveWorker(QObject):
    progress = Signal(int)
    save_run_end = Signal()
    error = Signal(str)
    logger = MyLog("SaveAllData", BASEDIR)
    def __init__(self,*args):
        super().__init__()
        self.keyPara,self.dataSavePath,self.d2H,self.d2_xedges,self.d2_yedges,self.peak_bins,self.peakH,self.trough_bins = args

    def run(self):
        t1 = time.perf_counter()
        try:
            self.VibsaveData(self.dataSavePath)
        except Exception as e:
            errMsg = f"数据保存异常：{e}"
            self.logger.error(errMsg)
        t2 = time.perf_counter()

        logMsg = f"并行执行时间：{int(t2 - t1)}"
        self.logger.debug(logMsg)
        self.save_run_end.emit()
        self.progress.emit(100)
        
    def zero_pad(self, x_2D_edges, y_2D_edges):
        x_use = x_2D_edges[1:]
        y_use = y_2D_edges[1:]
        len_x = len(x_use)
        len_y = len(y_use)

        if len_x < len_y:
            _PAD_NUM = len_y - len_x
            x_2D_edges_pad = np.pad(x_use, (0, _PAD_NUM), 'constant', constant_values=(0))
            y_2D_edges_pad = y_use
        else:
            _PAD_NUM = len_x - len_y
            x_2D_edges_pad = x_use
            y_2D_edges_pad = np.pad(y_use, (0, _PAD_NUM), 'constant', constant_values=(0))
        return x_2D_edges_pad, y_2D_edges_pad
    def VibsaveData(self, dataSavePath):
        """
        数据保存
        :param dataSavePath:
        :return:
        """
        dataPath = os.path.join(dataSavePath, "imgData")
        GeneralUtils.creatFolder(dataSavePath, "imgData")
        d2Path = os.path.join(dataPath, "2Dcond.txt")
        peakPath = os.path.join(dataPath, "Log_G_Peak.txt")
        troughPath = os.path.join(dataPath, "Log_G_trough.txt")
            
        if hasattr(self, 'd2H') and self.d2H is not None:
            H = np.nan_to_num(self.d2H, nan=0.0)  # 替换 NaN 为 0
            np.savetxt(d2Path, H, fmt='%.6f', delimiter='\t')
            x_2dbins, y_2dbins = self.zero_pad(self.d2_xedges,self.d2_yedges)
            all_2d_edges = np.array([x_2dbins, y_2dbins]).T
            np.savetxt(os.path.join(dataPath, "2Dcond_edges.txt"), all_2d_edges, fmt='%.6f', delimiter='\t')
            self.progress.emit(75)
        if self.keyPara['mode'] == 'Bias_Square_Vabration' or self.keyPara['mode'] == 'Bias_Sine_Vabration':
            if hasattr(self, 'peak_bins') and self.peak_bins is not None:
                peak_centers = (self.peak_bins[:-1] + self.peak_bins[1:]) / 2
                peak_data = np.column_stack((peak_centers, self.peakH))
                np.savetxt(peakPath, peak_data, fmt='%.6f', delimiter='\t')
                np.savetxt(os.path.join(dataPath, "Log_G_Peak_bins.txt"), self.peak_bins, fmt='%.6f', delimiter='\t')
            if hasattr(self, 'trough_bins') and self.trough_bins is not None:
                peak_centers = (self.trough_bins[:-1] + self.trough_bins[1:]) / 2
                peak_data = np.column_stack((peak_centers, self.peakH))
                np.savetxt(troughPath, peak_data, fmt='%.6f', delimiter='\t')
                np.savetxt(os.path.join(dataPath, "Log_G_trough_bins.txt"), self.trough_bins, fmt='%.6f', delimiter='\t')
            self.progress.emit(90)