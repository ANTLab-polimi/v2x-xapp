from typing import List
import numpy as np
import time
import logging

_V2X_FRAMENUM = "frameNum"
_V2X_SUBFRAMENUM = "subframeNum"
_V2X_SLOTNUM = "slotNum"
_V2X_NUMEROLOGY = "numerology"
_V2X_DSTL2ID = "dstl2id"
_V2X_NDI = "ndi"
_V2X_RV = "rv"
_V2X_PRIORITY = "priority"
_V2X_SLRLCPDUINFO = "slRlcPduInfo"
_V2X_MCS = "mcs"
_V2X_NUMSLPSCCHRBS = "numSlPscchRbs"
_V2X_SLPSCCHSYMSTART = "slPscchSymStart"
_V2X_SLPSCCHSYMLENGTH = "slPscchSymLength"
_V2X_SLPSSCHSYMSTART = "slPsschSymStart"
_V2X_SLPSSCHSYMLENGTH = "slPsschSymLength"
_V2X_SLPSSCHSUBCHSTART = "slPsschSubchStart"
_V2X_SLPSSCHSUBCHLENGTH = "slPsschSubchLength"
_V2X_MAXNUMPERRESERVE = "maxNumPerReserve"
_V2X_TXSCI1A = "txSci1a"
_V2X_SLOTNUMIND = "slotNumInd"
_V2X_UE_ID = "ue_id"
_V2X_CRESELCOUNTER = "cReselCounter"
_V2X_SLRESORESELCOUNTER = "slResoReselCounter"
_V2X_PREVSLRESORESELCOUNTER = "prevSlResoReselCounter"
_V2X_NRSLHARQID = "nrSlHarqId"
_V2X_NSELECTED = "nSelected"
_V2X_TBTXCOUNTER = "tbTxCounter"
_V2X_USERALLOCATIONSIZE = "userAllocationSize"
_V2X_USERSCHEDULING = "userScheduling"
_V2X_LCID = "lcid"
_V2X_SIZE = "size"
_V2X_SOURCE_UE_ID = "source_ue_id"
_V2X_SOURCE_DESTINATION_USER_SCHEDULING = "destination_scheduling"
_V2X_PLMN = "plmn"
_V2X_TIME = "time"


class SlRlcPduInfo:
    def __init__(self, lcid = 0, size = 0, from_dict=None):
        self.lcid = lcid
        self.size = size
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()

    def is_valid(self):
        return True
    
    def to_dict_c(self):
        return {
            _V2X_LCID: self.lcid,
            _V2X_SIZE: self.size
        }
    def __str__(self) -> str:
        return str(self.lcid) + "," + str(self.size)
    
    def str_var_order() -> str:
        return  _V2X_LCID + "," + _V2X_SIZE
    
    def _from_dict(self):
        self.lcid = self._from_dict_data[_V2X_LCID]
        self.size = self._from_dict_data[_V2X_SIZE]

    def __eq__(self, __value: object) -> bool:
        return (self.lcid == __value.lcid) & (self.size == __value.lcid)


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
                slPsschSymLength = int(np.iinfo(np.uint16).max), 
                slPsschSubChStart = int(np.iinfo(np.uint16).max), 
                slPsschSubChLength = int(np.iinfo(np.uint16).max), 
                maxNumPerReserve = int(np.iinfo(np.uint16).max), 
                txSci1A: bool=False, slotNumInd =  0, 
                from_dict=None):
        self._m_frameNum = m_frameNum
        self._m_subframeNum = m_subframeNum
        self._m_slotNum = m_slotNum
        self._m_numerology = m_numerology
        self._dstL2Id = dstL2Id
        self._ndi = ndi
        self._rv = rv
        self._priority = priority
        self.slRlcPduInfo: List[SlRlcPduInfo] = slRlcPduInfo
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
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()

    def is_valid(self):
        return all( [_slRlcPduInfo.is_valid() for _slRlcPduInfo in self.slRlcPduInfo]) & True

    def to_dict(self):
        return {_V2X_FRAMENUM: self._m_frameNum,
                _V2X_SUBFRAMENUM: self._m_subframeNum,
                _V2X_SLOTNUM: self._m_slotNum,
                _V2X_NUMEROLOGY: self._m_numerology,
                _V2X_DSTL2ID: self._dstL2Id,
                _V2X_NDI: self._ndi,
                _V2X_RV: self._rv,
                _V2X_PRIORITY: self._priority,
                _V2X_SLRLCPDUINFO: [_slRlcPduInfo.to_dict() for _slRlcPduInfo in self.slRlcPduInfo],
                _V2X_MCS: self._mcs,
                _V2X_NUMSLPSCCHRBS: self._numSlPscchRbs,
                _V2X_SLPSCCHSYMSTART: self._slPscchSymStart,
                _V2X_SLPSCCHSYMLENGTH: self._slPscchSymLength,
                _V2X_SLPSSCHSYMSTART: self._slPsschSymStart,
                _V2X_SLPSSCHSYMLENGTH: self._slPsschSymLength,
                _V2X_SLPSSCHSUBCHSTART: self._slPsschSubChStart,
                _V2X_SLPSSCHSUBCHLENGTH: self._slPsschSubChLength,
                _V2X_MAXNUMPERRESERVE: self._maxNumPerReserve,
                _V2X_TXSCI1A: self._txSci1A,
                _V2X_SLOTNUMIND: self._slotNumInd}
    
    def to_dict_c(self):
        logger = logging.getLogger('')
        # logger.debug("ndi to_dict_c in Single Scheduling " + str(self._ndi))
        return {"m_frameNum": self._m_frameNum,
                "m_subframeNum": self._m_subframeNum,
                "m_slotNum": self._m_slotNum,
                "m_numerology": self._m_numerology,
                "dstL2Id": self._dstL2Id,
                "ndi": self._ndi,
                "rv": self._rv,
                "priority": self._priority,
                "slRlcPduInfo": [_slRlcPduInfo.to_dict_c() for _slRlcPduInfo in self.slRlcPduInfo],
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

    def _from_dict(self):
        logger = logging.getLogger('')
        self._m_frameNum = self._from_dict_data["m_frameNum"]
        self._m_subframeNum = self._from_dict_data["m_subframeNum"]
        self._m_slotNum = self._from_dict_data["m_slotNum"]
        self._m_numerology = self._from_dict_data["m_numerology"]
        self._dstL2Id = self._from_dict_data["dstL2Id"]
        self._ndi = self._from_dict_data["ndi"]
        # logger.debug("ndi from dict in Single Scheduling " + str(self._ndi))
        self._rv = self._from_dict_data["rv"]
        self._priority = self._from_dict_data["priority"]
        self.slRlcPduInfo = [SlRlcPduInfo(from_dict=_ue_report) for _ue_report in self._from_dict_data["slRlcPduInfo"]]
        self._mcs = self._from_dict_data["mcs"]
        self._numSlPscchRbs = self._from_dict_data["numSlPscchRbs"]
        self._slPscchSymStart = self._from_dict_data["slPscchSymStart"]
        self._slPscchSymLength = self._from_dict_data["slPscchSymLength"]
        self._slPsschSymStart = self._from_dict_data["slPsschSymStart"]
        self._slPsschSymLength = self._from_dict_data["slPsschSymLength"]
        self._slPsschSubChStart = self._from_dict_data["slPsschSubChStart"]
        self._slPsschSubChLength = self._from_dict_data["slPsschSubChLength"]
        self._maxNumPerReserve = self._from_dict_data["maxNumPerReserve"]
        self._txSci1A = self._from_dict_data["txSci1A"]
        self._slotNumInd = self._from_dict_data["slotNumInd"]

    def single_line_str(self)-> str:
        return str(self._m_frameNum) + "," + str(self._m_subframeNum) + "," + str(self._m_slotNum) + "," + \
              str(self._m_numerology) + "," + str(self._dstL2Id) + "," + str(self._ndi) + "," + str(self._rv) + \
                "," + str(self._priority) + "," + str(self._mcs) + \
                "," + str(self._numSlPscchRbs) + "," + str(self._slPscchSymStart) + "," + str(self._slPscchSymLength) + \
                "," + str(self._slPsschSymStart) + "," + str(self._slPsschSymLength) + "," + str(self._slPsschSubChStart) + \
                "," + str(self._slPsschSubChLength) + "," + str(self._maxNumPerReserve) + "," + str(self._txSci1A) + \
                "," + str(self._slotNumInd)

    def __str__(self) -> str:
        return self.single_line_str() + "," + str([str(_rlc_pdu_info) for _rlc_pdu_info in self.slRlcPduInfo])

    def str_var_order_single_line()->str:
        return  _V2X_FRAMENUM + "," + \
                _V2X_SUBFRAMENUM + "," + \
                _V2X_SLOTNUM + "," + \
                _V2X_NUMEROLOGY + "," + \
                _V2X_DSTL2ID + "," + \
                _V2X_NDI + "," + \
                _V2X_RV + "," + \
                _V2X_PRIORITY + "," + \
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

    def str_var_order() -> str:
        return SingleScheduling.str_var_order_single_line() + "," + _V2X_SLRLCPDUINFO

    def add_sl_rlc_pdu_info(self, lcid = 0, size = 0):
        self.slRlcPduInfo.append(SlRlcPduInfo(lcid=lcid, size=size))

    def change_reference_slot(self, new_frame: int, new_subframe: int, new_slot: int, ndi: int):
        # logger = logging.getLogger('')
        # logger.debug(f"New frame {new_frame} {new_subframe} {new_slot} {ndi}")
        self._m_frameNum = new_frame
        self._m_subframeNum = new_subframe
        self._m_slotNum = new_slot
        self._ndi = ndi

    def __eq__(self, __value: object) -> bool:
        return ((self._m_frameNum == __value._m_frameNum) & \
        (self._m_subframeNum == __value._m_subframeNum) & \
        (self._m_slotNum == __value._m_slotNum) & \
        (self._m_numerology == __value._m_numerology) & \
        (self._dstL2Id == __value._dstL2Id) & \
        (self._ndi == __value._ndi) & \
        (self._rv == __value._rv) & \
        (self._priority == __value._priority) & \
        (self.slRlcPduInfo == __value.slRlcPduInfo) & \
        (self._mcs == __value._mcs) & \
        (self._numSlPscchRbs == __value._numSlPscchRbs) & \
        (self._slPscchSymStart == __value._slPscchSymStart) & \
        (self._slPscchSymLength == __value._slPscchSymLength) & \
        (self._slPsschSymStart == __value._slPsschSymStart) & \
        (self._slPsschSymLength == __value._slPsschSymLength) & \
        (self._slPsschSubChStart == __value._slPsschSubChStart) & \
        (self._slPsschSubChLength == __value._slPsschSubChLength) & \
        (self._maxNumPerReserve == __value._maxNumPerReserve) & \
        (self._txSci1A == __value._txSci1A) & \
        (self._slotNumInd == __value._slotNumInd))


class UserScheduling:
    def __init__(self, ue_id, 
                 cReselCounter =  int(np.iinfo(np.uint16).max), 
                 slResoReselCounter = int(np.iinfo(np.uint8).max), 
                 prevSlResoReselCounter = int(np.iinfo(np.uint8).max), 
                 nrSlHarqId = int(np.iinfo(np.uint8).max), 
                 nSelected = int(np.iinfo(np.uint8).max), 
                 tbTxCounter = int(np.iinfo(np.uint8).max), 
                 from_dict=None) -> None:
        self.ue_id = ue_id
        self.cReselCounter = cReselCounter
        self.slResoReselCounter = slResoReselCounter
        self.prevSlResoReselCounter = prevSlResoReselCounter
        self.nrSlHarqId = nrSlHarqId
        self.nSelected = nSelected
        self.tbTxCounter = tbTxCounter
        self.user_scheduling:List[SingleScheduling] = []
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        
    def add_single_scheduling(self, single_sched: SingleScheduling):
        self.user_scheduling.append(single_sched)

    def to_dict_c(self):
        return{
            "ue_id": self.ue_id,
            "cReselCounter" : self.cReselCounter,
            "slResoReselCounter" : self.slResoReselCounter,
            "prevSlResoReselCounter" : self.prevSlResoReselCounter,
            "nrSlHarqId" : self.nrSlHarqId,
            "nSelected" : self.nSelected,
            "tbTxCounter" : self.tbTxCounter,
            "userScheduling" : [_singleSched.to_dict_c() for _singleSched in self.user_scheduling]
            }

    def _from_dict(self):
        self.ue_id = self._from_dict_data["ue_id"]
        self.cReselCounter = self._from_dict_data["cReselCounter"]
        self.slResoReselCounter = self._from_dict_data["slResoReselCounter"]
        self.prevSlResoReselCounter = self._from_dict_data["prevSlResoReselCounter"]
        self.nrSlHarqId = self._from_dict_data["nrSlHarqId"]
        self.nSelected = self._from_dict_data["nSelected"]
        self.tbTxCounter = self._from_dict_data["tbTxCounter"]
        self.user_scheduling = [SingleScheduling(from_dict=_ue_report) for _ue_report in self._from_dict_data["userScheduling"]]
    
    def __str__(self) -> str:
        return self.single_line_str() + "," + str([str(_user_sched) for _user_sched in  self.user_scheduling])
    
    def single_line_str(self)-> str:
        return str(self.ue_id) + "," + str(self.cReselCounter) + "," + str(self.slResoReselCounter) + "," + \
              str(self.prevSlResoReselCounter) + "," + str(self.nrSlHarqId) + "," + str(self.nSelected) + \
                "," + str(self.tbTxCounter)
    
    def str_var_order_single_line()->str:
        return  _V2X_UE_ID + "," + \
                _V2X_CRESELCOUNTER + "," + \
                _V2X_SLRESORESELCOUNTER + "," + \
                _V2X_PREVSLRESORESELCOUNTER + "," + \
                _V2X_NRSLHARQID + "," + \
                _V2X_NSELECTED + "," + \
                _V2X_TBTXCOUNTER

    def str_var_order() -> str:
        return  UserScheduling.str_var_order_single_line() + "," + _V2X_USERSCHEDULING
    
    def __eq__(self, __value: object) -> bool:
        return ((self.ue_id == __value.ue_id) & \
        (self.cReselCounter == __value.cReselCounter) & \
        (self.slResoReselCounter == __value.slResoReselCounter) & \
        (self.prevSlResoReselCounter == __value.prevSlResoReselCounter) & \
        (self.nrSlHarqId == __value.nrSlHarqId) & \
        (self.nSelected == __value.nSelected) & \
        (self.tbTxCounter == __value.tbTxCounter) & \
        (self.user_scheduling == __value.user_scheduling))


class SourceUserScheduling:
    def __init__(self, ue_id, from_dict=None) -> None:
        self.ue_id = ue_id
        self.destination_scheduling:List[UserScheduling] = []
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        
    def add_dest_user(self, dest_sched: UserScheduling):
        self.destination_scheduling.append(dest_sched) 

    def to_dict_c(self):
        return{
            "source_id": self.ue_id,
            "destScheduling" : [_destSched.to_dict_c() for _destSched in self.destination_scheduling]
            }
    
    def _from_dict(self):
        self.ue_id = self._from_dict_data["source_id"]
        self.destination_scheduling = [UserScheduling(-1, from_dict=_ue_report) for _ue_report in self._from_dict_data["destScheduling"]]
    
    def __str__(self) -> str:
        return str(self.ue_id) + "," + str([str(_dest_sched) for _dest_sched in self.destination_scheduling])

    def str_var_order() -> str:
        return _V2X_SOURCE_UE_ID + "," + _V2X_SOURCE_DESTINATION_USER_SCHEDULING

    def get_field_names():
        return _V2X_TIME + "," + _V2X_PLMN + "," +_V2X_SOURCE_UE_ID + "," + \
            UserScheduling.str_var_order_single_line() + "," + \
            SingleScheduling.str_var_order_single_line() + "," + \
            SlRlcPduInfo.str_var_order()
    
    def __eq__(self, __value: object) -> bool:
        return (self.ue_id == __value.ue_id) & (self.destination_scheduling == __value.destination_scheduling)
    
    def write_data_to_file(self, filename = "/home/traces/ric_messages.txt", plmn = "111"):
        # open the file and write the data in recursive mode
        logger = logging.getLogger('')
        with open(filename, mode="a+") as file:
            for _dest_sched in self.destination_scheduling:
                _dest_sched_str = _dest_sched.single_line_str()
                for _user_sched in _dest_sched.user_scheduling:
                    _user_sched_str = _user_sched.single_line_str()
                    for _rlc_pdu in _user_sched.slRlcPduInfo:
                        _rlc_pdu_str = str(_rlc_pdu)
                        _single_row_str =   str(self.ue_id) + "," + \
                                            _dest_sched_str + "," + \
                                            _user_sched_str + "," + \
                                            _rlc_pdu_str
                        # logger.debug(f"Writing to file: {_single_row_str}")
                        file.write(str(time.time())+ "," + plmn + "," + _single_row_str + "\n")
                        

    
