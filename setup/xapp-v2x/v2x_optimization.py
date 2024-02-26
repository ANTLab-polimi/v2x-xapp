import numpy as np
from typing import List, Tuple
from operator import itemgetter
from v2x_pre_optimize import V2XPreScheduling, UserPreoptimization
from transform_xml_to_dict_v2x import _JSON_PLMN
from v2x_ric_message_format import SourceUserScheduling, UserScheduling, SingleScheduling, SlRlcPduInfo
import pickle
import datetime

_JSON_TIMESTAMP = 'time'
_USABLE_SYMBOLS_PER_SLOT = 8
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
def get_payload_size(mcs: int, rbNum:int, usefulSC:int = 11):
    rscElement = usefulSC * rbNum
    Rcode = McsEcrTable[mcs]
    Qm = ModulationSchemeForMcs[mcs]
    spectralEfficiency = rscElement * Qm * Rcode
    return spectralEfficiency / 8



# the sci format 2A has an overhead 5 bytes along the data part size
def calculate_tb_size(mcs:int, subchannelSize: int, assignedSubchannels:int, availableSymbols:int):
    return get_payload_size(mcs=mcs, rbNum=subchannelSize*assignedSubchannels*availableSymbols)

def calculate_needed_nr_rbs_per_tb_size(mcs:int, tb_size:int, usefulSC:int = 11):
    # subchannel size is preconfigured, the assigned subchannels and available symbols might change
    Rcode = McsEcrTable[mcs]
    Qm = ModulationSchemeForMcs[mcs]
    min_nr_rbs_needed = np.ceil(tb_size*8/(Qm * Rcode*usefulSC))
    return min_nr_rbs_needed

def calculate_needed_symbols_per_rbs(num_rbs, subchannel_size: int = 50, num_subchannels: int = 50):
    return np.ceil(num_rbs/(num_subchannels*subchannel_size))


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
            plmn: str = "110"
    ):
        self.preoptimize: V2XPreScheduling = preoptimize
        self.plmn = plmn
        self.available_symbols_per_sl=14
        self.subchannel_size = 50 # accounted in number of rbs per subchannel
        self.control_channel_rbs = 10
        self.useful_subcarriers_sl = 11 # 12 total - 1 for the reference signal
        self.mcs = 14 # preconfigured
        # the only configurable parameter is the number of subchannels assigned to an user
        # this will hold all the buffer status as indicated in pre optimize
        self._all_buffer_status: List[Tuple[int, int, float, float, int, int]] = []
        # a boolean list to hold information of whethe the buffer has been served or not
        self._buffer_served: List[bool] = []
        # the list of needed rbs per buffer
        self._needed_rbs_per_buffer: List[int] = []
        self._needed_symbols_per_buffer: List[int] = []
        self._served_symbols_per_buffer: List[int] = []
        self._buffer_being_served_ind = 0
        # the harq part
        self._harq_buffer_status: List[Tuple[int, int, int, int, int]] = []
        self._harq_buffer_served: List[bool] = []
        self._harq_needed_rbs_per_buffer: List[int] = []
        self._harq_needed_symbols_per_buffer: List[int] = []
        self._harq_buffer_being_served = 0

    # the function will get all the tuple of all the connections
    # and will sort them based on the sorting order given by the formula in point 1.
    def _update_resource_request_by_priority(self):
        if self.preoptimize.is_data_updated():
            self._all_buffer_status = self.preoptimize.get_all_users_buffer_status()
            # _tuple[3] is reservation period and _tuple[2] is head of line
            self._all_buffer_status.sort(key=lambda _tuple: _tuple[3] -  _tuple[2]) 
            self._buffer_served = [False]*len(self._all_buffer_status)
            self._needed_rbs_per_buffer = [calculate_needed_nr_rbs_per_tb_size(_buffer_status_tuple[UserPreoptimization.BUFFER_SIZE_INDEX]) for _buffer_status_tuple in self._all_buffer_status]
            self._needed_symbols_per_buffer = [calculate_needed_symbols_per_rbs(num_rbs) for num_rbs in self._needed_rbs_per_buffer]
            self._served_symbols_per_buffer = [0]*len(self._needed_symbols_per_buffer)
            self._buffer_being_served_ind = 0
            # harq buffer
            self._harq_buffer_status = self.preoptimize.get_all_users_harq_buffer_status()
            self._harq_buffer_served = [False]*len(self._harq_buffer_status)
            self._harq_needed_rbs_per_buffer = [calculate_needed_nr_rbs_per_tb_size(_buffer_status_tuple[UserPreoptimization.HARQ_BUFFER_SIZE_INDEX]) for _buffer_status_tuple in self._harq_buffer_status]
            self._harq_needed_symbols_per_buffer = [calculate_needed_symbols_per_rbs(num_rbs) for num_rbs in self._harq_needed_rbs_per_buffer]
            self._harq_served_symbols_per_buffer = [0]*len(self._harq_needed_symbols_per_buffer)
            self._harq_buffer_being_served_ind = 0

    def _add_source_scheduling_list(self, source_user_scheduling: List[SourceUserScheduling],
                                   source_ue_id: int, dest_ue_id: int,
                                   frame: int, subframe: int, slot: int,
                                   numerology: int, ndi: int,
                                   sym_start: int, sym_length: int,
                                   subchannel_start: int, subchannel_length: int ,
                                   nr_sl_harq_id: int= -1
                                   ):
        _single_sched = SingleScheduling(m_frameNum=frame, 
                                m_subframeNum=subframe,
                                m_slotNum=slot, 
                                m_numerology = numerology, 
                                dstL2Id = self._all_buffer_status[self._buffer_being_served_ind][1],
                                ndi=ndi,
                                priority=0,
                                slPsschSymStart = sym_start,
                                slPsschSymLength = sym_length,
                                slPsschSubChStart = subchannel_start,
                                slPsschSubChLength = subchannel_length,
                                )
        
        _filter_source_user = list(filter(lambda source_sched: source_sched.ue_id == source_ue_id, source_user_scheduling))
        if len(_filter_source_user) == 0:
            # we create the User scheduling with all counters to 1
            _dest_sched = UserScheduling(ue_id=dest_ue_id, cReselCounter=1, 
                                         slResoReselCounter=1, 
                                         prevSlResoReselCounter=1,
                                         nrSlHarqId=nr_sl_harq_id,
                                         nSelected=1, 
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

    # the scheduled scheme is a simple TDMA, where we assign a symbol over the entire bandwidth
    def schedule_slot(self, frame: int, subframe: int, slot: int)->List[SourceUserScheduling]:
        # first update the buffer status if new data has arrived
        self._update_resource_request_by_priority()
        _used_symbols_in_slot = 0
        # we exit the while loop when we have used whole of the symbols in the slot
        # or we have serverd all of the buffer
        source_user_scheduling: List[SourceUserScheduling] = []

        # we serve first all the harq buffer
        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (self._harq_buffer_being_served_ind < len(self._harq_needed_symbols_per_buffer)):
            # first case is when the available symbols in slot is smaller than what needed by buffer
            # we assign all the symbols to that buffer
            _served_symbols = 0
            _needed_unserved_symbols = (self._harq_needed_symbols_per_buffer[self._harq_buffer_being_served_ind] - \
                                        self._harq_served_symbols_per_buffer[self._harq_buffer_being_served_ind])
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            if _needed_unserved_symbols>_remaining_available_symbols:
                _served_symbols = _remaining_available_symbols
                self._harq_served_symbols_per_buffer[self._harq_buffer_being_served_ind]+=_served_symbols
                _used_symbols_in_slot += _served_symbols
            else:
                # we assign the amount of resources needed
                _served_symbols = _needed_unserved_symbols
                self._harq_served_symbols_per_buffer[self._harq_buffer_being_served_ind] += _served_symbols
                # move to the next buffer until
                self._harq_buffer_being_served_ind +=1
                _used_symbols_in_slot += _served_symbols
            
            if _served_symbols > 0:
                # add data to the list
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                 source_ue_id= self._harq_buffer_status[self._harq_buffer_being_served_ind][0],
                                                 dest_ue_id=self._harq_buffer_status[self._harq_buffer_being_served_ind][1],
                                                 frame=frame, subframe=subframe, slot=slot, 
                                                 numerology=2, ndi=0,
                                                 sym_start = _used_symbols_in_slot, 
                                                 sym_length=_served_symbols,
                                                 subchannel_start=0, 
                                                 subchannel_length=self.subchannel_size,
                                                 nr_sl_harq_id=self._harq_buffer_status[self._harq_buffer_being_served_ind][UserPreoptimization.HARQ_ID_INDEX]
                                                 )

        while (_used_symbols_in_slot < _USABLE_SYMBOLS_PER_SLOT) & \
               (self._buffer_being_served_ind < len(self._served_symbols_per_buffer)):
            # first case is when the available symbols in slot is smaller than what needed by buffer
            # we assign all the symbols to that buffer
            _served_symbols = 0
            _needed_unserved_symbols = (self._needed_symbols_per_buffer[self._buffer_being_served_ind] - \
                                        self._served_symbols_per_buffer[self._buffer_being_served_ind])
            _remaining_available_symbols = (_USABLE_SYMBOLS_PER_SLOT - _used_symbols_in_slot)
            if  _needed_unserved_symbols > _remaining_available_symbols:
                _served_symbols = _remaining_available_symbols
                
                self._served_symbols_per_buffer[self._buffer_being_served_ind]+=_served_symbols
                _used_symbols_in_slot += _served_symbols
            else:
                # we assign the amount of resources needed
                _served_symbols = _needed_unserved_symbols
                self._served_symbols_per_buffer[self._buffer_being_served_ind] += _served_symbols
                # move to the next buffer until
                self._buffer_being_served_ind +=1
                _used_symbols_in_slot += _served_symbols
            if _served_symbols > 0:
                # add data to the list
                self._add_source_scheduling_list(source_user_scheduling = source_user_scheduling, 
                                                source_ue_id= self._all_buffer_status[self._buffer_being_served_ind][0],
                                                dest_ue_id=self._all_buffer_status[self._buffer_being_served_ind][1],
                                                frame=frame, subframe=subframe, slot=slot, 
                                                numerology=2, ndi=1,
                                                sym_start = _used_symbols_in_slot, 
                                                sym_length=_served_symbols,
                                                subchannel_start=0, 
                                                subchannel_length=self.subchannel_size
                                                )
                

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

if __name__ == '__main__':
    _all_rntis = [1, 2, 3, 4]
    rnti = 1
    peer_rnti = 2
    _potential_relay_nodes = [_rnti for _rnti in _all_rntis if _rnti not in [rnti, peer_rnti]]
    print(_potential_relay_nodes)
