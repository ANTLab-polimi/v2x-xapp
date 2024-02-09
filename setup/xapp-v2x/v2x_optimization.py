import numpy as np
from typing import List, Tuple
from operator import itemgetter
from v2x_pre_optimize import V2XPreoptimize
import pickle
import datetime

_JSON_RNTI = "Rnti"
_JSON_PEER_RNTI = "PeerRnti"
_JSON_SNR_RELAY_NODES_RNTI = 'SnrRelayNodesRnti'
_JSON_SNR_RELAY_NODES_GOODNESS = 'SnrRelayNodesGoodness'
_JSON_DISTANCE_RELAY_NODES_RNTI = 'DistanceRelayNodesRnti'
_JSON_DISTANCE_RELAY_NODES_GOODNESS = 'DistanceRelayNodesGoodness'
_JSON_GOODNESS = "RelayGoodness"
_JSON_DISTANCE = "RelayDistance"

_JSON_ACTIVE_LINK_RELAY_LIST = "RelayList"
_JSON_PLMN = "Plmn"
_JSON_TIMESTAMP = 'time'


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

# def get_max_cb_size() -> int:
#     return 768 # 6144/8

class ActiveLinkRelayList:
    def __init__(
            self,
            rnti: int,
            peer_rnti: int,
            relay_nodes_rnti_goodness: List[Tuple[int, float]] = [],  # relay rnti and path goodness
            relay_nodes_distance: List[Tuple[int, float]] = [] # relay rnti, x & y position
    ):
        self.rnti = rnti
        self.peer_rnti = peer_rnti
        self.relay_nodes_rnti_goodness = relay_nodes_rnti_goodness
        self.relay_nodes_distance = relay_nodes_distance

    # get snr of main link
    def get_original_link_goodness(self)->Tuple[int, float]:
        _filter_main_link = list(filter(lambda _single_link: (_single_link[0] == int(np.iinfo(np.uint16).max)) \
                                                    , self.relay_nodes_rnti_goodness))
        if len(_filter_main_link)>0:
            return _filter_main_link[0]
        return (int(np.iinfo(np.uint16).max), -1)

    def choose_best_relay_goodness(self, main_link_goodness_threshold:float = -1) -> Tuple[int, float]:
        # the choosing strategy is based upon the best value of goodness
        # return the tuple (rnti, goodness) with highest goodness
        # return max(self.relay_nodes_rnti_goodness, key=itemgetter(1))
        _main_link_goodness = self.get_original_link_goodness()
        # print("threshold " + str(main_link_goodness_threshold))
        # print(_main_link_goodness)
        if _main_link_goodness[1] == -1:
            return max(filter(lambda x: not np.isnan(x[1]), self.relay_nodes_rnti_goodness),
                    key=itemgetter(1))
        else:
            # means exist the main link goodness factor
            # check if main link goodness (snr) is above threshold
            if _main_link_goodness[1] > main_link_goodness_threshold:
                # return (int(np.iinfo(np.uint16).max))
                return _main_link_goodness
            else:
                # retunr the max among all possible relays
                # considering the main link as well
                try:
                    return max(filter(lambda x: not np.isnan(x[1]), self.relay_nodes_rnti_goodness),
                        key=itemgetter(1))
                except ValueError:
                    return _main_link_goodness

    def choose_best_relay_position(self):
        # the choosing strategy is based upon the shortest path
        # return min(self.relay_nodes_distance, key=itemgetter(1))
        return min(filter(lambda x: not np.isnan(x[1]), self.relay_nodes_distance),
                   key=itemgetter(1))

    def choose_best_relay_position_threshold(self, main_link_goodness_threshold:float = -1) -> Tuple[int, float]:
        # the choosing strategy is based upon the shortest path
        _main_link_goodness = self.get_original_link_goodness()
        # print("threshold pos " + str(main_link_goodness_threshold))
        # print(_main_link_goodness)
        # print(self.relay_nodes_distance)
        if _main_link_goodness[1] == -1:
            return min(filter(lambda x: not np.isnan(x[1]), self.relay_nodes_distance),
                    key=itemgetter(1))
        else:
            # means exist the main link goodness factor
            # check if main link goodness (snr) is above threshold
            if _main_link_goodness[1] > main_link_goodness_threshold:
                # return (int(np.iinfo(np.uint16).max))
                return _main_link_goodness
            else:
                # retunr the min distance among all possible relays
                # considering the main link as well
                return min(filter(lambda x: not np.isnan(x[1]), self.relay_nodes_distance),
                    key=itemgetter(1))

    def to_dict(self):
        _filter_goodness = list(filter(lambda _single_link: (not np.isnan(_single_link[1]) ) \
                                                    , self.relay_nodes_rnti_goodness))
        _filter_distance_goodness = list(filter(lambda _single_link: (not np.isinf(_single_link[1]) ) \
                                                    , self.relay_nodes_distance))
        return {
            _JSON_RNTI: self.rnti,
            _JSON_PEER_RNTI: self.peer_rnti,
            _JSON_GOODNESS: [[_tuple[0], _tuple[1]] for _tuple in _filter_goodness],
            _JSON_DISTANCE: [[_tuple[0], _tuple[1]] for _tuple in _filter_distance_goodness]
        }

class V2XFormulation:
    def __init__(
            self,
            preoptimize,
            plmn: str = "110"
    ):
        self.preoptimize: V2XPreoptimize = preoptimize
        self.plmn = plmn
        self.available_symbols_per_sl=14
        self.subchannel_size = 50
        self.control_channel_rbs = 10
        self.useful_subcarriers_sl = 11 # 12 total - 1 for the reference signal
        self.mcs = 14 # preconfigured
        # the only configurable parameter is the number of subchannels assigned to an user

    
    def optimize(self):
        _relay_paths_chosen: List[List[int, int, int]] = []
        _active_links_with_relays: List[ActiveLinkRelayList] = []
        # traces 
        _map = {_JSON_TIMESTAMP: str(datetime.datetime.now()),
                _JSON_PLMN:self.plmn,
                _JSON_ACTIVE_LINK_RELAY_LIST: [_link_relay_list.to_dict() for _link_relay_list in _active_links_with_relays]}
        pickle_out = open('/home/traces/relay_links_reports.pickle', 'ab+')
        pickle.dump(_map, pickle_out)
        pickle_out.close()
        return _relay_paths_chosen

if __name__ == '__main__':
    _all_rntis = [1, 2, 3, 4]
    rnti = 1
    peer_rnti = 2
    _potential_relay_nodes = [_rnti for _rnti in _all_rntis if _rnti not in [rnti, peer_rnti]]
    print(_potential_relay_nodes)
