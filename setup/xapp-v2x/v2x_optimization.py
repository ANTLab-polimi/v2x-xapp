import numpy as np
from typing import List, Tuple
from operator import itemgetter
from v2x_pre_optimize import V2XPreScheduling, UserPreoptimization
from transform_xml_to_dict_v2x import _JSON_PLMN
from v2x_ric_message_format import SourceUserScheduling, UserScheduling, SingleScheduling, SlRlcPduInfo
import pickle
import datetime
import logging
import sl_slot_validation
import copy
import random

_JSON_TIMESTAMP = 'time'
_USABLE_SYMBOLS_PER_SLOT = 13
_SYMBOL_START_SLOT = 0



McsEcrTable  = [
  0.08, 0.1, 0.11, 0.15, 0.19, 0.24, 0.3, 0.37, 0.44, 0.51, 0.3, 0.33, 0.37,
  0.42, 0.48, 0.54, 0.6, 0.43, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
  0.85, 0.89, 0.92
]

ModulationSchemeForMcs = [
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
  4, 4, 4, 4, 4, 4, 4,
  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
  2,      # reserved
  4,      # reserved
  6,      # reserved
]

# by default there are 12 subcarriers of RB, 1 of each is used for reference signal, remining only 11
def get_payload_size(mcs: int, rbNum:int, usefulSC:int = 11) -> int:
    rscElement = usefulSC * rbNum
    Rcode = McsEcrTable[mcs]
    Qm = ModulationSchemeForMcs[mcs]
    spectralEfficiency = rscElement * Qm * Rcode
    return int(np.floor(spectralEfficiency / 8))



# the sci format 2A has an overhead 5 bytes along the data part size
# we have only 1 subchannel for the configured bandwidht and 50 rbs per subchannel
def calculate_tb_size(mcs:int, availableSymbols:int, subchannelSize: int = 50, assignedSubchannels:int = 1) -> int:
    return get_payload_size(mcs=mcs, rbNum=subchannelSize*assignedSubchannels*availableSymbols)

def calculate_needed_nr_rbs_per_tb_size(mcs:int, tb_size:int, usefulSC:int = 11) -> int:
    # subchannel size is preconfigured, the assigned subchannels and available symbols might change
    Rcode = McsEcrTable[mcs]
    Qm = ModulationSchemeForMcs[mcs]
    min_nr_rbs_needed = int(np.ceil(tb_size*8/(Qm * Rcode*usefulSC)))
    return min_nr_rbs_needed

def calculate_needed_symbols_per_rbs(num_rbs, subchannel_size: int = 50, num_subchannels: int = 1) -> int:
    return int(np.ceil(num_rbs/(num_subchannels*subchannel_size)))


# The scheduling happening here needs to have information about the following:
# 1. the sorted list trasmissions tuples priority defined by the formla Tmax(1000ms)/(T2 - Head_of_line_delay)
# 1.1. Inside each of the tuple the following data are present:
# a) the source ue id b) the destination ue id (l2 channel id) c) the group interval id; only 1 group means
# we do not group in interval d)buffer size per group
# 2. The resources needed by each interval group (calculated in number of resource blocks)
# 2.1. the scheduling shall be equivalent to a knapsack multidimensional problem 
# We do a TDMA at allocating the resources, allocating all the subchannels for the duration of a single symbol


class V2XFormulation:
    def __init__(
            self,
            preoptimize: V2XPreScheduling,
            plmn: str = "110",
            final_bitmap: List[int] = []
    ):
        self.preoptimize: V2XPreScheduling = preoptimize
        self.plmn = plmn
        self.lcid:int = 4 # default value of lcid in ns3 - should be updated
        self.available_symbols_per_sl=14
        self.subchannel_size = 50 # accounted in number of rbs per subchannel
        self.number_subchannels = 1 # depends on the preconfig; our example has only 1 subchannel
        self.control_channel_rbs = 10
        self.useful_subcarriers_sl = 11 # 12 total - 1 for the reference signal
        self.mcs = 10 # preconfigured
        # the only configurable parameter is the number of subchannels assigned to an user
        # this will hold all the buffer status as indicated in pre optimize
        # source, dest, upper limit, resercation period, num packets and buffer size
        self._all_buffer_status: List[Tuple[int, int, float, float, int, int]] = []
        # a boolean list to hold information of whethe the buffer has been served or not
        self._buffer_served: List[bool] = []
        # the list of needed rbs per buffer
        self._needed_rbs_per_buffer: List[int] = []
        self._needed_symbols_per_buffer: List[int] = []
        self._served_symbols_per_buffer: List[int] = []
        self._buffer_being_served_ind:int = 0
        # the harq part
        self._harq_buffer_status: List[Tuple[int, int, int, int, int]] = []
        self._harq_buffer_served: List[bool] = []
        self._harq_needed_rbs_per_buffer: List[int] = []
        self._harq_needed_symbols_per_buffer: List[int] = []
        self._harq_buffer_being_served:int = 0
        self._connection_anticipate_schedule_slot_ind:int = 0
        self.final_bitmap: List[int] = final_bitmap
        self._future_reserved_resources_retx: List[sl_slot_validation.SlotResources] = [] 
        self._future_reserved_resources_last_inserted_frame:int = 0

    # the function will get all the tuple of all the connections
    # and will sort them based on the sorting order given by the formula in point 1.
    def _update_resource_request_by_priority(self):
        if self.preoptimize.is_data_updated():
            self._all_buffer_status = self.preoptimize.get_all_users_buffer_status()
            # _tuple[3] is reservation period and _tuple[2] is delay upper limit
            self._all_buffer_status.sort(key=lambda _tuple: _tuple[UserPreoptimization.BUFFER_RESERVATION_PERIOD] -  _tuple[UserPreoptimization.BUFFER_UPPER_LIMIT]) 
            self._buffer_served = [False]*len(self._all_buffer_status)
            # the added 5 byte are included of the SCI message format 2
            # it will hold the mcs for decoding facilitation
            self._needed_rbs_per_buffer = [5+calculate_needed_nr_rbs_per_tb_size(self.mcs, _buffer_status_tuple[UserPreoptimization.BUFFER_SIZE_INDEX]) for _buffer_status_tuple in self._all_buffer_status]
            self._needed_symbols_per_buffer = [calculate_needed_symbols_per_rbs(num_rbs) for num_rbs in self._needed_rbs_per_buffer]
            self._served_symbols_per_buffer = [0]*len(self._needed_symbols_per_buffer)
            self._buffer_being_served_ind = 0
            # harq buffer
            self._harq_buffer_status = self.preoptimize.get_all_users_harq_buffer_status()
            self._harq_buffer_served = [False]*len(self._harq_buffer_status)
            self._harq_needed_rbs_per_buffer = [calculate_needed_nr_rbs_per_tb_size(self.mcs, _buffer_status_tuple[UserPreoptimization.HARQ_BUFFER_SIZE_INDEX]) for _buffer_status_tuple in self._harq_buffer_status]
            self._harq_needed_symbols_per_buffer = [calculate_needed_symbols_per_rbs(num_rbs) for num_rbs in self._harq_needed_rbs_per_buffer]
            self._harq_served_symbols_per_buffer = [0]*len(self._harq_needed_symbols_per_buffer)
            self._harq_buffer_being_served_ind = 0
            # logger = logging.getLogger('')
            # logger.debug(f"Update buffer status: size {len(self._all_buffer_status)}, data")
            # logger.debug(self._all_buffer_status)
            # update the anticipated traffic scheduling
            self._connection_anticipate_schedule_slot_ind = 0

    def _add_source_scheduling_list(self, source_user_scheduling: List[SourceUserScheduling],
                                   source_ue_id: int, dest_ue_id: int,
                                   frame: int, subframe: int, slot: int,
                                   numerology: int, ndi: int,
                                   sym_start: int, sym_length: int,
                                   subchannel_start: int, subchannel_length: int ,
                                   nr_sl_harq_id: int= -1,
                                   txSci1A=False
                                   ):
        # create list of slrlcpudinfo
        # get tbsize from the Number of served symbols assinged to the user
        # always tx sci1A for decoding
        logger = logging.getLogger('')
        
        _tb_size = calculate_tb_size(self.mcs, sym_length) 
        _sl_rlc_pdu_info: List[SlRlcPduInfo] = [SlRlcPduInfo(lcid=self.lcid, size=int(_tb_size))]
        _single_sched = SingleScheduling(m_frameNum=frame, 
                                m_subframeNum=subframe,
                                m_slotNum=slot, 
                                m_numerology = numerology, 
                                # dstL2Id = self._all_buffer_status[self._buffer_being_served_ind][1],
                                dstL2Id = dest_ue_id,
                                ndi=ndi,
                                rv=2,# from GetRv in nr-sl-ue-mac-scheduler-ns3 which indicated the number of slot allocation
                                # in our case we only have 1 slot allocation and the mapping of rv for that is 2
                                priority=7, # default value in pscch database
                                slRlcPduInfo = _sl_rlc_pdu_info,
                                mcs=self.mcs,
                                slPsschSymStart = sym_start,
                                slPsschSymLength = sym_length,
                                slPsschSubChStart = subchannel_start,
                                slPsschSubChLength = subchannel_length,
                                txSci1A=txSci1A, # for the moment we won't send the pscch messages
                                slPscchSymStart=0, # fist symbol in each slot is reserved for the sending of scch
                                slPscchSymLength=1,
                                maxNumPerReserve=1,
                                numSlPscchRbs=10,
                                )
        
        # logger.debug("Single scheduling")
        # logger.debug(str(_single_sched))
        
        _filter_source_user = list(filter(lambda source_sched: source_sched.ue_id == source_ue_id, source_user_scheduling))
        if len(_filter_source_user) == 0:
            # we create the User scheduling with all counters to 1
            _dest_sched = UserScheduling(ue_id=dest_ue_id, cReselCounter=1, 
                                         slResoReselCounter=1, 
                                         prevSlResoReselCounter=1,
                                         nrSlHarqId=nr_sl_harq_id,
                                         nSelected=sl_slot_validation._RETRASMISSIONS, 
                                         tbTxCounter=0)
            _dest_sched.add_single_scheduling(_single_sched)
            _source_user_scheduling = SourceUserScheduling(ue_id=source_ue_id)
            _source_user_scheduling.add_dest_user(_dest_sched)
            source_user_scheduling.append(_source_user_scheduling)
        else:
            # the other option is the length to be 1 as there should be only 1 source scheduling
            # with the give ue id
            _source_user_scheduling:SourceUserScheduling = _filter_source_user[0]
            # check if the given destinatio exists
            _dest_sched_list:List[UserScheduling] = list(filter(lambda _dest_sched:_dest_sched.ue_id == dest_ue_id, _source_user_scheduling.destination_scheduling))
            if len(_dest_sched_list)>0:
                # scheduling for this user already exist
                _dest_sched =_dest_sched_list[0]
            else:
                # add destination scheduling
                _dest_sched = UserScheduling(dest_ue_id)
                _dest_sched.add_single_scheduling(_single_sched)
                _source_user_scheduling.add_dest_user(_dest_sched)
            # add single scheduling in the dest sched obj
            _dest_sched.add_single_scheduling(_single_sched)
            
            # add sl harq if if it is retx 
            if ndi == 1:
                _dest_sched.nrSlHarqId = nr_sl_harq_id
                # nr_sl_harq_id

    def schedule_anticipated_traffic(self, frame: int, subframe: int, slot: int)->List[SourceUserScheduling]:
        source_user_scheduling: List[SourceUserScheduling] = []
        # if there is no data to anticipate scheduling return empty list
        if (len(self._all_buffer_status) ==0 ) & (len(self._harq_buffer_status) ==0):
            return []
        logger = logging.getLogger('')
        _start_symbol_in_slot = 1
        _sched_symbols = 0
        _source = -1
        _dest_ue_id = -1
        if len(self._all_buffer_status) > 0:
            _source = self._all_buffer_status[ self._connection_anticipate_schedule_slot_ind][UserPreoptimization.BUFFER_SOURCE_ID]
            _dest_ue_id = self._all_buffer_status[ self._connection_anticipate_schedule_slot_ind][UserPreoptimization.BUFFER_DEST_ID]
        # elif len(self._harq_buffer_status) > 0:
        #     # we take the harq buffer as reference
        #     _source = self._harq_buffer_status[ self._connection_anticipate_schedule_slot_ind][UserPreoptimization.HARQ_SOURCE_ID]
        #     _dest_ue_id = self._harq_buffer_status[ self._connection_anticipate_schedule_slot_ind][UserPreoptimization.HARQ_DEST_ID]
        # check if there exist data of harq
        _harq_buffer_list = list(filter(lambda _tuple: ((_tuple[UserPreoptimization.HARQ_SOURCE_ID] == _source ) & (_tuple[UserPreoptimization.HARQ_DEST_ID] == _dest_ue_id)), self._harq_buffer_status))
        if (_source>-1) & (_dest_ue_id>-1):
            # if len(_harq_buffer_list)>0:
            if False:
                # divide equally harq data and new tx
                _sched_symbols += int(np.ceil(_USABLE_SYMBOLS_PER_SLOT/2))
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                        source_ue_id= _source,
                                                        dest_ue_id=_dest_ue_id,
                                                        frame=frame, subframe=subframe, slot=slot, 
                                                        numerology=2, ndi=0,
                                                        sym_start = _start_symbol_in_slot, 
                                                        sym_length=_sched_symbols,
                                                        subchannel_start=0, 
                                                        subchannel_length=self.number_subchannels,
                                                        nr_sl_harq_id=_harq_buffer_list[0][UserPreoptimization.HARQ_ID_INDEX]
                                                        )
                _start_symbol_in_slot += _sched_symbols
            # allocate the remaining for the new data 
            _sched_symbols = _USABLE_SYMBOLS_PER_SLOT - _start_symbol_in_slot+1
            logger.debug(f"Anticipated scheduling  for con ({_source}, {_dest_ue_id}) symb harq {(1, _start_symbol_in_slot)} and new ({_start_symbol_in_slot}, {_sched_symbols})")
            
            self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                source_ue_id= _source,
                                                dest_ue_id=_dest_ue_id,
                                                frame=frame, subframe=subframe, slot=slot, 
                                                numerology=2, ndi=1,
                                                sym_start = _start_symbol_in_slot,  
                                                sym_length=_sched_symbols,
                                                subchannel_start=0, 
                                                subchannel_length=self.number_subchannels,
                                                # txSci1A=True
                                                txSci1A = True# we only send 1 pscch per slotW
                                                )
            
        # user served; move to the next user in circular way
        self._connection_anticipate_schedule_slot_ind = (self._connection_anticipate_schedule_slot_ind+1) % len(self._all_buffer_status)
        return source_user_scheduling
    
    def schedule_slot(self, frame: int, subframe: int, slot: int)->List[SourceUserScheduling]:
        self._update_resource_request_by_priority()
        # check if data scheduling has finished
        if (self._buffer_being_served_ind == len(self._all_buffer_status)) & \
            (self._harq_buffer_being_served_ind == len(self._harq_buffer_status)):
            return self.schedule_anticipated_traffic(frame, subframe, slot) #[]
        # the first symbol in each slot is reserved for the scch message
        _used_symbols_in_slot = 0
        _start_symbol_in_slot = 1
        source_user_scheduling: List[SourceUserScheduling] = []
        logger = logging.getLogger('')
        # logger.debug(f"Schedule slot ({frame}, {subframe}, {slot})")
        logger.debug("\n")
        logger.debug(f"Number of scheduling request {len(self._needed_rbs_per_buffer)}")
        # logger.debug(f"Needed rbs per buffer {self._needed_rbs_per_buffer}")
        logger.debug(f"Needed symbols per buffer { self._needed_symbols_per_buffer}")
        logger.debug(f"Served symbols per buffer { self._served_symbols_per_buffer}")
        logger.debug(f"Buffer being served ind {self._buffer_being_served_ind}")
        logger.debug(f"Harq buffer needed symbols {self._harq_needed_symbols_per_buffer}")
        logger.debug(f"Harq buffer served symbols {self._harq_served_symbols_per_buffer}")
        logger.debug(f"New data buffer src destination pair {[(_tuple[UserPreoptimization.BUFFER_SOURCE_ID], _tuple[UserPreoptimization.BUFFER_DEST_ID]) for _tuple in self._all_buffer_status]}")
        # we serve a single user in a slot and just decide the nr of symbols per harq and ndi
        # _harq_symbols
        # the buffer status is updated in base user requests
        # check we have not reached the out of bound 
        _user_id_to_serve = -1
        if self._buffer_being_served_ind < len(self._all_buffer_status):
            _user_id_to_serve = self._all_buffer_status[self._buffer_being_served_ind][UserPreoptimization.BUFFER_SOURCE_ID]
        elif self._harq_buffer_being_served_ind < len(self._harq_buffer_status):
            _user_id_to_serve = self._harq_buffer_status[self._harq_buffer_being_served_ind][UserPreoptimization.HARQ_SOURCE_ID]
        _unserved_symbols_for_user = 0
        # _remaining_symbols = _USABLE_SYMBOLS_PER_SLOT
        # get the symbols needed for harq and new traffic

        
        _list_new_data_buffer_status_indexes = [_ind for _ind, _value in enumerate(self._all_buffer_status) if _value[UserPreoptimization.BUFFER_SOURCE_ID] == _user_id_to_serve]
        _unserved_symbols_new_data_array = [self._needed_symbols_per_buffer[_ind] - self._served_symbols_per_buffer[_ind] for _ind in _list_new_data_buffer_status_indexes]
        _scheduled_symbols_new_data = [0]*len(_unserved_symbols_new_data_array)

        _list_harq_data_buffer_status_indexes = [_ind for _ind, _value in enumerate(self._harq_buffer_status) if _value[UserPreoptimization.BUFFER_SOURCE_ID] == _user_id_to_serve]
        _unserved_symbols_harq_array = [self._harq_needed_symbols_per_buffer[_ind]+1 - self._harq_served_symbols_per_buffer[_ind] for _ind in _list_harq_data_buffer_status_indexes]
        _scheduled_symbols_harq_data = [0]*len(_unserved_symbols_harq_array)

        logger.debug(f"Scheduling user with id {_user_id_to_serve} with unserved harq {_unserved_symbols_harq_array} and new data unserved {_unserved_symbols_new_data_array}")

        # _unserved_symbols_new_data = int(sum(_unserved_symbols_new_data_array))
        # _unserved_symbols_harq = int(sum(_unserved_symbols_harq_array))

        # the part of new data
        _unserved_symbols_new_data_array_ind = 0
        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (_unserved_symbols_new_data_array_ind < len(_unserved_symbols_new_data_array)):
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            if _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind]>_remaining_available_symbols:
                _scheduled_symbols_new_data[_unserved_symbols_new_data_array_ind] = _remaining_available_symbols
                _used_symbols_in_slot +=_remaining_available_symbols
            else:
                _scheduled_symbols_new_data[_unserved_symbols_new_data_array_ind] = _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind]
                _used_symbols_in_slot += _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind]
                _unserved_symbols_new_data_array_ind+=1

        _unserved_symbols_harq_array_ind = 0
        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (_unserved_symbols_harq_array_ind < len(_unserved_symbols_harq_array)):
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            if  _unserved_symbols_harq_array[_unserved_symbols_harq_array_ind] > _remaining_available_symbols:
                # it exceeds the need, thus we assign the remaining available symbols
                _scheduled_symbols_harq_data[_unserved_symbols_harq_array_ind] = _remaining_available_symbols
                # user all the symbols
                _used_symbols_in_slot +=_remaining_available_symbols
            else:
                # we have more remaining symbols than needed, thus we assing the needed symbols
                _scheduled_symbols_harq_data[_unserved_symbols_harq_array_ind] = _unserved_symbols_harq_array[_unserved_symbols_harq_array_ind]
                _used_symbols_in_slot+=_unserved_symbols_harq_array[_unserved_symbols_harq_array_ind]
                # go the next buffer
                _unserved_symbols_harq_array_ind+=1

        logger.debug(f"Scheduled symbols new data {_scheduled_symbols_new_data} and harq data {_scheduled_symbols_harq_data}")

        _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
        _num_active_buffers = len(_scheduled_symbols_new_data) + len(_scheduled_symbols_harq_data)
        # if there is reamaining symbols in slot we distribute them as them by adding a symbol at each buffer
        if (_remaining_available_symbols > 0) & (_num_active_buffers > 0):
            _symbols_to_add_per_buffer =int( np.floor(_remaining_available_symbols/_num_active_buffers)) # added to all the buffers _symbols_to_add_per_buffer
            _symbols_to_add_to_first_buffers = _remaining_available_symbols%_num_active_buffers # added by 1 to first _symbols_to_add_to_first_buffers buffers
            # add complete symbols per buffer
            _scheduled_symbols_harq_data = [num_symb + _symbols_to_add_per_buffer for num_symb in _scheduled_symbols_harq_data]
            _scheduled_symbols_new_data = [num_symb + _symbols_to_add_per_buffer for num_symb in _scheduled_symbols_new_data]
            
            # add remaining symbols to the first buffers starting with the harq buffers
            # if we have harq buffer,then we check if the single symbols to add fit all the buffers or not
            # we take the min between the symbols which can be given and the size of the vector
            # so that, first we do not assign more than _USABLE_SYMBOLS_PER_SLOT and second assign to the active harq buffers
            _symbols_to_add_to_harq_buffer_last_element_index = min(_symbols_to_add_to_first_buffers, len(_scheduled_symbols_harq_data))
            if _symbols_to_add_to_harq_buffer_last_element_index>0:
                # meas that the length of harq buffer is greater than 0, thus we assign the symbols
                for _ind in range(_symbols_to_add_to_harq_buffer_last_element_index):
                    _scheduled_symbols_harq_data[_ind] = _scheduled_symbols_harq_data[_ind]+1

            _symbols_to_add_to_harq_buffer_last_element_index = max(0, _symbols_to_add_to_first_buffers - _symbols_to_add_to_harq_buffer_last_element_index)
            if _symbols_to_add_to_harq_buffer_last_element_index>0:
                # meas that the length of harq buffer is greater than 0, thus we assign the symbols
                for _ind in range(_symbols_to_add_to_harq_buffer_last_element_index):
                    _scheduled_symbols_new_data[_ind] = _scheduled_symbols_new_data[_ind]+1

        logger.debug(f"After redestribution symbols new data {_scheduled_symbols_new_data} and harq data {_scheduled_symbols_harq_data}")

        # new data scheduling
        for _ind_filtered_array, _sched_symbols in enumerate (_scheduled_symbols_new_data):
            _original_new_data_buffer_status_ind = _list_new_data_buffer_status_indexes[_ind_filtered_array]
            logger.debug(f"Scheduled new data s {self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_SOURCE_ID]}" + \
                         f" & dest {self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_DEST_ID]} " +\
                        f" in slot ({frame}, {subframe}, {slot}) " 
                        f" sym start {_start_symbol_in_slot} & sym length {_sched_symbols}")
            if _sched_symbols >0:
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                    source_ue_id= self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_SOURCE_ID],
                                                    dest_ue_id=self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_DEST_ID],
                                                    frame=frame, subframe=subframe, slot=slot, 
                                                    numerology=2, ndi=1,
                                                    sym_start = _start_symbol_in_slot, 
                                                    sym_length=_sched_symbols,
                                                    subchannel_start=0, 
                                                    subchannel_length=self.number_subchannels,
                                                    # txSci1A=True
                                                    txSci1A = _ind_filtered_array == 0# we only send 1 pscch per slotW
                                                    )
                _start_symbol_in_slot += _sched_symbols
            if self._served_symbols_per_buffer[_original_new_data_buffer_status_ind] + _sched_symbols >= self._needed_symbols_per_buffer[_original_new_data_buffer_status_ind]:
                self._served_symbols_per_buffer[_original_new_data_buffer_status_ind] = self._needed_symbols_per_buffer[_original_new_data_buffer_status_ind]
            else:
                self._served_symbols_per_buffer[_original_new_data_buffer_status_ind]+=_sched_symbols

        # check the data to be sent
        for _ind_filtered_array, _sched_symbols in enumerate (_scheduled_symbols_harq_data):

            # add data to the list
            _original_harq_buffer_status_ind = _list_harq_data_buffer_status_indexes[_ind_filtered_array]
            # logger.debug(f"Buffer status of ind {self._buffer_being_served_ind}: {self._all_buffer_status[self._buffer_being_served_ind]}")
            logger.debug(f"Scheduled harq s {self._harq_buffer_status[_original_harq_buffer_status_ind][UserPreoptimization.HARQ_SOURCE_ID]}" + \
                         f" & dest {self._harq_buffer_status[_original_harq_buffer_status_ind][UserPreoptimization.HARQ_DEST_ID]} " +\
                        f" in slot ({frame}, {subframe}, {slot}) " 
                        f" sym start {_start_symbol_in_slot} & sym length {_sched_symbols}")
            
            self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                 source_ue_id= self._harq_buffer_status[_original_harq_buffer_status_ind][UserPreoptimization.HARQ_SOURCE_ID],
                                                 dest_ue_id=self._harq_buffer_status[_original_harq_buffer_status_ind][UserPreoptimization.HARQ_DEST_ID],
                                                 frame=frame, subframe=subframe, slot=slot, 
                                                 numerology=2, ndi=0,
                                                 sym_start = _start_symbol_in_slot, 
                                                 sym_length=_sched_symbols,
                                                 subchannel_start=0, 
                                                 subchannel_length=self.number_subchannels,
                                                 nr_sl_harq_id=self._harq_buffer_status[_original_harq_buffer_status_ind][UserPreoptimization.HARQ_ID_INDEX]
                                                 )
            # change the start symbols for the next scheduling
            _start_symbol_in_slot += _sched_symbols
            # need to change the vectors 
            # check if after shceduling harq user we change the index and move to a new buffer
            # if what scheduled reaches what needed, we set served as what needed
            if self._harq_served_symbols_per_buffer[_original_harq_buffer_status_ind] + _sched_symbols >= self._harq_needed_symbols_per_buffer[_original_harq_buffer_status_ind]:
                self._harq_served_symbols_per_buffer[_original_harq_buffer_status_ind] = self._harq_needed_symbols_per_buffer[_original_harq_buffer_status_ind]
            else:
                self._harq_served_symbols_per_buffer[_original_harq_buffer_status_ind] += _sched_symbols

        
        # at the end we should update the reports of served symbols
        # update the buffer index
        _unserve_bytes_list = [a-b for a,b in zip(self._needed_symbols_per_buffer, self._served_symbols_per_buffer)]
        try:
            # the first index in buffer for which the difference of needed and served is 0
            self._buffer_being_served_ind = next((_ind for (_ind, _item) in enumerate(_unserve_bytes_list) if _item>0), 
                                                 len(self._needed_symbols_per_buffer))
        except TypeError:
            self._buffer_being_served_ind = len(self._needed_symbols_per_buffer)

        _unserve_bytes_list = [a-b for a,b in zip(self._harq_needed_symbols_per_buffer, self._harq_served_symbols_per_buffer)]
        try:
            # the first index in buffer for which the difference of needed and served is 0
            self._harq_buffer_being_served_ind = next((_ind for (_ind, _item) in enumerate(_unserve_bytes_list) if _item>0),
                                                      len(self._harq_needed_symbols_per_buffer))
        except TypeError:
            self._harq_buffer_being_served_ind = len(self._harq_needed_symbols_per_buffer)
        logger.debug("\n")
        return source_user_scheduling
        
    def schedule_only_new_data(self, frame: int, subframe: int, slot: int)->List[SourceUserScheduling]:
        logger = logging.getLogger('')
        self._update_resource_request_by_priority()
        # check if data scheduling has finished
        if (self._buffer_being_served_ind == len(self._all_buffer_status)) & \
            (self._harq_buffer_being_served_ind == len(self._harq_buffer_status)):
            # return self.schedule_anticipated_traffic(frame, subframe, slot) #[]
            return []
        # the first symbol in each slot is reserved for the scch message

        _used_symbols_in_slot = 0
        _start_symbol_in_slot = 1
        # get the number of user symbols from retx
        _l_retx_resources = list(filter(lambda resources: ((resources.frame == frame) & 
                                                       (resources.subframe == subframe) & 
                                                       (resources.slot == slot)), 
                                    self._future_reserved_resources_retx))
        _future_reserved_ues = []
        # remove 
        for _resources_retx in self._future_reserved_resources_retx:
            if _resources_retx.frame < frame:
                self._future_reserved_resources_retx.remove(_resources_retx)
        if self._future_reserved_resources_last_inserted_frame < frame:
            self._future_reserved_resources_last_inserted_frame = frame
        if len(_l_retx_resources)>0:
            _start_symbol_in_slot = _l_retx_resources[0].symStart + _l_retx_resources[0].numSymbols
            _used_symbols_in_slot = _l_retx_resources[0].numSymbols
            _future_reserved_ues = _l_retx_resources[0].sched_ues
        
        source_user_scheduling: List[SourceUserScheduling] = []
        
        logger.debug("\n")
        logger.debug(f"Schedule slot ({frame}, {subframe}, {slot})")
        logger.debug(f"schedule_only_new_data")
        logger.debug(f"Number of scheduling request {len(self._needed_rbs_per_buffer)}")
        # logger.debug(f"Needed rbs per buffer {self._needed_rbs_per_buffer}")
        logger.debug(f"Needed symbols per buffer { self._needed_symbols_per_buffer}")
        logger.debug(f"Served symbols per buffer { self._served_symbols_per_buffer}")
        logger.debug(f"Buffer being served ind {self._buffer_being_served_ind}")
        logger.debug(f"Harq buffer needed symbols {self._harq_needed_symbols_per_buffer}")
        logger.debug(f"Harq buffer served symbols {self._harq_served_symbols_per_buffer}")
        logger.debug(f"New data buffer src destination pair {[(_tuple[UserPreoptimization.BUFFER_SOURCE_ID], _tuple[UserPreoptimization.BUFFER_DEST_ID]) for _tuple in self._all_buffer_status]}")
        logger.debug(f"future reserved ues {_future_reserved_ues}")
        # the buffer status is updated in base user requests
        # check we have not reached the out of bound 

        _list_new_data_buffer_status_indexes = [_ind for _ind, _ in enumerate(self._all_buffer_status)]
        _unserved_symbols_new_data_array = [self._needed_symbols_per_buffer[_ind] - self._served_symbols_per_buffer[_ind] for _ind in _list_new_data_buffer_status_indexes]
        _scheduled_symbols_new_data = [0]*len(_unserved_symbols_new_data_array)

        # the part of new data
        _unserved_symbols_new_data_array_ind = 0
        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (_unserved_symbols_new_data_array_ind < len(_unserved_symbols_new_data_array)):
            # check if the user has already been scheduled in this slot
            # if yes we do not schedule this user anymore in this slot
            if self._all_buffer_status[_unserved_symbols_new_data_array_ind][UserPreoptimization.BUFFER_SOURCE_ID] in _future_reserved_ues:
                _unserved_symbols_new_data_array_ind+=1
                continue
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            if _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind] < 1:
                _unserved_symbols_new_data_array_ind+=1
            elif _remaining_available_symbols == 0:
                break
            elif _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind]>_remaining_available_symbols:
                _scheduled_symbols_new_data[_unserved_symbols_new_data_array_ind] = _remaining_available_symbols
                _used_symbols_in_slot +=_remaining_available_symbols
                # serve only 1 user in this slot to avoid collision of PSCCH
                break
            else:
                _scheduled_symbols_new_data[_unserved_symbols_new_data_array_ind] = _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind]
                _used_symbols_in_slot += _unserved_symbols_new_data_array[_unserved_symbols_new_data_array_ind]
                _unserved_symbols_new_data_array_ind+=1
                # serve only 1 user in this slot to avoid collision of PSCCH
                break
        
        logger.debug(f"Scheduled symbols new data {_scheduled_symbols_new_data}")

        _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)

        # new data scheduling
        for _ind_filtered_array, _sched_symbols in enumerate (_scheduled_symbols_new_data):
            _original_new_data_buffer_status_ind = _list_new_data_buffer_status_indexes[_ind_filtered_array]
            if _sched_symbols > 0:
                logger.debug(f"Scheduled new data s {self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_SOURCE_ID]}" + \
                            f" & dest {self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_DEST_ID]} " +\
                            f" in slot ({frame}, {subframe}, {slot}) " 
                            f" sym start {_start_symbol_in_slot} & sym length {_sched_symbols}")
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                    source_ue_id= self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_SOURCE_ID],
                                                    dest_ue_id=self._all_buffer_status[_original_new_data_buffer_status_ind][UserPreoptimization.BUFFER_DEST_ID],
                                                    frame=frame, subframe=subframe, slot=slot, 
                                                    numerology=2, ndi=1,
                                                    sym_start = _start_symbol_in_slot, 
                                                    sym_length=_sched_symbols,
                                                    subchannel_start=0, 
                                                    subchannel_length=self.number_subchannels,
                                                    txSci1A=True
                                                    # txSci1A = _ind_filtered_array == 0# we only send 1 pscch per slotW
                                                    )
                _start_symbol_in_slot += _sched_symbols
                # insert user in the list of scheduled ues 
            if self._served_symbols_per_buffer[_original_new_data_buffer_status_ind] + _sched_symbols >= self._needed_symbols_per_buffer[_original_new_data_buffer_status_ind]:
                self._served_symbols_per_buffer[_original_new_data_buffer_status_ind] = self._needed_symbols_per_buffer[_original_new_data_buffer_status_ind]
            else:
                self._served_symbols_per_buffer[_original_new_data_buffer_status_ind]+=_sched_symbols

        # at the end we should update the reports of served symbols
        # update the buffer index
        _unserve_bytes_list = [a-b for a,b in zip(self._needed_symbols_per_buffer, self._served_symbols_per_buffer)]
        try:
            # the first index in buffer for which the difference of needed and served is 0
            self._buffer_being_served_ind = next((_ind for (_ind, _item) in enumerate(_unserve_bytes_list) if _item>0), 
                                                 len(self._needed_symbols_per_buffer))
        except TypeError:
            self._buffer_being_served_ind = len(self._needed_symbols_per_buffer)
        logger.debug("\n")
        return source_user_scheduling

    def add_new_frame_resources(self):
        logger = logging.getLogger('')
        self._future_reserved_resources_last_inserted_frame += 1
        logger.debug(f"Adding new frame resources {self._future_reserved_resources_last_inserted_frame}")
        frame_sl_slots: List[sl_slot_validation.SlotResources] = sl_slot_validation.get_all_sidelink_slots_in_frame(self.final_bitmap, self._future_reserved_resources_last_inserted_frame)
        # logger.debug(f"Size of reser resoruces before extend {len(self._future_reserved_resources_retx)}")
        self._future_reserved_resources_retx.extend(frame_sl_slots)
        # logger.debug(f"Size of reser resoruces after extend {len(self._future_reserved_resources_retx)}")
        # for _fut_res in self._future_reserved_resources_retx:
        #     logger.debug(f"{str(_fut_res)}")

    def find_resources_retx(self, reference_frame:int, ue_id:int, num_symbols: int = 1)-> List[int]:
        # logger = logging.getLogger('')
        # logger.debug(f"find resources retx frame {reference_frame} & num symb {num_symbols}")
        return [_ind for _ind, _item in enumerate(self._future_reserved_resources_retx) if ((_item.get_unassigned_symbols()>num_symbols) & (_item.frame==reference_frame) & (ue_id not in _item.sched_ues))]
        
    def find_next_resources_retx(self, starting_frame: int, ue_id:int, num_symbols: int = 1) -> int:
        logger = logging.getLogger('')
        _ref_frame = starting_frame+1
        _l_next_resources: List[int] = []
        _v_len_next_resources = len(_l_next_resources)
        while(_v_len_next_resources == 0):
            _l_next_resources = self.find_resources_retx(_ref_frame, ue_id, num_symbols)
            _v_len_next_resources = len(_l_next_resources)
            logger.debug(f"Find resources: Ref frame {_ref_frame}, num symb {num_symbols}, ue id {ue_id} len resources {_v_len_next_resources}")
            if _v_len_next_resources==0:
                # insert new frame in the resources
                _ref_frame = self._future_reserved_resources_last_inserted_frame + 1
                # it means we are at the edge of reference resources, thus we need to add new ones
                self.add_new_frame_resources()  
            else:
                # it means we have found available resources 
                # we select a random index of the returned resources
                _resources_ind = random.randint(0, _v_len_next_resources-1)
                # original index in the original vector
                _original_ind = _l_next_resources[_resources_ind]
                return _original_ind

    def insert_resources_future_retx(self, slot_resources_ind: int, num_symbols: int, ue_id:int):
        logger = logging.getLogger('')
        _sym_start = self._future_reserved_resources_retx[slot_resources_ind].symStart +\
                    self._future_reserved_resources_retx[slot_resources_ind].numSymbols
        # logger.debug(f"resource index {slot_resources_ind} & num symb {num_symbols} & sym start {_sym_start}")
        # logger.debug(f"future reserved {str(self._future_reserved_resources_retx[slot_resources_ind])}")
        # for _fut_res in self._future_reserved_resources_retx:
        #     logger.debug(f"{str(_fut_res)}")
        self._future_reserved_resources_retx[slot_resources_ind].append_tti(_sym_start, num_symbols)
        self._future_reserved_resources_retx[slot_resources_ind].sched_ues.append(ue_id)
        logger.debug(f"scheduled ues {self._future_reserved_resources_retx[slot_resources_ind].sched_ues}")
        # for _fut_res in self._future_reserved_resources_retx:
        #     logger.debug(f"{str(_fut_res)}")
        # self._future_reserved_resources_retx[slot_resources_ind].numSymbols += num_symbols
    
    def schedule_only_retx_data(self, num_rext:int, num_retx_ind:int, 
                                new_data_sched:List[SourceUserScheduling])->List[SourceUserScheduling]:
        # _resources:sl_slot_validation.SlotResources = sl_slot_validation.SlotResources(frame, subframe, slot, [])
        # extract the scheduled new data
        logger = logging.getLogger('')
        # logger.debug(f"Reference frame ({frame}): ")
        _l_sourceSched_retx:List[SourceUserScheduling] = []
        _ndi = 0
        # _l_sourceSched_next = copy.deepcopy(new_data_sched)
        for _source in new_data_sched:
            _source_copy = copy.deepcopy(_source)
            logger.debug(f"Scheduled retx data s {_source_copy.ue_id}")
            for _dest in _source_copy.destination_scheduling:
                _dest.nSelected = num_rext-1
                _dest.tbTxCounter = num_retx_ind
                # logger.debug(f" dest {_dest.ue_id}")
                for _user in _dest.user_scheduling:
                    logger.debug(f"({_user._m_frameNum}, {_user._m_subframeNum}, {_user._m_slotNum}) ue id {_source.ue_id} ndi {_ndi} " +\
                                 f" sym start {_user._slPsschSymStart} & sym length {_user._slPsschSymLength}")
                    ## insert new retx
                    _retx_resources_ind = self.find_next_resources_retx(_user._m_frameNum, 
                                                                        _source.ue_id,
                                                                        _user._slPsschSymLength)
                    _retx_resources = self._future_reserved_resources_retx[_retx_resources_ind]
                    # number of symbols remain the same
                    # psschsym start symbols is the last used symbols of the reference resources
                    _user._slPsschSymStart = _retx_resources.symStart + _retx_resources.numSymbols
                    self.insert_resources_future_retx(_retx_resources_ind, _user._slPsschSymLength, _source.ue_id)
                    _user._m_frameNum = _retx_resources.frame
                    _user._m_subframeNum = _retx_resources.subframe
                    _user._m_slotNum = _retx_resources.slot
                    _user._ndi = 0
            _l_sourceSched_retx.append(_source_copy)
        return _l_sourceSched_retx
    
    def update_ref_retx(self, sourceSched: List[SourceUserScheduling], num_rext:int, num_retx_ind:int, 
                        frame:int, subframe:int, slot:int)->tuple[list[SourceUserScheduling], int, int, int]:
        logger = logging.getLogger('')
        logger.debug(f"in slot ({frame}, {subframe}, {slot}): ")
        _l_sourceSched_next = copy.deepcopy(sourceSched)
        for _source in _l_sourceSched_next:
            logger.debug(f"Scheduled retx data s {_source.ue_id}")
            for _dest in _source.destination_scheduling:
                _dest.nSelected = num_rext-1
                _dest.tbTxCounter = num_retx_ind
                logger.debug(f" dest {_dest.ue_id}")
                for _user in _dest.user_scheduling:
                    _ndi = 0
                    _user.change_reference_slot(frame, subframe, slot, _ndi)
                    logger.debug(f"ndi {_ndi} " +\
                                 f" sym start {_user._slPsschSymStart} & sym length {_user._slPsschSymLength}")
        return _l_sourceSched_next
            
    
    # the scheduled scheme is a simple TDMA, where we assign a symbol over the entire bandwidth
    def schedule_slot_multi_user_per_slot(self, frame: int, subframe: int, slot: int)->List[SourceUserScheduling]:
        # TODO: Consider the SCI message header
        # first update the buffer status if new data has arrived
        self._update_resource_request_by_priority()

        # check if data scheduling has finished
        if (self._buffer_being_served_ind == len(self._all_buffer_status)) & \
            (self._harq_buffer_being_served_ind == len(self._harq_buffer_status)):
            return self.schedule_anticipated_traffic(frame, subframe, slot)

        # the first symbol in each slot is reserved for the scch message
        _used_symbols_in_slot = 1
        # we exit the while loop when we have used whole of the symbols in the slot
        # or we have serverd all of the buffer
        source_user_scheduling: List[SourceUserScheduling] = []
        logger = logging.getLogger('')
        # logger.debug(f"Schedule slot ({frame}, {subframe}, {slot})")
        # logger.debug(f"Number of scheduling request {len(self._needed_rbs_per_buffer)}")
        # logger.debug(f"Needed rbs per buffer {self._needed_rbs_per_buffer}")
        # logger.debug(f"Needed symbols per buffer { self._needed_symbols_per_buffer}")
        # logger.debug(f"Buffer being served ind {self._buffer_being_served_ind}")
        # logger.debug(f"Harq buffer needed symbols {self._harq_needed_symbols_per_buffer}")
        # we serve first all the harq buffer
        _num_max_iter = _USABLE_SYMBOLS_PER_SLOT
        _iter_ind = 0
        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (self._buffer_being_served_ind < len(self._served_symbols_per_buffer)):
            # first case is when the available symbols in slot is smaller than what needed by buffer
            # we assign all the symbols to that buffer
            _iter_ind+=1
            _served_symbols = 0
            _needed_unserved_symbols = (self._needed_symbols_per_buffer[self._buffer_being_served_ind] - \
                                        self._served_symbols_per_buffer[self._buffer_being_served_ind])
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            if _needed_unserved_symbols <= 0:
                _finished_serving_user = True
            else:
                _finished_serving_user = False
            if  _needed_unserved_symbols > _remaining_available_symbols:
                _served_symbols = _remaining_available_symbols
                self._served_symbols_per_buffer[self._buffer_being_served_ind]+=_served_symbols
                _used_symbols_in_slot += _served_symbols
            else:
                # we assign the amount of resources needed
                _served_symbols = _needed_unserved_symbols
                self._served_symbols_per_buffer[self._buffer_being_served_ind] += _served_symbols
                # move to the next buffer until
                _finished_serving_user = True
                _used_symbols_in_slot += _served_symbols
            # logger.debug(f"Served symbols {_served_symbols}, used symbols in slot {_used_symbols_in_slot}")
            if _served_symbols > 0:
                # add data to the list

                # logger.debug(f"Buffer status of ind {self._buffer_being_served_ind}: {self._all_buffer_status[self._buffer_being_served_ind]}")
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                source_ue_id= self._all_buffer_status[self._buffer_being_served_ind][UserPreoptimization.BUFFER_SOURCE_ID],
                                                dest_ue_id=self._all_buffer_status[self._buffer_being_served_ind][UserPreoptimization.BUFFER_DEST_ID],
                                                frame=frame, subframe=subframe, slot=slot, 
                                                numerology=2, ndi=1,
                                                sym_start = _used_symbols_in_slot, 
                                                sym_length=_served_symbols,
                                                subchannel_start=0, 
                                                subchannel_length=self.number_subchannels
                                                )
            # move to the next user if we finished serving this user
            if _finished_serving_user:
                self._buffer_being_served_ind +=1    

            if (_iter_ind >_USABLE_SYMBOLS_PER_SLOT ):
                logger.debug(f"A probable loop")
                logger.debug(f"Serving ind {self._buffer_being_served_ind}, needed sym {_needed_unserved_symbols}" +\
                         f" remaining {_remaining_available_symbols}")
                
                logger.debug(f"Needed symbols per buffer { self._needed_symbols_per_buffer}")
                logger.debug(f"Needed symbols per buffer { self._served_symbols_per_buffer}")
                break

        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (self._harq_buffer_being_served_ind < len(self._harq_needed_symbols_per_buffer)):
            # first case is when the available symbols in slot is smaller than what needed by buffer
            # we assign all the symbols to that buffer
            _served_symbols = 0
            _needed_unserved_symbols = (self._harq_needed_symbols_per_buffer[self._harq_buffer_being_served_ind] - \
                                        self._harq_served_symbols_per_buffer[self._harq_buffer_being_served_ind])
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            _finished_serving_user = False
            if _needed_unserved_symbols>_remaining_available_symbols:
                _served_symbols = _remaining_available_symbols
                self._harq_served_symbols_per_buffer[self._harq_buffer_being_served_ind]+=_served_symbols
                _used_symbols_in_slot += _served_symbols
            else:
                # we assign the amount of resources needed
                _served_symbols = _needed_unserved_symbols
                self._harq_served_symbols_per_buffer[self._harq_buffer_being_served_ind] += _served_symbols
                # move to the next buffer until
                _finished_serving_user = True
                _used_symbols_in_slot += _served_symbols
            
            if _served_symbols > 0:
                # add data to the list
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                 source_ue_id= self._harq_buffer_status[self._harq_buffer_being_served_ind][UserPreoptimization.HARQ_SOURCE_ID],
                                                 dest_ue_id=self._harq_buffer_status[self._harq_buffer_being_served_ind][UserPreoptimization.HARQ_DEST_ID],
                                                 frame=frame, subframe=subframe, slot=slot, 
                                                 numerology=2, ndi=0,
                                                 sym_start = _used_symbols_in_slot, 
                                                 sym_length=_served_symbols,
                                                 subchannel_start=0, 
                                                 subchannel_length=self.number_subchannels,
                                                 nr_sl_harq_id=self._harq_buffer_status[self._harq_buffer_being_served_ind][UserPreoptimization.HARQ_ID_INDEX]
                                                 )
            if _finished_serving_user:
                self._harq_buffer_being_served_ind +=1    

        # logger.debug(f"Served symbols per buffer {self._served_symbols_per_buffer}")
        # logger.debug(f"Harq buffer served symbols {self._harq_served_symbols_per_buffer}")
        return source_user_scheduling


    # return the map of scheduling
    def optimize(self):
        # traces 
        _map = {_JSON_TIMESTAMP: str(datetime.datetime.now()),
                _JSON_PLMN:self.plmn
                }
        pickle_out = open('/home/traces/relay_links_reports.pickle', 'ab+')
        pickle.dump(_map, pickle_out)
        pickle_out.close()
        return []

    # def schedule_retx(self, sourceSched: List[SourceUserScheduling], num_rext:int, 
    #                   final_bitmap: List[int], frame:int, subframe:int, slot:int)->tuple[list[SourceUserScheduling], int, int, int]:
    #     _l_source_sched_retx: List[SourceUserScheduling] = []
    #     _num_retx_ind = -1
    #     _next_frame, _next_subframe, _next_slot = frame, subframe, slot
    #     logger = logging.getLogger('')
    #     while(_num_retx_ind<(num_rext-1)):
    #         _num_retx_ind+=1
    #         _next_frame, _next_subframe, _next_slot = sl_slot_validation.get_next_valid_slot(final_bitmap, frame, subframe, slot)
    #         _l_sourceSched_next = copy.deepcopy(sourceSched)
    #         for _source in _l_sourceSched_next:
    #             for _dest in _source.destination_scheduling:
    #                 _dest.nSelected = num_rext-1
    #                 _dest.tbTxCounter = _num_retx_ind
    #                 for _user in _dest.user_scheduling:
    #                     _ndi = 0
    #                     _user.change_reference_slot(_next_frame, _next_subframe, _next_slot, _ndi)
    #                     logger.debug(f"Scheduled retx data s {_source.ue_id}" + \
    #                      f" & dest {_dest.ue_id} ndi {_ndi} " +\
    #                     f" in slot ({_next_frame}, {_next_subframe}, {_next_slot}) " 
    #                     f" sym start {_user._slPsschSymStart} & sym length {_user._slPsschSymLength}")
    #         _l_source_sched_retx = _l_source_sched_retx+_l_sourceSched_next
    #     return _l_source_sched_retx, _next_frame, _next_subframe, _next_slot

if __name__ == '__main__':
    _all_rntis = [1, 2, 3, 4]
    rnti = 1
    peer_rnti = 2
    _potential_relay_nodes = [_rnti for _rnti in _all_rntis if _rnti not in [rnti, peer_rnti]]
    print(_potential_relay_nodes)
