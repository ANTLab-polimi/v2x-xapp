#include "tinyxml2.h"
// #include "stdio.h"
#include <ostream>
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include "control_message_encoder_decoder.h"
#include "nr-sl-phy-mac-common.h"
#include "v2x-scheduling-plmn.h"
#include "V2X-Scheduling-All-Users.h"
#include "V2X-Scheduling-Item.h"
#include "V2X-Single-User-report.h"
#include "V2X-Scheduling-User.h"
#include "V2X-Scheduling-Source.h"
#include "Buffer-String.h"

// using namespace tinyxml2;

int main(int argc, char* argv[]){
    v2x_source_slot_allocations_t* source_alloc = (v2x_source_slot_allocations_t *) calloc(4, sizeof(v2x_source_slot_allocations_t));
    source_alloc[0].source_ue_id = 11;
    source_alloc[1].source_ue_id = 12;
    source_alloc[2].source_ue_id = 13;
    source_alloc[3].source_ue_id = 14;
    v2x_user_nr_sl_slot_alloc_t* user_alloc = (v2x_user_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_user_nr_sl_slot_alloc_t));
    v2x_user_nr_sl_slot_alloc_t* user_alloc_2 = (v2x_user_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_user_nr_sl_slot_alloc_t));
    v2x_user_nr_sl_slot_alloc_t* user_alloc_3 = (v2x_user_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_user_nr_sl_slot_alloc_t));
    v2x_user_nr_sl_slot_alloc_t* user_alloc_4 = (v2x_user_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_user_nr_sl_slot_alloc_t));
    user_alloc[0].ue_id = 11;
    user_alloc[1].ue_id = 12;
    user_alloc_2[0].ue_id = 13;
    user_alloc_2[1].ue_id = 14;
    user_alloc_3[0].ue_id = 15;
    user_alloc_3[1].ue_id = 16;
    user_alloc_4[0].ue_id = 17;
    user_alloc_4[1].ue_id = 18;
    source_alloc[0].destinationAllocationsSize = 2;
    source_alloc[0].destinationAllocations = user_alloc;
    source_alloc[1].destinationAllocationsSize = 2;
    source_alloc[1].destinationAllocations = user_alloc_2;
    source_alloc[2].destinationAllocationsSize = 2;
    source_alloc[2].destinationAllocations = user_alloc_3;
    source_alloc[3].destinationAllocationsSize = 2;
    source_alloc[3].destinationAllocations = user_alloc_4;
    v2x_nr_sl_slot_alloc_t* slot_alloc = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_2 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_3 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_4 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_5 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_6 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_7 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    v2x_nr_sl_slot_alloc_t* slot_alloc_8 = (v2x_nr_sl_slot_alloc_t *) calloc(2, sizeof(v2x_nr_sl_slot_alloc_t));
    user_alloc[0].userAllocation = slot_alloc;
    user_alloc[0].userAllocationSize = 2;
    user_alloc[1].userAllocation = slot_alloc_2;
    user_alloc[1].userAllocationSize = 2;
    user_alloc_2[0].userAllocation = slot_alloc_3;
    user_alloc_2[0].userAllocationSize = 2;
    user_alloc_2[1].userAllocation = slot_alloc_4;
    user_alloc_2[1].userAllocationSize = 2;
    user_alloc_3[0].userAllocation = slot_alloc_5;
    user_alloc_3[0].userAllocationSize = 2;
    user_alloc_3[1].userAllocation = slot_alloc_6;
    user_alloc_3[1].userAllocationSize = 2;
    user_alloc_4[0].userAllocation = slot_alloc_7;
    user_alloc_4[0].userAllocationSize = 2;
    user_alloc_4[1].userAllocation = slot_alloc_8;
    user_alloc_4[1].userAllocationSize = 2;
    // slot_alloc[0]->m_frameNum = 12;
    
    v2x_source_slot_allocations_t * sourceAllocIt = (v2x_source_slot_allocations_t *) &source_alloc[0];
    for (int sourceAllocInd=0;sourceAllocInd<4;++sourceAllocInd){
        // sourceAllocIt = sourceAllocIt+sourceAllocInd;
        sourceAllocIt = &source_alloc[sourceAllocInd];
        // std::cout << "1  " << sourceAllocInd  << " " << sourceAllocIt->destinationAllocationsSize<<std::endl;
        // auto userAllocVecIt = sourceAllocIt->destinationAllocations;
        // std::cout << "2  " <<std::endl;
        for (uint32_t userAllocInd=0;userAllocInd<2;++userAllocInd){
            auto userAllocVecIt = sourceAllocIt->destinationAllocations + userAllocInd;
            // std::cout << "3  " << userAllocInd << " " << userAllocVecIt->userAllocationSize<<std::endl;
            // auto slotAllocVecIt = userAllocVecIt->userAllocation;
            // std::cout << "4  " <<std::endl;
            for (uint32_t slotAllocInd=0;slotAllocInd<2;++slotAllocInd){
                auto slotAllocVecIt = userAllocVecIt->userAllocation+slotAllocInd;
                // std::cout << "5  " << slotAllocInd << " " <<slotAllocVecIt->slRlcPduInfoSize <<std::endl;
                v2x_sl_rlc_pdu_info_t* sl_rlc_pdu = (v2x_sl_rlc_pdu_info_t *) calloc(2, sizeof(v2x_sl_rlc_pdu_info_t));
                slotAllocVecIt->slRlcPduInfo = sl_rlc_pdu;
                slotAllocVecIt->slRlcPduInfoSize = 2;
                // std::cout << "6  "<<std::endl;
                sl_rlc_pdu[0].size = 40;
                sl_rlc_pdu[1].size = 40;
            }
        }
    }
    // std::cout << "7  "<<std::endl;

    sctp_buffer_t* res = generate_e2ap_scheduling_control_message_plmn(&source_alloc[0], 4, "111");

    std::cout << "Length of encoding " << res->length << std::endl;
}

int main_message_creation(int argc, char* argv[]){

    std::string plmn("111");

    std::cout << "Inside the decoder with plmn id " << plmn << std::endl;

    // the python function shall give as input the data of the scheduling, which shall be encoded and treturn the buffer

    // create the control message
    V2X_Scheduling_All_UsersPlmn_t* v2XSchedulingAllUsersListPlmn = (V2X_Scheduling_All_UsersPlmn_t *) calloc(1, sizeof(V2X_Scheduling_All_UsersPlmn_t));
    V2X_Scheduling_All_Users_t* v2xSchedulingAllUsersList = (V2X_Scheduling_All_Users_t *) calloc(1, sizeof(V2X_Scheduling_All_Users_t));
    v2XSchedulingAllUsersListPlmn->v2XSchedulingAllUsersList = v2xSchedulingAllUsersList;
    v2XSchedulingAllUsersListPlmn->plmn_id.buf = (uint8_t *) calloc (1, 3);
    v2XSchedulingAllUsersListPlmn->plmn_id.size = 3;
    memcpy (v2XSchedulingAllUsersListPlmn->plmn_id.buf, plmn.c_str (), 3);

    

    std::cout << "Adding the data to the structure" << std::endl;


    for(int _ind = 0; _ind<1; ++_ind){
        // this is to shift the pointer to the next object
        v2x_source_slot_allocations_t* source_alloc = (v2x_source_slot_allocations_t *) calloc(1, sizeof(v2x_source_slot_allocations_t));
        // user_alloc+=_ind;
        v2x_user_nr_sl_slot_alloc_t* user_alloc = (v2x_user_nr_sl_slot_alloc_t *) calloc(1, sizeof(v2x_user_nr_sl_slot_alloc_t));
        source_alloc->destinationAllocations = user_alloc;
        user_alloc->userAllocation = new v2x_nr_sl_slot_alloc_t();
        // test print the ue id
        std::cout << "Ue id " << user_alloc->ue_id << std::endl;
        // goint to a single user 
        // create single source user scheduling object
        V2X_Scheduling_Source_t* v2XSourceUserScheduling = (V2X_Scheduling_Source_t *) calloc(1, sizeof(V2X_Scheduling_Source_t));
        v2XSourceUserScheduling->v2xNodeId = source_alloc->source_ue_id;
        // create single user scheduling object
        V2X_Scheduling_User_t* v2XSingleUserScheduling = (V2X_Scheduling_User_t *) calloc(1, sizeof(V2X_Scheduling_User_t));
        // adding v2 node id
        v2XSingleUserScheduling->v2xNodeId = (long) user_alloc->ue_id;
        // create the scheduling list for the single user

        std::cout << "1" << std::endl;
        auto sourceAllocVecIt = source_alloc->destinationAllocations;
        for (uint32_t sourceAllocInd=0;sourceAllocInd<1;++sourceAllocInd){

            auto userAllocVecIt = user_alloc->userAllocation;
            for (uint32_t userAllocInd=0;userAllocInd<1;++userAllocInd){
            // for (auto userAllocVecIt = user_alloc->userAllocation.begin(); userAllocVecIt!=user_alloc->userAllocation.end(); ++userAllocVecIt){
                V2X_Scheduling_Item_t* schedulingItem = (V2X_Scheduling_Item_t *) calloc(1, sizeof(V2X_Scheduling_Item_t));
                // create std::vector of rlc pdu
                std::vector<ns3::SlRlcPduInfo> rlRlcPduInfoVec;
                std::cout << "2" << std::endl;
                userAllocVecIt->slRlcPduInfo = new v2x_sl_rlc_pdu_info_t();
                // std::cout << "Size " << userAllocVecIt->slRlcPduInfo.size() << std::endl;
                auto slRlcPduInfoIt = userAllocVecIt->slRlcPduInfo;
                for (uint32_t allocInd=0;allocInd<1;++allocInd){
                // for (auto slRlcPduInfoIt = userAllocVecIt->slRlcPduInfo.begin(); 
                //         slRlcPduInfoIt!=userAllocVecIt->slRlcPduInfo.end(); 
                //         ++ slRlcPduInfoIt){
                    std::cout << "3" << std::endl;
                    // rlRlcPduInfoVec.push_back(ns3::SlRlcPduInfo(slRlcPduInfoIt->lcid, slRlcPduInfoIt->size));
                    // rlRlcPduInfoVec.push_back(ns3::SlRlcPduInfo(slRlcPduInfoIt->lcid, slRlcPduInfoIt->size));
                    rlRlcPduInfoVec.push_back(ns3::SlRlcPduInfo(slRlcPduInfoIt->lcid, 15));
                    rlRlcPduInfoVec.push_back(ns3::SlRlcPduInfo(slRlcPduInfoIt->lcid, 25));
                    // rlRlcPduInfoVec.push_back(ns3::SlRlcPduInfo(slRlcPduInfoIt->lcid, 35));
                }
                std::cout << "4" << std::endl;
                ns3::NrSlSlotAlloc nrSlSlotAlloc = ns3::NrSlSlotAlloc(
                    userAllocVecIt->m_frameNum, userAllocVecIt->m_subframeNum, userAllocVecIt->m_slotNum, userAllocVecIt->m_numerology, 
                    userAllocVecIt->dstL2Id, userAllocVecIt->ndi, userAllocVecIt->rv, userAllocVecIt->priority, 
                    rlRlcPduInfoVec,
                    userAllocVecIt->mcs, userAllocVecIt->numSlPscchRbs, userAllocVecIt->slPscchSymStart, userAllocVecIt->slPscchSymLength, 
                    userAllocVecIt->slPsschSymStart, userAllocVecIt->slPsschSymLength, userAllocVecIt->slPsschSubChStart, 
                    userAllocVecIt->slPsschSubChLength, userAllocVecIt->maxNumPerReserve, userAllocVecIt->txSci1A, userAllocVecIt->slotNumInd

                );
                std::cout << "Size 1 " << nrSlSlotAlloc.slRlcPduInfo.at(0).size << std::endl;
                // std::cout << "Size 1 " << nrSlSlotAlloc.slRlcPduInfo.at(1).size << std::endl;
                std::cout << "5" << std::endl;
                // user buffer for the serialization
                uint32_t nrSlotAllocBufferSize = nrSlSlotAlloc.GetSerializedSizeForE2();

                std::cout << "Serialization size " << nrSlotAllocBufferSize << std::endl;
                ns3::Buffer bufferNrSlotAlloc = ns3::Buffer();
                bufferNrSlotAlloc.AddAtStart(nrSlotAllocBufferSize);
                ns3::Buffer::Iterator bufferNrSlotAllocIterator = bufferNrSlotAlloc.Begin();
                nrSlSlotAlloc.SerializeForE2(bufferNrSlotAllocIterator);
                std::cout << "6" << std::endl;
                uint32_t extraSizeNrSlotAlloc = 30;
                uint8_t *bufferNrSlotAllocBuffer = (uint8_t *) calloc (1, nrSlotAllocBufferSize+extraSizeNrSlotAlloc);
                auto serReturn = bufferNrSlotAlloc.Serialize(bufferNrSlotAllocBuffer, nrSlotAllocBufferSize+extraSizeNrSlotAlloc);
                std::cout << "Serialization return " << serReturn << std::endl;
                extraSizeNrSlotAlloc = bufferNrSlotAlloc.GetSerializedSize() - bufferNrSlotAlloc.GetSize();
                uint8_t *cleanBufferAlloc = (uint8_t *)calloc(1, nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                std::cout << "7 " << bufferNrSlotAlloc.GetSerializedSize() << " " << bufferNrSlotAlloc.GetSize() << std::endl;
                std::cout << "7 " << " extra size alloc " << extraSizeNrSlotAlloc << std::endl;
                for (int buffSize = 0; buffSize<nrSlotAllocBufferSize+extraSizeNrSlotAlloc; ++ buffSize){
                    std::cout << " " << (uint32_t)bufferNrSlotAllocBuffer[buffSize];
                }
                std::cout << " " << std::endl;
                memcpy(cleanBufferAlloc, bufferNrSlotAllocBuffer, nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                // copy directly to the buffer of buffer string
                std::cout << "7 " << nrSlotAllocBufferSize <<  "  " << extraSizeNrSlotAlloc << std::endl;
                Buffer_String_t * allocBufferString = (Buffer_String_t *) calloc (1, sizeof (Buffer_String_t));
                allocBufferString->size = nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4;
                allocBufferString->buf = (uint8_t *) calloc (1, nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                memcpy (allocBufferString->buf, bufferNrSlotAllocBuffer, nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4);
                schedulingItem->nrSlotAllocBuffer = *allocBufferString;
                std::cout << "8" << std::endl;
                for (int buffSize = 0; buffSize<nrSlotAllocBufferSize+extraSizeNrSlotAlloc+4; ++ buffSize){
                    std::cout << " " << (uint32_t)allocBufferString->buf[buffSize];
                }
                
                ASN_SEQUENCE_ADD(&v2XSingleUserScheduling->V2X_Scheduling_ItemList.list, schedulingItem);
                std::cout << "9" << std::endl;
            }
            
            ASN_SEQUENCE_ADD(&v2XSourceUserScheduling->V2X_Scheduling_DestinationList.list, v2XSingleUserScheduling);
        }
        
        
        // add this user the the list of all users
        ASN_SEQUENCE_ADD(&v2xSchedulingAllUsersList->list, v2XSourceUserScheduling);
        std::cout << "10" << std::endl;
    }

    // AllHandoversListPlmn_t* allHandoversListPlmn = (AllHandoversListPlmn_t *) calloc(1, sizeof(AllHandoversListPlmn_t));
    // AllHandoversList_t* allHandoversList = (AllHandoversList_t *) calloc(1, sizeof(AllHandoversList_t));
    // allHandoversListPlmn->allHandoversList = allHandoversList;
    // allHandoversListPlmn->plmn_id.buf = (uint8_t *) calloc (1, 3);
    // allHandoversListPlmn->plmn_id.size = 3;
    // memcpy (allHandoversListPlmn->plmn_id.buf, plmn.c_str (), 3);
    // rcControlMessage->present = E2SM_RC_ControlMessage_PR_handoverMessage_Format;
    // rcControlMessage->choice.handoverMessage_Format = allHandoversListPlmn;

    
    std::cout << "11" << std::endl;
    xer_fprint(stdout, &asn_DEF_V2X_Scheduling_All_UsersPlmn, v2XSchedulingAllUsersListPlmn);
    // the rc control message which shall be returned to the python object
    E2SM_RC_ControlMessage_t* rcControlMessage = (E2SM_RC_ControlMessage_t *) calloc(1, sizeof(E2SM_RC_ControlMessage_t));
    rcControlMessage->present = E2SM_RC_ControlMessage_PR_v2xSchedulingMessage_Format;
    rcControlMessage->choice.v2xSchedulingMessage_Format = v2XSchedulingAllUsersListPlmn;

    // afterwords we have to generate the data part

    sctp_buffer_t* data = (sctp_buffer_t *) calloc(1, sizeof(sctp_buffer_t));

    uint8_t *buf;
    std::cout << "12" << std::endl;
    // encoding the rcControl message created into the buffer object
    data->length = e2ap_asn1c_encode_control_message(rcControlMessage, &buf);

    std::cout << "13" << std::endl;

    std::cout << "Data length " << data->length << std::endl;

    data->buffer = (uint8_t *) calloc(1, data->length);
    memcpy(data->buffer, buf, std::min(data->length, MAX_SCTP_BUFFER));

    // freeing all the data before returning the struct
    free(v2XSchedulingAllUsersListPlmn);

}