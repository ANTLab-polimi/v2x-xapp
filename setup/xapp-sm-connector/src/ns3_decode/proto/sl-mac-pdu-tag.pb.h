// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: proto/sl-mac-pdu-tag.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_proto_2fsl_2dmac_2dpdu_2dtag_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_proto_2fsl_2dmac_2dpdu_2dtag_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3012000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3012004 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_table_driven.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/inlined_string_field.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "proto/sl-sfnsf.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_proto_2fsl_2dmac_2dpdu_2dtag_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_proto_2fsl_2dmac_2dpdu_2dtag_2eproto {
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTableField entries[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::AuxillaryParseTableField aux[]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::ParseTable schema[1]
    PROTOBUF_SECTION_VARIABLE(protodesc_cold);
  static const ::PROTOBUF_NAMESPACE_ID::internal::FieldMetadata field_metadata[];
  static const ::PROTOBUF_NAMESPACE_ID::internal::SerializationTable serialization_table[];
  static const ::PROTOBUF_NAMESPACE_ID::uint32 offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto;
namespace ns3 {
class NrSlMacPduTagProto;
class NrSlMacPduTagProtoDefaultTypeInternal;
extern NrSlMacPduTagProtoDefaultTypeInternal _NrSlMacPduTagProto_default_instance_;
}  // namespace ns3
PROTOBUF_NAMESPACE_OPEN
template<> ::ns3::NrSlMacPduTagProto* Arena::CreateMaybeMessage<::ns3::NrSlMacPduTagProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace ns3 {

// ===================================================================

class NrSlMacPduTagProto PROTOBUF_FINAL :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:ns3.NrSlMacPduTagProto) */ {
 public:
  inline NrSlMacPduTagProto() : NrSlMacPduTagProto(nullptr) {};
  virtual ~NrSlMacPduTagProto();

  NrSlMacPduTagProto(const NrSlMacPduTagProto& from);
  NrSlMacPduTagProto(NrSlMacPduTagProto&& from) noexcept
    : NrSlMacPduTagProto() {
    *this = ::std::move(from);
  }

  inline NrSlMacPduTagProto& operator=(const NrSlMacPduTagProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline NrSlMacPduTagProto& operator=(NrSlMacPduTagProto&& from) noexcept {
    if (GetArena() == from.GetArena()) {
      if (this != &from) InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return GetMetadataStatic().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return GetMetadataStatic().reflection;
  }
  static const NrSlMacPduTagProto& default_instance();

  static void InitAsDefaultInstance();  // FOR INTERNAL USE ONLY
  static inline const NrSlMacPduTagProto* internal_default_instance() {
    return reinterpret_cast<const NrSlMacPduTagProto*>(
               &_NrSlMacPduTagProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(NrSlMacPduTagProto& a, NrSlMacPduTagProto& b) {
    a.Swap(&b);
  }
  inline void Swap(NrSlMacPduTagProto* other) {
    if (other == this) return;
    if (GetArena() == other->GetArena()) {
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(NrSlMacPduTagProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetArena() == other->GetArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  inline NrSlMacPduTagProto* New() const final {
    return CreateMaybeMessage<NrSlMacPduTagProto>(nullptr);
  }

  NrSlMacPduTagProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena) const final {
    return CreateMaybeMessage<NrSlMacPduTagProto>(arena);
  }
  void CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) final;
  void CopyFrom(const NrSlMacPduTagProto& from);
  void MergeFrom(const NrSlMacPduTagProto& from);
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  ::PROTOBUF_NAMESPACE_ID::uint8* _InternalSerialize(
      ::PROTOBUF_NAMESPACE_ID::uint8* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _cached_size_.Get(); }

  private:
  inline void SharedCtor();
  inline void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(NrSlMacPduTagProto* other);
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "ns3.NrSlMacPduTagProto";
  }
  protected:
  explicit NrSlMacPduTagProto(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  private:
  static void ArenaDtor(void* object);
  inline void RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena* arena);
  public:

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;
  private:
  static ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadataStatic() {
    ::PROTOBUF_NAMESPACE_ID::internal::AssignDescriptors(&::descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto);
    return ::descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto.file_level_metadata[kIndexInFileMessages];
  }

  public:

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kMSfnSfFieldNumber = 6,
    kMRntiFieldNumber = 1,
    kMSymStartFieldNumber = 2,
    kMNumSymFieldNumber = 3,
    kMTbSizeFieldNumber = 4,
    kMDstL2IdFieldNumber = 5,
  };
  // .ns3.SfnSfProto m_sfnSf = 6;
  bool has_m_sfnsf() const;
  private:
  bool _internal_has_m_sfnsf() const;
  public:
  void clear_m_sfnsf();
  const ::ns3::SfnSfProto& m_sfnsf() const;
  ::ns3::SfnSfProto* release_m_sfnsf();
  ::ns3::SfnSfProto* mutable_m_sfnsf();
  void set_allocated_m_sfnsf(::ns3::SfnSfProto* m_sfnsf);
  private:
  const ::ns3::SfnSfProto& _internal_m_sfnsf() const;
  ::ns3::SfnSfProto* _internal_mutable_m_sfnsf();
  public:
  void unsafe_arena_set_allocated_m_sfnsf(
      ::ns3::SfnSfProto* m_sfnsf);
  ::ns3::SfnSfProto* unsafe_arena_release_m_sfnsf();

  // uint32 m_rnti = 1;
  void clear_m_rnti();
  ::PROTOBUF_NAMESPACE_ID::uint32 m_rnti() const;
  void set_m_rnti(::PROTOBUF_NAMESPACE_ID::uint32 value);
  private:
  ::PROTOBUF_NAMESPACE_ID::uint32 _internal_m_rnti() const;
  void _internal_set_m_rnti(::PROTOBUF_NAMESPACE_ID::uint32 value);
  public:

  // uint32 m_symStart = 2;
  void clear_m_symstart();
  ::PROTOBUF_NAMESPACE_ID::uint32 m_symstart() const;
  void set_m_symstart(::PROTOBUF_NAMESPACE_ID::uint32 value);
  private:
  ::PROTOBUF_NAMESPACE_ID::uint32 _internal_m_symstart() const;
  void _internal_set_m_symstart(::PROTOBUF_NAMESPACE_ID::uint32 value);
  public:

  // uint32 m_numSym = 3;
  void clear_m_numsym();
  ::PROTOBUF_NAMESPACE_ID::uint32 m_numsym() const;
  void set_m_numsym(::PROTOBUF_NAMESPACE_ID::uint32 value);
  private:
  ::PROTOBUF_NAMESPACE_ID::uint32 _internal_m_numsym() const;
  void _internal_set_m_numsym(::PROTOBUF_NAMESPACE_ID::uint32 value);
  public:

  // uint32 m_tbSize = 4;
  void clear_m_tbsize();
  ::PROTOBUF_NAMESPACE_ID::uint32 m_tbsize() const;
  void set_m_tbsize(::PROTOBUF_NAMESPACE_ID::uint32 value);
  private:
  ::PROTOBUF_NAMESPACE_ID::uint32 _internal_m_tbsize() const;
  void _internal_set_m_tbsize(::PROTOBUF_NAMESPACE_ID::uint32 value);
  public:

  // uint32 m_dstL2Id = 5;
  void clear_m_dstl2id();
  ::PROTOBUF_NAMESPACE_ID::uint32 m_dstl2id() const;
  void set_m_dstl2id(::PROTOBUF_NAMESPACE_ID::uint32 value);
  private:
  ::PROTOBUF_NAMESPACE_ID::uint32 _internal_m_dstl2id() const;
  void _internal_set_m_dstl2id(::PROTOBUF_NAMESPACE_ID::uint32 value);
  public:

  // @@protoc_insertion_point(class_scope:ns3.NrSlMacPduTagProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  ::ns3::SfnSfProto* m_sfnsf_;
  ::PROTOBUF_NAMESPACE_ID::uint32 m_rnti_;
  ::PROTOBUF_NAMESPACE_ID::uint32 m_symstart_;
  ::PROTOBUF_NAMESPACE_ID::uint32 m_numsym_;
  ::PROTOBUF_NAMESPACE_ID::uint32 m_tbsize_;
  ::PROTOBUF_NAMESPACE_ID::uint32 m_dstl2id_;
  mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  friend struct ::TableStruct_proto_2fsl_2dmac_2dpdu_2dtag_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// NrSlMacPduTagProto

// uint32 m_rnti = 1;
inline void NrSlMacPduTagProto::clear_m_rnti() {
  m_rnti_ = 0u;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::_internal_m_rnti() const {
  return m_rnti_;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::m_rnti() const {
  // @@protoc_insertion_point(field_get:ns3.NrSlMacPduTagProto.m_rnti)
  return _internal_m_rnti();
}
inline void NrSlMacPduTagProto::_internal_set_m_rnti(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  
  m_rnti_ = value;
}
inline void NrSlMacPduTagProto::set_m_rnti(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  _internal_set_m_rnti(value);
  // @@protoc_insertion_point(field_set:ns3.NrSlMacPduTagProto.m_rnti)
}

// uint32 m_symStart = 2;
inline void NrSlMacPduTagProto::clear_m_symstart() {
  m_symstart_ = 0u;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::_internal_m_symstart() const {
  return m_symstart_;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::m_symstart() const {
  // @@protoc_insertion_point(field_get:ns3.NrSlMacPduTagProto.m_symStart)
  return _internal_m_symstart();
}
inline void NrSlMacPduTagProto::_internal_set_m_symstart(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  
  m_symstart_ = value;
}
inline void NrSlMacPduTagProto::set_m_symstart(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  _internal_set_m_symstart(value);
  // @@protoc_insertion_point(field_set:ns3.NrSlMacPduTagProto.m_symStart)
}

// uint32 m_numSym = 3;
inline void NrSlMacPduTagProto::clear_m_numsym() {
  m_numsym_ = 0u;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::_internal_m_numsym() const {
  return m_numsym_;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::m_numsym() const {
  // @@protoc_insertion_point(field_get:ns3.NrSlMacPduTagProto.m_numSym)
  return _internal_m_numsym();
}
inline void NrSlMacPduTagProto::_internal_set_m_numsym(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  
  m_numsym_ = value;
}
inline void NrSlMacPduTagProto::set_m_numsym(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  _internal_set_m_numsym(value);
  // @@protoc_insertion_point(field_set:ns3.NrSlMacPduTagProto.m_numSym)
}

// uint32 m_tbSize = 4;
inline void NrSlMacPduTagProto::clear_m_tbsize() {
  m_tbsize_ = 0u;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::_internal_m_tbsize() const {
  return m_tbsize_;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::m_tbsize() const {
  // @@protoc_insertion_point(field_get:ns3.NrSlMacPduTagProto.m_tbSize)
  return _internal_m_tbsize();
}
inline void NrSlMacPduTagProto::_internal_set_m_tbsize(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  
  m_tbsize_ = value;
}
inline void NrSlMacPduTagProto::set_m_tbsize(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  _internal_set_m_tbsize(value);
  // @@protoc_insertion_point(field_set:ns3.NrSlMacPduTagProto.m_tbSize)
}

// uint32 m_dstL2Id = 5;
inline void NrSlMacPduTagProto::clear_m_dstl2id() {
  m_dstl2id_ = 0u;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::_internal_m_dstl2id() const {
  return m_dstl2id_;
}
inline ::PROTOBUF_NAMESPACE_ID::uint32 NrSlMacPduTagProto::m_dstl2id() const {
  // @@protoc_insertion_point(field_get:ns3.NrSlMacPduTagProto.m_dstL2Id)
  return _internal_m_dstl2id();
}
inline void NrSlMacPduTagProto::_internal_set_m_dstl2id(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  
  m_dstl2id_ = value;
}
inline void NrSlMacPduTagProto::set_m_dstl2id(::PROTOBUF_NAMESPACE_ID::uint32 value) {
  _internal_set_m_dstl2id(value);
  // @@protoc_insertion_point(field_set:ns3.NrSlMacPduTagProto.m_dstL2Id)
}

// .ns3.SfnSfProto m_sfnSf = 6;
inline bool NrSlMacPduTagProto::_internal_has_m_sfnsf() const {
  return this != internal_default_instance() && m_sfnsf_ != nullptr;
}
inline bool NrSlMacPduTagProto::has_m_sfnsf() const {
  return _internal_has_m_sfnsf();
}
inline const ::ns3::SfnSfProto& NrSlMacPduTagProto::_internal_m_sfnsf() const {
  const ::ns3::SfnSfProto* p = m_sfnsf_;
  return p != nullptr ? *p : *reinterpret_cast<const ::ns3::SfnSfProto*>(
      &::ns3::_SfnSfProto_default_instance_);
}
inline const ::ns3::SfnSfProto& NrSlMacPduTagProto::m_sfnsf() const {
  // @@protoc_insertion_point(field_get:ns3.NrSlMacPduTagProto.m_sfnSf)
  return _internal_m_sfnsf();
}
inline void NrSlMacPduTagProto::unsafe_arena_set_allocated_m_sfnsf(
    ::ns3::SfnSfProto* m_sfnsf) {
  if (GetArena() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(m_sfnsf_);
  }
  m_sfnsf_ = m_sfnsf;
  if (m_sfnsf) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:ns3.NrSlMacPduTagProto.m_sfnSf)
}
inline ::ns3::SfnSfProto* NrSlMacPduTagProto::release_m_sfnsf() {
  auto temp = unsafe_arena_release_m_sfnsf();
  if (GetArena() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
  return temp;
}
inline ::ns3::SfnSfProto* NrSlMacPduTagProto::unsafe_arena_release_m_sfnsf() {
  // @@protoc_insertion_point(field_release:ns3.NrSlMacPduTagProto.m_sfnSf)
  
  ::ns3::SfnSfProto* temp = m_sfnsf_;
  m_sfnsf_ = nullptr;
  return temp;
}
inline ::ns3::SfnSfProto* NrSlMacPduTagProto::_internal_mutable_m_sfnsf() {
  
  if (m_sfnsf_ == nullptr) {
    auto* p = CreateMaybeMessage<::ns3::SfnSfProto>(GetArena());
    m_sfnsf_ = p;
  }
  return m_sfnsf_;
}
inline ::ns3::SfnSfProto* NrSlMacPduTagProto::mutable_m_sfnsf() {
  // @@protoc_insertion_point(field_mutable:ns3.NrSlMacPduTagProto.m_sfnSf)
  return _internal_mutable_m_sfnsf();
}
inline void NrSlMacPduTagProto::set_allocated_m_sfnsf(::ns3::SfnSfProto* m_sfnsf) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArena();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(m_sfnsf_);
  }
  if (m_sfnsf) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
      reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(m_sfnsf)->GetArena();
    if (message_arena != submessage_arena) {
      m_sfnsf = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, m_sfnsf, submessage_arena);
    }
    
  } else {
    
  }
  m_sfnsf_ = m_sfnsf;
  // @@protoc_insertion_point(field_set_allocated:ns3.NrSlMacPduTagProto.m_sfnSf)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace ns3

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_proto_2fsl_2dmac_2dpdu_2dtag_2eproto
