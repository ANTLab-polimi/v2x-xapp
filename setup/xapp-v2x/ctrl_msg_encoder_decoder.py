import ctypes
import logging
from ctypes import POINTER, Structure, create_string_buffer
from ctypes import c_long, c_size_t, c_int, c_uint8, c_char_p, c_void_p
from ctypes import c_int16, c_uint16, c_uint32, c_ubyte, cast

from typing import Any, List
import numpy as np

from v2x_ric_message_format import SourceUserScheduling, UserScheduling, SingleScheduling, SlRlcPduInfo

import sl_sci_f1a_header_pb2 as sci_header
import sl_mac_pdu_tag_pb2 as sci_tag
from google.protobuf.message import Message

# from run_xapp_parallel import _JSON_SOURCE_SCHEDULING
# import transform_xml_to_dict_v2x as transform

class BaseStructure(ctypes.Structure):

    def __init__(self, **kwargs):
        """
        Ctypes.Structure with integrated default values.

        :param kwargs: values different to defaults
        :type kwargs: dict
        """

        values = type(self)._defaults_.copy()
        values.update(kwargs)
        super().__init__(**values)            # Python 3 syntax

class buffer_lengtht_t(Structure):
    _fields_ = [
        ("length", c_int),
        ("buffer", POINTER(c_ubyte)) # POINTER(c_uint8)
    ]
class e2ap_stcp_buffer_t(Structure):
    _fields_ = [
        ("msg_length", c_int),
        ("bytes_consumed", c_int),
        ("msg_buffer", POINTER(c_ubyte)) # POINTER(c_uint8)
    ]

class v2x_sci_header_buffer_t(Structure):
    _fields_ = [
        ("m_totalSubChannels", c_uint16),
        ("m_priority", c_uint8),
        ("m_indexStartSubChannel", c_uint8),
        ("m_lengthSubChannel", c_uint8),
        ("m_mcs", c_uint8),
        ("m_slResourceReservePeriod", c_uint16),
        ("m_slMaxNumPerReserve", c_uint8),
        ("m_slSciStage2Format", c_uint8),
        ("m_indexStartSbChReTx1", c_uint8),
        ("m_indexStartSbChReTx2", c_uint8),
        ("m_gapReTx1", c_uint8),
        ("m_gapReTx2", c_uint8),
    ]

class v2x_sci_tag_buffer_t(Structure):
    _fields_ = [
        ("m_frameNum", c_uint16),
        ("m_subframeNum", c_uint8),
        ("m_slotNum", c_uint16),
        ("m_numerology", c_int16),
        ("m_rnti", c_uint16),
        ("m_symStart", c_uint8),
        ("m_numSym", c_uint8),
        ("m_tbSize", c_uint32),
        ("m_dstL2Id", c_uint32),
    ]
# the equivalent class of scheduling struct
class v2x_sl_rlc_pdu_info_t(Structure):
    _fields_ = [
        ("lcid", c_uint8),
        ("size", c_uint32),
    ]    

    _defaults_ = { "lcid" : 0,
                   "size" : 0,
                 }

    def __init__(self, **kwargs):
        # print("Insided the v2x_sl_rlc_pdu_info_t constructor")
        # print(kwargs)
        super().__init__(**kwargs)

class v2x_nr_sl_slot_alloc_t(BaseStructure):
    _fields_ = [
        ("m_frameNum", c_uint16),
        ("m_subframeNum", c_uint8),
        ("m_slotNum", c_uint16),
        ("m_numerology", c_int16),
        ("dstL2Id", c_uint32),
        ("ndi", c_uint8),
        ("rv", c_uint8),
        ("priority", c_uint8),
        ("slRlcPduInfoVectorSize", c_uint32),
        ("slRlcPduInfo", POINTER(v2x_sl_rlc_pdu_info_t)),# type vector with size 0
        ("mcs", c_uint16),
        ("numSlPscchRbs", c_uint16),
        ("slPscchSymStart", c_uint16),
        ("slPscchSymLength", c_uint16),
        ("slPsschSymStart", c_uint16),
        ("slPsschSymLength", c_uint16),
        ("slPsschSubChStart", c_uint16),
        ("slPsschSubChLength", c_uint16),
        ("maxNumPerReserve", c_uint16),
        ("txSci1A", c_uint8),
        ("slotNumInd", c_uint8),
    ]
    _defaults_ = { "m_frameNum" : 2,
                   "m_subframeNum" : 3,
                 }
    
    def __init__(self, **kwargs):
        # get the list of sl rlc infor
        _dict_sl_rlc = kwargs['slRlcPduInfo']
        slRlcPduInfoArrayType= v2x_sl_rlc_pdu_info_t*len(_dict_sl_rlc)
        slRlcPduInfoArray = slRlcPduInfoArrayType()
        if len(_dict_sl_rlc)>0:
            # update values
            for i in range(len(_dict_sl_rlc)):
                slRlcPduInfoArray[i] = v2x_sl_rlc_pdu_info_t(**_dict_sl_rlc[i])

        pointer_to_first_element = cast(slRlcPduInfoArray, POINTER(v2x_sl_rlc_pdu_info_t))# store the pointer of vector
        kwargs.update({'slRlcPduInfo': pointer_to_first_element, "slRlcPduInfoVectorSize": len(_dict_sl_rlc)})
        # print("Insided the v2x_nr_sl_slot_alloc_t constructor")
        # print(kwargs)
        super().__init__(**kwargs)

class v2x_user_nr_sl_slot_alloc_t(BaseStructure):
    _fields_ = [
        ("ue_id", c_uint16),
        ("cReselCounter", c_uint16),
        ("slResoReselCounter", c_uint8),
        ("prevSlResoReselCounter", c_uint8),
        ("nrSlHarqId", c_uint8),
        ("nSelected", c_uint8),
        ("tbTxCounter", c_uint8),
        ("userSchedulingVectorSize", c_uint32),
        ("userScheduling", POINTER(v2x_nr_sl_slot_alloc_t)),# type vector with size 0
    ]

    _defaults_ = {  "ue_id" : 0,
                    "cReselCounter": int(np.iinfo(np.uint8).max),
                    "slResoReselCounter": int(np.iinfo(np.uint8).max),
                    "prevSlResoReselCounter": int(np.iinfo(np.uint8).max),
                    "nrSlHarqId": int(np.iinfo(np.uint8).max),
                    "nSelected": 0,
                    "tbTxCounter": 0,
                 }

    def __init__(self, **kwargs):
        # print ("User scheduling")
        # print(kwargs)
        _dict_user_scheduling = kwargs['userScheduling']
        userSchedulingArrayType= v2x_nr_sl_slot_alloc_t*len(_dict_user_scheduling)
        userSchedulingArray = userSchedulingArrayType()
        if len(_dict_user_scheduling)>0:
            # update values
            for i in range(len(_dict_user_scheduling)):
                userSchedulingArray[i] = v2x_nr_sl_slot_alloc_t(**_dict_user_scheduling[i])

        pointer_to_first_element = cast(userSchedulingArray, POINTER(v2x_nr_sl_slot_alloc_t))# store the pointer of vector
        kwargs.update({'userScheduling': pointer_to_first_element, "userSchedulingVectorSize": len(_dict_user_scheduling)})
        super().__init__(**kwargs)

class v2x_source_user_nr_sl_slot_alloc_t(BaseStructure):
    _fields_ = [
        ("source_id", c_uint16),
        ("destSchedulingVectorSize", c_uint32),
        ("destScheduling", POINTER(v2x_user_nr_sl_slot_alloc_t)),# type vector with size 0
    ]

    _defaults_ = { "source_id" : 0,
                 }

    def __init__(self, **kwargs):
        # logger = logging.getLogger('')
        # logger.debug("Dest scheduling")
        # logger.debug(kwargs)
        # print ("Dest scheduling")
        # print(kwargs)
        _dict_user_scheduling = kwargs['destScheduling']
        destUserSchedulingArrayType= v2x_user_nr_sl_slot_alloc_t*len(_dict_user_scheduling)
        destUserSchedulingArray = destUserSchedulingArrayType()
        if len(_dict_user_scheduling)>0:
            # update values
            for i in range(len(_dict_user_scheduling)):
                destUserSchedulingArray[i] = v2x_user_nr_sl_slot_alloc_t(**_dict_user_scheduling[i])

        pointer_to_first_element = cast(destUserSchedulingArray, POINTER(v2x_user_nr_sl_slot_alloc_t))# store the pointer of vector
        kwargs.update({'destScheduling': pointer_to_first_element, "destSchedulingVectorSize": len(_dict_user_scheduling)})
        super().__init__(**kwargs)

class RicControlMessageEncoder:
    def __init__(self):
        self._asn1_c_lib = ctypes.CDLL("libe2sim.so", mode=ctypes.RTLD_GLOBAL)

    def _wrap_asn1_function(self, funcname, restype, argtypes):
        func = self._asn1_c_lib.__getattr__(funcname)
        func.restype = restype
        func.argtypes = argtypes
        return func
    
    def encode_scheduling_plmn(self, v2x_scheduling_all_users: List[SourceUserScheduling], plmnId:str):
        _asn1_generate_v2x_scheduling_msg = self._wrap_asn1_function(
        'generate_e2ap_scheduling_control_message_plmn', POINTER(buffer_lengtht_t), 
        [POINTER(v2x_source_user_nr_sl_slot_alloc_t), c_size_t, c_char_p]) 

        # creating the slot alloc object

        _length = len(v2x_scheduling_all_users)
        v2x_all_users_allocation_vector_type = v2x_source_user_nr_sl_slot_alloc_t*_length
        v2x_all_users_allocation_vector = v2x_all_users_allocation_vector_type()
        # single destination 


        for _ind in range(_length):
            # generate single source user allocation
            v2x_all_users_allocation_vector[_ind] = v2x_source_user_nr_sl_slot_alloc_t(**v2x_scheduling_all_users[_ind].to_dict_c())

        plmnId_encoded = plmnId.encode("utf-8")
        plmnId_c = create_string_buffer(plmnId_encoded)
        # print("Encoding data in the c class")
        # cast array to pointer of the first element
        pointer_to_first_element = cast(v2x_all_users_allocation_vector, POINTER(v2x_source_user_nr_sl_slot_alloc_t))# store the pointer of vector
        msg: buffer_lengtht_t = _asn1_generate_v2x_scheduling_msg(pointer_to_first_element, _length, plmnId_c)
        _buffer_res = ctypes.cast(msg.contents.buffer, ctypes.POINTER(ctypes.c_ubyte * msg.contents.length))

        _data_bytes = bytes(_buffer_res.contents)
        _data_length = msg.contents.length

        return _data_length, _data_bytes

    def encode_result(self, ef_ids: List[int], ef_start_allocation: List[int], ef_optimized_allocation: List[int]):

        _asn1_decode_handoverMsg = self._wrap_asn1_function(
        'gnerate_e2ap_encode_handover_control_message', POINTER(buffer_lengtht_t), 
        [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), c_size_t]) 
        
        _length = len(ef_ids)
        id_vec = (c_uint16*_length)()
        start_pos = (c_uint16*_length)()
        end_pos = (c_uint16*_length)()
        for _ind in range(_length):
            id_vec[_ind] = ef_ids[_ind]
            start_pos[_ind] = ef_start_allocation[_ind]
            end_pos[_ind] = ef_optimized_allocation[_ind]

        # msg: POINTER(buffer_lengtht_t) = _asn1_decode_handoverMsg(id_vec, start_pos, end_pos, _length)
        msg: buffer_lengtht_t = _asn1_decode_handoverMsg(id_vec, start_pos, end_pos, _length)
        _buffer_res = ctypes.cast(msg.contents.buffer, ctypes.POINTER(ctypes.c_ubyte * msg.contents.length))

        _data_bytes = bytes(_buffer_res.contents)
        _data_length = msg.contents.length

        return _data_length, _data_bytes
    
    def encode_result_plmn(self, ef_ids: List[int], ef_start_allocation: List[int], ef_optimized_allocation: List[int], plmnId:str):

        _asn1_decode_handoverMsg = self._wrap_asn1_function(
        'generate_e2ap_encode_handover_control_message_plmn', POINTER(buffer_lengtht_t), 
        [POINTER(c_uint16), POINTER(c_uint16), POINTER(c_uint16), c_size_t, c_char_p]) 
        
        _length = len(ef_ids)
        id_vec = (c_uint16*_length)()
        start_pos = (c_uint16*_length)()
        end_pos = (c_uint16*_length)()
        for _ind in range(_length):
            id_vec[_ind] = ef_ids[_ind]
            start_pos[_ind] = ef_start_allocation[_ind]
            end_pos[_ind] = ef_optimized_allocation[_ind]
        
        plmnId_encoded = plmnId.encode("utf-8")
        plmnId_c = create_string_buffer(plmnId_encoded)
        
        msg: buffer_lengtht_t = _asn1_decode_handoverMsg(id_vec, start_pos, end_pos, _length, plmnId_c)
        _buffer_res = ctypes.cast(msg.contents.buffer, ctypes.POINTER(ctypes.c_ubyte * msg.contents.length))

        _data_bytes = bytes(_buffer_res.contents)
        _data_length = msg.contents.length

        return _data_length, _data_bytes
    
    def decode_e2ap_ric_indication_msg(self, input_bytes):
        logger = logging.getLogger('')
        _asn1_decode_e2ap = self._wrap_asn1_function(
        'decode_e2ap_to_xml', POINTER(e2ap_stcp_buffer_t), 
        [POINTER(c_uint8), c_size_t]) 
        _length: int = len(input_bytes)
        _input_bytes_cast = (c_uint8*_length)()
        for _ind in range(_length):
            _input_bytes_cast[_ind] = input_bytes[_ind]
        # _input_bytes_cast = ctypes.cast(input_bytes, ctypes.POINTER(ctypes.c_ubyte))

        msg: e2ap_stcp_buffer_t = _asn1_decode_e2ap(_input_bytes_cast, _length)
        try:
            _data_length = msg.contents.msg_length
            _bytes_consumed = msg.contents.bytes_consumed
            logger.debug("Data length " + str(_data_length) + " bytes consumed " + str(_bytes_consumed))
            _buffer_res = ctypes.cast(msg.contents.msg_buffer, ctypes.POINTER(ctypes.c_ubyte * _data_length))
            _data_bytes = bytes(_buffer_res.contents)
            # print("Data length " + str(_data_length))
            return _data_bytes, _data_length, _bytes_consumed
            # print(_data_bytes)
        except ValueError:
            # print("Null pointer returned")
            return None, None, None
        
    def decode_sci_header(self, input_bytes):
        _asn1_decode_e2ap = self._wrap_asn1_function(
                                'decode_v2x_sci_header', 
                                POINTER(v2x_sci_header_buffer_t), 
                                [POINTER(c_uint8), c_size_t]) 
        _length: int = len(input_bytes)
        _input_bytes_cast = (c_uint8*_length)()
        for _ind in range(_length):
            _input_bytes_cast[_ind] = input_bytes[_ind]
        msg: v2x_sci_header_buffer_t = _asn1_decode_e2ap(_input_bytes_cast, _length)
        _total_subchannels = msg.contents.m_totalSubChannels
        _priority = msg.contents.m_priority
        _indexStartSubChannel = msg.contents.m_indexStartSubChannel
        _lengthSubChannel = msg.contents.m_lengthSubChannel
        _mcs = msg.contents.m_mcs
        _slResourceReservePeriod = msg.contents.m_slResourceReservePeriod
        _slMaxNumPerReserve = msg.contents.m_slMaxNumPerReserve
        _slSciStage2Format = msg.contents.m_slSciStage2Format
        _indexStartSbChReTx1 = msg.contents.m_indexStartSbChReTx1
        _indexStartSbChReTx2 = msg.contents.m_indexStartSbChReTx2
        _gapReTx1 = msg.contents.m_gapReTx1
        _gapReTx2 = msg.contents.m_gapReTx2
        return (_total_subchannels, _priority, _indexStartSubChannel, _lengthSubChannel, _mcs, 
            _slResourceReservePeriod, _slMaxNumPerReserve, _slSciStage2Format, 
            _indexStartSbChReTx1, _indexStartSbChReTx2, _gapReTx1, _gapReTx2)
    
    def decode_sci_header_proto(self, input_bytes):
        _msg: Message = Message()
        _msg.ParseFromString(input_bytes)
        _sci_header_proto:sci_header.NrSlSciF1aHeaderProto = sci_header.NrSlSciF1aHeaderProto(_msg)

        _total_subchannels = _sci_header_proto.m_totalSubChannels
        _priority = _sci_header_proto.m_priority
        _indexStartSubChannel = _sci_header_proto.m_indexStartSubChannel
        _lengthSubChannel = _sci_header_proto.m_lengthSubChannel
        _mcs = _sci_header_proto.m_mcs
        _slResourceReservePeriod = _sci_header_proto.m_slResourceReservePeriod
        _slMaxNumPerReserve = _sci_header_proto.m_slMaxNumPerReserve
        _slSciStage2Format = _sci_header_proto.m_slSciStage2Format
        _indexStartSbChReTx1 = _sci_header_proto.m_indexStartSbChReTx1
        _indexStartSbChReTx2 = _sci_header_proto.m_indexStartSbChReTx2
        _gapReTx1 = _sci_header_proto.m_gapReTx1
        _gapReTx2 = _sci_header_proto.m_gapReTx2
        return (_total_subchannels, _priority, _indexStartSubChannel, _lengthSubChannel, _mcs, 
            _slResourceReservePeriod, _slMaxNumPerReserve, _slSciStage2Format, 
            _indexStartSbChReTx1, _indexStartSbChReTx2, _gapReTx1, _gapReTx2)

    
    def decode_sci_tag(self, input_bytes):
        _asn1_decode_e2ap = self._wrap_asn1_function(
                                'decode_v2x_sci_tag', 
                                POINTER(v2x_sci_tag_buffer_t), 
                                [POINTER(c_uint8), c_size_t]) 
        _length: int = len(input_bytes)
        _input_bytes_cast = (c_uint8*_length)()
        for _ind in range(_length):
            _input_bytes_cast[_ind] = input_bytes[_ind]
        msg: v2x_sci_tag_buffer_t = _asn1_decode_e2ap(_input_bytes_cast, _length)
        frameNum = msg.contents.m_frameNum
        subframeNum = msg.contents.m_subframeNum
        slotNum = msg.contents.m_slotNum
        numerology = msg.contents.m_numerology
        rnti = msg.contents.m_rnti
        symStart = msg.contents.m_symStart
        numSym = msg.contents.m_numSym
        tbSize = msg.contents.m_tbSize
        dstL2Id = msg.contents.m_dstL2Id
        return (frameNum, subframeNum, slotNum, numerology, rnti, symStart, numSym, tbSize, dstL2Id)
        
    def decode_sci_tag_proto(self, input_bytes):
        _msg: Message = Message()
        _msg.ParseFromString(input_bytes)
        _sci_tag:sci_tag.NrSlMacPduTagProto = sci_tag.NrSlMacPduTagProto(_msg)
        frameNum = _sci_tag.m_sfnSf.m_frameNum
        subframeNum = _sci_tag.m_sfnSf.m_subframeNum
        slotNum = _sci_tag.m_sfnSf.m_slotNum
        numerology = _sci_tag.m_sfnSf.m_numerology
        rnti = _sci_tag.m_rnti
        symStart = _sci_tag.m_symStart
        numSym = _sci_tag.m_numSym
        tbSize = _sci_tag.m_tbSize
        dstL2Id = _sci_tag.m_dstL2Id
        return (frameNum, subframeNum, slotNum, numerology, rnti, symStart, numSym, tbSize, dstL2Id)

def generate_sched_data() -> List[SourceUserScheduling]:
    v2x_scheduling_source_users: List[SourceUserScheduling] = []
    v2x_scheduling_all_users: List[UserScheduling] = []
    v2x_scheduling_all_users.append(UserScheduling(ue_id=11))
    v2x_scheduling_all_users.append(UserScheduling(ue_id=12))
    v2x_scheduling_all_users.append(UserScheduling(ue_id=13))
    v2x_scheduling_all_users.append(UserScheduling(ue_id=14))
    # v2x_scheduling_all_users[0].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=1, slRlcPduInfo=[]))
    # v2x_scheduling_all_users[0].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=2, slRlcPduInfo=[]))
    v2x_scheduling_all_users[0].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=1, slRlcPduInfo=[SlRlcPduInfo(1, 1), SlRlcPduInfo(10, 10)]))
    v2x_scheduling_all_users[0].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=2, slRlcPduInfo=[SlRlcPduInfo(2, 2), SlRlcPduInfo(20, 20)]))
    v2x_scheduling_all_users[1].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=5, slRlcPduInfo=[SlRlcPduInfo(5, 5), SlRlcPduInfo(50, 50)]))
    v2x_scheduling_all_users[1].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=6, slRlcPduInfo=[SlRlcPduInfo(6, 6), SlRlcPduInfo(60, 60)]))
    v2x_scheduling_all_users[2].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=5, slRlcPduInfo=[SlRlcPduInfo(5, 5), SlRlcPduInfo(50, 50)]))
    v2x_scheduling_all_users[2].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=6, slRlcPduInfo=[SlRlcPduInfo(6, 6), SlRlcPduInfo(60, 60)]))
    v2x_scheduling_all_users[3].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=5, slRlcPduInfo=[SlRlcPduInfo(5, 5), SlRlcPduInfo(50, 50)]))
    v2x_scheduling_all_users[3].add_single_scheduling(single_sched=SingleScheduling(m_frameNum=6, slRlcPduInfo=[SlRlcPduInfo(6, 6), SlRlcPduInfo(60, 60)]))

    v2x_scheduling_source_users.append((SourceUserScheduling(ue_id=9)))
    v2x_scheduling_source_users.append((SourceUserScheduling(ue_id=10)))
    v2x_scheduling_source_users.append((SourceUserScheduling(ue_id=11)))
    v2x_scheduling_source_users.append((SourceUserScheduling(ue_id=12)))
    v2x_scheduling_source_users[0].add_dest_user(v2x_scheduling_all_users[0])
    v2x_scheduling_source_users[0].add_dest_user(v2x_scheduling_all_users[1])
    v2x_scheduling_source_users[1].add_dest_user(v2x_scheduling_all_users[0])
    v2x_scheduling_source_users[1].add_dest_user(v2x_scheduling_all_users[1])
    v2x_scheduling_source_users[2].add_dest_user(v2x_scheduling_all_users[0])
    v2x_scheduling_source_users[2].add_dest_user(v2x_scheduling_all_users[1])
    v2x_scheduling_source_users[3].add_dest_user(v2x_scheduling_all_users[0])
    v2x_scheduling_source_users[3].add_dest_user(v2x_scheduling_all_users[1])
    v2x_scheduling_source_users[0].add_dest_user(v2x_scheduling_all_users[0+2])
    v2x_scheduling_source_users[0].add_dest_user(v2x_scheduling_all_users[1+2])
    v2x_scheduling_source_users[1].add_dest_user(v2x_scheduling_all_users[0+2])
    v2x_scheduling_source_users[1].add_dest_user(v2x_scheduling_all_users[1+2])
    v2x_scheduling_source_users[2].add_dest_user(v2x_scheduling_all_users[0+2])
    v2x_scheduling_source_users[2].add_dest_user(v2x_scheduling_all_users[1+2])
    v2x_scheduling_source_users[3].add_dest_user(v2x_scheduling_all_users[0+2])
    v2x_scheduling_source_users[3].add_dest_user(v2x_scheduling_all_users[1+2])
    return v2x_scheduling_source_users

def test_single_source_sched():
    _data_dict = {'Plmn': '111', 'SourceScheduling': [{'source_id': 1, 'destScheduling': [{'ue_id': 1, 'cReselCounter': 1, 'slResoReselCounter': 1, 'prevSlResoReselCounter': 1, 'nrSlHarqId': -1, 'nSelected': 1, 'tbTxCounter': 0, 'userScheduling': [{'m_frameNum': 3006, 'm_subframeNum': 2, 'm_slotNum': 0, 'm_numerology': 2, 'dstL2Id': 1, 'ndi': 1, 'rv': 255, 'priority': 0, 'slRlcPduInfo': [{'lcid': 4, 'size': 19800}], 'mcs': 14, 'numSlPscchRbs': 65535, 'slPscchSymStart': 65535, 'slPscchSymLength': 65535, 'slPsschSymStart': 3, 'slPsschSymLength': 3, 'slPsschSubChStart': 0, 'slPsschSubChLength': 50, 'maxNumPerReserve': 65535, 'txSci1A': False, 'slotNumInd': 0}, {'m_frameNum': 3006, 'm_subframeNum': 2, 'm_slotNum': 0, 'm_numerology': 2, 'dstL2Id': 1, 'ndi': 1, 'rv': 255, 'priority': 0, 'slRlcPduInfo': [{'lcid': 4, 'size': 33000}], 'mcs': 14, 'numSlPscchRbs': 65535, 'slPscchSymStart': 65535, 'slPscchSymLength': 65535, 'slPsschSymStart': 8, 'slPsschSymLength': 5, 'slPsschSubChStart': 0, 'slPsschSubChLength': 50, 'maxNumPerReserve': 65535, 'txSci1A': False, 'slotNumInd': 0}]}]}]}
    _plmn = _data_dict.get("Plmn")
    # the data that should be sent to the send callback should be the list of source user scheduling
    v2x_scheduling_all_users: List[SourceUserScheduling] = [SourceUserScheduling(-1, _source_sched) for _source_sched in _data_dict.get("SourceScheduling")]
    _msg_encoder = RicControlMessageEncoder()
    data_length, data_bytes = _msg_encoder.encode_scheduling_plmn(v2x_scheduling_all_users, _plmn)
    print(f"Data length {data_length}")
    print("Data bytes")
    print(data_bytes.hex())

if __name__ == '__main__':
    # test_single_source_sched()
    _asn1_c_lib = ctypes.CDLL("libe2sim.so", mode=ctypes.RTLD_GLOBAL)
    # _encoder = RicControlMessageEncoder()
    # print("decoding data")
    # v2x_scheduling_source_users = generate_sched_data()

    # _data_length, _data_bytes = _encoder.encode_scheduling_plmn(v2x_scheduling_source_users, "111")
    # print("Encoded data length " + str(_data_length))

    # print("Ended")

