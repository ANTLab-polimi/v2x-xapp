#ifndef CONTROL_MESSAGE_ENCODER_DECODER_HPP
#define CONTROL_MESSAGE_ENCODER_DECODER_HPP


#include <mdclog/mdclog.h>
#include <vector>

// extern "C" {
#include "handover_item.h"
#include "handover_list.h"
#include "all_handovers.h"
#include "all_handovers_plmn.h"
#include "cell_handovers_list.h"
#include "E2SM-RC-ControlMessage.h"
// }

#include "nr-sl-sci-f1a-header.h"
#include "nr-sl-mac-pdu-tag.h" 


#define MAX_SCTP_BUFFER     500000

#ifdef __cplusplus
extern "C" {
#endif

typedef struct sctp_buffer{
  int length;
  // uint8_t buffer[MAX_SCTP_BUFFER];
  uint8_t* buffer;
} sctp_buffer_t;

typedef struct e2ap_stcp_buffer{
    int msg_length;
    int bytes_consumed;
    uint8_t* msg_buffer;
  }e2ap_stcp_buffer_t;

typedef struct v2x_sci_header_buffer{

  // create the struct from a clas instance
  v2x_sci_header_buffer(ns3::NrSlSciF1aHeader sciF1Header)
        : m_totalSubChannels(sciF1Header.GetTotalSubChannels()),
          m_priority(sciF1Header.GetPriority()),
          m_indexStartSubChannel(sciF1Header.GetIndexStartSubChannel()),
          m_lengthSubChannel(sciF1Header.GetLengthSubChannel()),
          m_mcs(sciF1Header.GetMcs()),
          m_slResourceReservePeriod(sciF1Header.GetSlResourceReservePeriod()),
          m_slMaxNumPerReserve(sciF1Header.GetSlMaxNumPerReserve()),
          m_slSciStage2Format(sciF1Header.GetSciStage2Format()),
          m_indexStartSbChReTx1(sciF1Header.GetIndexStartSbChReTx1()),
          m_indexStartSbChReTx2(sciF1Header.GetIndexStartSbChReTx2()),
          m_gapReTx1(sciF1Header.GetGapReTx1()),
          m_gapReTx2(sciF1Header.GetGapReTx2())
        {
        }

  v2x_sci_header_buffer(){}

  // remaining data
  //Mandatory fields including the SCI fields
  uint16_t m_totalSubChannels {std::numeric_limits <uint16_t>::max ()}; //!< The total number of sub-channels
  //SCI fields
  uint8_t m_priority {std::numeric_limits <uint8_t>::max ()}; //!< The priority
  uint8_t m_indexStartSubChannel {std::numeric_limits <uint8_t>::max ()}; //!< The index of the starting sub-channel allocated
  uint8_t m_lengthSubChannel {std::numeric_limits <uint8_t>::max ()}; //!< The total number of the sub-channel allocated
  uint8_t m_mcs {std::numeric_limits <uint8_t>::max ()}; //!< The Modulation and Coding Scheme (MCS)
  uint16_t m_slResourceReservePeriod {std::numeric_limits <uint16_t>::max ()}; //!< Resource reservation period
  uint8_t m_slMaxNumPerReserve {std::numeric_limits <uint8_t>::max ()}; //!< maximum number of reserved resources
  uint8_t m_slSciStage2Format {std::numeric_limits <uint8_t>::max ()}; //!< maximum number of reserved resources
  //SCI fields end
  //Optional fields
  uint8_t m_indexStartSbChReTx1 {std::numeric_limits <uint8_t>::max ()}; //!< The index of the starting sub-channel allocated to first retransmission
  uint8_t m_indexStartSbChReTx2 {std::numeric_limits <uint8_t>::max ()}; //!< The index of the starting sub-channel allocated to second retransmission
  uint8_t m_gapReTx1 {std::numeric_limits <uint8_t>::max ()}; //!< The gap between a transmission and its first retransmission in slots
  uint8_t m_gapReTx2 {std::numeric_limits <uint8_t>::max ()}; //!< The gap between a transmission and its second retransmission in slots
}v2x_sci_header_buffer_t;

typedef struct v2x_sci_tag_buffer{

  // create the struct from a clas instance
  v2x_sci_tag_buffer(ns3::NrSlMacPduTag sciTag)
        : m_frameNum(sciTag.GetSfn().GetFrame ()),
          m_subframeNum(sciTag.GetSfn().GetSubframe ()),
          m_slotNum(sciTag.GetSfn().GetSlot ()),
          m_numerology(sciTag.GetSfn().GetNumerology ()),
          m_rnti(sciTag.GetRnti()),
          m_symStart(sciTag.GetSymStart()),
          m_numSym(sciTag.GetNumSym()),
          m_tbSize(sciTag.GetTbSize()),
          m_dstL2Id(sciTag.GetDstL2Id())
        {
        }

  v2x_sci_tag_buffer(){}
  // sfnsf
  uint16_t m_frameNum   { 0 };  //!< Frame Number
  uint8_t m_subframeNum { 0 };  //!< SubFrame Number
  uint16_t m_slotNum    { 0 };  //!< Slot number (a slot is made by 14 symbols)
  int16_t m_numerology  {-1 };  //!< Slot per subframe: 2^{numerology}
  // remaining data
  uint16_t m_rnti {0};       //!< RNTI
  uint8_t m_symStart {0};    //!< Symstart
  uint8_t m_numSym {0};      //!< Num sym
  uint32_t m_tbSize {0};     //!< The transport block size
  uint32_t m_dstL2Id {0};    //!< The destination layer 2 id

}v2x_sci_tag_buffer_t;

// scheduling 
typedef struct v2x_sl_rlc_pdu_info{

  v2x_sl_rlc_pdu_info (uint8_t lcid, uint32_t size) :
    lcid (lcid), size (size)
  {}
  v2x_sl_rlc_pdu_info(){}

  uint8_t lcid  {0}; //!< The Logical channel id
  uint32_t size {0}; //!< The transport block size

}v2x_sl_rlc_pdu_info_t;

// this shall be created in python and passed to the c++ function to be deconded afterwards
typedef struct v2x_nr_sl_slot_alloc{
// std::vector <v2x_sl_rlc_pdu_info_t> slRlcPduInfo,
  v2x_nr_sl_slot_alloc (uint16_t m_frameNum, uint8_t m_subframeNum, uint16_t m_slotNum, int16_t m_numerology, 
                    uint32_t dstL2Id, uint8_t ndi, uint8_t rv, uint8_t priority, 
                    uint32_t slRlcPduInfoSize, v2x_sl_rlc_pdu_info_t* slRlcPduInfo,
                    uint16_t mcs, uint16_t numSlPscchRbs, uint16_t slPscchSymStart, uint16_t slPscchSymLength, 
                    uint16_t slPsschSymStart, uint16_t slPsschSymLength, uint16_t slPsschSubChStart, 
                    uint16_t slPsschSubChLength, uint16_t maxNumPerReserve, uint8_t txSci1A, uint8_t slotNumInd) :
      m_frameNum (m_frameNum), 
      m_subframeNum (m_subframeNum), 
      m_slotNum (m_slotNum), 
      m_numerology (m_numerology), 
      dstL2Id (dstL2Id), 
      ndi (ndi), 
      rv (rv), 
      priority (priority), 
      slRlcPduInfoSize(slRlcPduInfoSize),
      slRlcPduInfo (slRlcPduInfo), 
      mcs (mcs), 
      numSlPscchRbs (numSlPscchRbs), 
      slPscchSymStart (slPscchSymStart), 
      slPscchSymLength (slPscchSymLength), 
      slPsschSymStart (slPsschSymStart), 
      slPsschSymLength (slPsschSymLength), 
      slPsschSubChStart (slPsschSubChStart), 
      slPsschSubChLength (slPsschSubChLength), 
      maxNumPerReserve (maxNumPerReserve), 
      txSci1A (txSci1A), 
      slotNumInd (slotNumInd) 
  {}
  v2x_nr_sl_slot_alloc(){}

// uint16_t m_frameNum, (m_frameNum), 
// uint8_t m_subframeNum, (m_subframeNum), 
// uint16_t m_slotNum, (m_slotNum), 
// int16_t m_numerology, (m_numerology), 
// uint32_t dstL2Id, (dstL2Id), 
// uint8_t ndi, (ndi), 
// uint8_t rv, (rv), 
// uint8_t priority, (priority), 
// std::vector <v2x_sl_rlc_pdu_info_t> slRlcPduInfo (slRlcPduInfo), 
// uint16_t mcs (mcs), 
// uint16_t numSlPscchRbs (numSlPscchRbs), 
// uint16_t slPscchSymStart (slPscchSymStart), 
// uint16_t slPscchSymLength (slPscchSymLength), 
// uint16_t slPsschSymStart (slPsschSymStart), 
// uint16_t slPsschSymLength (slPsschSymLength), 
// uint16_t slPsschSubChStart (slPsschSubChStart), 
// uint16_t slPsschSubChLength (slPsschSubChLength), 
// uint16_t maxNumPerReserve (maxNumPerReserve), 
// uint8_t txSci1A (txSci1A), 
// uint8_t slotNumInd (slotNumInd), 


  // sfnsf
  uint16_t m_frameNum   { 0 };  //!< Frame Number
  uint8_t m_subframeNum { 0 };  //!< SubFrame Number
  uint16_t m_slotNum    { 0 };  //!< Slot number (a slot is made by 14 symbols)
  int16_t m_numerology  {-1 };  //!< Slot per subframe: 2^{numerology}

  uint32_t dstL2Id {std::numeric_limits <uint32_t>::max ()}; //!< The destination Layer 2 Id
  uint8_t ndi {std::numeric_limits <uint8_t>::max ()}; //!< The flag to indicate the new data allocation
  uint8_t rv {std::numeric_limits <uint8_t>::max ()}; //!< The redundancy version
  uint8_t priority {std::numeric_limits <uint8_t>::max ()}; //!< The LC priority
  // std::vector <v2x_sl_rlc_pdu_info_t> slRlcPduInfo; //!< The vector containing the transport block size per LC id
  uint32_t slRlcPduInfoSize {0};
  v2x_sl_rlc_pdu_info_t* slRlcPduInfo; //!< The vector containing the transport block size per LC id
  uint16_t mcs {std::numeric_limits <uint16_t>::max ()}; //!< The MCS
  //PSCCH
  uint16_t numSlPscchRbs {std::numeric_limits <uint16_t>::max ()}; //!< Indicates the number of PRBs for PSCCH in a resource pool where it is not greater than the number PRBs of the subchannel.
  uint16_t slPscchSymStart {std::numeric_limits <uint16_t>::max ()}; //!< Indicates the starting symbol used for sidelink PSCCH in a slot
  uint16_t slPscchSymLength {std::numeric_limits <uint16_t>::max ()}; //!< Indicates the total number of symbols available for sidelink PSCCH
  //PSSCH
  uint16_t slPsschSymStart {std::numeric_limits <uint16_t>::max ()}; //!< Indicates the starting symbol used for sidelink PSSCH in a slot
  uint16_t slPsschSymLength {std::numeric_limits <uint16_t>::max ()}; //!< Indicates the total number of symbols allocated for sidelink PSSCH
  uint16_t slPsschSubChStart {std::numeric_limits <uint16_t>::max ()}; //!< Index of the first subchannel allocated for data
  uint16_t slPsschSubChLength {std::numeric_limits <uint16_t>::max ()}; //!< Indicates the total number of subchannel allocated for data

  uint16_t maxNumPerReserve {std::numeric_limits <uint16_t>::max ()}; //!< The maximum number of reserved PSCCH/PSSCH resources that can be indicated by an SCI.
  uint8_t txSci1A {false}; //!< Flag to indicate if the slots must carry SCI 1-A
  uint8_t slotNumInd {0}; //!< The number of future TXs an SCI 1-A can indicate

}v2x_nr_sl_slot_alloc_t;

typedef struct v2x_user_nr_sl_slot_alloc{

  uint16_t ue_id{0};
  // std::vector <v2x_nr_sl_slot_alloc> userAllocation;
  // v2x_user_nr_sl_slot_alloc (uint16_t ue_id, std::vector <v2x_nr_sl_slot_alloc> userAllocation) :\std::vector <v2x_nr_sl_slot_alloc> userAllocation;
  uint32_t userAllocationSize {0};
  v2x_nr_sl_slot_alloc* userAllocation;
  v2x_user_nr_sl_slot_alloc (uint16_t ue_id, uint32_t userAllocationSize, v2x_nr_sl_slot_alloc* userAllocation) :
    ue_id (ue_id), userAllocationSize(userAllocationSize), userAllocation (userAllocation)
  {}
  v2x_user_nr_sl_slot_alloc(){}
}v2x_user_nr_sl_slot_alloc_t;

int e2ap_asn1c_encode_handover_item(CellHandoverItem_t* pdu, unsigned char **buffer);

int e2ap_asn1c_encode_all_handovers_item_list(CellHandoverItemList_t* pdu, unsigned char **buffer);

int e2ap_asn1c_encode_all_handovers(AllHandoversList_t* pdu, unsigned char **buffer);

int e2ap_asn1c_encode_control_message(E2SM_RC_ControlMessage_t* pdu, unsigned char **buffer);

extern struct asn_dec_rval_s e2ap_asn1c_decode_handover_item(CellHandoverItem_t *pdu, enum asn_transfer_syntax syntax, unsigned char *buffer, int len);

extern sctp_buffer_t* gnerate_e2ap_encode_handover_control_message(uint16_t* ue_id, uint16_t* start_position, uint16_t* optimized, size_t size);

extern sctp_buffer_t* generate_e2ap_encode_handover_control_message_plmn(uint16_t* ue_id, uint16_t* start_position, uint16_t* optimized, size_t size, char* plmnId);

extern sctp_buffer_t* generate_e2ap_scheduling_control_message_plmn(v2x_user_nr_sl_slot_alloc_t* user_alloc, size_t size, char* plmnId);

extern e2ap_stcp_buffer_t* decode_e2ap_to_xml(uint8_t* buffer, size_t buffSize);

extern v2x_sci_header_buffer_t* decode_v2x_sci_header(uint8_t* buffer, size_t buffSize);

extern v2x_sci_tag_buffer_t* decode_v2x_sci_tag(uint8_t* buffer, size_t buffSize);

char* converHexToByte(std::string hexString);

  
#ifdef __cplusplus
}
#endif

#endif