import socket
# import sctp
import logging
# import asn1tools
# import binascii
# from ipso import scenario_creation
import pandas as pd
import os
from ctrl_msg_encoder_decoder import RicControlMessageEncoder


_delimiter_bytes = bytes(";;;", 'utf-8')

# open control socket
def open_control_socket(port: int):

    print('Waiting for xApp connection on port ' + str(port))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4097152)  
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4097152)  

    # server = sctp.sctpsocket_tcp(socket.AF_INET)
    # host = socket.gethostname()
    # bind to INADDR_ANY
    # port = 37423
    server.bind(('', port))
    # server.bind(('0.0.0.0', port))

    server.listen(5)

    control_sck, client_addr = server.accept()
    print('xApp connected: ' + client_addr[0] + ':' + str(client_addr[1]))

    return control_sck


# send through socket
def send_socket(socket, msg: str):
    bytes_num = socket.send(msg)
    # bytes_num = socket.send(msg.encode('utf-8'))
    print('Socket sent ' + str(bytes_num) + ' bytes')


# receive data from socker
def receive_from_socket(socket, ric_encoder: RicControlMessageEncoder): # -> tuple[list[dict], list[dict], list[dict]]:
    logger = logging.getLogger('')
    ack = 'Indication ACK\n'

    data = socket.recv(200000) 

    # might happen that multiple messages arrive at the same time
    # thus they are appended one another and the buffer appears as continuos
    # we have to decode the message one by one until there is no more data to the buffer
    _list_of_ric_messages = []
    _input_data_length: int = len(data)
    _total_bytes_consumed = 0
    # save data buffer to file
    # with open("/home/traces/data_buffer.txt", mode="ab+") as file:
    #     file.write(data)
    # print(data.hex())
    # if len(data)>0:
    #     print(data)
    while(_total_bytes_consumed < _input_data_length):
        # means we have attached messages, so we have to separate them
        # and put in a the list

        _data_buffer, _data_length, _bytes_consumed =  ric_encoder.decode_e2ap_ric_indication_msg(data[_total_bytes_consumed:])
        # print("Data buffer")
        # print(_data_buffer)
        # print("Bytes consumed " + str(_bytes_consumed) + " input data length " + str(_input_data_length))
        if _data_buffer is not None:
            _total_bytes_consumed+=_bytes_consumed
            logger.debug("Total bytes consumed " + str(_total_bytes_consumed) + " input length " + str(_input_data_length) + " & bytes consumed " + str(_bytes_consumed))
            # return str(_data_buffer)
            # print(_data_buffer)
            # print(_data_buffer.decode('utf-8'))
            _list_of_ric_messages.append(_data_buffer.decode('utf-8'))
        else:
            print("Cannot decode data")
            return _list_of_ric_messages
            # break
    if len(_list_of_ric_messages) > 0:
        return _list_of_ric_messages

    try:
        data = data.decode('utf-8')
    except UnicodeDecodeError:
        return ''

    if ack in data:
        data = data[len(ack):]

    if len(data) > 0:
        return data.strip()
    else:
        return ''
    
def setup_logger_xapp_control():
    logging_filename = os.path.join(os.getcwd(), 'report.log')
    # logging_filename = '/home/ef-xapp/xapp-logger.log' # os.path.join(os.getcwd(), )
    logging.basicConfig(level=logging.INFO, filename=logging_filename, filemode='a',
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

if __name__ == '__main__':
    setup_logger_xapp_control()
    _data_buff = b'\x00\x05@\x82\xef\x00\x00\x08\x00\x1d\x00\x05\x00\x00\x18\x00\x00\x00\x05\x00\x02\x00\xc8\x00\x0f\x00\x01\x01\x00\x1b\x00\x02\x00\x01\x00\x1c\x00\x01\x00\x00\x19\x00\x12\x11\x00\x00\x00\x00\x00\x00\x00\x16^`111\x001\x00\xf0\x00\x1a\x00\x82\xa9\x82\xa7\x10\x98\x00\x01\x00\x00\x08NRCellCU\x00\x01@\x0500003\x07\x000PosX\x10\x00\x000PosY\x10\x00\x00@Frame\x00\x02\x02<\x00pSubFrame\x00\x01\x06\x000Slot\x00\x01\x00\x00\x80Timestamp\x00\x02\x16^\x00\xb0SingleReport6\x00\x00\x00\x00\x03\x00\x03\x00\x00\x03\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x04\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x0e\x00\x00\x00\x01\x01\x00\x00\x0c\x00\n\x07\x01\x03\x0c\x01\x0b\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\x00\x00\x00\x00\x14\x00\x00\x00\x01\x00\x00\x01\x00\x01\x01\x00\x01\x00\x01\x01\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x80\x01\x05@\x0500001\x07\x000PosX\x10\x00\x000PosY\x10\x00\x00@Frame\x00\x02\x02<\x00pSubFrame\x00\x01\x06\x000Slot\x00\x01\x00\x00\x80Timestamp\x00\x02\x16^\x00\xb0SingleReport6\x00\x00\x00\x00\x01\x00\x05\x00\x00\x01\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x02\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x03\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x04\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\n\x00\x01\x00d@\x02\x00\x00\n\x00\x14\x00\x02\x00d@\x04\x00\x00\x14\x00\x1e\x00\x02\x00d@\x04\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x0e\x00\x00\x00\x01\x01\x00\x00\x0c\x00\n\x07\x01\x03\x0c\x01\x0b\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90\x00\x00\x00\x00\x14\x00\x00\x00\x01\x00\x00\x01\x00\x01\x01\x00\x01\x00\x01\x01\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x80\x01\x05\x00\x14\x00\x05\x04cpid'
    _l_plmn_size = [] 
    _l_plmn = [111, 112, 113, 114, 115, 116, 117, 118]
    _l_plmn_bytes = [b'111', b'112', b'113', b'114', b'115', b'116', b'117', b'118']
    _msg_encoder = RicControlMessageEncoder()
    with open("/home/traces/data_buffer.txt", mode="rb+") as file:
        _data_list = file.readlines()
        _data = b''.join(_data_list)
        # _data = bytes()
        # print(_data)
    # _data = _data_buff
    _all_data_length = len(_data)
    print(f"Data length {_all_data_length}")
    _total_bytes_consumed = 0
    _nr_msg_read = 0
    _nr_min_msg_print = 0
    # _nr_max_msg_print = 30
    while(_total_bytes_consumed < _all_data_length):
        
        _read_until = min([_total_bytes_consumed+5000, _all_data_length])
        # print(f"Enter cycle read until {_read_until}")
        # _data_buffer, _data_length, _bytes_consumed =  _msg_encoder.decode_e2ap_ric_indication_msg(_data[_total_bytes_consumed:])
        _data_buffer, _data_length, _bytes_consumed =  _msg_encoder.decode_e2ap_ric_indication_msg(_data[_total_bytes_consumed:_read_until])
        print(f"data legnth {_data_length} and bytes consumed {_bytes_consumed}")
        if _data_buffer is not None:
            _nr_msg_read+=1
            _total_bytes_consumed+=_bytes_consumed
            print(f"Message read {_nr_msg_read} total bytes consumed {_total_bytes_consumed} ")
            # _decoded_msg = _data_buffer.decode('utf-8')
            # if _nr_msg_read>=_nr_min_msg_print:
            #     print(_decoded_msg)
            # if _nr_msg_read>=_nr_max_msg_print:
                # break
            _plmn = -1
            for _ind_bytes, _val_bytes in enumerate([b'111', b'112', b'113', b'114', b'115', b'116', b'117', b'118']):
                if _val_bytes in _data_buffer:
                    _plmn = _l_plmn[_ind_bytes]
            _l_plmn_size.append([_plmn, _bytes_consumed])
    df_msg_size = pd.DataFrame(_l_plmn_size, columns=['plmn', 'size'])
    df_msg_size.to_csv("/home/traces/plmn_msg_size.txt", index=False)
