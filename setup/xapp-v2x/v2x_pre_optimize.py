from transform_xml_to_dict_v2x import MillicarUeSingleReport
from typing import List, Tuple
import numpy as np
from more_itertools import locate

# in this file the preoptimization procedure shall be defined
# The steps: 
# 1. The single ue reports shall be grouped in a single class, which
# will hold all the received measurments of the peer v2x devices
# 2. A master class (V2XPreoptimize) which shall hold the overall logic
# and the information for whole ues; it will be called by the optimization class
# to provide the necessary information

class UserPreoptimization:
    def __init__(self, ue_id: int = -1, head_of_line_packet_delay: List[Tuple[int, float]]=[], 
                 position_x: float = None, position_y: float = None,
                 needed_resources: int = -1, 
                 goodnes_table_of_resources:np.ndarray=None) -> None:
        self.ue_id:int=ue_id
        self.head_of_line_packet_delay:List[Tuple[int, float, float]]=head_of_line_packet_delay 
        # the head of line delay of all packets (packet id & head of line delay, max delay for the packet)
        self.position_x:float=position_x
        self.position_y:float=position_y
        self.needed_resources:int = needed_resources # the number of resources needed by this user in rbs or throughput
        self.goodnes_table_of_resources = goodnes_table_of_resources # a goognes factor determinin the goodness of resources from
        # the perspective of an user
    
    def set_goodness_table(self, goodness_table: np.ndarray):
        self.goodnes_table_of_resources = goodness_table

    def _get_packet_ids_in_head_of_line(self)->List[int]:
        return [_tuple[0] for _tuple in self.head_of_line_packet_delay]


    def update_user_preopt_data(self, data: MillicarUeSingleReport):
        # updating the user preoptimization data
        # check if there are new head of line packet delay
        self.position_x = data.position_x
        self.position_y = data.position_y
        # add the packet head of line packet dely
        # _head_of_line_packet_ids = self._get_packet_ids_in_head_of_line()

    
class V2XPreoptimize:
    def __init__(self) -> None:
        self._single_user_preopt_list:List[UserPreoptimization]=[]

    def can_perform_optimization(self) -> bool:
        # we only perform optimization when we have full buffer
        return self._measurements_queue.full()

    def _update_preoptimization_data(self, ue_id: int=-1, single_report:MillicarUeSingleReport = None):
        _ue_preopt_item = self._get_user_preopt(ue_id)
        if _ue_preopt_item is None:
            # user does not exist, thus we need to insert it
            _new_ue_preopt_item = UserPreoptimization()
            self._single_user_preopt_list.append(_new_ue_preopt_item)
            self._single_user_preopt_list[-1].update_user_preopt_data(single_report)
        else:
            _ue_preopt_item.update_user_preopt_data(single_report)

    def update_reports(self, reports: List[MillicarUeSingleReport]):
        # iterate over the reports an update the data
        for _report in reports:
            _ue_id =_report.ue_id
            # update the user report
            self._update_preoptimization_data(_ue_id, _report)

    # get single user Preopt class instance
    def _get_user_preopt(self, ue_id: int=-1) -> UserPreoptimization:
        _ue_id_list = list(filter(lambda _user_preopt: _user_preopt.ue_id == ue_id), self._single_user_preopt_list)
        if len(_ue_id_list)==0:
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
        
    # def add_user_preopt(self, _user_preopt: UserPreoptimization):
    #     # check if user exist in the list
    #     _user_preopt_list = list(filter(lambda _user_preopt_single: _user_preopt_single.ue_id == _user_preopt.ue_id, self._single_user_preopt_list))
    #     if len(_user_preopt_list)>0:
    #         # if user exists, then just update it's values
    #         _user_preopt_list[0] = _user_preopt
    #     else:
    #         self._single_user_preopt_list.append(_user_preopt)
    # def set_goodness_factor_table_for_user(self, ue_id:int, goodnes_table_of_resources: np.ndarray):
    #     _ue_preopt_item = self._get_user_preopt(ue_id)
    #     if _ue_preopt_item is None:
    #         return 0
    #     else:
    #         _ue_preopt_item.set_goodness_table(goodnes_table_of_resources)
    #         return 1
    # get head of line delays for user with ue id
    # def get_user_head_of_line_delays(self, ue_id:int):
    #     _ue_id_item = self._get_user_preopt(ue_id)
    #     if _ue_id_item is None:
    #         return []
    #     else:
    #         return _ue_id_item.head_of_line_packet_delay
        


if __name__ == '__main__':
    pass


