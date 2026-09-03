import time
import os
from PySide6.QtCore import QObject, Signal, Slot
from multiprocessing import cpu_count, Pool
from joblib import Parallel, delayed
from DataProUtil import DataProcessUtil
from gangLogger.myLog import MyLog
from AnalysisConst import *

class DataAnalysisModel(QObject):
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
            # cpuCount = cpu_count()
            # # 进程池
            # pool = Pool(cpuCount - 1)
            # self.logger.debug(f"{keyPara['mode']}:Number of CPU core:{cpuCount},Process pool size:{cpuCount - 1}")
            t1 = time.perf_counter()
            if keyPara['mode'] == 'Bias_Square_Vabration':
                results = Parallel(n_jobs=-1,verbose=0,backend='threading')(delayed(self.BiasSquareDataReactor)(file,keyPara) for file in fileList)
                if results:
                    print(f"lll{type(results)},len(results):{len(results)}")
                    self.datasets = [cycle for file in results if file is not None for cycle in file]
                    print(f"len(self.datasets):{len(self.datasets)}")
                # self.datasets = pool.starmap_async(self.BiasSquareDataReactor, args).get()
            elif keyPara['mode'] == 'Bias_Sine_Vabration':
                results = Parallel(n_jobs=-1,verbose=0,backend='threading')(delayed(self.BiasSineDataReactor)(file,keyPara) for file in fileList)
                if results:
                     self.datasets = [cycle for file in results if file is not None for cycle in file]
                # self.datasets = pool.starmap_async(self.BiasSineDataReactor, args).get()
            elif keyPara['mode'] == 'Bias_Irregular_Vabration':
                results = Parallel(n_jobs=-1,verbose=0,backend='threading')(delayed(self.BiasIrregularDataReactor)(file,keyPara) for file in fileList)
                if results:
                     self.datasets = [cycle for file in results if file is not None for cycle in file]
                # self.datasets = pool.starmap_async(self.BiasIrregularDataReactor, args).get()
            elif keyPara['mode'] == 'RE_Irregular_Vabration':
                results = Parallel(n_jobs=-1,verbose=0,backend='threading')(delayed(self.REIrregularDataReactor)(file,keyPara) for file in fileList)
                if results:
                     self.datasets = [cycle for file in results if file is not None for cycle in file]
                # self.datasets = pool.starmap_async(self.REIrregularDataReactor, args).get()

            # pool.close()
            # pool.join()

            t2 = time.perf_counter()
            self.logger.debug(f"Parallel time:{int(t2 - t1)}")
            self.runEnd.emit()

    @classmethod
    def BiasSquareDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"BiasSquareProcessData:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            all_result = DataProcessUtil.BiasSquareProcessData(filePath, keyPara)
            # cls.logger.debug(
            # f"{df_bias}")
            print(type(all_result),len(all_result))
            return all_result
        except Exception as e:
            errMsg = f"BiasSquareProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None
        
    @classmethod
    def BiasSineDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"BiasSineProcessData:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            all_result = DataProcessUtil.BiasSineProcessData(filePath, keyPara)
            return all_result
        except Exception as e:
            errMsg = f"BiasSineProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None
        
    @classmethod
    def BiasIrregularDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"BiasIrregularProcessData:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            # 调用 DataProUtil 处理不规则波形
            # 返回值: df_logG, df_bias, data_s_e, num
            all_result = DataProcessUtil.BiasIrregularProcessData(filePath, keyPara)
            return all_result
        except Exception as e:
            errMsg = f"BiasIrregularProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None 
    
    
    @classmethod
    def REIrregularDataReactor(cls, filePath, keyPara):
        cls.logger.debug(
            f"REIrregularProcessData:Computing process PID: {os.getpid()},Calculates the start time of the process: {time.perf_counter()}")

        try:
            # 调用 DataProUtil 处理RE不规则波形
            all_result = DataProcessUtil.REIrregularProcessData(filePath, keyPara)
            return all_result
        except Exception as e:
            errMsg = f"REIrregularProcessData ERROR:{e}"
            cls.logger.error(errMsg)
            return None 
    
    @classmethod
    def REDataReactor(cls, filePath, keyPara):
        pass 



