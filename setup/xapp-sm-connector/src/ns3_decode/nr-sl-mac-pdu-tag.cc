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


#include "nr-sl-mac-pdu-tag.h"
#include "tag.h"

namespace ns3 {


NrSlMacPduTag::NrSlMacPduTag (uint16_t rnti, SfnSf sfn, uint8_t symStart, uint8_t numSym, uint32_t tbSize, uint32_t dstL2Id)
  :  m_rnti (rnti), m_sfnSf (sfn), m_symStart (symStart), m_numSym (numSym), m_tbSize (tbSize), m_dstL2Id (dstL2Id)
{
}

uint32_t
NrSlMacPduTag::GetSerializedSize (void) const
{ 
  return 2 + 8 + 1 + 1 + 4 + 4;
}

void
NrSlMacPduTag::Serialize (TagBuffer i) const
{
  i.WriteU16 (m_rnti);
  i.WriteU64 (m_sfnSf.GetEncoding ());
  i.WriteU8 (m_symStart);
  i.WriteU8 (m_numSym);
  i.WriteU32 (m_tbSize);
  i.WriteU32 (m_dstL2Id);
}

void
NrSlMacPduTag::Deserialize (TagBuffer i)
{
  m_rnti = i.ReadU16 ();
  uint64_t v = i.ReadU64 ();
  m_sfnSf.FromEncoding (v);

  m_symStart = (uint8_t)i.ReadU8 ();
  m_numSym = (uint8_t)i.ReadU8 ();
  m_tbSize = i.ReadU32 ();
  m_dstL2Id = i.ReadU32 ();
}

// modified
void
NrSlMacPduTag::SerializeForE2 (Buffer::Iterator i) const
{

  i.WriteU16 (m_rnti);
  i.WriteU64 (m_sfnSf.GetEncoding ());
  i.WriteU8 (m_symStart);
  i.WriteU8 (m_numSym);
  i.WriteU32 (m_tbSize);
  i.WriteU32 (m_dstL2Id);
}

uint32_t
NrSlMacPduTag::DeserializeForE2 (Buffer::Iterator i)
{

  m_rnti = i.ReadU16 ();
  uint64_t v = i.ReadU64 ();
  m_sfnSf.FromEncoding (v);

  m_symStart = (uint8_t)i.ReadU8 ();
  m_numSym = (uint8_t)i.ReadU8 ();
  m_tbSize = i.ReadU32 ();
  m_dstL2Id = i.ReadU32 ();
    

  return GetSerializedSizeForE2 ();
}


uint32_t
NrSlMacPduTag::GetSerializedSizeForE2 (void) const
{
  return GetSerializedSize();
}
// end modification

void
NrSlMacPduTag::Print (std::ostream &os) const
{
  os << "RNTI " << m_rnti
     << ", Destination id " << m_dstL2Id
     << ", Frame " << m_sfnSf.GetFrame ()
     << ", Subframe " << +m_sfnSf.GetSubframe ()
     << ", Slot " << m_sfnSf.GetSlot ()
     << ", PSCCH symbol start " << +m_symStart
     << ", Total number of symbols " << +m_numSym
     << ", TB size " << m_tbSize << " bytes";
}

uint16_t
NrSlMacPduTag::GetRnti () const
{
  return m_rnti;
}

void
NrSlMacPduTag::SetRnti (uint16_t rnti)
{
  m_rnti = rnti;
}

SfnSf
NrSlMacPduTag::GetSfn () const
{
  return m_sfnSf;
}

void
NrSlMacPduTag::SetSfn (SfnSf sfn)
{
  m_sfnSf = sfn;
}


uint8_t
NrSlMacPduTag::GetSymStart () const
{
  return m_symStart;
}


uint8_t
NrSlMacPduTag::GetNumSym () const
{
  return m_numSym;
}


void
NrSlMacPduTag::SetSymStart (uint8_t symStart)
{
  m_symStart = symStart;
}


void
NrSlMacPduTag::SetNumSym (uint8_t numSym)
{
  m_numSym = numSym;
}


uint32_t
NrSlMacPduTag::GetTbSize () const
{
  return m_tbSize;
}

void
NrSlMacPduTag::SetTbSize (uint32_t tbSize)
{
  m_tbSize = tbSize;
}

uint32_t
NrSlMacPduTag::GetDstL2Id () const
{
  return m_dstL2Id;
}

void
NrSlMacPduTag::SetDstL2Id (uint32_t dstL2Id)
{
  m_dstL2Id = dstL2Id;
}

bool
NrSlMacPduTag::operator == (const NrSlMacPduTag &b) const
{
  if (m_rnti == b.m_rnti
      && m_sfnSf == b.m_sfnSf
      && m_symStart == b.m_symStart
      && m_numSym == b.m_numSym
      && m_tbSize == b.m_tbSize
      && m_dstL2Id == b.m_dstL2Id
      )
    {
      return true;
    }

  return false;
}

NrSlMacPduTagProto
NrSlMacPduTag::GenerateProtoBuff (void) const
{
  NS_LOG_FUNCTION(this);
  NrSlMacPduTagProto tagProto = NrSlMacPduTagProto();
  tagProto.set_m_rnti(m_rnti);
  
  SfnSfProto sfnProto = SfnSfProto();
  sfnProto.set_m_framenum(m_sfnSf.GetFrame());
  sfnProto.set_m_subframenum(m_sfnSf.GetSubframe());
  sfnProto.set_m_slotnum(m_sfnSf.GetSlot());
  sfnProto.set_m_numerology(m_sfnSf.GetNumerology());

  tagProto.set_allocated_m_sfnsf(&sfnProto);
  tagProto.set_m_symstart(m_symStart);
  tagProto.set_m_numsym(m_numSym);
  tagProto.set_m_tbsize(m_tbSize);
  tagProto.set_m_dstl2id(m_dstL2Id);
}

void
NrSlMacPduTag::DeserializeFromProtoBuff (NrSlMacPduTagProto protoBuf)
{
  m_rnti = (uint16_t)protoBuf.m_rnti();
  SfnSfProto sfnProto = protoBuf.m_sfnsf();
  m_sfnSf = SfnSf((uint16_t)sfnProto.m_framenum(),
        (uint8_t)sfnProto.m_subframenum(),
        (uint16_t)sfnProto.m_slotnum(),
        (int16_t)sfnProto.m_numerology());
  m_symStart = (uint8_t)protoBuf.m_symstart();
  m_numSym = (uint8_t)protoBuf.m_numsym();
  m_tbSize = (uint32_t)protoBuf.m_tbsize();
  m_dstL2Id = (uint32_t)protoBuf.m_dstl2id();
}

} // namespace ns3

