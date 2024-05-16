import xml
import logging
from typing import Mapping, List, Union, Tuple
import xmltodict
from functools import reduce
import operator
import re
import pickle
import datetime
from ctrl_msg_encoder_decoder import RicControlMessageEncoder
from numpy import iinfo as c_types_info
from numpy import uint8, uint16, uint32
import os
from operator import itemgetter

# _MAIN_TAG = ["E2AP-PDU"]
_MAIN_TAG = ["message"]
_MESSAGE_PART = ['E2SM-KPM-IndicationMessage', 'indicationMessage-Format1']
_HEADER_PART = ['E2SM-KPM-IndicationHeader', 'indicationHeader-Format1']

_PM_CONTAINERS = ['pm-Containers']
_LIST_OF_MATCHED_UES = ['list-of-matched-UEs', 'PerUE-PM-Item']

_HEADER_COLLECTION_START_TIME = ['collectionStartTime']
_HEADER_CELL_ID = [ ['id-GlobalE2node-ID', 'gNB', 'global-gNB-ID', 'gnb-id', 'gnb-ID'],
                    ['id-GlobalE2node-ID', 'eNB', 'global-eNB-ID', 'eNB-ID', 'macro-eNB-ID'],
                    ['id-GlobalE2node-ID', 'ng-eNB', 'global-ng-eNB-ID', 'enb-id', 'enb-ID-longmacro'], ]
_HEADER_PLMN_ID = [ ['id-GlobalE2node-ID', 'gNB', 'global-gNB-ID', 'plmn-id'],
                    ['id-GlobalE2node-ID', 'eNB', 'global-eNB-ID', 'plmn-id'],
                    ['id-GlobalE2node-ID', 'eNB', 'global-eNB-ID', 'pLMN-Identity'],
                    ['id-GlobalE2node-ID', 'ng-eNB', 'global-ng-eNB-ID', 'plmn-id'], ]

_CUCP_PM_REPORTS_NUMBER = ['pm-Containers', 'PM-Containers-Item', 'performanceContainer',
                           'oCU-CP', 'cu-CP-Resource-Status', 'numberOfActive-UEs']

_PM_CONTAINERS_UE_ID = ['ueId']
_PM_CONTAINERS_LIST_PM_INFORMATION = ['list-of-PM-Information', 'PM-Info-Item']
_PM_INFO_ITEM_TYPE = ['pmType', 'measName']
_PM_INFO_ITEM_VALUE = ['pmVal']


_GENERATING_MILLICAR_NODE_ID = "UEID.Rnti"
_GENERATING_MILLICAR_IMSI = "UEID.Imsi"
_GENERATING_MILLICAR_SINGLE_REPORT = "SingleReport"
_GENERATING_MILLICAR_NODE_POSITION_X = "PosX"
_GENERATING_MILLICAR_NODE_POSITION_Y = "PosY"
_GENERATING_MILLICAR_FRAME = "Frame"
_GENERATING_MILLICAR_SUBFRAME = "SubFrame"
_GENERATING_MILLICAR_SLOT = "Slot"
_GENERATING_MILLICAR_NS3_TIMESTAMP = "Timestamp"
_GENERATING_MILLICAR_NODE_RSRP_DBM = "RsrpdBm"

# sci header 
_SCI_HEADER_TOTAL_SUBCHANNELS = "TOTAL_SUBCHANNELS"
_SCI_HEADER_PRIORITY = "PRIORITY"
_SCI_HEADER_INDEXSTARTSUBCHANNEL = "INDEXSTARTSUBCHANNEL"
_SCI_HEADER_LENGTHSUBCHANNEL = "LENGTHSUBCHANNEL"
_SCI_HEADER_MCS = "MCS"
_SCI_HEADER_SLRESOURCERESERVEPERIOD = "SLRESOURCERESERVEPERIOD"
_SCI_HEADER_SLMAXNUMPERRESERVE = "SLMAXNUMPERRESERVE"
_SCI_HEADER_SLSCISTAGE2FORMAT = "SLSCISTAGE2FORMAT"
_SCI_HEADER_INDEXSTARTSBCHRETX1 = "INDEXSTARTSBCHRETX1"
_SCI_HEADER_INDEXSTARTSBCHRETX2 = "INDEXSTARTSBCHRETX2"
_SCI_HEADER_GAPRETX1 = "GAPRETX1"
_SCI_HEADER_GAPRETX2 = "GAPRETX2"
#sci tag
_SCI_TAG_FRAMENUM = "FRAMENUM"
_SCI_TAG_SUBFRAMENUM = "SUBFRAMENUM"
_SCI_TAG_SLOTNUM = "SLOTNUM"
_SCI_TAG_NUMEROLOGY = "NUMEROLOGY"
_SCI_TAG_RNTI = "RNTI"
_SCI_TAG_SYMSTART = "SYMSTART"
_SCI_TAG_NUMSYM = "NUMSYM"
_SCI_TAG_TBSIZE = "TBSIZE"
_SCI_TAG_DSTL2ID = "DSTL2ID"

# Packet delays
_PACKET_DELAYS_ALL_USERS_ALL_CONNECTIONS = ['userBufferDelayList']
_PACKET_DELAYS_USER_ID =  ["v2xNodeId"]
_PACKET_DELAYS_USER_ALL_CONNECTIONS =  ['v2XBufferPacketDelaysList', 'v2XBufferPacketDelays']
# _PACKET_DELAYS_DELAY_INTERVAL_LIST = "v2XPacketDelayIntervalList"
_PACKET_DELAYS_DELAY_INTERVAL = ["v2XPacketDelayIntervalList", "v2XPacketDelayIntervalList"]
_PACKET_DELAYS_HARQ_BUFFER_SIZE = ["v2XPacketDelayIntervalList", "V2XHarqBufferSizeList"]
_PACKET_DELAYS_DELAY_INTERVAL_LOWER_INTERVAL = ["lowerInterval"]
_PACKET_DELAYS_DELAY_INTERVAL_UPPER_INTERVAL = ["upperInterval"]
_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS = ["numberOfPackets"]
_PACKET_DELAYS_DELAY_INTERVAL_RESERVATION_PERIOD = ["reservationPeriod"]
_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE = ["bufferSize"]

_SCI_MESSAGE_V2X = ["userReceivedSciMessages", 'v2XSciMessageSingleItem', 'V2XSciMessageItem']
_SCI_HEADER_V2X = ["header"]
_SCI_TAG_V2X = ["tag"]
_SCI_RSRP = ["rsrp"]

_JSON_FRAME = "Frame"
_JSON_SUBFRAME = "Subframe"
_JSON_SLOT = "Slot"
_JSON_NS3_TIMESTAMP = "Timestamp"

_JSON_SINR = "sinr"
_JSON_MCS = "mcs"
_JSON_IMSI = "imsi"
_JSON_POSITION_X = "PositionX"
_JSON_POSITION_Y = "PositionY"
_JSON_SOURCE_RNTI = "SourceRnti"
_JSON_SOURCE_IMSI = "SourceImsi"
_JSON_SOURCE_UE_ID = "SourceUeId"
_JSON_SOURCE_SCI_HEADER = "SourceSciHeader"
_JSON_SOURCE_SCI_TAG = "SourceSciTag"
# _JSON_CELL_ID = "cellId"
_JSON_PEER_RNTI = "PeerRnti"
_JSON_COLLECTION_TIME = "CollectionTime"
_JSON_ALL_UE_REPORTS = "AllDataReports"
_JSON_PLMN = "Plmn"
_JSON_TIMESTAMP = 'time'

# Packet delays
_JSON_PACKET_DELAYS_USER_ID = "v2xNodeId"
_JSON_PACKET_DELAYS_ALL_USERS_ALL_CONNECTIONS = 'userBufferDelayList'
_JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS = 'V2XBufferPacketDelaysList'
# _PACKET_DELAYS_DELAY_INTERVAL_LIST = "v2XPacketDelayIntervalList"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_LIST = "v2XPacketDelayIntervalList"
_JSON_PACKET_DELAYS_DELAY_HARQ_BUFFER_SIZE_LIST = "v2XHarqBufferSizeList"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_LOWER_INTERVAL = "lowerInterval"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_UPPER_INTERVAL = "upperInterval"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS = "numberOfPackets"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_RESERVATION_PERIOD = "reservationPeriod"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE = "bufferSize"
_JSON_PACKET_DELAYS_DELAY_INTERVAL_HARQ_ID = "harqId"

# sci message 
_JSON_SCI_MESSAGES = "sciMessages"
_JSON_SCI_MESSAGE_HEADER = "header"
_JSON_SCI_MESSAGE_TAG = "tag"
_JSON_SCI_MESSAGE_RSRP = "rsrp"


class V2XSciTag:
    def __init__(self, buffer: str, decoder:RicControlMessageEncoder, from_dict=None):
        self._buffer = buffer
        self._decoder = decoder
        self._frameNum = 0
        self._subframeNum = 0
        self._slotNum = 0
        self._numerology = -1
        self._rnti = 0
        self._symStart = 0
        self._numSym = 0
        self._tbSize = 0
        self._dstL2Id = 0
        # decoding the tag buffer through the c libraries
        # self.decode_sci_tag()
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            # decoding the tag buffer through the c libraries
            self.decode_sci_tag()

    def decode_sci_tag(self):
        (frameNum, subframeNum, slotNum, numerology, 
            rnti, symStart, numSym, tbSize, dstL2Id) =self._decoder.decode_sci_tag(self._buffer.encode())
        self._frameNum = frameNum
        self._subframeNum = subframeNum
        self._slotNum = slotNum
        self._numerology = numerology
        self._rnti = rnti
        self._symStart = symStart
        self._numSym = numSym
        self._tbSize = tbSize
        self._dstL2Id = dstL2Id

    def _is_slot_valid(self):
        return not ((self._frameNum <= 0) & (self._subframeNum <= 0) & (self._slotNum <= 0))
    
    def _is_numerology_valid(self):
        return self._numerology > -1
    
    def _is_rnti_valid(self):
        return self._rnti>0

    def is_valid(self):
        return self._is_slot_valid() & self._is_numerology_valid() & self._is_rnti_valid()

    def to_dict(self):
        return {_SCI_TAG_FRAMENUM : self._frameNum,
                _SCI_TAG_SUBFRAMENUM : self._subframeNum,
                _SCI_TAG_SLOTNUM : self._slotNum,
                _SCI_TAG_NUMEROLOGY : self._numerology,
                _SCI_TAG_RNTI : self._rnti,
                _SCI_TAG_SYMSTART : self._symStart,
                _SCI_TAG_NUMSYM : self._numSym,
                _SCI_TAG_TBSIZE : self._tbSize,
                _SCI_TAG_DSTL2ID : self._dstL2Id}

    def _from_dict(self):
        self._frameNum = self._from_dict_data[_SCI_TAG_FRAMENUM]
        self._subframeNum = self._from_dict_data[_SCI_TAG_SUBFRAMENUM]
        self._slotNum = self._from_dict_data[_SCI_TAG_SLOTNUM]
        self._numerology = self._from_dict_data[_SCI_TAG_NUMEROLOGY]
        self._rnti = self._from_dict_data[_SCI_TAG_RNTI]
        self._symStart = self._from_dict_data[_SCI_TAG_SYMSTART]
        self._numSym = self._from_dict_data[_SCI_TAG_NUMSYM]
        self._tbSize = self._from_dict_data[_SCI_TAG_TBSIZE]
        self._dstL2Id = self._from_dict_data[_SCI_TAG_DSTL2ID]

    def __str__(self) -> str:
        return str(self._frameNum) + "," + str(self._subframeNum) + "," + str(self._slotNum) + "," + \
        str(self._numerology) + "," + str(self._rnti) + "," + str(self._symStart) + "," + \
        str(self._numSym) + "," + str(self._tbSize) + "," + str(self._dstL2Id)

    def str_var_order() -> str:
        return  _SCI_TAG_FRAMENUM + "," + \
                _SCI_TAG_SUBFRAMENUM + "," + \
                _SCI_TAG_SLOTNUM + "," + \
                _SCI_TAG_NUMEROLOGY + "," + \
                _SCI_TAG_RNTI + "," + \
                _SCI_TAG_SYMSTART + "," + \
                _SCI_TAG_NUMSYM + "," + \
                _SCI_TAG_TBSIZE + "," + \
                _SCI_TAG_DSTL2ID

class V2XSciHeader:
    def __init__(self, buffer: str, decoder:RicControlMessageEncoder, from_dict=None):
        self._buffer = buffer
        self._decoder = decoder
        self._total_subchannels = c_types_info(uint16).max
        self._priority = c_types_info(uint8).max
        self._indexStartSubChannel = c_types_info(uint8).max
        self._lengthSubChannel = c_types_info(uint8).max
        self._mcs = c_types_info(uint8).max
        self._slResourceReservePeriod = c_types_info(uint16).max
        self._slMaxNumPerReserve = c_types_info(uint8).max
        self._slSciStage2Format = c_types_info(uint8).max
        self._indexStartSbChReTx1 = c_types_info(uint8).max
        self._indexStartSbChReTx2 = c_types_info(uint8).max
        self._gapReTx1 = c_types_info(uint8).max
        self._gapReTx2 = c_types_info(uint8).max
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            # decoding the tag buffer through the c libraries
            self.decode_header_buffer()

    def decode_header_buffer(self):
        (_total_subchannels, _priority, _indexStartSubChannel, _lengthSubChannel, _mcs, 
            _slResourceReservePeriod, _slMaxNumPerReserve, _slSciStage2Format, 
            _indexStartSbChReTx1, _indexStartSbChReTx2, _gapReTx1, _gapReTx2) = self._decoder.decode_sci_header(self._buffer.encode())
        
        self._total_subchannels = _total_subchannels
        self._priority = _priority
        self._indexStartSubChannel = _indexStartSubChannel
        self._lengthSubChannel = _lengthSubChannel
        self._mcs = _mcs
        self._slResourceReservePeriod = _slResourceReservePeriod
        self._slMaxNumPerReserve = _slMaxNumPerReserve
        self._slSciStage2Format = _slSciStage2Format
        self._indexStartSbChReTx1 = _indexStartSbChReTx1
        self._indexStartSbChReTx2 = _indexStartSbChReTx2
        self._gapReTx1 = _gapReTx1
        self._gapReTx2 = _gapReTx2

    def _is_uint8_types_valid(self):
        return  (self._priority<c_types_info(uint8).max) & \
                (self._indexStartSubChannel < c_types_info(uint8).max) & \
                (self._lengthSubChannel < c_types_info(uint8).max) & \
                (self._mcs < c_types_info(uint8).max) & \
                (self._slMaxNumPerReserve < c_types_info(uint8).max) & \
                (self._slSciStage2Format < c_types_info(uint8).max) & \
                (self._indexStartSbChReTx1 < c_types_info(uint8).max) & \
                (self._indexStartSbChReTx2 < c_types_info(uint8).max) & \
                (self._gapReTx1 < c_types_info(uint8).max) & \
                (self._gapReTx2 < c_types_info(uint8).max)
    
    def _is_uint16_types_valid(self):
        return  (self._total_subchannels<c_types_info(uint16).max) & \
                (self._slResourceReservePeriod < c_types_info(uint16).max)
    
    def is_valid(self):
        return self._is_uint8_types_valid() & self._is_uint16_types_valid()

    def to_dict(self):
        return {_SCI_HEADER_TOTAL_SUBCHANNELS : self._total_subchannels,
                _SCI_HEADER_PRIORITY : self._priority,
                _SCI_HEADER_INDEXSTARTSUBCHANNEL : self._indexStartSubChannel,
                _SCI_HEADER_LENGTHSUBCHANNEL : self._lengthSubChannel,
                _SCI_HEADER_MCS : self._mcs,
                _SCI_HEADER_SLRESOURCERESERVEPERIOD : self._slResourceReservePeriod,
                _SCI_HEADER_SLMAXNUMPERRESERVE : self._slMaxNumPerReserve,
                _SCI_HEADER_SLSCISTAGE2FORMAT : self._slSciStage2Format,
                _SCI_HEADER_INDEXSTARTSBCHRETX1 : self._indexStartSbChReTx1,
                _SCI_HEADER_INDEXSTARTSBCHRETX2 : self._indexStartSbChReTx2,
                _SCI_HEADER_GAPRETX1 : self._gapReTx1,
                _SCI_HEADER_GAPRETX2 : self._gapReTx2}

    def _from_dict(self):
        self._total_subchannels = self._from_dict_data[_SCI_HEADER_TOTAL_SUBCHANNELS]
        self._priority = self._from_dict_data[_SCI_HEADER_PRIORITY]
        self._indexStartSubChannel = self._from_dict_data[_SCI_HEADER_INDEXSTARTSUBCHANNEL]
        self._lengthSubChannel = self._from_dict_data[_SCI_HEADER_LENGTHSUBCHANNEL]
        self._mcs = self._from_dict_data[_SCI_HEADER_MCS]
        self._slResourceReservePeriod = self._from_dict_data[_SCI_HEADER_SLRESOURCERESERVEPERIOD]
        self._slMaxNumPerReserve = self._from_dict_data[_SCI_HEADER_SLMAXNUMPERRESERVE]
        self._slSciStage2Format = self._from_dict_data[_SCI_HEADER_SLSCISTAGE2FORMAT]
        self._indexStartSbChReTx1 = self._from_dict_data[_SCI_HEADER_INDEXSTARTSBCHRETX1]
        self._indexStartSbChReTx2 = self._from_dict_data[_SCI_HEADER_INDEXSTARTSBCHRETX2]
        self._gapReTx1 = self._from_dict_data[_SCI_HEADER_GAPRETX1]
        self._gapReTx2 = self._from_dict_data[_SCI_HEADER_GAPRETX2]

    def __str__(self) -> str:
        return str(self._total_subchannels) + "," + str(self._priority) + "," + str(self._indexStartSubChannel) + "," + str(self._lengthSubChannel) + "," + \
        str(self._mcs) + "," + str(self._slResourceReservePeriod) + "," + str(self._slMaxNumPerReserve) + "," + str(self._slSciStage2Format) + "," + \
        str(self._indexStartSbChReTx1) + "," + str(self._indexStartSbChReTx2) + "," + str(self._gapReTx1) + "," + str(self._gapReTx2)

    def str_var_order() -> str:
        return  _SCI_HEADER_TOTAL_SUBCHANNELS + "," + \
                _SCI_HEADER_PRIORITY + "," + \
                _SCI_HEADER_INDEXSTARTSUBCHANNEL + "," + \
                _SCI_HEADER_LENGTHSUBCHANNEL + "," + \
                _SCI_HEADER_MCS + "," + \
                _SCI_HEADER_SLRESOURCERESERVEPERIOD + "," + \
                _SCI_HEADER_SLMAXNUMPERRESERVE + "," + \
                _SCI_HEADER_SLSCISTAGE2FORMAT + "," + \
                _SCI_HEADER_INDEXSTARTSBCHRETX1 + "," + \
                _SCI_HEADER_INDEXSTARTSBCHRETX2 + "," + \
                _SCI_HEADER_GAPRETX1 + "," + \
                _SCI_HEADER_GAPRETX2 
                

class V2XSciMessage:
    def __init__(self, input_dict, decoder:RicControlMessageEncoder, from_dict=None):
        self._input_dict = input_dict
        self._decoder = decoder
        self.header: V2XSciHeader = None
        self.tag: V2XSciTag = None
        self.rsrp: float = None
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            self._parse()

    def _parse(self, input_dict: Union[dict, List[dict]] = None):
       
        if input_dict is None:
            input_dict = self._input_dict
        # print("V2XSciMessage")
        # print(input_dict)
        try:
            _sci_message_header = reduce(operator.getitem, _SCI_HEADER_V2X, input_dict)
            _sci_message_header.replace(" ", "")
            self.header = V2XSciHeader(_sci_message_header, self._decoder)
            self.header._slSciStage2Format = 1
        except KeyError:
            pass
        except AttributeError:
            pass
        try:
            _sci_message_tag:str = reduce(operator.getitem, _SCI_TAG_V2X, input_dict)
            _sci_message_tag.replace(" ", "")
            self.tag = V2XSciTag(_sci_message_tag, self._decoder)
        except KeyError:
            pass
        except AttributeError:
            pass
        try:
            self.rsrp:float = float(reduce(operator.getitem, _SCI_RSRP, input_dict))
        except KeyError:
            pass

        

    def is_valid(self):
        # return (False if self.header is None else self.header.is_valid()) & \
        #         (False if self.tag is None else self.tag.is_valid()) & \
        #         (self.rsrp is not None)
        return (self.rsrp is not None)
    
    def __str__(self) -> str:
        return str(self.header) + "," + str(self.tag)
    
    def to_dict(self):
        return{
            _JSON_SCI_MESSAGE_HEADER: None if self.header is None else self.header.to_dict(),
            _JSON_SCI_MESSAGE_TAG: None if self.tag is None else  self.tag.to_dict(),
            _JSON_SCI_MESSAGE_RSRP: self.rsrp
        }

    def _from_dict(self):
        _sci_header_dict = self._from_dict_data[_JSON_SCI_MESSAGE_HEADER]
        _sci_tag_dict = self._from_dict_data[_JSON_SCI_MESSAGE_TAG]
        self.header = V2XSciHeader("", None, _sci_header_dict) if _sci_header_dict is not None  else None
        self.tag = V2XSciTag("", None, _sci_tag_dict) if _sci_tag_dict is not None else None
        self.rsrp = self._from_dict_data[_JSON_SCI_MESSAGE_RSRP]

    def str_var_order() -> str:
        return  _JSON_SCI_MESSAGE_HEADER + "," + \
                _JSON_SCI_MESSAGE_TAG + "," + \
                _JSON_SCI_MESSAGE_RSRP

class V2XSciMessages:
    def __init__(self, input_dict, decoder:RicControlMessageEncoder, from_dict=None):
        self._input_dict = input_dict
        self.sci_messages: List[V2XSciMessage]= []
        self.decoder: RicControlMessageEncoder = decoder
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            self._parse()

    def _parse(self, input_dict: Union[dict, List[dict]] = None):
        if input_dict is None:
            input_dict = self._input_dict
        # print ("V2XSciMessages")
        # print(input_dict)
        try:
            _sci_messages = reduce(operator.getitem, _SCI_MESSAGE_V2X, input_dict)
            _sci_messages_instances_list:List[V2XSciMessage] = []
            # print("reduced sci messages ")
            # print(_sci_messages)
            if isinstance(_sci_messages, list):
                for _sci_message in _sci_messages:
                    _sci_message_instance = V2XSciMessage(_sci_message, self.decoder)
                    if _sci_message_instance.is_valid():
                        _sci_messages_instances_list.append(_sci_message_instance)
            else:
                _sci_message_instance = V2XSciMessage(_sci_messages, self.decoder)
                if _sci_message_instance.is_valid():
                    _sci_messages_instances_list.append(_sci_message_instance)
            # print(f"Length of valid sci msgs {len(_sci_messages_instances_list)}")
            self.sci_messages = _sci_messages_instances_list
            
        except KeyError:
            pass
        except TypeError:
            pass

    def is_valid(self):
        return all([_sci_message.is_valid() for _sci_message in self.sci_messages])
    
    def __str__(self) -> str:
        return str([str(sci_message) for sci_message in self.sci_messages]) #+ ","  + str(datetime.datetime.now())
    
    def to_dict(self):
        return{
            _JSON_SCI_MESSAGES: [_sci_message.to_dict() for _sci_message in self.sci_messages],
        }

    def str_var_order() -> str:
        return  _JSON_SCI_MESSAGES
    
    def _from_dict(self):
        self.sci_messages = [V2XSciMessage(None, None, from_dict=_sci_dict_msg) for _sci_dict_msg in self._from_dict_data[_JSON_SCI_MESSAGES]]

class PacketDelayHarqBufferSize:
    def __init__(self, input_dict, from_dict=None):
        self._input_dict = input_dict
        self.harqId:int = -1
        self.numberOfPackets: int = -1
        self.bufferSize:int = -1
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            # decoding the tag buffer through the c libraries
            self._parse()
    
    def _parse(self, input_dict: Union[dict, List[dict]] = None):
        if input_dict is None:
            input_dict = self._input_dict
        try:
            self.harqId = float(reduce(operator.getitem, _JSON_PACKET_DELAYS_DELAY_INTERVAL_HARQ_ID, input_dict))
            self.numberOfPackets = int(reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS, input_dict))
            self.bufferSize = int(reduce(operator.getitem, _JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE, input_dict))
        except KeyError:
            pass
    
    def is_valid(self):
        return (self.harqId > -1) & (self.bufferSize > -1) & (self.numberOfPackets>-1)

    def to_dict(self):
        return {_JSON_PACKET_DELAYS_DELAY_INTERVAL_HARQ_ID: self.harqId, 
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS: self.numberOfPackets,
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE: self.bufferSize
                }
    
    def _from_dict(self):
        self.numberOfPackets = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS]
        self.harqId = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_HARQ_ID]
        self.bufferSize = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE]
    
    def __str__(self) -> str:
        return str(self.harqId) + "," + str(self.numberOfPackets) + "," + str(self.bufferSize)

    def str_var_order() -> str:
        return  _JSON_PACKET_DELAYS_DELAY_INTERVAL_HARQ_ID + "," + \
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS + "," + \
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE     

class PacketDelayInterval:
    def __init__(self, input_dict, from_dict=None):
        self._input_dict = input_dict
        self.lowerInterval: float = None
        self.upperInterval:float = None
        self.numberOfPackets: int = -1
        self.bufferSize:int = -1
        self.reservationPeriod: float = None # the reservation period or the periodicity of traffic
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            # decoding the tag buffer through the c libraries
            self._parse()

    def _parse(self, input_dict: Union[dict, List[dict]] = None):
        if input_dict is None:
            input_dict = self._input_dict
        # print("packet delay interval")
        # print(input_dict)
        try:
            self.lowerInterval = float(reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL_LOWER_INTERVAL, input_dict))
            self.upperInterval = float(reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL_UPPER_INTERVAL, input_dict))
            self.numberOfPackets = int(reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS, input_dict))
            self.reservationPeriod = float(reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL_RESERVATION_PERIOD, input_dict))
            self.bufferSize = int(reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE, input_dict))
        except KeyError:
            # print("Error in PacketDelayInterval")
            pass
    
    def is_valid(self):
        return (self.lowerInterval is not None) & (self.upperInterval is not None) & (self.numberOfPackets>-1)

    def to_dict(self):
        return {_JSON_PACKET_DELAYS_DELAY_INTERVAL_LOWER_INTERVAL: self.lowerInterval, 
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_UPPER_INTERVAL: self.upperInterval,
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS: self.numberOfPackets,
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_RESERVATION_PERIOD: self.reservationPeriod,
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE: self.bufferSize
                }
    
    def _from_dict(self):
        self.lowerInterval = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_LOWER_INTERVAL]
        self.upperInterval = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_UPPER_INTERVAL]
        self.numberOfPackets = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS]
        self.reservationPeriod = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_RESERVATION_PERIOD]
        self.bufferSize = self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_BUFFER_SIZE]
    
    def __str__(self) -> str:
        return str(self.lowerInterval) + "," + str(self.upperInterval) + "," + str(self.numberOfPackets) + "," + str(self.reservationPeriod)

    def str_var_order() -> str:
        return  _JSON_PACKET_DELAYS_DELAY_INTERVAL_LOWER_INTERVAL + "," + \
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_UPPER_INTERVAL + "," + \
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_NUM_PACKETS + "," + \
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_RESERVATION_PERIOD

class PacketDelayConnectionsIntervals:
    def __init__(self, input_dict: Union[dict, List[dict]] = None, from_dict=None):
        self._input_dict = input_dict
        self.ue_id: int = -1
        self.delayIntervals:List[PacketDelayInterval] = []
        self.harqBufferSize: List[PacketDelayHarqBufferSize] = []
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            self._parse()

    def _parse(self, input_dict: Union[dict, List[dict]] = None):
        if input_dict is None:
            input_dict = self._input_dict
        # print("PacketDelayConnectionsIntervals input dict")
        # print(input_dict)
        self.ue_id = int(reduce(operator.getitem, _PACKET_DELAYS_USER_ID, input_dict))
        try:
            _packet_delay_intervals = reduce(operator.getitem, _PACKET_DELAYS_DELAY_INTERVAL, input_dict)
        except (TypeError, KeyError):
            _packet_delay_intervals = None
        try:
            _harq_buffer_size_list = reduce(operator.getitem, _PACKET_DELAYS_HARQ_BUFFER_SIZE, input_dict)
        except (TypeError, KeyError):
            _harq_buffer_size_list = None
        # print("Packet delay interval")
        # print(_packet_delay_intervals)
        # print("Harq buffer size")
        # print(_harq_buffer_size_list)
        try:
            packet_intervals_list:List[PacketDelayInterval] = []
            if _packet_delay_intervals is not None:
                if isinstance(_packet_delay_intervals, list):
                    for packet_delay_interval in _packet_delay_intervals:
                        _packet_interval = PacketDelayInterval(packet_delay_interval)
                        # print(f"list is valid {_packet_interval.is_valid()}")
                        if _packet_interval.is_valid():
                            packet_intervals_list.append(_packet_interval)
                else:
                    _packet_interval = PacketDelayInterval(_packet_delay_intervals)
                    # print(f" is valid {_packet_interval.is_valid()}")
                    if _packet_interval.is_valid():
                        packet_intervals_list.append(_packet_interval)
            # return packet_intervals_list
            # print(f"PacketDelayConnectionsIntervals list size {len(packet_intervals_list)}")
            self.delayIntervals = packet_intervals_list
        except KeyError:
            pass
        try:
            harq_buffer_size_objs: List[PacketDelayHarqBufferSize] = []
            if _harq_buffer_size_list is not None:
                if isinstance(_harq_buffer_size_list, list):
                    for _harq_buffer_size in _harq_buffer_size_list:
                        _harq_buffer_size_obj = PacketDelayHarqBufferSize(_harq_buffer_size)
                        if _harq_buffer_size_obj.is_valid():
                            harq_buffer_size_objs.append(_harq_buffer_size_obj)
                else:
                    _harq_buffer_size = _harq_buffer_size_list
                    _harq_buffer_size_obj = PacketDelayHarqBufferSize(_harq_buffer_size)
                    if _harq_buffer_size_obj.is_valid():
                        harq_buffer_size_objs.append(_harq_buffer_size_obj)
            # print(f"PacketDelayConnectionsIntervals harq buffer size {len(harq_buffer_size_objs)}")
            self.harqBufferSize = harq_buffer_size_objs
        except KeyError:
            pass

    def is_valid(self):
        _all_is_valid_intervals = all([interval.is_valid() for interval in self.delayIntervals])
        _all_is_valid_harq_buffer = all([_buffer_size.is_valid() for _buffer_size in self.harqBufferSize])
        _all_is_valid = _all_is_valid_intervals & (self.ue_id>-1) & _all_is_valid_harq_buffer
                
        # print(f"is valid PacketDelayConnectionsIntervals {_all_is_valid_intervals}" + \
        #                                                  f" { _all_is_valid_harq_buffer} " + \
        #                                                 f" {(self.ue_id>-1)} " + \
        #                                                 f" {_all_is_valid} ")
        return _all_is_valid
    
    def to_dict(self):
        return {_JSON_PACKET_DELAYS_USER_ID: self.ue_id, 
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_LIST: [delays_interval.to_dict() for delays_interval in self.delayIntervals],
                _JSON_PACKET_DELAYS_DELAY_HARQ_BUFFER_SIZE_LIST: [_buffer_size.to_dict() for _buffer_size in self.harqBufferSize]
                }
    
    def _from_dict(self):
        self.ue_id = self._from_dict_data[_JSON_PACKET_DELAYS_USER_ID]
        self.delayIntervals = [PacketDelayInterval(None, from_dict=_packet_delay_interval_msg) for _packet_delay_interval_msg in self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_INTERVAL_LIST]]
        self.harqBufferSize = [PacketDelayHarqBufferSize(None, from_dict=_harq_buffer_size_msg) for _harq_buffer_size_msg in self._from_dict_data[_JSON_PACKET_DELAYS_DELAY_HARQ_BUFFER_SIZE_LIST]]

    def __str__(self) -> str:
        return str(self.ue_id) + "," + str([str(delay_interval) for delay_interval in self.delayIntervals]) + "," + \
                str([str(harq_buff) for harq_buff in self.harqBufferSize])

    def str_var_order() -> str:
        return  _JSON_PACKET_DELAYS_USER_ID + "," + \
                _JSON_PACKET_DELAYS_DELAY_INTERVAL_LIST + "," + \
                _JSON_PACKET_DELAYS_DELAY_HARQ_BUFFER_SIZE_LIST
    
class PacketDelaySingleUserConnectionsDelay:
    def __init__(self, input_dict, from_dict=None):
        self._input_dict = input_dict
        self.ue_id: int = -1
        self.all_connections_delays:List[PacketDelayConnectionsIntervals] = []
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()
        else:
            self._parse()

    def _parse(self, input_dict: Union[dict, List[dict]] = None):
        if input_dict is None:
            input_dict = self._input_dict
        # print("PacketDelaySingleUserConnectionsDelay")
        # print(input_dict)
        self.ue_id = int(reduce(operator.getitem, 
                                _PACKET_DELAYS_ALL_USERS_ALL_CONNECTIONS + _PACKET_DELAYS_USER_ID 
                                , input_dict))
        _packet_delay_all_connections_intervals = reduce(operator.getitem, 
                                _PACKET_DELAYS_ALL_USERS_ALL_CONNECTIONS + _PACKET_DELAYS_USER_ALL_CONNECTIONS, 
                                input_dict)
        # print("all connections dict")
        # print(_packet_delay_all_connections_intervals)
        try:
            _packet_delay_all_connections_intervals_list:List[PacketDelayConnectionsIntervals] = []
            if isinstance(_packet_delay_all_connections_intervals, list):
                for _packet_delay_all_connections_interval in _packet_delay_all_connections_intervals:
                    _connection_intervals = PacketDelayConnectionsIntervals(_packet_delay_all_connections_interval)
                    if _connection_intervals.is_valid():
                        _packet_delay_all_connections_intervals_list.append(_connection_intervals)
            else:
                _connection_intervals = PacketDelayConnectionsIntervals(_packet_delay_all_connections_intervals)
                if _connection_intervals.is_valid():
                    _packet_delay_all_connections_intervals_list.append(_connection_intervals)
            # print(f"PacketDelaySingleUserConnectionsDelay size {len(_packet_delay_all_connections_intervals_list)}")
            self.all_connections_delays = _packet_delay_all_connections_intervals_list
        except KeyError:
            pass

    def is_valid(self):
        _valid_single_conn_delays = [connection_delays.is_valid() for connection_delays in self.all_connections_delays]
        # print(f"PacketDelaySingleUserConnectionsDelay is valid {_valid_single_conn_delays}")
        return all(_valid_single_conn_delays)

    def to_dict(self):
        return {_JSON_PACKET_DELAYS_USER_ID: self.ue_id, 
                _JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS: [connection_delays.to_dict() for connection_delays in self.all_connections_delays],
                }
    
    def _from_dict(self):
        self.ue_id = self._from_dict_data[_JSON_PACKET_DELAYS_USER_ID]
        self.all_connections_delays = [PacketDelayConnectionsIntervals(None, from_dict=_packet_delays_single_user_msg) for _packet_delays_single_user_msg in self._from_dict_data[_JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS]]

    def __str__(self) -> str:
        return str(self.ue_id) + "," + str([str(_connection) for _connection in  self.all_connections_delays])

    def str_var_order() -> str:
        return  _JSON_PACKET_DELAYS_USER_ID + "," + \
                _JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS

class MillicarUeSingleReport:
    def __init__(self, input_dict, decoder:RicControlMessageEncoder, header_collection_time: int = -1,
                 from_dict=None
                 ):
        self._input_dict = input_dict
        self._decoder = decoder
        self.ue_id: int = -1
        self.rnti:int = -1
        self.imsi:int = -1
        self.position_x:float = None
        self.position_y:float = None
        self.frame: int = -1
        self.subframe: int = -1
        self.slot: int = -1
        self.ns3_timestamp: int = -1
        self.sci_messages: V2XSciMessages = None
        self.user_packet_delays: PacketDelaySingleUserConnectionsDelay = None
        self.collection_time = header_collection_time
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()

    def _from_dict(self):
        self.rnti = self._from_dict_data[_JSON_SOURCE_RNTI]
        self.imsi = self._from_dict_data[_JSON_SOURCE_IMSI]
        self.ue_id = self._from_dict_data[_JSON_SOURCE_UE_ID]
        self.frame = self._from_dict_data[_JSON_FRAME]
        self.subframe = self._from_dict_data[_JSON_SUBFRAME]
        self.slot = self._from_dict_data[_JSON_SLOT]
        self.ns3_timestamp = self._from_dict_data[_JSON_NS3_TIMESTAMP]
        self.position_x = self._from_dict_data[_JSON_POSITION_X]
        self.position_y = self._from_dict_data[_JSON_POSITION_Y]
        self.sci_messages = V2XSciMessages (None, None, from_dict=self._from_dict_data[_JSON_SCI_MESSAGES]) if self._from_dict_data[_JSON_SCI_MESSAGES] is not None else None
        self.user_packet_delays = PacketDelaySingleUserConnectionsDelay(None, from_dict=self._from_dict_data[_JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS]) if self._from_dict_data[_JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS] is not None else None
        self.collection_time = self._from_dict_data[_JSON_COLLECTION_TIME]

    def _parse_pm_container_single_element(self, input_dict=None):
        name_field = reduce(operator.getitem, _PM_INFO_ITEM_TYPE, input_dict)
        _single_data_dict = reduce(operator.getitem, _PM_INFO_ITEM_VALUE, input_dict)
        if name_field == _GENERATING_MILLICAR_SINGLE_REPORT:
            _field_value = reduce(operator.getitem, ["valueV2XSingleUserReport"], _single_data_dict)
            self.sci_messages = V2XSciMessages(_field_value, self._decoder)
            self.user_packet_delays = PacketDelaySingleUserConnectionsDelay(_field_value)
        if name_field == _GENERATING_MILLICAR_NODE_POSITION_X:
            self.position_x = int(float(reduce(operator.getitem, ['valueReal'], _single_data_dict)))
        if name_field == _GENERATING_MILLICAR_NODE_POSITION_Y:
            self.position_y = int(float(reduce(operator.getitem, ['valueReal'], _single_data_dict)))
        if name_field == _GENERATING_MILLICAR_FRAME:
            self.frame = int(reduce(operator.getitem, ['valueInt'], _single_data_dict))
        if name_field == _GENERATING_MILLICAR_SUBFRAME:
            self.subframe = int(reduce(operator.getitem, ['valueInt'], _single_data_dict))
        if name_field == _GENERATING_MILLICAR_SLOT:
            self.slot = int(reduce(operator.getitem, ['valueInt'], _single_data_dict))
        if name_field == _GENERATING_MILLICAR_NS3_TIMESTAMP:
            self.ns3_timestamp = int(reduce(operator.getitem, ['valueInt'], _single_data_dict))

    def _parse_pm_container(self, input_dict=None):
        if input_dict is None:
            input_dict = self._input_dict
        if isinstance(input_dict, list):# & (len(input_dict) == 5):
            for _single_report in input_dict:
                self._parse_pm_container_single_element(_single_report)
        else:
            self._parse_pm_container_single_element(input_dict)
        
    def parse(self, input_dict: Union[dict, List[dict]] = None):
        if input_dict is None:
            input_dict = self._input_dict
        # print("Parse MillicarUeSingleReport")
        # print(input_dict)
        try:
            _ue_id = reduce(operator.getitem, _PM_CONTAINERS_UE_ID, input_dict)
            self.ue_id = int(bytes.fromhex(str(_ue_id)))  # binary to int conversion
            self.rnti = self.ue_id
            self.imsi = self.ue_id
            _list_pm_info_dict = reduce(operator.getitem, _PM_CONTAINERS_LIST_PM_INFORMATION, input_dict)
            self._parse_pm_container(_list_pm_info_dict)

        except KeyError:
            pass

    def is_valid(self) -> bool:
        return  (self.position_x is not None) & (self.position_y is not None) & \
                (self.rnti > 0) &(self.imsi >0) & (self.ue_id >0) & \
                (False if self.sci_messages is None else self.sci_messages.is_valid()) & \
                (False if self.user_packet_delays is None else self.user_packet_delays.is_valid())

    def to_dict(self):
        # print("MillicarUeSingleReport user packets")
        # print(self.user_packet_delays.to_dict())
        return {_JSON_SOURCE_RNTI: self.rnti, _JSON_SOURCE_IMSI: self.imsi, _JSON_SOURCE_UE_ID:self.ue_id,
                _JSON_FRAME: self.frame, _JSON_SUBFRAME: self.subframe, _JSON_SLOT: self.slot,
                _JSON_NS3_TIMESTAMP: self.ns3_timestamp,
                _JSON_POSITION_X: self.position_x, _JSON_POSITION_Y: self.position_y,
                _JSON_SCI_MESSAGES: self.sci_messages.to_dict(), 
                _JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS: self.user_packet_delays.to_dict(), 
                _JSON_COLLECTION_TIME: self.collection_time, _JSON_TIMESTAMP: str(datetime.datetime.now()),
                }
    
    def __str__(self) -> str:
        return str(self.rnti) + "," + str(self.imsi) + "," + str(self.ue_id) + "," + \
                str(self.position_x) + "," + str(self.position_y) + "," + \
                str(self.sci_messages) + "," + str(self.user_packet_delays) + "," + \
                str(self.collection_time) + str(datetime.datetime.now())
    
    def str_var_order() -> str:
        return _JSON_SOURCE_RNTI + "," + _JSON_SOURCE_IMSI + "," + _JSON_SOURCE_UE_ID + "," + \
                _JSON_POSITION_X + "," + _JSON_POSITION_X + "," + \
                _JSON_SCI_MESSAGES + "," + _JSON_PACKET_DELAYS_USER_ALL_CONNECTIONS + "," + \
                _JSON_COLLECTION_TIME + "," + _JSON_TIMESTAMP 

    def get_frame_encoding(self) -> int:
        return self.slot + self.subframe*100 + self.frame*1000

class XmlToDictDataTransform:
    def __init__(self, decoder:RicControlMessageEncoder, plmn="110", from_dict=None):
        self.num_of_received_reports = 0
        self.num_of_reports = 0
        self._decoder = decoder
        self.plmn_id = plmn
        self.frame: int = -1
        self.subframe: int = -1
        self.slot: int = -1
        self.all_users_reports: List[MillicarUeSingleReport] = []
        self._from_dict_data = from_dict
        if self._from_dict_data is not None:
            # we parse the dict and update the fields
            self._from_dict()

    def get_frame_encoding(self) -> int:
        return self.slot + self.subframe*100 + self.frame*1000

    def reset(self):
        self.num_of_received_reports = 0
        self.num_of_reports = 0
        self.all_users_reports = []

    def has_received_all_reports(self):
        return (self.num_of_reports != 0) & (self.num_of_received_reports == self.num_of_reports)

    def can_perform_optimization(self):
        _received_all_reports = (self.num_of_reports != 0) & (self.num_of_received_reports == self.num_of_reports)
        if _received_all_reports:
            print("All reports received thus we can perform optimization")
        return _received_all_reports

    def peek_header(xml_string: str):
        try:
            _data = xmltodict.parse(xml_string)
            _input_dict = reduce(operator.getitem, _MAIN_TAG, _data)
            _header = reduce(operator.getitem, _HEADER_PART, _input_dict)
            _collection_time = reduce(operator.getitem, _HEADER_COLLECTION_START_TIME, _header)
            # print("Collection time " + str(int(re.sub(r"[\\n\t\s\n]*", "", _collection_time), 16)))
            _cell_id = -1
            for _header_cell_id_path in _HEADER_CELL_ID:
                try:
                    _cell_id = str(reduce(operator.getitem, _header_cell_id_path, _header))
                    # remove all tabs, whitespaces and new lines
                    _cell_id = re.sub(r"[\\n\t\s\n]*", "", _cell_id)
                except KeyError:
                    pass
            # print(_cell_id)
            _plmn_id = -1
            for _header_plmn_id_path in _HEADER_PLMN_ID:
                try:
                    _plmn_id = reduce(operator.getitem, _header_plmn_id_path, _header)
                    try:
                        _plmn_id = bytes.fromhex(_plmn_id).decode('utf-8')
                    except ValueError:
                        pass
                except KeyError:
                    pass
            return _collection_time, _cell_id, _plmn_id
        except xml.parsers.expat.ExpatError:
            print(xml_string)
            return -1, -1, -1

    def parse_incoming_data(self, xml_string: str):
        try:
            _data = xmltodict.parse(xml_string)
            _input_dict = reduce(operator.getitem, _MAIN_TAG, _data)
            _header_collection_time, _header_cell_id, _header_plmn_id = self.parse_header(_input_dict)
            _cell_id_int = -1
            try:
                _cell_id_int = int(bytes.fromhex(_header_cell_id).split(b'\x00')[0], 16)
            except ValueError:
                try:
                    _cell_id_int = int(
                        bytes(int(_header_cell_id[i: i + 8], 2) for i in range(0, len(_header_cell_id), 8)).split(
                            b'\x00')[
                            0])
                except ValueError:
                    _cell_id_only = _header_cell_id.split('(')[0]
                    _cell_id_int = int(bytes.fromhex(_cell_id_only).split(b'\x00')[0], 16)
            try:
                _header_plmn_id = bytes.fromhex(_header_plmn_id).decode('utf-8')
            except ValueError:
                pass
            _header_collection_time_int: int = -1
            try:
                # _header_collection_time = int(_header_collection_time, 16)
                _header_collection_time_int = int(re.sub(r"[\\n\t\s\n]*", "", _header_collection_time), 16)
            except ValueError:
                pass
            # print(_header_collection_time, _cell_id_int, _header_plmn_id)
            self.parse_message_single_report(_input_dict, _header_collection_time_int)
            # print("Received report " + str(self.num_of_received_reports) + " from " + str(self.num_of_reports) + \
            #       " for collection time " + str(_header_collection_time))
        except xml.parsers.expat.ExpatError:
            print("Error in parsing the xml string")
            print(xml_string)

    def parse_header(self, input_dict: Mapping):
        _header = reduce(operator.getitem, _HEADER_PART, input_dict)
        _collection_time = reduce(operator.getitem, _HEADER_COLLECTION_START_TIME, _header)
        _cell_id = -1
        for _header_cell_id_path in _HEADER_CELL_ID:
            try:
                _cell_id = str(reduce(operator.getitem, _header_cell_id_path, _header))
                # remove all tabs, whitespaces and new lines
                _cell_id = re.sub(r"[\\n\t\s\n]*", "", _cell_id)
            except KeyError:
                pass
        # print(_cell_id)
        _plmn_id = -1
        for _header_plmn_id_path in _HEADER_PLMN_ID:
            try:
                _plmn_id = reduce(operator.getitem, _header_plmn_id_path, _header)
            except KeyError:
                pass
        return _collection_time, _cell_id, _plmn_id

    def parse_message_single_report(self, input_dict: Mapping, header_collection_time: int):
        _reports_per_user_list: List[MillicarUeSingleReport] = self._parse_message_ues_single_report(input_dict, header_collection_time)

        # sync with maximum slot
        # print(f"Length {len(_reports_per_user_list)}")
        # print("input dict")
        # print(input_dict)
        # print("ue reports ")
        # print(_reports_per_user_list[0].to_dict())
        try:
            # _max_frame_sync = max(filter(lambda ue_report: ue_report.get_frame_encoding(), _reports_per_user_list), key=itemgetter(1))
            _max_frame_sync = max(_reports_per_user_list, key=lambda ue_report: ue_report.get_frame_encoding())
            self.frame = _max_frame_sync.frame
            self.subframe = _max_frame_sync.subframe
            self.slot = _max_frame_sync.slot
        except ValueError:
            # should not happen just for safety
            self.frame = -1
            self.subframe = -1
            self.slot = -1
        
        # can receive multi-user reports in a single msg
        self.all_users_reports+=_reports_per_user_list
        # pickle_out = open('/home/traces/ue_reports_' + self.plmn_id + '.pickle', 'ab+')
        # # print(f"Writing to pickle we plmn {self.plmn_id}")
        # for _reports_per_user in _reports_per_user_list:
        #     # print(_reports_per_user)
        #     _ue_reports_dict = _reports_per_user.to_dict()
        #     _ue_reports_dict[_JSON_PLMN] = self.plmn_id
        #     pickle.dump(_ue_reports_dict, pickle_out)
        # pickle_out.close()

    def _parse_message_ues_single_report(self, input_dict: Mapping, header_collection_time: int) -> List:
        _message_dict = reduce(operator.getitem, _MESSAGE_PART, input_dict)
        _matched_ues_dict = {}
        logger = logging.getLogger("")
        # print("MEssage dict ")
        # print(_message_dict)
        # logging.debug(f"Data of dict {_message_dict}")
        try:
            _matched_ues_dict = reduce(operator.getitem, _LIST_OF_MATCHED_UES, _message_dict)
            self.num_of_reports = int(reduce(operator.getitem, _CUCP_PM_REPORTS_NUMBER, _message_dict))
        except KeyError:
            pass
        except TypeError:
            # the data in the _LIST_OF_MATCHED_UES are incomplete
            return []
        logger.debug(f"Num of reports {self.num_of_reports}")
        
        try:
            _reports_per_user_list = []
            if not isinstance(_matched_ues_dict, list):
                _matched_ues_dict = [_matched_ues_dict]
            for _imsi_data_report in _matched_ues_dict:
                single_report = MillicarUeSingleReport(_imsi_data_report, self._decoder, header_collection_time)
                single_report.parse()
                # print("print ue single report ")
                # print(single_report.to_dict())
                if single_report.is_valid():
                    _reports_per_user_list.append(single_report)
                # add to the number of receivef reports
                self.num_of_received_reports += 1
                logger.debug(f"Num of reports received {self.num_of_received_reports}")
            return _reports_per_user_list
        except KeyError:
            pass
        return []

    def to_dict(self):
        # return [report.to_dict() for report in self.all_users_reports]
        return {
            _JSON_TIMESTAMP: str(datetime.datetime.now()),
            _JSON_PLMN: self.plmn_id,
            _JSON_FRAME: self.frame,
            _JSON_SUBFRAME: self.subframe,
            _JSON_SLOT: self.slot,
            _JSON_ALL_UE_REPORTS: [report.to_dict() for report in self.all_users_reports]
        }
    
    def _from_dict(self):
        # logger = logging.getLogger('')
        # logger.debug("_from_dict XmlToDictDataTransform data ")
        # logger.debug(self._from_dict_data)
        self.plmn_id = self._from_dict_data[_JSON_PLMN]
        self.frame = self._from_dict_data[_JSON_FRAME]
        self.subframe = self._from_dict_data[_JSON_SUBFRAME]
        self.slot = self._from_dict_data[_JSON_SLOT]
        self.all_users_reports = [MillicarUeSingleReport(None, self._decoder, from_dict=_ue_report) for _ue_report in self._from_dict_data[_JSON_ALL_UE_REPORTS]]


# _msg = b'<message><E2SM-KPM-IndicationHeader><indicationHeader-Format1><collectionStartTime>65 6C 66 65 72 28 21 00</collectionStartTime><id-GlobalE2node-ID><gNB><global-gNB-ID><plmn-id>31 31 31</plmn-id><gnb-id><gnb-ID>31 00 00 00\n                        </gnb-ID></gnb-id></global-gNB-ID></gNB></id-GlobalE2node-ID></indicationHeader-Format1></E2SM-KPM-IndicationHeader><E2SM-KPM-IndicationMessage><indicationMessage-Format1><pm-Containers><PM-Containers-Item><performanceContainer><oCU-CP><cu-CP-Resource-Status><numberOfActive-UEs>2</numberOfActive-UEs></cu-CP-Resource-Status></oCU-CP></performanceContainer></PM-Containers-Item></pm-Containers><cellObjectID>NRCellCU</cellObjectID><list-of-matched-UEs><PerUE-PM-Item><ueId>30 30 30 30 31</ueId><list-of-PM-Information><PM-Info-Item><pmType><measName>GeneratingNode.Rnti.UEID</measName></pmType><pmVal><valueInt>1</valueInt></pmVal></PM-Info-Item><PM-Info-Item><pmType><measName>GeneratingNode.PositionX.UEID</measName></pmType><pmVal><valueInt>0</valueInt></pmVal></PM-Info-Item><PM-Info-Item><pmType><measName>GeneratingNode.PositionY.UEID</measName></pmType><pmVal><valueInt>3</valueInt></pmVal></PM-Info-Item><PM-Info-Item><pmType><measName>HO.TrgtCellQual.RS-SINR.UEID</measName></pmType><pmVal><valueRRC><rrcEvent><b1/></rrcEvent></valueRRC></pmVal></PM-Info-Item></list-of-PM-Information></PerUE-PM-Item></list-of-matched-UEs></indicationMessage-Format1></E2SM-KPM-IndicationMessage></message>'

if __name__ == '__main__':
    _msg_encoder = RicControlMessageEncoder()
    _transformer = XmlToDictDataTransform(_msg_encoder)
    # print(os.getcwd())
    _filename = 'data_ctrl.xml'
    _dir = './data'
    _complete_msg = ""
    _tmp_msg = ""
    _start_new_msg = False
    # with open(_filename) as _file:
    with open(os.path.join(_dir, _filename)) as _file:
        lines = _file.readlines()
        # print(lines)
        _complete_msg = "".join([_line.strip() for _line in lines])
    #     _transformer.parse_incoming_data(lines[0])
    #     print(_transformer.measurements)
    # _transformer.parse_incoming_data(str(_msg))
    # print(_complete_msg)
    _transformer.parse_incoming_data(_complete_msg)

