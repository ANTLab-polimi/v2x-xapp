import logging
from typing import List
from xapp_control import *
# from xapp_control_local_test import *
# import functools 
import os
import numpy as np
import transform_xml_to_dict_v2x as transform
from ctrl_msg_encoder_decoder import RicControlMessageEncoder, generate_sched_data
# from millicar_pre_optimize import MillicarPreoptimize
from v2x_pre_optimize import V2XPreScheduling
from v2x_optimization import V2XFormulation
from v2x_ric_message_format import SourceUserScheduling, UserScheduling, SingleScheduling, SlRlcPduInfo
import itertools
import pickle
import time

from multiprocessing import shared_memory as shm
from time import sleep
from threading import Thread
import multiprocessing as mp

_JSON_SOURCE_SCHEDULING = "SourceScheduling"
_NUMEROLOGY = 2

class XmlToDictManager:
    def __init__(self,
                 decoder:RicControlMessageEncoder,
                 plmn: str = "111",
                 ) -> None:
        self.plmn = plmn
        self.transform = transform.XmlToDictDataTransform(decoder, plmn)
        # number of samples to take to for mean
        # _sim_map_filter = list(filter(lambda _sim: str(_sim[0]) == str(plmn), _simulation_map))
        _relay_threshold = 46
        # if len(_sim_map_filter) == 1:
        #     _relay_threshold += 2*_sim_map_filter[0][1]
        # self.preoptimize_queue = MillicarPreoptimize(peer_measurements_history_depth=5,
        #                                              to_relay_threshold=_relay_threshold)
        
        self.preoptimize = V2XPreScheduling()


def send_optimized_data(socket, encoder_class:RicControlMessageEncoder):
    def send_data(v2x_scheduling_all_users: List[SourceUserScheduling], plmn:str):
        data_length, data_bytes = encoder_class.encode_scheduling_plmn(v2x_scheduling_all_users, plmn)
        # we could make a check here that data length is identical to received data length from c++ function
        logging.info('Sending back the data with size ..' + str(data_length))
        send_socket(socket, data_bytes)
    return send_data

def write_assignment_data_to_file(plmn:str, allImsi: np.ndarray, real_assignments: np.ndarray, 
                       optimized_assignment: np.ndarray, mcs_table: np.ndarray,
                       assignment_table: np.ndarray):
    with open("/home/traces/report_assign.txt", mode="a+") as file:
        _all_imsi_str = ",".join([str(_imsi) for _imsi in allImsi])
        _assign_str = ",".join([str(_imsi) for _imsi in real_assignments])
        _optimized_str = ",".join([str(_imsi) for _imsi in optimized_assignment])
        _mcs_table_str = np.array2string(mcs_table)
        _assignment_table = np.array2string(assignment_table)
        file.write(str(time.time()) + "|" + plmn + "|" + _all_imsi_str  + "|" +_assign_str + "|" +_optimized_str+ "|" + _mcs_table_str + "|" + _assignment_table +"\r\n")

def _schedule_data_and_save(data: dict, v2x_preopt_obj: V2XPreScheduling, v2x_scheduling_obj: V2XFormulation, 
                            frame: int = 0, subframe: int = 0, slot: int = 0)->List[SourceUserScheduling]:
    # print("Here we optimize the scenarion and return back the data")
    # _plmn = int(data[transform._JSON_PLMN])
    # set the current optimization branch to being optimized
    v2x_source_scheduling_users: List[SourceUserScheduling] = _schedule_data(data, v2x_preopt_obj, v2x_scheduling_obj, frame, subframe, slot)
    # store data to the list of optimized scenarios and to be sent back
    return v2x_source_scheduling_users #, _plmn

def _schedule_data(data: dict, v2x_preopt_obj: V2XPreScheduling, v2x_scheduling_obj: V2XFormulation, frame: int, subframe: int, slot: int)->List[SourceUserScheduling]:
    # _buffer_status = data['buffer_status']
    # _plmn = int(data[transform._JSON_PLMN])

    # optimization afterwards which shall return the list of scheduled data
    v2x_source_scheduling_users: List[SourceUserScheduling] = v2x_scheduling_obj.schedule_slot(frame, subframe, slot)
    # store data in file to compare with data in ns3
    

    return v2x_source_scheduling_users

def _check_ric_commands_to_be_sent(send_callback):
    try:
        _shared_list_ric_command = shm.ShareableList(name="ric_commands")
    except FileNotFoundError as err:
        print("Ric commands shared list not created")
        _shared_list_ric_command = []
    # print("Checking if there are ric commands")
    # here inside the string of each ric command might be multiple ric commands
    for _ric_command_ind ,_ric_command_dict_str in enumerate(_shared_list_ric_command):
        # check if there is data
        if len(_ric_command_dict_str) > 0:
            _data_dict = eval(_ric_command_dict_str)
            # get the data from the dict
            _plmn = _data_dict.get(transform._JSON_PLMN)

            # the data that should be sent to the send callback should be the list of source user scheduling
            v2x_scheduling_all_users: List[SourceUserScheduling] = []
            if send_callback is not None:
                send_callback(v2x_scheduling_all_users, str(_plmn))
            _shared_list_ric_command[_ric_command_ind] = ""

def create_or_reset_shareable_memory():
    try:
        # we see to search for it
        _shared_list_data = shm.ShareableList(name="data")
        for _ind, _ in enumerate(_shared_list_data):
            _shared_list_data[_ind] = ""
    except FileNotFoundError:
        _shared_list_data = shm.ShareableList([" "*int(1e6)]*50, name="data")
    try:
        # we see to search for it
        _shared_list_data_updated = shm.ShareableList(name="data_updated")
        for _ind, _ in enumerate(_shared_list_data_updated):
            _shared_list_data_updated[_ind] = False
    except FileNotFoundError:
        _shared_list_data_updated = shm.ShareableList([False]*50, name="data_updated")
    try:
        # we see to search for it
        _shared_list_ric_command = shm.ShareableList(name="ric_commands")
        for _ind, _ in enumerate(_shared_list_ric_command):
            _shared_list_ric_command[_ind] = ""
    except FileNotFoundError:
        # the ric commands can be long since it contains scheduling info
        _shared_list_ric_command = shm.ShareableList([" "*int(1e6)]*50, name="ric_commands")
    try:
        # we see to search for it
        _shared_list_being_optimized = shm.ShareableList(name="data_being_optimized")
        for _ind, _ in enumerate(_shared_list_being_optimized):
            _shared_list_being_optimized[_ind] = False
    except FileNotFoundError:
        _shared_list_being_optimized = shm.ShareableList([False]*50, name="data_being_optimized")

def add_sample_data_for_optimization():

    _shared_list_data = shm.ShareableList(name="data")
    _shared_list_ric_command = shm.ShareableList(name="ric_commands")
    _shared_list_data_updated = shm.ShareableList(name="data_updated")
    
    print("Adding data to buffer")
    with open('data_xml/reports_as_dict.txt') as file:
        _title = file.readline()
        for _ind in range(5):
            _data_str = str(file.readline())
            _data_dict = eval(eval(_data_str))
            _data_dict['time'] = time.time()
            _plmn_ind = int(_data_dict[transform._JSON_PLMN]) - 111
            print("Adding plmn data " + str(int(_data_dict[transform._JSON_PLMN])))
            _shared_list_data[_plmn_ind] = str(_data_dict)
            _shared_list_data_updated[_plmn_ind]=True
            _shared_list_ric_command[_plmn_ind]=""

def _check_optimization_to_be_executed()->List[dict]:
    _l_to_be_optimized = []
    # print("Check optimization")
    logger = logging.getLogger('')
    try:
        # we see to search for it
        _shared_list_data_updated = shm.ShareableList(name="data_updated")
        _shared_list_being_optimized = shm.ShareableList(name="data_being_optimized")
        _shared_list_data = shm.ShareableList(name="data")
        _v_plmn_print = any(_shared_list_data_updated)
        if _v_plmn_print:
            print("Plmn to be optimized ", end = "")
        for _ind, _elem in enumerate(_shared_list_data_updated):
            if _elem & (not _shared_list_being_optimized[_ind]):
                _data = eval(_shared_list_data[_ind])
                # logger.debug("Data in _check_optimization_to_be_executed")
                # logger.debug(_data)
                print(_data[transform._JSON_PLMN], end=" ")
                _l_to_be_optimized.append(_data)
                # set the data not updated , since we put it in the queue to optimize
                _shared_list_being_optimized[_ind] = True
                _shared_list_data_updated[_ind] = False
                _shared_list_data[_ind] = ""
    except FileNotFoundError:
        logging.info("Data updated array not created")
    if _v_plmn_print:
        print("")
    return _l_to_be_optimized

def _scheduling_main_func(queue:mp.Queue, v2x_scheduling_obj: V2XFormulation, 
                          v2x_preopt_obj: V2XPreScheduling, plmn: str = "111"):
    _shared_list_being_optimized = shm.ShareableList(name="data_being_optimized")
    # _shared_list_data_updated = shm.ShareableList(name="data_updated")
    _shared_list_ric_command = shm.ShareableList(name="ric_commands")
    # _shared_list_data = shm.ShareableList(name="data")
    # logger = logging.getLogger('demo')
    logger = logging.getLogger('')
    logger.info(f"Scheduling main func {plmn}")
    frame = 0
    subframe = 0
    _plmn = plmn
    _frame_schedule_until = frame + 10
    _subframe_schedule_until = subframe + 10
    slot = 0
    _data: dict = {}
    # if we get new data we update the ue reports in the preopt object
    # the updated data shall be used in the optmization object afterwards on the new slot 
    # otherwise we schedule the next coming slot until we reach the interval
    # the parameter _block_queue shall block proceding until new data is available in the buffer
    # this will be useful in two scenarios:
    # 1. at the beginning of the simulation when it will wait for data to start the implented logic
    # therefore it will stop executing the loop infinitely
    # 2. When the scheduling for a given interval has stopped, therefore there is no need to proceed
    # and run the loop, rather wait for new data coming in the queue

    _block_queue = True
    _is_scheduled_needed = False
    while True:
        # if not queue.empty():
        if _block_queue:
            _data = queue.get()
            _block_queue = False
            # logger.debug("Data type coming from queue")
            # logger.debug(_data)
            # here are the data coming from quueu
            # we update the v2x scheduling and sync to the new frame
            # if _data is not None:
            
            _plmn = _data[transform._JSON_PLMN]
            _plmn_ind = int(_plmn) - 111
            # _shared_list_being_optimized[_plmn_ind] = True
            frame = _data[transform._JSON_FRAME]
            subframe = _data[transform._JSON_SUBFRAME]
            # slot = _data[transform._JSON_SLOT]
            # we start scheduling from the next subframe with slot index 0
            subframe = (subframe+1)%10 # we shift to the next subframe index
            _added_frame = 1 if subframe == 0 else 0 # means it has moved to the next frame
            frame+=_added_frame # if subframe moved to the new frame (i.e. subframe == 0) we add 1 else we add 0
            _frame_schedule_until = frame + 10
            _subframe_schedule_until = subframe + 10
            # slot = 0 # we have already set slot = 0, this it is ok 
            # we get the reports send and update the data in the preoptimizer
            _buffer_status_reports = _data['buffer_status']
            # construct the object from the buffer 
            _xml_tranform = transform.XmlToDictDataTransform(None, _plmn, _buffer_status_reports)
            v2x_preopt_obj.update_reports(_xml_tranform.all_users_reports)
            _is_scheduled_needed = True
        else:
            # when there is new data we block the queue to get new data
            if not queue.empty():
                _block_queue = True
        if _is_scheduled_needed:
            # id data is available
            # here we schedule for the next slot until we reach the limit of 1 frame or 10 subframes
            
            print("Q size in get " + str((plmn, queue.qsize())))
            v2x_source_scheduling_all_users = _schedule_data_and_save(_data, 
                                                        v2x_preopt_obj, v2x_scheduling_obj,
                                                        frame, subframe, slot)
            logger.info("Data scheduled")
            # write data to the file
            for _source_sched in v2x_source_scheduling_all_users:
                _source_sched.write_data_to_file(plmn=_plmn)
            # insert data in the shareable list
            _optimized_dict = {
                transform._JSON_PLMN: _plmn,
                _JSON_SOURCE_SCHEDULING: [_single_source_sched.to_dict_c() for _single_source_sched in v2x_source_scheduling_all_users]
            }
            # inser the ric command to the list
            # here instead of mere adding it, we can append the new command 
            _shared_list_ric_command[_plmn_ind] += str(_optimized_dict)
            # remove the state of being optimized
            _shared_list_being_optimized[_plmn_ind] = False
            slot = (slot+1)%(pow(2,_NUMEROLOGY))
            # in case the slot goes again to 0, it means a new subframe has
            # started, thus we add by 1
            subframe = (subframe + (1 if slot==0 else 0))%10
            # the same logic we deploy for the frame 
            frame = frame + (1 if ((subframe == 0) & (slot==0)) else 0)

            # check if all the slot in the needed has been scheduled
            # if so we set _block_queue to true to wait for new data to save 
            # cpu usage
            if (_frame_schedule_until == frame) & (_subframe_schedule_until == subframe):
                _block_queue = True
                _is_scheduled_needed = False

def recreate_report_files():
    with open("/home/traces/ric_messages.txt", 'w') as f:
        _fields_name_str = SourceUserScheduling.get_field_names() + "\n"
        f.write(_fields_name_str)
    file = open("/home/traces/data_buffer.txt", mode="wb")
    file.close()

def handle_optimization_thread(is_test_mode: bool=False):
    # in total we define 50 queues for 50 simulation instances at max we can run in a server
    # the queues shall hold the data of _shared_list_data shareble list and new data coming
    # and inserted in the _all_queues shall trigger the _scheduling_main_func to trigger 
    # its execution
    # recreate the report files
    if (not is_test_mode):
        # in test mode we do not want to delete the received reports before
        recreate_report_files()

    _all_queues = [mp.Queue() for _ in range(2)]
    _all_preopt_objs = [V2XPreScheduling() for _ in range(len(_all_queues))]
    _all_sched_objs = [V2XFormulation(_all_preopt_objs[_ind], str(_ind + 111)) for _ind in range(len(_all_queues))]
    
    _all_processes = [mp.Process(target=_scheduling_main_func, 
                                 args=(_all_queues[_ind], 
                                       _all_sched_objs[_ind],
                                       _all_preopt_objs[_ind],
                                       str(_ind + 111),)) for _ind in range(len(_all_queues))]
    _nr_active_processes = len(_all_processes)
    for _process in _all_processes[:_nr_active_processes]:
        _process.start()

    while True:
        # check if data is updated and ready to optimize
        _l_to_be_optimized = _check_optimization_to_be_executed()
        _l_to_be_optimized_sorted: List[dict] = sorted(_l_to_be_optimized, key=lambda d: d['time']) 
        if len(_l_to_be_optimized_sorted)>0:
            # we put data to the queue
            # distribute among initialized processes by putting data in the queue
            print("Queue size per plmn ", end="")

            for _v_ind, _v_to_be_optimized in enumerate(_l_to_be_optimized_sorted):
                _plmn = _v_to_be_optimized[transform._JSON_PLMN]
                _plmn_ind = int(_plmn) - 111
                _queue = _all_queues[_plmn_ind%_nr_active_processes]
                dc = _v_to_be_optimized.copy()
                _queue.put(dc)
                print(str((_plmn, _queue.qsize())), end=" ")
            print()
        sleep(2)

def parse_xml_msg(msg: str, msg_encoder: RicControlMessageEncoder, _transform_list: List[XmlToDictManager]):
    # logging.info('Received data: ' + msg)
    _collection_time, _cell_id, _plmn_id = transform.XmlToDictDataTransform.peek_header(msg)
    # print("Plmn id of the sender " + str(_plmn_id))
    if (_plmn_id!= -1) & (_cell_id!= -1)& (_collection_time!= -1):
        # find the right manager to parse data 
        _xml_manager_filter: List[XmlToDictManager] = list(filter(lambda _xmlManager: _xmlManager.plmn == _plmn_id, _transform_list))
        # either there exist a manager, so the filter gives only 1 element
        if len(_xml_manager_filter) == 1:
            _transform: XmlToDictManager = _xml_manager_filter[0]
        else:
            # we insert a new manager 
            _transform = XmlToDictManager(msg_encoder, _plmn_id)
            _transform_list.append(_transform)
        _transform.transform.parse_incoming_data(msg)

def setup_logger():
    logging_filename = os.path.join(os.getcwd(), 'report.log')
    # logging_filename = '/home/ef-xapp/xapp-logger.log' # os.path.join(os.getcwd(), )
    logging.basicConfig(level=logging.DEBUG, filename=logging_filename, filemode='a',
                        format='%(asctime)-15s %(levelname)-8s %(message)s')
    
    logger = logging.getLogger('')
    # logger.handlers.clear()
    # to avoid propagating logger to root
    # logger.propagate = False
    formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    
def main():
    _report_filename = "/home/ef-xapp/report.csv"
    # configure logger and console output
    setup_logger()
    logger = logging.getLogger('')

    # Create the pickle file for data reports
    for _plmn in range(110, 180):
        pickle_out = open('/home/traces/ue_reports_' +str(_plmn)+ '.pickle', 'wb')
        pickle_out.close()

    # pickle_out = open('/home/traces/relay_links_reports.pickle', 'wb')
    # pickle_out.close()
    # pickle_out = open('/home/traces/sent_relays_reports.pickle', 'wb')
    # pickle_out.close()

    # # create the deamon thread for message handling
    print("Creating the shareable memory")
    logger.debug("Creating the shareable memory")

    create_or_reset_shareable_memory()
    create_or_reset_shareable_memory()
    _shared_list_data = shm.ShareableList(name="data")
    _shared_list_data_updated = shm.ShareableList(name="data_updated")

    # # create the deamon thread for message handling
    print("Starting the handler of optimization threads")
    logger.debug("Starting the handler")
    _msg_handling_thread = Thread(name="optimization", target=handle_optimization_thread, 
                                  args=(False,), daemon=True)
    _msg_handling_thread.start()

    control_sck = open_control_socket(4200)

    _transform_list: List[XmlToDictManager] = []

    _msg_encoder = RicControlMessageEncoder()

    _send_encoded_data_func = send_optimized_data(control_sck, _msg_encoder)

    # _test_ric_messages = generate_sched_data()


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
                    # print("Received data")
                    # print(_msg)
                    parse_xml_msg(_msg, _msg_encoder, _transform_list)
            else:
                parse_xml_msg(data_sck, _msg_encoder, _transform_list)
            # here we send data to the right sharable list which will be used afterwards for scheduling
            for _transform in _transform_list:
                logging.info(f"Has recevied all reports {_transform.transform.has_received_all_reports()}") 
                if _transform.transform.has_received_all_reports():
                    # insert in queue
                    # update data from the preoptimization 
                    _time_int = int(time.time())
                    _data = {
                        'time': _time_int,
                        transform._JSON_PLMN: _transform.plmn,
                        transform._JSON_FRAME: _transform.transform.frame ,
                        transform._JSON_SUBFRAME: _transform.transform.subframe ,
                        transform._JSON_SLOT: _transform.transform.slot ,
                        'buffer_status': _transform.transform.to_dict()
                    }
                    logging.info(f"Data inserted in the queue: ")
                    logging.info(_data)
                    _plmn_ind = int(_transform.plmn) - 111
                    _shared_list_data[_plmn_ind] = str(_data)
                    _shared_list_data_updated[_plmn_ind] = True
                    _transform.transform.reset()
        # generate and send data    
        _check_ric_commands_to_be_sent(_send_encoded_data_func)



def test_schedule_working():
    setup_logger()
    logger = logging.getLogger('')
    _msg_encoder = RicControlMessageEncoder()
    _list_received_msgs: List[str] = []
    _transform_list: List[XmlToDictManager] = []
    create_or_reset_shareable_memory()
    create_or_reset_shareable_memory()
    _shared_list_data = shm.ShareableList(name="data")
    _shared_list_data_updated = shm.ShareableList(name="data_updated")
    logger.debug("Starting the handler")
    _msg_handling_thread = Thread(name="optimization", target=handle_optimization_thread, 
                                  args=(True,), daemon=True)
    _msg_handling_thread.start()
    # _send_encoded_data_func = send_optimized_data(control_sck, _msg_encoder)
    with open("/home/traces/data_buffer.txt", mode="rb+") as file:
        _data_list = file.readlines()
        _data = b''.join(_data_list)
    
    _all_data_length = len(_data)
    logger.debug(f"Data length {_all_data_length}")
    _total_bytes_consumed = 0
    _nr_msg_read = 0
    _nr_min_msg_print = 0
    _nr_max_msg_print = 4
    while(_total_bytes_consumed < _all_data_length):
        _data_buffer, _data_length, _bytes_consumed =  _msg_encoder.decode_e2ap_ric_indication_msg(_data[_total_bytes_consumed:])
        # print(f"data legnth {_data_length} and bytes consumed {_bytes_consumed}")
        if _data_buffer is not None:
            _nr_msg_read+=1
            _total_bytes_consumed+=_bytes_consumed
            logger.debug(f"Message read {_nr_msg_read} total bytes consumed {_total_bytes_consumed} ")
            _decoded_msg = _data_buffer.decode('utf-8')
            _list_received_msgs.append(_decoded_msg)
            # if _nr_msg_read>=_nr_min_msg_print:
            #     print(_decoded_msg)
            if _nr_msg_read>=_nr_max_msg_print:
                break
    # print("Checing the received reports")
    for _msg in _list_received_msgs:
        # print("Received data")
        # print(_msg)
        parse_xml_msg(_msg, _msg_encoder, _transform_list)

        # print(f"size of tranform list {len(_transform_list)}")
        # print(_transform_list[0].transform.to_dict())
        for _transform in _transform_list:
            print(f"Has recevied all reports {_transform.transform.has_received_all_reports()}") 
            if _transform.transform.has_received_all_reports():
                # insert in queue
                # update data from the preoptimization 
                _time_int = int(time.time())
                _data = {
                    'time': _time_int,
                    transform._JSON_PLMN: _transform.plmn,
                    transform._JSON_FRAME: _transform.transform.frame ,
                    transform._JSON_SUBFRAME: _transform.transform.subframe ,
                    transform._JSON_SLOT: _transform.transform.slot ,
                    'buffer_status': _transform.transform.to_dict()
                }
                logging.info(f"Data inserted in the queue: ")
                # logging.info(_data)
                _plmn_ind = int(_transform.plmn) - 111
                _shared_list_data[_plmn_ind] = str(_data)
                _shared_list_data_updated[_plmn_ind] = True
                _transform.transform.reset()
    # generate and send data    
    _check_ric_commands_to_be_sent(None)


if __name__ == '__main__':
    test_schedule_working()
    # main()