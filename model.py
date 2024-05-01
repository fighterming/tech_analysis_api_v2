from dataclasses import dataclass, field
from enum import Enum
from decimal import Decimal

class eTA_Type(Enum):
    SMA = 0
    WMA = 1
    EMA  = 2
    KD = 3
    MACD = 4
    SAR = 5
    RSI = 6
    CDP = 7
    BBands = 8
    
class eNK_Kind(Enum):
    DAY = 0,
    K_1m = 1
    K_3m = 3
    K_5m = 5

class eRaiseFall(Enum):
    Raise = 0
    Fall = 1

@dataclass
class TKBarRec:
    Date: str
    Product: str
    TimeSn:int
    TimeSn_Dply: int
    Quantity: int
    Volume: int
    OPrice: float
    HPrice: float
    LPrice: float
    CPrice: float

@dataclass
class TBSRec:
    Prod: str
    Sequence: int
    Match_Time: float
    Match_Price: float
    Match_Quantity: int
    Match_Volume: int
    Is_TryMatch: bool
    BS: int
    BP_1_Pre: float
    SP_1_Pre: float

@dataclass
class ta_sma():
    KBar: TKBarRec
    Value: float

@dataclass
class ta_ema():
    KBar: TKBarRec
    Value: float

@dataclass
class ta_wma():
    KBar: TKBarRec
    Value: float

@dataclass
class ta_sar():
    KBar: TKBarRec
    SAR: float
    EPh: float
    EPl: float
    AF: float
    RaiseFall: eRaiseFall

@dataclass
class ta_rsi():
    KBar: TKBarRec
    RSI: float
    UpDn: float
    UpAvg: float
    DnAvg: float

@dataclass
class ta_macd():
    KBar: TKBarRec
    DIF: float
    OSC: float

@dataclass
class ta_kd():
    KBar: TKBarRec
    K: float
    D: float

@dataclass
class ta_cdp():
    KBar: TKBarRec
    CDP: float
    AH: float
    NH: float
    AL: float
    NL: float

@dataclass
class ta_bbands():
    KBar: TKBarRec
    MA: Decimal#中軌
    UB2: Decimal#上軌
    LB2: Decimal#下軌

class k_settnig:
    def __init__(self, ProdID, NK, TA_Type, DateBegin):
        self.ProdID = ProdID
        self.NK = NK
        self.TA_Type = TA_Type
        self.DateBegin = DateBegin