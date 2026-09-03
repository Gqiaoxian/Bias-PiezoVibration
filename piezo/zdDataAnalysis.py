import os
import time
from PySide6.QtCore import QObject, Signal, Slot
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from DataProUtil import DataProcessUtil
from New_DataProUtil import NewDataProcessUtil
from gangLogger.myLog import MyLog
from AnalysisConst import *


def new_vib_data_reactor_worker(filePath, keyPara):
    logger = MyLog("DataAnalysis", BASEDIR)
    logger.debug(
        f"newvibration:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")
    try:
        return NewDataProcessUtil.NewVibProcessData(filePath, keyPara)
    except Exception as e:
        errMsg = f"NewVibProcessData ERROR:{e}"
        logger.error(errMsg)
        return None


class DataAnalysismodel(QObject):
    runEnd = Signal()
    logger = MyLog("DataAnalysis",BASEDIR)

    def __init__(self, keyPara):
        super().__init__()
        self.keyPara = keyPara
        self.datasets = None
    
    @Slot()
    def Run(self):
        keyPara = self.keyPara
        fileList = keyPara['FILE_PATHS']
        args = []
        
        if keyPara['FILE_TYPE'] == "tdms":
            for file in fileList:
                args.append((file,keyPara))
            if args:
                t1 = time.perf_counter()
                if keyPara['mode'] == 'vibration':
                    cpuCount = cpu_count()
                # 进程池
                    pool = Pool(cpuCount - 1)
                    self.logger.debug(f"{keyPara['mode']}:Number of CPU core:{cpuCount},Process pool size:{cpuCount - 1}")
                    self.datasets = pool.starmap_async(self.VibDataReactor, args).get()
                    pool.close()
                    pool.join()
                elif keyPara['mode'] == 'piezo_calibration':
                    cpuCount = cpu_count()
                    pool = Pool(cpuCount - 1)
                    self.logger.debug(f"{keyPara['mode']}:Number of CPU core:{cpuCount},Process pool size:{cpuCount - 1}")
                    self.datasets = pool.starmap_async(self.PiezoDataReactor, args).get()
                    pool.close()
                    pool.join()
                elif keyPara['mode'] != 'vibration' and keyPara['mode'] != 'piezo_calibration':
                    cpuCount = cpu_count()
                    pool_size = max(1, min(len(fileList), cpuCount - 1))
                    self.logger.debug(f"{keyPara['mode']}:Number of CPU core:{cpuCount},Thread pool size:{pool_size}")
                    with ThreadPool(pool_size) as pool:
                        results = pool.starmap(new_vib_data_reactor_worker, args)
                    self.datasets = []
                    for result in results:
                        if result:
                            self.datasets.extend(result)
                    # print(self.datasets)
                    self.logger.debug(f"{keyPara['mode']}:joblib Parallel processing......")
                t2 = time.perf_counter()
                self.logger.debug(f"Parallel time:{int(t2 - t1)}")
                self.runEnd.emit()

    @classmethod
    def VibDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"vibration:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            df_logG, df_piezo,data_s_e,data_square_wave_s_e, start_point, end_point,valid_num = DataProcessUtil.VibProcessData(filePath, keyPara)
            return df_logG, df_piezo,data_s_e,data_square_wave_s_e, start_point, end_point,valid_num
        except Exception as e:
            errMsg = f"VibProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None
        
    @classmethod
    def PiezoDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"piezocalibration:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            delta_piezo_voltage,data_s_e,len_s_e,valid_num = DataProcessUtil.CalProcessData(filePath, keyPara)
            return delta_piezo_voltage,data_s_e,len_s_e,valid_num
        except Exception as e:
            errMsg = f"CalProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None
        
    @classmethod
    def NewVibDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"newvibration:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            all_result = NewDataProcessUtil.NewVibProcessData(filePath, keyPara)
            return all_result
        except Exception as e:
            errMsg = f"NewVibProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None
        



