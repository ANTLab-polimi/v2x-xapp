
#ifndef NR_SL_PHY_MAC_COMMON_H
#define NR_SL_PHY_MAC_COMMON_H

#include "sfnsf.h"
#include "buffer.h"

#include <stdint.h>
#include <limits>
#include <vector>
#include <set>

namespace ns3 {

/**
 * \ingroup utils
 * \brief The SlRlcPduInfo struct
 *
 * \see NrSlSlotAlloc
 */
struct SlRlcPduInfo
{
  /**
   * \brief SlRlcPduInfo constructor
   * \param lcid The Logical channel id
   * \param size The transport block size
   */
  SlRlcPduInfo (uint8_t lcid, uint32_t size) :
    lcid (lcid), size (size)
  {}
  uint8_t lcid  {0}; //!< The Logical channel id
  uint32_t size {0}; //!< The transport block size
};
/**
 * \ingroup utils
 * \brief A struct used by the NR SL UE MAC scheduler to communicate slot
 *        allocation to UE MAC.
 */
struct NrSlSlotAlloc
{
  SfnSf sfn {}; //!< The SfnSf
  uint32_t dstL2Id {std::numeric_limits <uint32_t>::max ()}; //!< The destination Layer 2 Id

  uint8_t ndi {std::numeric_limits <uint8_t>::max ()}; //!< The flag to indicate the new data allocation
  uint8_t rv {std::numeric_limits <uint8_t>::max ()}; //!< The redundancy version
  uint8_t priority {std::numeric_limits <uint8_t>::max ()}; //!< The LC priority
  std::vector <SlRlcPduInfo> slRlcPduInfo; //!< The vector containing the transport block size per LC id
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
  bool txSci1A {false}; //!< Flag to indicate if the slots must carry SCI 1-A
  uint8_t slotNumInd {0}; //!< The number of future TXs an SCI 1-A can indicate

  /**
   * \ingroup utils
   * \brief Less than operator overloaded for NrSlSlotAlloc
   * \param rhs other NrSlSlotAlloc to compare
   * \return true if this NrSlSlotAlloc SfnSf parameter values are less than the rhs NrSlSlotAlloc SfnSf parameters
   *
   * The comparison is done on sfnSf
   */
  bool operator < (const NrSlSlotAlloc& rhs) const;

  // modified
  void SerializeForE2 (Buffer::Iterator i) const;

  uint32_t DeserializeForE2 (Buffer::Iterator i);

  uint32_t GetSerializedSizeForE2 (void) const;

  NrSlSlotAlloc (uint16_t m_frameNum, uint8_t m_subframeNum, uint16_t m_slotNum, int16_t m_numerology, 
                    uint32_t dstL2Id, uint8_t ndi, uint8_t rv, uint8_t priority, 
                    std::vector <SlRlcPduInfo> slRlcPduInfo,
                    uint16_t mcs, uint16_t numSlPscchRbs, uint16_t slPscchSymStart, uint16_t slPscchSymLength, 
                    uint16_t slPsschSymStart, uint16_t slPsschSymLength, uint16_t slPsschSubChStart, 
                    uint16_t slPsschSubChLength, uint16_t maxNumPerReserve, uint8_t txSci1A, uint8_t slotNumInd);
  // end modification
};
}

#endif /* NR_SL_PHY_MAC_COMMON_H_ */