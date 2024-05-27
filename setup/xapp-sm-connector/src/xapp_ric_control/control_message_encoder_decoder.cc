#include <mdclog/mdclog.h>
#include <vector>
#include <iostream>
#include <list>
#include <set>
#include <algorithm>
#include <memory>
#include <string>
#include <sstream>
#include <cassert>  
// #include "assert.h"

#include "control_message_encoder_decoder.h"
// extern "C" {
// #include "E2SM-RC-ControlMessage.h"
#include "E2SM-KPM-IndicationMessage.h"
#include "E2SM-KPM-IndicationHeader.h"
#include "RICindication.h"
#include "InitiatingMessage.h"
#include "ProtocolIE-Field.h"
#include "E2AP-PDU.h"
#include "nr-sl-phy-mac-common.h"
#include "v2x-scheduling-plmn.h"
#include "V2X-Scheduling-All-Users.h"
#include "V2X-Scheduling-Item.h"
#include "V2X-Single-User-report.h"
#include "V2X-Scheduling-User.h"
#include "V2X-Scheduling-Source.h"
// }

#include "tinyxml2.h"

// #include "sl-sci-msg.pb.h"

template<typename T>
std::vector<int> findItems(std::vector<T> const &v, int target) {
    std::vector<int> indices;
    auto it = v.begin();
    while ((it = std::find_if(it, v.end(), [&] (T const &e) { return e == target; }))
        != v.end())
    {
        indices.push_back(std::distance(v.begin(), it)); 
        it++;
    }
    return indices;
}

CellHandoverItem_t* create_handover_item(long ueId, long destinationCellId){
    CellHandoverItem_t* control_message = (CellHandoverItem_t *) calloc(1, sizeof(CellHandoverItem_t));
    control_message->ueId = ueId;
    control_message->destinationCellId = destinationCellId;
    return control_message;
}

CellHandoverItemList_t* create_handover_item_list(std::list<CellHandoverItem_t*> handoverItems){
    CellHandoverItemList_t* cellHandoverList = (CellHandoverItemList_t *) calloc(1, sizeof(CellHandoverItemList_t));
    for (auto it = handoverItems.begin(); it != handoverItems.end(); ++it){
        ASN_SEQUENCE_ADD(&cellHandoverList->list, (*it));
    }
    return cellHandoverList;
}

int e2ap_asn1c_encode_handover_item(CellHandoverItem_t* pdu, unsigned char **buffer)
{
    int len;

    *buffer = NULL;
    assert(pdu != NULL);
    assert(buffer != NULL);

    return aper_encode_to_new_buffer(&asn_DEF_CellHandoverItem, 0, pdu, (void **)buffer);

    // len = aper_encode_to_new_buffer(&asn_DEF_CellHandoverItem, 0, pdu, (void **)buffer);

    if (len < 0) {
        // mdclog_write(MDCLOG_INFO,"[E2AP ASN] Unable to aper encode");
    } else {
        // mdclog_write(MDCLOG_INFO, "[E2AP ASN] Encoded succesfully, encoded size = %d", len);
        xer_fprint(stderr, &asn_DEF_CellHandoverItem, pdu);
    }

    // ASN_STRUCT_RESET(asn_DEF_CellHandoverItem, pdu);
    // ASN_STRUCT_FREE_CONTENTS_ONLY(asn_DEF_CellHandoverItem, pdu);

    // return len;
}

int e2ap_asn1c_encode_all_handovers_item_list(CellHandoverItemList_t* pdu, unsigned char **buffer){
    int len;

    *buffer = NULL;
    assert(pdu != NULL);
    assert(buffer != NULL);

    len = aper_encode_to_new_buffer(&asn_DEF_CellHandoverItemList, 0, pdu, (void **)buffer);

    if (len < 0) {
        // mdclog_write(MDCLOG_INFO,"[E2AP ASN] Unable to aper encode");
    } else {
        // mdclog_write(MDCLOG_INFO, "[E2AP ASN] Encoded succesfully, encoded size = %d", len);
        xer_fprint(stderr, &asn_DEF_CellHandoverItemList, pdu);
    }

    return len;
}

int e2ap_asn1c_encode_cell_handovers(CellHandoverList_t* pdu, unsigned char **buffer)
{
    int len;

    *buffer = NULL;
    assert(pdu != NULL);
    assert(buffer != NULL);

    len = aper_encode_to_new_buffer(&asn_DEF_CellHandoverList, 0, pdu, (void **)buffer);

    if (len < 0) {
        // mdclog_write(MDCLOG_INFO,"[E2AP ASN] Unable to aper encode");
    } else {
        // mdclog_write(MDCLOG_INFO, "[E2AP ASN] Encoded succesfully, encoded size = %d", len);
        xer_fprint(stderr, &asn_DEF_CellHandoverList, pdu);
    }

    return len;
}

int e2ap_asn1c_encode_all_handovers(AllHandoversList_t* pdu, unsigned char **buffer)
{
    int len;

    *buffer = NULL;
    assert(pdu != NULL);
    assert(buffer != NULL);

    len = aper_encode_to_new_buffer(&asn_DEF_AllHandoversList, 0, pdu, (void **)buffer);

    if (len < 0) {
        // mdclog_write(MDCLOG_INFO,"[E2AP ASN] Unable to aper encode");
    } else {
        // mdclog_write(MDCLOG_INFO, "[E2AP ASN] Encoded succesfully, encoded size = %d", len);
        // xer_fprint(stderr, &asn_DEF_AllHandoversList, pdu);
    }

    return len;
}

int e2ap_asn1c_encode_control_message(E2SM_RC_ControlMessage_t* pdu, unsigned char **buffer){
    int len;

    *buffer = NULL;
    assert(pdu != NULL);
    assert(buffer != NULL);

    len = aper_encode_to_new_buffer(&asn_DEF_E2SM_RC_ControlMessage, 0, pdu, (void **)buffer);

    if (len < 0) {
        // mdclog_write(MDCLOG_INFO,"[E2AP ASN] Unable to aper encode");
        std::cout << "[E2AP ASN] Unable to aper encode" <<std::endl;
    } else {
        // mdclog_write(MDCLOG_INFO, "[E2AP ASN] Encoded succesfully, encoded size = %d", len);
        // xer_fprint(stderr, &asn_DEF_E2SM_RC_ControlMessage, pdu);
    }

    return len;
}

struct asn_dec_rval_s e2ap_asn1c_decode_handover_item(CellHandoverItem_t *pdu, enum asn_transfer_syntax syntax, unsigned char *buffer, int len) {
    asn_dec_rval_t dec_ret;
    assert(buffer != NULL);

    dec_ret = asn_decode(NULL, syntax, &asn_DEF_CellHandoverItem, (void **) &pdu, buffer, len);
    if (dec_ret.code != RC_OK) {
        // mdclog_write(MDCLOG_ERR,"[E2AP ASN] Failed to decode pdu");
        // exit(EXIT_FAILURE);
    } else {
        // mdclog_write(MDCLOG_INFO, "[E2AP ASN] Decoded successfully");
        return dec_ret;
    }
    return dec_ret;
}

e2ap_stcp_buffer_t*
decode_e2ap_to_xml(uint8_t* buffer, size_t buffSize){
    // std::cout << "Buffer length " << buffSize << std::endl;
    E2AP_PDU_t *pdu = (E2AP_PDU_t * )calloc(1, sizeof(E2AP_PDU_t));
    uint8_t* buff = (uint8_t *) calloc(1, buffSize);
    memcpy(buff, buffer, buffSize);
    // std::cout << "Buffer print" <<std::endl;
    // for(int i=0; i<buffSize; ++i){
    //     std::cout << std::hex << (int)buff[i];
    // }
    // std::cout << std::endl;
    InitiatingMessage_t* initMsg; 
    e2ap_stcp_buffer* data = (e2ap_stcp_buffer *) calloc(1, sizeof(e2ap_stcp_buffer));
    tinyxml2::XMLDocument pduDoc;
	tinyxml2::XMLDocument headerDoc;
	tinyxml2::XMLDocument msgDoc;
    // printf("Buffer %s \n", buff);
	auto retval = asn_decode(nullptr, ATS_ALIGNED_BASIC_PER, &asn_DEF_E2AP_PDU, (void **) &pdu, (void *)buff, buffSize);
	// auto retval = asn_decode(nullptr, ATS_ALIGNED_BASIC_PER, &asn_DEF_E2AP_PDU, (void **) &pdu, buffer, buffSize);
    // std::cout << "priting the E2AP_PDU_t" << std::endl;
    // xer_fprint(stdout, &asn_DEF_E2AP_PDU, pdu);
    uint8_t idx;
    if (retval.code == RC_OK) {
        // printf("Bytes consumed %s ", std::to_string(retval.consumed).c_str());
        if(pdu->present == E2AP_PDU_PR_initiatingMessage){
            initMsg = (InitiatingMessage_t *)pdu->choice.initiatingMessage;
            RICindication_t* ricIndication = (RICindication_t *)&initMsg->value.choice.RICindication;
            for (idx = 0; idx < ricIndication->protocolIEs.list.count; idx++)
            {
                
                RICindication_IEs *ie = ricIndication->protocolIEs.list.array [idx];
                // std::cout << "Id of array " << ie->value.present << std::endl;
                switch(ie->value.present)
                {
                    case RICindication_IEs__value_PR_RICindicationMessage:  // RIC indication message
                    {
                        int payload_size = ie->value.choice.RICindicationMessage.size;

                        char* payload = (char*) calloc(payload_size, sizeof(char));
                        memcpy(payload, ie->value.choice.RICindicationMessage.buf, payload_size);

                        // E2SM_KPM_IndicationMessage_t *descriptor = 0;
                        E2SM_KPM_IndicationMessage_t *descriptor = (E2SM_KPM_IndicationMessage_t *) calloc (
                                                  1, sizeof (E2SM_KPM_IndicationMessage_t));
                        ASN_STRUCT_RESET(asn_DEF_E2SM_KPM_IndicationMessage, descriptor);
                        auto retvalMsgKpm = asn_decode(nullptr, ATS_ALIGNED_BASIC_PER, &asn_DEF_E2SM_KPM_IndicationMessage, 
                                            (void **) &descriptor, payload, payload_size);
                        char *printBufferMessage;
                        size_t sizeMessage;
                        FILE *streamMessage = open_memstream(&printBufferMessage, &sizeMessage);
                        xer_fprint(streamMessage, &asn_DEF_E2SM_KPM_IndicationMessage, descriptor);
                        // std::cout << "priting the ind msg" << std::endl;
                        // xer_fprint(stdout, &asn_DEF_E2SM_KPM_IndicationMessage, descriptor);
                        msgDoc.Parse(printBufferMessage);
                        delete streamMessage;
                        delete printBufferMessage;
                        free(payload);
                        break;
                    }
                    break;
                    case RICindication_IEs__value_PR_RICindicationHeader:  // RIC indication header
                    {
                        int payload_size = ie->value.choice.RICindicationHeader.size;
                        char* payload = (char*) calloc(payload_size, sizeof(char));
                        memcpy(payload, ie->value.choice.RICindicationHeader.buf, payload_size);
                        E2SM_KPM_IndicationHeader_t *descriptor = 0;
                        auto retvalMsgKpm = asn_decode(nullptr, ATS_ALIGNED_BASIC_PER, &asn_DEF_E2SM_KPM_IndicationHeader, (void **) &descriptor, payload, payload_size);
                        char *printBufferHeader;
                        size_t sizeHeader;
                        FILE *streamHeader = open_memstream(&printBufferHeader, &sizeHeader);
                        xer_fprint(streamHeader, &asn_DEF_E2SM_KPM_IndicationHeader, descriptor);
                        headerDoc.Parse(printBufferHeader);
                        delete streamHeader;
                        delete printBufferHeader;
                        free(payload);
                        break;
                    }
                }
            }
            tinyxml2::XMLElement* mainElement = pduDoc.NewElement("message");
            tinyxml2::XMLNode* headerNode = pduDoc.InsertFirstChild(mainElement->DeepClone(&pduDoc));
            tinyxml2::XMLNode* rootHeader = headerDoc.FirstChild()->DeepClone(&pduDoc); 
            pduDoc.FirstChild()->InsertEndChild(rootHeader);
            tinyxml2::XMLNode* rootMessage = msgDoc.FirstChild()->DeepClone(&pduDoc);
            pduDoc.FirstChild()->InsertEndChild(rootMessage);
            // sending the final
            char* printBufferFinal;
            size_t sizeFinal;
            FILE *streamFinal = open_memstream(&printBufferFinal, &sizeFinal);
            pduDoc.SaveFile(streamFinal, true);
            fflush(streamFinal);
            data->msg_length = sizeFinal; 
            data->bytes_consumed = retval.consumed;
            // printf( "Data length of decoded message %d", data->msg_length); 
            data->msg_buffer = (uint8_t *) calloc(1, data->msg_length);
            memcpy(data->msg_buffer, printBufferFinal, std::min(data->msg_length, MAX_SCTP_BUFFER));
            // deleting pointers
            delete printBufferFinal;
            delete streamFinal;
        }
    }
    fflush(stdout);
    // delete pdu;
    // delete buff;
    free(pdu);
    free(buff);
    return data;
}

char* converHexToByte(std::string hexString) {

    char * bytes = new char[hexString.length()/2];
    std::stringstream converter;

    for(int i = 0; i < hexString.length(); i+=2)
    {
        converter << std::hex << hexString.substr(i,2);
        int byte;
        converter >> byte;
        bytes[i/2] = byte & 0xFF;
        converter.str(std::string());
        converter.clear();
    }
    // char* bytesPointer= bytes;
    // return bytesPointer;
    return bytes;
}  

v2x_sci_header_buffer_t*
decode_v2x_sci_header(uint8_t* buffer, size_t buffSize){
    v2x_sci_header_buffer_t* data;
    // std::cout << " entered " << std::endl;
    try{
        std::string s((char*) buffer);
        // removing white space if there is any
        s.erase(std::remove_if(s.begin(), s.end(), [](unsigned char x) { return std::isspace(x); }), s.end());
        // std::cout << " the buffer with no spaces " << s << std::endl;
        char* bytes = converHexToByte(s);

        uint8_t *bufferHeader = (uint8_t *)calloc(1, s.length());
        memcpy(bufferHeader, bytes, s.length());

        // ns3::Buffer bufferSciHeader = ns3::Buffer();
        // bufferSciHeader.Deserialize(bufferHeader, s.length());
        // ns3::NrSlSciF1aHeader sciHeader = ns3::NrSlSciF1aHeader();
        // ns3::Buffer::Iterator bufferSciHeaderIt = bufferSciHeader.Begin();
        // sciHeader.DeserializeForE2(bufferSciHeaderIt);
    
        // Protobuff deserialization
        ns3::NrSlSciF1aHeader sciHeader = ns3::NrSlSciF1aHeader();
        // ns3::NrSlSciF1aHeaderProto sciHeaderProto = ns3::NrSlSciF1aHeaderProto();        
        // sciHeaderProto.ParseFromArray(bufferHeader, s.length());
        // sciHeader.DeserializeFromProtoBuff(sciHeaderProto);

        data = new v2x_sci_header_buffer_t(sciHeader);
        free(bufferHeader);
        delete[] bytes;
    }catch(...){
        // return empty struct
        // checked in python if data is valid or not
        data = new v2x_sci_header_buffer_t();
    }

    return data;
}

v2x_sci_tag_buffer_t*
decode_v2x_sci_tag(uint8_t* buffer, size_t buffSize){
    v2x_sci_tag_buffer_t* data;
    try{
        // uint8_t* buff = (uint8_t *) calloc(1, buffSize);
        // memcpy(buff, buffer, buffSize);
        std::string s((char*) buffer);
        // removing white space if there is any
        s.erase(std::remove_if(s.begin(), s.end(), [](unsigned char x) { return std::isspace(x); }), s.end());

        char* bytes = converHexToByte(s);
        uint8_t *bufferTag = (uint8_t *)calloc(1, s.length());
        memcpy(bufferTag, bytes, s.length());

        // ns3::Buffer bufferSciTag = ns3::Buffer();
        // bufferSciTag.Deserialize(bufferTag, s.length());
        // ns3::NrSlMacPduTag sciTag = ns3::NrSlMacPduTag();
        // ns3::Buffer::Iterator bufferSciTagIt = bufferSciTag.Begin();
        // sciTag.DeserializeForE2(bufferSciTagIt);

        ns3::NrSlMacPduTag sciTag = ns3::NrSlMacPduTag();
        // ns3::NrSlMacPduTagProto sciTagProto = ns3::NrSlMacPduTagProto();        
        // sciTagProto.ParseFromArray(bufferTag, s.length());
        // sciTag.DeserializeFromProtoBuff(sciTagProto);

        data = new v2x_sci_tag_buffer_t(sciTag);
        free(bufferTag);
        delete[] bytes;
    }catch(...){
        // return empty struct
        // checked in python if data is valid or not
        data = new v2x_sci_tag_buffer_t();
    }
    return data;
}

sctp_buffer_t* gnerate_e2ap_encode_handover_control_message(uint16_t* ue_id, uint16_t* start_position, uint16_t* optimized, size_t size){
    // default value
    std::string plmn("111");
    std::vector<long> ue_id_vec (size);
    std::vector<long> start_position_vec (size);
    std::vector<long> optimized_vec (size);
    for(int _ind = 0; _ind<size; ++_ind){
        ue_id_vec[_ind] = (ue_id[_ind]);
        start_position_vec[_ind] = (start_position[_ind]);
        optimized_vec[_ind] = (optimized[_ind]);
    }

    std::set<long> sourceCellIdSet;
    for (long x: start_position_vec){
        sourceCellIdSet.insert(x);
    }
    AllHandoversListPlmn_t* allHandoversListPlmn = (AllHandoversListPlmn_t *) calloc(1, sizeof(AllHandoversListPlmn_t));
    AllHandoversList_t* allHandoversList = (AllHandoversList_t *) calloc(1, sizeof(AllHandoversList_t));
    allHandoversListPlmn->allHandoversList = allHandoversList;
    allHandoversListPlmn->plmn_id.buf = (uint8_t *) calloc (1, 3);
    allHandoversListPlmn->plmn_id.size = 3;
    memcpy (allHandoversListPlmn->plmn_id.buf, plmn.c_str (), 3);

    for (long sourceCellId: sourceCellIdSet){
        CellHandoverList_t* cellHandovers = (CellHandoverList_t *) calloc(1, sizeof(CellHandoverList_t));
        cellHandovers->sourceCellId = sourceCellId;
        // find items in the starting vec from the set
        std::vector<int> indices = findItems(start_position_vec, sourceCellId);
        std::list<CellHandoverItem_t*> handoverItems;
        for (int index : indices){
            long _ue_ind = ue_id_vec.at(index);
            long _dst_cell_id = optimized_vec.at(index);
            CellHandoverItem_t* control_message = create_handover_item(_ue_ind, _dst_cell_id);
            handoverItems.push_back(control_message);
        }
        CellHandoverItemList_t* cellHandoverList = create_handover_item_list(handoverItems);
        cellHandovers->cellHandoverItemList = cellHandoverList;
        ASN_SEQUENCE_ADD(&allHandoversList->list, cellHandovers);
    }

    // create E2SM
    // this is to keeep compatability with decoding in ns3
    E2SM_RC_ControlMessage_t* rcControlMessage = (E2SM_RC_ControlMessage_t *) calloc(1, sizeof(E2SM_RC_ControlMessage_t));
    rcControlMessage->present = E2SM_RC_ControlMessage_PR_handoverMessage_Format;
    // rcControlMessage->choice.handoverMessage_Format = allHandoversList;
    rcControlMessage->choice.handoverMessage_Format = allHandoversListPlmn;

    uint8_t *buf;
    sctp_buffer_t* data = (sctp_buffer_t *) calloc(1, sizeof(sctp_buffer_t));

    // data->length = e2ap_asn1c_encode_all_handovers_item_list(cellHandoverList, &buf);
    // data->length = e2ap_asn1c_encode_cell_handovers(cellHandovers, &buf);
    // data->length = e2ap_asn1c_encode_all_handovers(allHandoversList, &buf);
    data->length = e2ap_asn1c_encode_control_message(rcControlMessage, &buf);
    // printf( "Data length %d", data->length);
    data->buffer = (uint8_t *) calloc(1, data->length);
    memcpy(data->buffer, buf, std::min(data->length, MAX_SCTP_BUFFER));
    // data->buffer = buf;
    // printf( "Data length %d", data->length);

    free(allHandoversListPlmn);
    // delete allHandoversList;
    // delete allHandoversListPlmn;

    return data;
}

sctp_buffer_t* generate_e2ap_encode_handover_control_message_plmn(uint16_t* ue_id, uint16_t* start_position, uint16_t* optimized, size_t size, char* plmnId){
    
    std::string plmn(plmnId);
    // std::cout<< "Plmn " << plmn << std::endl;
    std::vector<long> ue_id_vec (size);
    std::vector<long> start_position_vec (size);
    std::vector<long> optimized_vec (size);
    for(int _ind = 0; _ind<size; ++_ind){
        ue_id_vec[_ind] = (ue_id[_ind]);
        start_position_vec[_ind] = (start_position[_ind]);
        optimized_vec[_ind] = (optimized[_ind]);
    }

    std::set<long> sourceCellIdSet;
    for (long x: start_position_vec){
        sourceCellIdSet.insert(x);
    }

    AllHandoversListPlmn_t* allHandoversListPlmn = (AllHandoversListPlmn_t *) calloc(1, sizeof(AllHandoversListPlmn_t));
    AllHandoversList_t* allHandoversList = (AllHandoversList_t *) calloc(1, sizeof(AllHandoversList_t));
    allHandoversListPlmn->plmn_id.buf = (uint8_t *) calloc (1, 3);
    allHandoversListPlmn->plmn_id.size = 3;
    memcpy (allHandoversListPlmn->plmn_id.buf, plmn.c_str (), 3);

    // memcpy (allHandoversList->plmn_id.buf, plmn.c_str (), 3);

    allHandoversListPlmn->allHandoversList = allHandoversList;

    for (long sourceCellId: sourceCellIdSet){
        CellHandoverList_t* cellHandovers = (CellHandoverList_t *) calloc(1, sizeof(CellHandoverList_t));
        cellHandovers->sourceCellId = sourceCellId;
        // find items in the starting vec from the set
        std::vector<int> indices = findItems(start_position_vec, sourceCellId);
        std::list<CellHandoverItem_t*> handoverItems;
        for (int index : indices){
            long _ue_ind = ue_id_vec.at(index);
            long _dst_cell_id = optimized_vec.at(index);
            CellHandoverItem_t* control_message = create_handover_item(_ue_ind, _dst_cell_id);
            handoverItems.push_back(control_message);
        }
        CellHandoverItemList_t* cellHandoverList = create_handover_item_list(handoverItems);
        cellHandovers->cellHandoverItemList = cellHandoverList;
        ASN_SEQUENCE_ADD(&allHandoversList->list, cellHandovers);
    }

    // create E2SM
    // this is to keeep compatability with decoding in ns3
    E2SM_RC_ControlMessage_t* rcControlMessage = (E2SM_RC_ControlMessage_t *) calloc(1, sizeof(E2SM_RC_ControlMessage_t));
    rcControlMessage->present = E2SM_RC_ControlMessage_PR_handoverMessage_Format;
    // rcControlMessage->choice.handoverMessage_Format = allHandoversList;
    rcControlMessage->choice.handoverMessage_Format = allHandoversListPlmn;

    uint8_t *buf;
    sctp_buffer_t* data = (sctp_buffer_t *) calloc(1, sizeof(sctp_buffer_t));

    // data->length = e2ap_asn1c_encode_all_handovers_item_list(cellHandoverList, &buf);
    // data->length = e2ap_asn1c_encode_cell_handovers(cellHandovers, &buf);
    // data->length = e2ap_asn1c_encode_all_handovers(allHandoversList, &buf);
    data->length = e2ap_asn1c_encode_control_message(rcControlMessage, &buf);
    // printf( "Data length %d", data->length);
    data->buffer = (uint8_t *) calloc(1, data->length);
    memcpy(data->buffer, buf, std::min(data->length, MAX_SCTP_BUFFER));
    // data->buffer = buf;
    // printf( "Data length %d", data->length);

    free(allHandoversListPlmn);
    return data;
}
 

sctp_buffer_t* generate_e2ap_scheduling_control_message_plmn(v2x_source_slot_allocations* source_alloc_it, size_t sourceUsersSize, char* plmnId){
    
    std::string plmn(plmnId);

    // the python function shall give as input the data of the scheduling, which shall be encoded and treturn the buffer

    // create the control message
    V2X_Scheduling_All_UsersPlmn_t* v2XSchedulingAllUsersListPlmn = (V2X_Scheduling_All_UsersPlmn_t *) calloc(1, sizeof(V2X_Scheduling_All_UsersPlmn_t));
    V2X_Scheduling_All_Users_t* v2xSchedulingAllUsersList = (V2X_Scheduling_All_Users_t *) calloc(1, sizeof(V2X_Scheduling_All_Users_t));
    v2XSchedulingAllUsersListPlmn->plmn_id.buf = (uint8_t *) calloc (1, 3);
    v2XSchedulingAllUsersListPlmn->plmn_id.size = 3;
    memcpy (v2XSchedulingAllUsersListPlmn->plmn_id.buf, plmn.c_str (), 3);

    v2XSchedulingAllUsersListPlmn->v2XSchedulingAllUsersList = v2xSchedulingAllUsersList;

    for(int _ind = 0; _ind<sourceUsersSize; ++_ind){
        // this is to shift the pointer to the next object
        auto source_alloc = source_alloc_it + _ind;
        // in the structure there is the scheduling of single user
        V2X_Scheduling_Source_t* v2XSourceUserScheduling = (V2X_Scheduling_Source_t *) calloc(1, sizeof(V2X_Scheduling_Source_t));
        v2XSourceUserScheduling->v2xNodeId = (long) source_alloc->source_ue_id;
        uint32_t sourceNumDestination = source_alloc->destinationAllocationsSize;
        
        for (int destInd = 0; destInd< sourceNumDestination; ++destInd){
            // goint to a single user 
            auto user_alloc = source_alloc->destinationAllocations + destInd;
            // create single user scheduling object
            V2X_Scheduling_User_t* v2XSingleUserScheduling = (V2X_Scheduling_User_t *) calloc(1, sizeof(V2X_Scheduling_User_t));
            // adding v2 node id
            v2XSingleUserScheduling->v2xNodeId = (long) user_alloc->ue_id;
            v2XSingleUserScheduling->cReselectionCounter = (long) user_alloc->cReselCounter;
            v2XSingleUserScheduling->slResourceReselectionCounter = (long) user_alloc->slResoReselCounter;
            v2XSingleUserScheduling->prevSlResoReselCounter = (long) user_alloc->prevSlResoReselCounter;
            v2XSingleUserScheduling->nrSlHarqId = (long) user_alloc->nrSlHarqId;
            v2XSingleUserScheduling->nSelected = (long) user_alloc->nSelected;
            v2XSingleUserScheduling->tbTxCounter = (long) user_alloc->tbTxCounter;
            // create the scheduling list for the single user
            uint32_t userNumOfAllocation = user_alloc->userAllocationSize;
            for (int userAllocInd = 0; userAllocInd< userNumOfAllocation; ++userAllocInd){
                auto userAllocVecIt = user_alloc->userAllocation+userAllocInd;
                V2X_Scheduling_Item_t* schedulingItem = (V2X_Scheduling_Item_t *) calloc(1, sizeof(V2X_Scheduling_Item_t));
                // create std::vector of rlc pdu
                std::vector<ns3::SlRlcPduInfo> rlRlcPduInfoVec;
                for (int slRlcPduInd = 0; slRlcPduInd<userAllocVecIt->slRlcPduInfoSize; ++slRlcPduInd){
                    auto slRlcPduInfoIt = userAllocVecIt->slRlcPduInfo + slRlcPduInd;
                    slRlcPduInfoIt = slRlcPduInfoIt + slRlcPduInd;
                    rlRlcPduInfoVec.push_back(ns3::SlRlcPduInfo(slRlcPduInfoIt->lcid, 
                                            slRlcPduInfoIt->size));
                }
                std::cout << "control_message_encoder_decoder: ndi " << +userAllocVecIt->ndi << std::endl;
                ns3::NrSlSlotAlloc nrSlSlotAlloc = ns3::NrSlSlotAlloc(
                    userAllocVecIt->m_frameNum, userAllocVecIt->m_subframeNum, userAllocVecIt->m_slotNum, userAllocVecIt->m_numerology, 
                    userAllocVecIt->dstL2Id, userAllocVecIt->ndi, userAllocVecIt->rv, userAllocVecIt->priority, 
                    rlRlcPduInfoVec,
                    userAllocVecIt->mcs, userAllocVecIt->numSlPscchRbs, userAllocVecIt->slPscchSymStart, userAllocVecIt->slPscchSymLength, 
                    userAllocVecIt->slPsschSymStart, userAllocVecIt->slPsschSymLength, userAllocVecIt->slPsschSubChStart, 
                    userAllocVecIt->slPsschSubChLength, userAllocVecIt->maxNumPerReserve, userAllocVecIt->txSci1A, userAllocVecIt->slotNumInd

                );
                // user buffer for the serialization
                // uint32_t nrSlotAllocBufferSize = nrSlSlotAlloc.GetSerializedSizeForE2();
                // ns3::Buffer bufferNrSlotAlloc = ns3::Buffer();
                // bufferNrSlotAlloc.AddAtStart(nrSlotAllocBufferSize);
                // nrSlSlotAlloc.SerializeForE2(bufferNrSlotAlloc.Begin());
                // uint32_t extraSizeNrSlotAlloc = 30;
                // uint8_t *bufferNrSlotAllocBuffer = (uint8_t *) calloc (1, nrSlotAllocBufferSize+extraSizeNrSlotAlloc);
                // bufferNrSlotAlloc.Serialize(bufferNrSlotAllocBuffer, nrSlotAllocBufferSize+extraSizeNrSlotAlloc);
                // extraSizeNrSlotAlloc = bufferNrSlotAlloc.GetSerializedSize() - bufferNrSlotAlloc.GetSize();

                // Buffer_String_t * allocBufferString = (Buffer_String_t *) calloc (1, sizeof (Buffer_String_t));
                // allocBufferString->buf = (uint8_t *) calloc (1, nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                // allocBufferString->size = nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4;
                // memcpy (allocBufferString->buf, bufferNrSlotAllocBuffer, nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                // schedulingItem->nrSlotAllocBuffer = *allocBufferString;

                // schedulingItem->nrSlotAllocBuffer.buf = (uint8_t *) calloc (1, (nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4));
                // schedulingItem->nrSlotAllocBuffer.size = (nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                // memcpy (schedulingItem->nrSlotAllocBuffer.buf, bufferNrSlotAllocBuffer, (nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4));
                // protobuf serialization

                ns3::NrSlSlotAllocProto nrSlSlotProto = nrSlSlotAlloc.GenerateProtoBuff();
                uint8_t *bufferNrSlotAllocBuffer = (uint8_t *) calloc (1, nrSlSlotProto.ByteSizeLong());
                nrSlSlotProto.SerializeToArray(bufferNrSlotAllocBuffer, nrSlSlotProto.ByteSizeLong());
                schedulingItem->nrSlotAllocBuffer.buf = (uint8_t *) calloc (1, (nrSlSlotProto.ByteSizeLong()));
                schedulingItem->nrSlotAllocBuffer.size = (nrSlSlotProto.ByteSizeLong());
                memcpy (schedulingItem->nrSlotAllocBuffer.buf, bufferNrSlotAllocBuffer, (nrSlSlotProto.ByteSizeLong()));

                ASN_SEQUENCE_ADD(&v2XSingleUserScheduling->V2X_Scheduling_ItemList.list, schedulingItem);
            }
            // add this user the the list of all users
            ASN_SEQUENCE_ADD(&v2XSourceUserScheduling->V2X_Scheduling_DestinationList.list, v2XSingleUserScheduling);
        }
        ASN_SEQUENCE_ADD(&v2xSchedulingAllUsersList->list, v2XSourceUserScheduling);
    }
    
    // xer_fprint(stdout, &asn_DEF_V2X_Scheduling_All_UsersPlmn, v2XSchedulingAllUsersListPlmn);
    // the rc control message which shall be returned to the python object
    E2SM_RC_ControlMessage_t* rcControlMessage = (E2SM_RC_ControlMessage_t *) calloc(1, sizeof(E2SM_RC_ControlMessage_t));
    rcControlMessage->present = E2SM_RC_ControlMessage_PR_v2xSchedulingMessage_Format;
    rcControlMessage->choice.v2xSchedulingMessage_Format = v2XSchedulingAllUsersListPlmn;

    sctp_buffer_t* data = (sctp_buffer_t *) calloc(1, sizeof(sctp_buffer_t));

    uint8_t *buf;
    // encoding the rcControl message created into the buffer object
    data->length = e2ap_asn1c_encode_control_message(rcControlMessage, &buf);

    data->buffer = (uint8_t *) calloc(1, data->length);
    memcpy(data->buffer, buf, std::min(data->length, MAX_SCTP_BUFFER));

    // xer_fprint(stdout, &asn_DEF_E2SM_RC_ControlMessage, rcControlMessage);
    // afterwords we have to generate the data part

    // char printBuffer[40960]{};
    // char *tmp = printBuffer;
    // for (size_t _buffInd = 0; (size_t)_buffInd<data->length; ++_buffInd){
    //     snprintf(tmp, 3, "%02x", data->buffer[_buffInd]);
    //     tmp += 2;
    //     // std::cout << std::setfill('0') << std::setw(2) << data.buffer[_buffInd];
    // }
    // printf("Buffer %s \n", printBuffer);

    // freeing all the data before returning the struct
    free(v2XSchedulingAllUsersListPlmn);
    return data;

}