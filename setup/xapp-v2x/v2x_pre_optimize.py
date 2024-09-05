from transform_xml_to_dict_v2x import MillicarUeSingleReport
from typing import List, Tuple
import numpy as np
import logging
from more_itertools import locate

# in this file the preoptimization procedure shall be defined
# The steps: 
# 1. The single ue reports shall be grouped in a single class, which
# will hold all the received measurments of the peer v2x devices
# 2. A master class (V2XPreoptimize) which shall hold the overall logic
# and the information for whole ues; it will be called by the optimization class
# to provide the necessary information

class UserPreoptimization:
    BUFFER_SOURCE_ID = 0
    BUFFER_DEST_ID = 1
    BUFFER_LOWER_LIMIT = 2
    BUFFER_RESERVATION_PERIOD = 3
    BUFFER_NUM_PACKETS = 4
    BUFFER_SIZE_INDEX = 5
    BUFFER_UPPER_LIMIT = 6
    HARQ_SOURCE_ID = 0
    HARQ_DEST_ID = 1
    HARQ_ID_INDEX = 2
    HARQ_BUFFER_SIZE_INDEX = 3
    HARQ_NUM_PACKETS_INDEX = 4
    
    
    def __init__(self, ue_id: int = -1, 
                 head_of_line_packet_delay: List[Tuple[int, int, float, float, int, int]]=[], 
                 retx_buffer_size: List[Tuple[int, int, int, int, int]] = [],
                 position_x: float = None, position_y: float = None,
                 needed_resources: int = -1, 
                 goodnes_table_of_resources:np.ndarray=None) -> None:
        self.ue_id:int=ue_id
        # head of line packet: source id, dest id, lower Interval (serve as id in the group of interval),
        # reservation period, number of packets, buffer size
        self.head_of_line_packet_delay:List[Tuple[int, int, float, float, int, int]]=head_of_line_packet_delay 
        # the retx buffer size report: source id, dest id, harq iq, buffer size, num packets
        self.retx_buffer_size: List[Tuple[int, int, int, int, int]] = retx_buffer_size
        # the head of line delay of all packets (packet interval id & head of line delay, max delay for the packet)
        self.position_x:float=position_x
        self.position_y:float=position_y
        self.needed_resources:int = needed_resources # the number of resources needed by this user in rbs or throughput
        self.goodnes_table_of_resources = goodnes_table_of_resources # a goognes factor determinin the goodness of resources from
        # the perspective of an user
    
    def set_goodness_table(self, goodness_table: np.ndarray):
        self.goodnes_table_of_resources = goodness_table

    def update_user_preopt_data(self, data: MillicarUeSingleReport):
        logger = logging.getLogger("")
        # updating the user preoptimization data
        # check if there are new head of line packet delay
        self.position_x = data.position_x
        self.position_y = data.position_y
        # referring to a single user we see the packet delays for the destination of reference
        # source_ue_id = data.user_packet_delays.ue_id
        # whenever new report comes we update entirely the interval data
        self.head_of_line_packet_delay = []
        self.retx_buffer_size = []
        logger.debug(f"Delays {[str(delay) for delay in data.user_packet_delays.all_connections_delays]}")
        for _con in data.user_packet_delays.all_connections_delays:
            for _delay_intervals in _con.delayIntervals:
                _interval_group_id = _delay_intervals.lowerInterval
                _upper_limit = _delay_intervals.upperInterval
                self.head_of_line_packet_delay.append(
                    (self.ue_id, _con.ue_id, 
                     _interval_group_id, 
                     _delay_intervals.reservationPeriod, 
                     _delay_intervals.numberOfPackets,
                     _delay_intervals.bufferSize,
                     _upper_limit, #
                     )
                )
            # for each delay interval we add the harq buffer
            # for _harq_buff_size in _con.harqBufferSize:
            #     self.retx_buffer_size.append(
            #         self.ue_id, _con.ue_id,
            #         _harq_buff_size.harqId,
            #         _harq_buff_size.bufferSize,
            #         _harq_buff_size.numberOfPackets
            #     )

            # this is a blind retransmission
            # for each active flow we add a blind retransmission
                # self.retx_buffer_size.append(
                #     (
                #         self.ue_id, _con.ue_id,
                #         np.iinfo(np.uint8).max,
                #         _delay_intervals.bufferSize,
                #         _delay_intervals.numberOfPackets
                #     )
                # )

    def __str__(self) -> str:
        return f"{self.ue_id} " + str(self.head_of_line_packet_delay)

class V2XPreScheduling:
    def __init__(self) -> None:
        self._single_user_preopt_list:List[UserPreoptimization]=[]
        self._is_data_updated = False
        # self._element_inserted = 0

    def is_data_updated(self)->bool:
        return  self._is_data_updated

    def can_perform_optimization(self) -> bool:
        return True
        # we only perform optimization when we have full buffer
        # return self._measurements_queue.full()

    # update the ddata whenever new report has been received
    # set _is_data_updated as true
    def _update_preoptimization_data(self, ue_id: int=-1, single_report:MillicarUeSingleReport = None):
        _ue_preopt_item = self._get_user_preopt(ue_id)
        logger = logging.getLogger('')
        # logger.debug("_update_preoptimization_data")
        # logger.debug(single_report)
        if _ue_preopt_item is None:
            # self._element_inserted += 1
            # user does not exist, thus we need to insert it
            _new_ue_preopt_item = UserPreoptimization(ue_id=ue_id)
            _new_ue_preopt_item.update_user_preopt_data(single_report)
            self._single_user_preopt_list.append(_new_ue_preopt_item)
            # logger.info(f"Ue id {ue_id}; Inserting {_new_ue_preopt_item} into preopt")

            # if (self._element_inserted > 30):
            #     exit(1)

            # self._single_user_preopt_list[-1].update_user_preopt_data(single_report)
        else:
            _ue_preopt_item.update_user_preopt_data(single_report)

    def update_reports(self, reports: List[MillicarUeSingleReport]):
        # iterate over the reports an update the data
        logger = logging.getLogger("")
        self._is_data_updated = True
        logger.debug("Start updating reports")
        for _report in reports:
            # update the user report
            self._update_preoptimization_data(_report.ue_id, _report)
        logger.debug("Finished updating reports")

    # get 
    def get_all_users_buffer_status(self) -> List[Tuple[int, int, float, float, int, int]]:
        _all_users_buffer_data: List[Tuple[int, int, float, float, int, int]]= [] 
        for _preopt_list in self._single_user_preopt_list:
            _all_users_buffer_data.extend(_preopt_list.head_of_line_packet_delay)
        self._is_data_updated = False
        return _all_users_buffer_data
    
    def get_all_users_harq_buffer_status(self):
        _all_users_harq_buffer_data: List[Tuple[int, int, int, int, int]] = []
        for _preopt_list in self._single_user_preopt_list:
            _all_users_harq_buffer_data.extend(_preopt_list.retx_buffer_size)
        self._is_data_updated = False
        return _all_users_harq_buffer_data
            

    # get single user Preopt class instance
    def _get_user_preopt(self, ue_id: int=-1) -> UserPreoptimization:
        logger = logging.getLogger('')
        _ue_id_list = list(filter(lambda _user_preopt: _user_preopt.ue_id == ue_id, self._single_user_preopt_list))
        if len(_ue_id_list)==0:
            logger.debug(f"Considering {ue_id}; List of user preopt: {[str(_sing_user) for _sing_user in self._single_user_preopt_list]}")
            return None
        else:
            return _ue_id_list[0]
        
    def get_all_ue_ids(self)->set:
        _ue_id_list = set()
        for _single_ue_preopt in self._single_user_preopt_list:
            _ue_id = _single_ue_preopt.ue_id
            if _ue_id !=-1:
                _ue_id_list.update([_ue_id])
        return _ue_id_list
    
    def peer_positions(self) -> np.array:
        # get position by the last report
        _all_ue_ids = list(sorted(self.get_all_ue_ids()))
        _nr_reports = len(_all_ue_ids)
        _nr_ue_ids = len(_all_ue_ids)
        distance_matrix = np.full((_nr_ue_ids, _nr_ue_ids), dtype=float, fill_value=np.inf)
        
        for _first_index in range(_nr_reports):
            _first_position_x = self._single_user_preopt_list[_first_index].position_x
            _first_position_y = self._single_user_preopt_list[_first_index].position_y
            _first_position_ue_id = self._single_user_preopt_list[_first_index].ue_id
            _first_position_ue_id_index = _all_ue_ids.index(_first_position_ue_id)
            for _second_index in range(_first_index+1, _nr_reports):
                _second_position_x = self._single_user_preopt_list[_second_index].position_x
                _second_position_y = self._single_user_preopt_list[_second_index].position_y
                _second_position_ue_id = self._single_user_preopt_list[_second_index].ue_id
                _second_position_ue_id_index = _all_ue_ids.index(_second_position_ue_id)
                _distance = abs(_second_position_x - _first_position_x) + \
                            abs(_second_position_y - _first_position_y)
                distance_matrix[_first_position_ue_id_index][_second_position_ue_id_index] = _distance
                distance_matrix[_second_position_ue_id_index][_first_position_ue_id_index] = _distance

        return distance_matrix, _all_ue_ids
        

if __name__ == '__main__':
    pass


