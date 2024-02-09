import logging
from typing import List
from xapp_control import *
# from xapp_control_local_test import *
# import functools 
import os
import numpy as np
import transform_xml_to_dict_v2x as transform
from ctrl_msg_encoder_decoder import RicControlMessageEncoder
# from millicar_pre_optimize import MillicarPreoptimize
from v2x_pre_optimize import V2XPreoptimize
from v2x_optimization import V2XFormulation
import itertools
import platform
import pickle
import datetime

_simulation_map = [
    [111, 0, 'no_relay', 16] ,
    [112, -10, 'distance', 16] ,
    [113, -10, 'sinr', 16] ,
    [114, -10, 'decentralized', 16] ,
    [115, -5, 'distance', 16] ,
    [116, -5, 'sinr', 16] ,
    [117, -5, 'decentralized', 16] ,
    [118, 0, 'distance', 16] ,
    [119, 0, 'sinr', 16] ,
    [120, 0, 'decentralized', 16] ,
    [121, 5, 'distance', 16] ,
    [122, 5, 'sinr', 16] ,
    [123, 5, 'decentralized', 16] ,
    [124, 10, 'distance', 16] ,
    [125, 10, 'sinr', 16] ,
    [126, 10, 'decentralized', 16] ,
    [127, 0, 'no_relay', 24] ,
    [128, -10, 'distance', 24] ,
    [129, -10, 'sinr', 24] ,
    [130, -10, 'decentralized', 24] ,
    [131, -5, 'distance', 24] ,
    [132, -5, 'sinr', 24] ,
    [133, -5, 'decentralized', 24] ,
    [134, 0, 'distance', 24] ,
    [135, 0, 'sinr', 24] ,
    [136, 0, 'decentralized', 24] ,
    [137, 5, 'distance', 24] ,
    [138, 5, 'sinr', 24] ,
    [139, 5, 'decentralized', 24] ,
    [140, 10, 'distance', 24] ,
    [141, 10, 'sinr', 24] ,
    [142, 10, 'decentralized', 24] ,
    [143, 0, 'no_relay', 48] ,
    [144, -10, 'distance', 48] ,
    [145, -10, 'sinr', 48] ,
    [146, -10, 'decentralized', 48] ,
    [147, -5, 'distance', 48] ,
    [148, -5, 'sinr', 48] ,
    [149, -5, 'decentralized', 48] ,
    [150, 0, 'distance', 48] ,
    [151, 0, 'sinr', 48] ,
    [152, 0, 'decentralized', 48] ,
    [153, 5, 'distance', 48] ,
    [154, 5, 'sinr', 48] ,
    [155, 5, 'decentralized', 48] ,
    [156, 10, 'distance', 48] ,
    [157, 10, 'sinr', 48] ,
    [158, 10, 'decentralized', 48] ,
    [159, 0, 'no_relay', 64] ,
    [160, -10, 'distance', 64] ,
    [161, -10, 'sinr', 64] ,
    [162, -10, 'decentralized', 64] ,
    [163, -5, 'distance', 64] ,
    [164, -5, 'sinr', 64] ,
    [165, -5, 'decentralized', 64] ,
    [166, 0, 'distance', 64] ,
    [167, 0, 'sinr', 64] ,
    [168, 0, 'decentralized', 64] ,
    [169, 5, 'distance', 64] ,
    [170, 5, 'sinr', 64] ,
    [171, 5, 'decentralized', 64] ,
    [172, 10, 'distance', 64] ,
    [173, 10, 'sinr', 64] ,
    [174, 10, 'decentralized', 64] 
]

_JSON_REPORTS_SEND = "Reports"
_JSON_PLMN = "Plmn"

class XmlToDictManager:
    def __init__(self,
                 decoder:RicControlMessageEncoder,
                 plmn: str = "111",
                 ) -> None:
        self.plmn = plmn
        self.transform = transform.XmlToDictDataTransform(decoder, plmn)
        # number of samples to take to for mean
        _sim_map_filter = list(filter(lambda _sim: str(_sim[0]) == str(plmn), _simulation_map))
        _relay_threshold = 46
        if len(_sim_map_filter) == 1:
            _relay_threshold += 2*_sim_map_filter[0][1]
        # self.preoptimize_queue = MillicarPreoptimize(peer_measurements_history_depth=5,
        #                                              to_relay_threshold=_relay_threshold)
        
        self.preoptimize = V2XPreoptimize()
    

def send_optimized_data(socket, encoder_class:RicControlMessageEncoder):
    def send_data(ue_ids, initial_assignment, optimized_assignment, plmn):
        data_length, data_bytes = encoder_class.encode_result_plmn(ue_ids, initial_assignment, optimized_assignment, plmn)
        # we could make a check here that data length is identical to received data length from c++ function
        logging.info('Sending back the data with size ..' + str(data_length))
        send_socket(socket, data_bytes)
    return send_data

def _optimize_and_send_data(transform: XmlToDictManager, sendingDataCallback):
    plmn = transform.plmn
    ##### Optimization part
    _sim_map_filter = list(filter(lambda _sim: str(_sim[0]) == plmn, _simulation_map))
    if len(_sim_map_filter) == 1:
        _formulation = V2XFormulation(transform.preoptimize, plmn)

    # removing duplicates in the list
    _all_relays = list(k for k,_ in itertools.groupby(_all_relays))
    pickle_out = open('/home/traces/sent_relays_reports.pickle', 'ab+')
    pickle.dump({_JSON_PLMN: plmn,
                _JSON_REPORTS_SEND: _all_relays}, pickle_out)
    pickle_out.close()

    # transform data 
    # _source_rntis = [_relay[0] for _relay in _all_relays]
    # _dest_rntis = [_relay[1] for _relay in _all_relays]
    # _relay_rntis = [_relay[2] for _relay in _all_relays]
    # sendingDataCallback(_source_rntis, _dest_rntis, _relay_rntis, plmn)
    transform.transform.reset()

def main():
    _report_filename = "/home/ef-xapp/report.csv"
    # configure logger and console output
    logging_filename = os.path.join(os.getcwd(), 'report.log')
    # logging_filename = '/home/ef-xapp/xapp-logger.log' # os.path.join(os.getcwd(), )
    logging.basicConfig(level=logging.DEBUG, filename=logging_filename, filemode='a',
                        format='%(asctime)-15s %(levelname)-8s %(message)s')
    logger = logging.getLogger('')
    # logger.handlers.clear()
    # to avoid propagating logger to root
    logger.propagate = False
    formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # Create the pickle file for data reports
    for _plmn in range(110, 180):
        pickle_out = open('/home/traces/ue_reports_' +str(_plmn)+ '.pickle', 'wb')
        pickle_out.close()

    pickle_out = open('/home/traces/relay_links_reports.pickle', 'wb')
    pickle_out.close()
    pickle_out = open('/home/traces/sent_relays_reports.pickle', 'wb')
    pickle_out.close()

    control_sck = open_control_socket(4200)

    _transform_list: List[XmlToDictManager] = []

    _msg_encoder = RicControlMessageEncoder()

    _send_encoded_data_func = send_optimized_data(control_sck, _msg_encoder)


    while True:
        data_sck = receive_from_socket(control_sck, _msg_encoder)

        if len(data_sck) <= 0:
            if len(data_sck) == 0:
                continue
            else:
                logging.info('Negative value for socket')
                break
        else:
            logging.info('Received data')
            
            # appending the data to the tranformer
            if isinstance(data_sck, list):
                for _msg in data_sck:
                    print("Received data")
                    print(_msg)
                    # logging.info('Received data: ' + _msg)
                    _collection_time, _cell_id, _plmn_id = transform.XmlToDictDataTransform.peek_header(_msg)
                    # print("Plmn id of the sender " + str(_plmn_id))
                    if (_plmn_id!= -1) & (_cell_id!= -1)& (_collection_time!= -1):
                        # find the right manager to parse data 
                        _xml_manager_filter: List[XmlToDictManager] = list(filter(lambda _xmlManager: _xmlManager.plmn == _plmn_id, _transform_list))
                        # either there exist a manager, so the filter gives only 1 element
                        if len(_xml_manager_filter) == 1:
                            _xml_manager_filter[0].transform.parse_incoming_data(_msg)
                        else:
                            # we insert a new manager 
                            _transform = XmlToDictManager(_msg_encoder, _plmn_id)
                            _transform.transform.parse_incoming_data(_msg)
                            _transform_list.append(_transform)
                            
            else:
                # logging.info('Received data: ' + data_sck)
                _collection_time, _cell_id, _plmn_id = transform.XmlToDictDataTransform.peek_header(data_sck)
                if (_plmn_id!= -1) & (_cell_id!= -1)& (_collection_time!= -1):
                    # find the right manager to parse data 
                    _xml_manager_filter = list(filter(lambda _xmlManager: _xmlManager.plmn == _plmn_id,_transform_list))
                    # either there exist a manager, so the filter gives only 1 element
                    if len(_xml_manager_filter) == 1:
                        _xml_manager_filter[0].transform.parse_incoming_data(data_sck)
                    else:
                        # we insert a new manager 
                        _transform = XmlToDictManager(_msg_encoder, _plmn_id)
                        _transform.transform.parse_incoming_data(data_sck)
                        _transform_list.append(_transform)

                    # _transform.parse_incoming_data(data_sck)
            # have to decide what to do next; when to start optimizing
            # one option might be to wait for a certain time and eventually start doing the optimization
            # optimize after 10 ms and send the result
            # having a single report we can optimize directly as there is only one set of data
            # for _transform in _transform_list:
            #     if _transform.transform.has_received_all_reports():
            #         # insert in queue
            #         # update data from the preoptimization 
            #         _transform.preoptimize.update_reports(_transform.transform.all_users_reports)
            #         if _transform.preoptimize.can_perform_optimization():
            #             _optimize_and_send_data(_transform, _send_encoded_data_func)
            #         _transform.transform.reset()


if __name__ == '__main__':
    main()
    # data_length, data_bytes = _msg_encoder.encode_result_plmn(ue_ids, initial_assignment, optimized_assignment, plmn)