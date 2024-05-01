from .model import *
import os, sys, clr
from datetime import datetime
from datetime import timedelta

lib_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(lib_path)
clr.AddReference(f'{lib_path}\\TechAnalysisAPI')
import TechAnalysisAPI

class TechAnalysis:
    def __init__(self, OnDigitalSSOEvent, OnTAConnStuEvent, OnUpdate, OnRcvDone):
        self.OnTAConnStuEvent = OnTAConnStuEvent
        self.OnDigitalSSOEvent = OnDigitalSSOEvent
        self.OnUpdate = OnUpdate
        self.OnRcvDone = OnRcvDone
        self._is_sso_ok = False

        tOnTAConnStuEvent = TechAnalysisAPI.OnTAConnStuHandler(self.TechAnalysisAPI_OnTAConnStuEvent)
        tOnDigitalSSOEvent = TechAnalysisAPI.OnDigitalSSOHandler(self.TechAnalysisAPI_OnDigitalSSOEvent)
        self.fTechAnalysisAPI = TechAnalysisAPI.TTechAnalysisAPI(tOnDigitalSSOEvent, tOnTAConnStuEvent)

    def TechAnalysisAPI_OnTAConnStuEvent(self, sender, aIsOK):
        self.OnTAConnStuEvent(aIsOK)

    def TechAnalysisAPI_OnDigitalSSOEvent(self, sender, aIsOK, aMsg):
        self._is_sso_ok = aIsOK
        self.OnDigitalSSOEvent(aIsOK, aMsg)

    def __get_rres(self, tmpTA_BAS, ares):
        rres = None
        ta_type = None
        if ares != None:
            tk = TKBarRec(ares.KBar.Date, ares.KBar.Product, ares.KBar.TimeSn, ares.KBar.TimeSn_Dply, ares.KBar.Quantity, \
                        ares.KBar.Volume, float(str(ares.KBar.OPrice)), float(str(ares.KBar.HPrice)), float(str(ares.KBar.LPrice)), \
                        float(str(ares.KBar.CPrice)))

            if tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.SMA:
                ta_type = eTA_Type.SMA
                sma = ta_sma(tk, float(str(ares.Value)))
                sma.__str__ = ares.GetDplyStr()
                rres = sma
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.EMA:
                ta_type = eTA_Type.EMA
                ema = ta_ema(tk, float(str(ares.Value)))
                ema.__str__ = ares.GetDplyStr()
                rres = ema
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.WMA:
                ta_type = eTA_Type.WMA
                wma = ta_wma(tk, float(str(ares.Value)))
                wma.__str__ = ares.GetDplyStr()
                rres = wma
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.SAR:
                ta_type = eTA_Type.SAR
                raise_fall = None
                if ares.RaiseFall == TechAnalysisAPI.eRaiseFall.Fall:
                    raise_fall = eRaiseFall.Fall
                elif ares.RaiseFall == TechAnalysisAPI.eRaiseFall.Raise:
                    raise_fall = eRaiseFall.Raise
                sar = ta_sar(tk, float(str(ares.SAR)), float(str(ares.EPh)), float(str(ares.EPl)), float(str(ares.AF)), raise_fall)
                sar.__str__ = ares.GetDplyStr()
                rres = sar
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.RSI:
                ta_type = eTA_Type.RSI
                rsi = ta_rsi(tk, float(str(ares.RSI)), float(str(ares.UpDn)), float(str(ares.UpAvg)), float(str(ares.DnAvg)))
                rsi.__str__ = ares.GetDplyStr()
                rres = rsi
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.MACD:
                ta_type = eTA_Type.MACD
                macd = ta_macd(tk, float(str(ares.DIF)), float(str(ares.OSC)))
                macd.__str__ = ares.GetDplyStr()
                rres = macd
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.KD:
                ta_type = eTA_Type.KD
                kd = ta_kd(tk, float(str(ares.K)), float(str(ares.D)))
                kd.__str__ = ares.GetDplyStr()
                rres = kd
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.CDP:
                ta_type = eTA_Type.CDP
                cdp = ta_cdp(tk, float(str(ares.CDP)), float(str(ares.AH)), float(str(ares.NH)), float(str(ares.AL)), float(str(ares.NL)))
                cdp.__str__ = ares.GetDplyStr()
                rres = cdp
            elif tmpTA_BAS.SubTARec.TA_Type == TechAnalysisAPI.eTA_Type.BBands:
                ta_type = eTA_Type.BBands                
                bbands = ta_bbands(tk, float(str(ares.MA)), float(str(ares.UB2)), float(str(ares.LB2)))
                bbands.__str__ = ares.GetDplyStr()
                rres = bbands

        return ta_type, rres
    def TACallBack_OnUpdate(self, sender, aResultPre, aResultLast):
        tmpTA_BAS = sender
         
        ta_type, res_pre = self.__get_rres(tmpTA_BAS, aResultPre)
        ta_type, res_last = self.__get_rres(tmpTA_BAS, aResultLast)

        self.OnUpdate(ta_type, res_pre, res_last)

    def TACallBack_OnRcvDone(self, sender, aResult):
        if aResult != None:
            if aResult.Count == 0:
                return

            tmpTA_BAS = sender
            ta_type = None
            res_rcvs = []
            for x in aResult:
                ta_type, res_rcv = self.__get_rres(tmpTA_BAS, x)
                res_rcvs.append(res_rcv)

            self.OnRcvDone(ta_type, res_rcvs)
    def SubTA(self, k_config):
        fTAMap = TechAnalysisAPI.mapTAParam()
        tmpSubTA = TechAnalysisAPI.TSubTARec()
        tmpSubTA.ProdID = k_config.ProdID
        tmpSubTA.NK = k_config.NK
        tmpSubTA.TA_Type = k_config.TA_Type
        tmpSubTA.ParamObj = fTAMap[tmpSubTA.TA_Type].GetParamClass()
        tmpSubTA.PROC_CallBack_Update = TechAnalysisAPI.OnUpdateHandler(self.TACallBack_OnUpdate)
        tmpSubTA.PROC_CallBack_RcvDone = TechAnalysisAPI.OnRcvDoneHandler(self.TACallBack_OnRcvDone)
        tmpSubTA.DateBegin = k_config.DateBegin
        flag, errmsg = self.fTechAnalysisAPI.SubTA(tmpSubTA, "")
        if not flag:
            print(f'error: {errmsg}')

    def UnSubTA(self, k_config):
        fTAMap = TechAnalysisAPI.mapTAParam()
        tmpUnSubTA = TechAnalysisAPI.TUnSubTARec()
        tmpUnSubTA.ProdID = k_config.ProdID
        tmpUnSubTA.NK = k_config.NK
        tmpUnSubTA.TA_Type = k_config.TA_Type
        tmpUnSubTA.ParamObj = fTAMap[tmpUnSubTA.TA_Type].GetParamClass()

        flag, errmsg = self.fTechAnalysisAPI.UnSubTA(tmpUnSubTA, "")
        if not flag:
            print(f'error: {errmsg}')

    def GetHisBS_Stock(self, ProdID, Date):
        datetime_value = datetime.strptime(Date, '%Y%m%d')
        print(datetime_value)
        print(datetime.now())
        if datetime_value + timedelta(days=1) >= datetime.now():
            return None, '不能回補當天'

        tSubBSRec = TechAnalysisAPI.TSubBSRec()
        tSubBSRec.ProdID = ProdID
        tSubBSRec.Date = Date

        flag, lsBS, aErrMsg = self.fTechAnalysisAPI.GetHisBS_Stock(tSubBSRec, None, "")
        if flag:
            lsbss = []
            for x in lsBS:
                tk_bar_rec = TBSRec(x.Prod, x.Sequence, float(str(x.Match_Time)), float(str(x.Match_Price)), \
                                    x.Match_Quantity, x.Match_Volume, x.Is_TryMatch, x.BS, \
                                    float(str(x.BP_1_Pre)), float(str(x.SP_1_Pre)))

                lsbss.append(tk_bar_rec)
            return lsbss, aErrMsg
        else:
            return None, 'api錯誤'

    def Login(self, userid, password):
        print(self.fTechAnalysisAPI.Login(userid, password))

    @staticmethod        
    def get_k_setting(product, ta_type, nk_Kind, date):
        ProdID = product
        STA_Type = ta_type
        SNK = nk_Kind
        DateBegin = date

        NK = TechAnalysisAPI.eNK_Kind.K_1m
        if SNK == eNK_Kind.K_1m:
            NK = TechAnalysisAPI.eNK_Kind.K_1m
        elif SNK == eNK_Kind.K_3m:
            NK = TechAnalysisAPI.eNK_Kind.K_3m
        elif SNK == eNK_Kind.K_5m:
            NK = TechAnalysisAPI.eNK_Kind.K_5m
        elif SNK == eNK_Kind.DAY:
            NK = TechAnalysisAPI.eNK_Kind.DAY

        TA_Type = TechAnalysisAPI.eTA_Type.SMA
        if ta_type == eTA_Type.SMA:
            TA_Type = TechAnalysisAPI.eTA_Type.SMA
        elif STA_Type == eTA_Type.EMA:
            TA_Type = TechAnalysisAPI.eTA_Type.EMA
        elif STA_Type == eTA_Type.WMA:
            TA_Type = TechAnalysisAPI.eTA_Type.WMA
        elif STA_Type == eTA_Type.SAR:
            TA_Type = TechAnalysisAPI.eTA_Type.SAR
        elif STA_Type == eTA_Type.RSI:
            TA_Type = TechAnalysisAPI.eTA_Type.RSI
        elif STA_Type == eTA_Type.MACD:
            TA_Type = TechAnalysisAPI.eTA_Type.MACD
        elif STA_Type == eTA_Type.KD:
            TA_Type = TechAnalysisAPI.eTA_Type.KD
        elif STA_Type == eTA_Type.CDP:
            TA_Type = TechAnalysisAPI.eTA_Type.CDP
        elif STA_Type == eTA_Type.BBands:
            TA_Type = TechAnalysisAPI.eTA_Type.BBands

        return k_settnig(ProdID, NK, TA_Type, DateBegin)
    