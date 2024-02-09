from typing import List
import numpy as np

_V2X_FRAMENUM = "FRAMENUM"
_V2X_SUBFRAMENUM = "SUBFRAMENUM"
_V2X_SLOTNUM = "SLOTNUM"
_V2X_NUMEROLOGY = "NUMEROLOGY"
_V2X_DSTL2ID = "DSTL2ID"
_V2X_NDI = "NDI"
_V2X_RV = "RV"
_V2X_PRIORITY = "PRIORITY"
_V2X_SLRLCPDUINFO = "SLRLCPDUINFO"
_V2X_MCS = "MCS"
_V2X_NUMSLPSCCHRBS = "NUMSLPSCCHRBS"
_V2X_SLPSCCHSYMSTART = "SLPSCCHSYMSTART"
_V2X_SLPSCCHSYMLENGTH = "SLPSCCHSYMLENGTH"
_V2X_SLPSSCHSYMSTART = "SLPSSCHSYMSTART"
_V2X_SLPSSCHSYMLENGTH = "SLPSSCHSYMLENGTH"
_V2X_SLPSSCHSUBCHSTART = "SLPSSCHSUBCHSTART"
_V2X_SLPSSCHSUBCHLENGTH = "SLPSSCHSUBCHLENGTH"
_V2X_MAXNUMPERRESERVE = "MAXNUMPERRESERVE"
_V2X_TXSCI1A = "TXSCI1A"
_V2X_SLOTNUMIND = "SLOTNUMIND"



class SlRlcPduInfo:
    def __init__(self, lcid = 0, size = 0):
        self.lcid = lcid
        self.size = size

    def is_valid(self):
        return True
    
    def to_dict_c(self):
        return {
            "lcid":self.lcid,
            "size": self.size
        }


class SingleScheduling:
    def __init__(self, m_frameNum = 0, m_subframeNum = 0, 
                 m_slotNum = 0, m_numerology = -1, 
                 dstL2Id = int(np.iinfo(np.uint32).max), ndi = int(np.iinfo(np.uint8).max), 
                 rv = int(np.iinfo(np.uint8).max), priority = int(np.iinfo(np.uint8).max), 
                 slRlcPduInfo: List[SlRlcPduInfo] = [], mcs = int(np.iinfo(np.uint16).max), 
                numSlPscchRbs = int(np.iinfo(np.uint16).max), 
                slPscchSymStart = int(np.iinfo(np.uint16).max), 
                slPscchSymLength = int(np.iinfo(np.uint16).max), 
                slPsschSymStart = int(np.iinfo(np.uint16).max), 
                slPsschSymLength = int(np.iinfo(np.uint16).max), slPsschSubChStart = int(np.iinfo(np.uint16).max), 
                slPsschSubChLength = int(np.iinfo(np.uint16).max), maxNumPerReserve = int(np.iinfo(np.uint16).max), 
                txSci1A: bool=False, slotNumInd =  0):
        self._m_frameNum = m_frameNum
        self._m_subframeNum = m_subframeNum
        self._m_slotNum = m_slotNum
        self._m_numerology = m_numerology
        self._dstL2Id = dstL2Id
        self._ndi = ndi
        self._rv = rv
        self._priority = priority
        self._slRlcPduInfo: List[SlRlcPduInfo] = slRlcPduInfo
        self._mcs = mcs
        self._numSlPscchRbs = numSlPscchRbs
        self._slPscchSymStart = slPscchSymStart
        self._slPscchSymLength = slPscchSymLength
        self._slPsschSymStart = slPsschSymStart
        self._slPsschSymLength = slPsschSymLength
        self._slPsschSubChStart = slPsschSubChStart
        self._slPsschSubChLength = slPsschSubChLength
        self._maxNumPerReserve = maxNumPerReserve
        self._txSci1A = txSci1A
        self._slotNumInd = slotNumInd

    def is_valid(self):
        return all( [_slRlcPduInfo.is_valid() for _slRlcPduInfo in self.slRlcPduInfo]) & True

    def to_dict(self):
        return {_V2X_FRAMENUM: self.m_frameNum,
                _V2X_SUBFRAMENUM: self.m_subframeNum,
                _V2X_SLOTNUM: self.m_slotNum,
                _V2X_NUMEROLOGY: self.m_numerology,
                _V2X_DSTL2ID: self.dstL2Id,
                _V2X_NDI: self.ndi,
                _V2X_RV: self.rv,
                _V2X_PRIORITY: self.priority,
                _V2X_SLRLCPDUINFO: [_slRlcPduInfo.to_dict() for _slRlcPduInfo in self.slRlcPduInfo],
                _V2X_MCS: self.mcs,
                _V2X_NUMSLPSCCHRBS: self.numSlPscchRbs,
                _V2X_SLPSCCHSYMSTART: self.slPscchSymStart,
                _V2X_SLPSCCHSYMLENGTH: self.slPscchSymLength,
                _V2X_SLPSSCHSYMSTART: self.slPsschSymStart,
                _V2X_SLPSSCHSYMLENGTH: self.slPsschSymLength,
                _V2X_SLPSSCHSUBCHSTART: self.slPsschSubChStart,
                _V2X_SLPSSCHSUBCHLENGTH: self.slPsschSubChLength,
                _V2X_MAXNUMPERRESERVE: self.maxNumPerReserve,
                _V2X_TXSCI1A: self.txSci1A,
                _V2X_SLOTNUMIND: self.slotNumInd}
    
    def to_dict_c(self):
        return {"m_frameNum": self._m_frameNum,
                "m_subframeNum": self._m_subframeNum,
                "m_slotNum": self._m_slotNum,
                "m_numerology": self._m_numerology,
                "dstL2Id": self._dstL2Id,
                "ndi": self._ndi,
                "rv": self._rv,
                "priority": self._priority,
                "slRlcPduInfo": [_slRlcPduInfo.to_dict_c() for _slRlcPduInfo in self._slRlcPduInfo],
                "mcs": self._mcs,
                "numSlPscchRbs": self._numSlPscchRbs,
                "slPscchSymStart": self._slPscchSymStart,
                "slPscchSymLength": self._slPscchSymLength,
                "slPsschSymStart": self._slPsschSymStart,
                "slPsschSymLength": self._slPsschSymLength,
                "slPsschSubChStart": self._slPsschSubChStart,
                "slPsschSubChLength": self._slPsschSubChLength,
                "maxNumPerReserve": self._maxNumPerReserve,
                "txSci1A": self._txSci1A,
                "slotNumInd": self._slotNumInd}

    def __str__(self) -> str:
        return str(self._m_frameNum) + "," + str(self._m_subframeNum) + "," + str(self._m_slotNum) + "," + \
              str(self._m_numerology) + "," + str(self._dstL2Id) + "," + str(self._ndi) + "," + str(self._rv) + \
                "," + str(self._priority) + "," + str(self._slRlcPduInfo) + "," + str(self._mcs) + \
                "," + str(self._numSlPscchRbs) + "," + str(self._slPscchSymStart) + "," + str(self._slPscchSymLength) + \
                "," + str(self._slPsschSymStart) + "," + str(self._slPsschSymLength) + "," + str(self._slPsschSubChStart) + \
                "," + str(self._slPsschSubChLength) + "," + str(self._maxNumPerReserve) + "," + str(self._txSci1A) + "," + str(self._slotNumInd)

    def str_var_order() -> str:
        return  _V2X_FRAMENUM + "," + \
                _V2X_SUBFRAMENUM + "," + \
                _V2X_SLOTNUM + "," + \
                _V2X_NUMEROLOGY + "," + \
                _V2X_DSTL2ID + "," + \
                _V2X_NDI + "," + \
                _V2X_RV + "," + \
                _V2X_PRIORITY + "," + \
                _V2X_SLRLCPDUINFO + "," + \
                _V2X_MCS + "," + \
                _V2X_NUMSLPSCCHRBS + "," + \
                _V2X_SLPSCCHSYMSTART + "," + \
                _V2X_SLPSCCHSYMLENGTH + "," + \
                _V2X_SLPSSCHSYMSTART + "," + \
                _V2X_SLPSSCHSYMLENGTH + "," + \
                _V2X_SLPSSCHSUBCHSTART + "," + \
                _V2X_SLPSSCHSUBCHLENGTH + "," + \
                _V2X_MAXNUMPERRESERVE + "," + \
                _V2X_TXSCI1A + "," + \
                _V2X_SLOTNUMIND

    def add_sl_rlc_pdu_info(self, lcid = 0, size = 0):
        self._slRlcPduInfo.append(SlRlcPduInfo(lcid=lcid, size=size))


class UserScheduling:
    def __init__(self, ue_id) -> None:
        self.ue_id = ue_id
        self.single_scheduling:List[SingleScheduling] = []
        
    def add_single_scheduling(self, single_sched: SingleScheduling):
        self.single_scheduling.append(single_sched)

    def to_dict_c(self):
        return{
            "ue_id": self.ue_id,
            "userScheduling" : [_singleSched.to_dict_c() for _singleSched in self.single_scheduling]
            }