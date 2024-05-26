/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
*   Copyright (c) 2020 Centre Tecnologic de Telecomunicacions de Catalunya (CTTC)
*
*   This program is free software; you can redistribute it and/or modify
*   it under the terms of the GNU General Public License version 2 as
*   published by the Free Software Foundation;
*
*   This program is distributed in the hope that it will be useful,
*   but WITHOUT ANY WARRANTY; without even the implied warranty of
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*   GNU General Public License for more details.
*
*   You should have received a copy of the GNU General Public License
*   along with this program; if not, write to the Free Software
*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*
*/


#include "nr-sl-phy-mac-common.h"

namespace ns3 {

bool
NrSlSlotAlloc::operator < (const NrSlSlotAlloc &rhs) const
{
  return (sfn < rhs.sfn);
}

// modified
void 
NrSlSlotAlloc::SerializeForE2 (Buffer::Iterator i) const
{
  // Buffer::Iterator i = start;
  // NS_LOG_FUNCTION(this);
  // NS_LOG_DEBUG("Writing");
  // the vector
  // first encode the number of elements in the vector
  i.WriteU32 ((uint32_t) slRlcPduInfo.size());
  for (auto &vecElem: slRlcPduInfo){
    i.WriteU8 (vecElem.lcid);
    i.WriteU32 (vecElem.size);
  }

  i.WriteU64 (SfnSf::Encode(sfn));
  // NS_LOG_DEBUG("Writing");
  i.WriteU32 (dstL2Id);
  i.WriteU8 (ndi);
  i.WriteU8 (rv);
  i.WriteU8 (priority);
  i.WriteU16 (mcs);
  //PSCCH
  i.WriteU16 (numSlPscchRbs);
  i.WriteU16 (slPscchSymStart);
  i.WriteU16 (slPscchSymLength);
  //PSSCH
  i.WriteU16 (slPsschSymStart);
  i.WriteU16 (slPsschSymLength);
  i.WriteU16 (slPsschSubChStart);
  i.WriteU16 (slPsschSubChLength);

  i.WriteU16 (maxNumPerReserve);
  i.WriteU8 ((uint8_t) txSci1A);
  i.WriteU8 (slotNumInd);

}

uint32_t 
NrSlSlotAlloc::DeserializeForE2 (Buffer::Iterator i)
{
  // Buffer::Iterator i = start;

  slRlcPduInfo.clear();
  uint32_t vecSize =  i.ReadU32 ();
  for (uint32_t _ind = 0; _ind< vecSize; _ind++){
    uint8_t lcid = i.ReadU8 ();
    uint32_t size = i.ReadU32 ();
    slRlcPduInfo.push_back(SlRlcPduInfo(lcid, size));
  }

  sfn = SfnSf::Decode(i.ReadU64 ());
  // NS_LOG_DEBUG("Writing");
  dstL2Id = i.ReadU32 ();
  ndi = i.ReadU8 ();
  rv = i.ReadU8 ();
  priority = i.ReadU8 ();
  mcs = i.ReadU16 ();
  //PSCCH
  numSlPscchRbs = i.ReadU16 ();
  slPscchSymStart = i.ReadU16 ();
  slPscchSymLength = i.ReadU16 ();
  //PSSCH
  slPsschSymStart = i.ReadU16 ();
  slPsschSymLength = i.ReadU16 ();
  slPsschSubChStart = i.ReadU16 ();
  slPsschSubChLength = i.ReadU16 ();

  maxNumPerReserve = i.ReadU16 ();
  txSci1A = (bool)i.ReadU8 ();
  slotNumInd = i.ReadU8 ();
    

  return GetSerializedSizeForE2 ();
}

uint32_t
NrSlSlotAlloc::GetSerializedSizeForE2 (void) const
{
  uint32_t totalSize = 4 + 5*slRlcPduInfo.size() + 
                    8 + 4 + 1 + 1 +1 + 2 +
                    2 + 2 + 2 +
                    2 + 2 + 2 + 2 +
                    2 + 1 + 1;
  return totalSize;
}

NrSlSlotAlloc::NrSlSlotAlloc (uint16_t m_frameNum, uint8_t m_subframeNum, uint16_t m_slotNum, int16_t m_numerology, 
                    uint32_t dstL2Id, uint8_t ndi, uint8_t rv, uint8_t priority, 
                    std::vector <SlRlcPduInfo> slRlcPduInfo,
                    uint16_t mcs, uint16_t numSlPscchRbs, uint16_t slPscchSymStart, uint16_t slPscchSymLength, 
                    uint16_t slPsschSymStart, uint16_t slPsschSymLength, uint16_t slPsschSubChStart, 
                    uint16_t slPsschSubChLength, uint16_t maxNumPerReserve, uint8_t txSci1A, uint8_t slotNumInd):
      sfn(SfnSf(m_frameNum, m_subframeNum, m_slotNum, m_numerology)),
      dstL2Id (dstL2Id), 
      ndi (ndi), 
      rv (rv), 
      priority (priority), 
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
      slotNumInd (slotNumInd){

      }

NrSlSlotAllocProto
NrSlSlotAlloc::GenerateProtoBuff (void) const
{
  NrSlSlotAllocProto allocProto = NrSlSlotAllocProto();
  
  SfnSfProto sfnProto = SfnSfProto();
  sfnProto.set_m_framenum(sfn.GetFrame());
  sfnProto.set_m_subframenum(sfn.GetSubframe());
  sfnProto.set_m_slotnum(sfn.GetSlot());
  sfnProto.set_m_numerology(sfn.GetNumerology());
  allocProto.set_allocated_sfn(&sfnProto);

  allocProto.set_dstl2id(dstL2Id);
  allocProto.set_ndi(ndi);
  allocProto.set_rv(rv);
  allocProto.set_priority(priority);

  for (uint32_t i = 0; i<slRlcPduInfo.size(); ++i){
    SlRlcPduInfoProto* slRlcProto = allocProto.add_slrlcpduinfo();
    slRlcProto->set_lcid(slRlcPduInfo[i].lcid);
    slRlcProto->set_size(slRlcPduInfo[i].size);
  }

  allocProto.set_mcs(mcs);
  allocProto.set_numslpscchrbs(numSlPscchRbs);
  allocProto.set_slpscchsymstart(slPscchSymStart);
  allocProto.set_slpscchsymlength(slPscchSymLength);
  allocProto.set_slpsschsymstart(slPsschSymStart);
  allocProto.set_slpsschsymlength(slPsschSymLength);
  allocProto.set_slpsschsubchstart(slPsschSubChStart);
  allocProto.set_slpsschsubchlength(slPsschSubChLength);
  allocProto.set_maxnumperreserve(maxNumPerReserve);
  allocProto.set_txsci1a(txSci1A);
  allocProto.set_slotnumind(slotNumInd);
  return allocProto;
}

void
NrSlSlotAlloc::DeserializeFromProtoBuff (NrSlSlotAllocProto protoBuf)
{   
  SfnSfProto sfnProto = protoBuf.sfn();
  // sfn.m_frameNum = (uint16_t)sfnProto.m_framenum();
  // sfn.m_subframeNum = (uint8_t)sfnProto.m_subframenum();
  // sfn.m_slotNum = (uint16_t)sfnProto.m_slotnum();
  // sfn.m_numerology = (int16_t)sfnProto.m_numerology();
  sfn = SfnSf((uint16_t)sfnProto.m_framenum(),
        (uint8_t)sfnProto.m_subframenum(),
        (uint16_t)sfnProto.m_slotnum(),
        (int16_t)sfnProto.m_numerology());

  dstL2Id = protoBuf.dstl2id();
  ndi = protoBuf.ndi();
  rv = protoBuf.rv();
  priority = protoBuf.priority();

  for (int i = 0; i < protoBuf.slrlcpduinfo_size(); ++i){
    slRlcPduInfo.push_back(SlRlcPduInfo(protoBuf.slrlcpduinfo(i)));
  }
  
  mcs = protoBuf.mcs();
  numSlPscchRbs = protoBuf.numslpscchrbs();
  slPscchSymStart = protoBuf.slpscchsymstart();
  slPscchSymLength = protoBuf.slpscchsymlength();
  slPsschSymStart = protoBuf.slpsschsymstart();
  slPsschSymLength = protoBuf.slpsschsymlength();
  slPsschSubChStart = protoBuf.slpsschsubchstart();
  slPsschSubChLength = protoBuf.slpsschsubchlength();
  maxNumPerReserve = protoBuf.maxnumperreserve();
  txSci1A = protoBuf.txsci1a();
  slotNumInd = protoBuf.slotnumind();
}

// end modification
}
