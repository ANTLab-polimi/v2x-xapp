// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: proto/sl-mac-pdu-tag.proto

#include "proto/sl-mac-pdu-tag.pb.h"

#include <algorithm>

#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/extension_set.h>
#include <google/protobuf/wire_format_lite.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/reflection_ops.h>
#include <google/protobuf/wire_format.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
extern PROTOBUF_INTERNAL_EXPORT_proto_2fsl_2dsfnsf_2eproto ::PROTOBUF_NAMESPACE_ID::internal::SCCInfo<0> scc_info_SfnSfProto_proto_2fsl_2dsfnsf_2eproto;
namespace ns3 {
class NrSlMacPduTagProtoDefaultTypeInternal {
 public:
  ::PROTOBUF_NAMESPACE_ID::internal::ExplicitlyConstructed<NrSlMacPduTagProto> _instance;
} _NrSlMacPduTagProto_default_instance_;
}  // namespace ns3
static void InitDefaultsscc_info_NrSlMacPduTagProto_proto_2fsl_2dmac_2dpdu_2dtag_2eproto() {
  GOOGLE_PROTOBUF_VERIFY_VERSION;

  {
    void* ptr = &::ns3::_NrSlMacPduTagProto_default_instance_;
    new (ptr) ::ns3::NrSlMacPduTagProto();
    ::PROTOBUF_NAMESPACE_ID::internal::OnShutdownDestroyMessage(ptr);
  }
  ::ns3::NrSlMacPduTagProto::InitAsDefaultInstance();
}

::PROTOBUF_NAMESPACE_ID::internal::SCCInfo<1> scc_info_NrSlMacPduTagProto_proto_2fsl_2dmac_2dpdu_2dtag_2eproto =
    {{ATOMIC_VAR_INIT(::PROTOBUF_NAMESPACE_ID::internal::SCCInfoBase::kUninitialized), 1, 0, InitDefaultsscc_info_NrSlMacPduTagProto_proto_2fsl_2dmac_2dpdu_2dtag_2eproto}, {
      &scc_info_SfnSfProto_proto_2fsl_2dsfnsf_2eproto.base,}};

static ::PROTOBUF_NAMESPACE_ID::Metadata file_level_metadata_proto_2fsl_2dmac_2dpdu_2dtag_2eproto[1];
static constexpr ::PROTOBUF_NAMESPACE_ID::EnumDescriptor const** file_level_enum_descriptors_proto_2fsl_2dmac_2dpdu_2dtag_2eproto = nullptr;
static constexpr ::PROTOBUF_NAMESPACE_ID::ServiceDescriptor const** file_level_service_descriptors_proto_2fsl_2dmac_2dpdu_2dtag_2eproto = nullptr;

const ::PROTOBUF_NAMESPACE_ID::uint32 TableStruct_proto_2fsl_2dmac_2dpdu_2dtag_2eproto::offsets[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) = {
  ~0u,  // no _has_bits_
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, _internal_metadata_),
  ~0u,  // no _extensions_
  ~0u,  // no _oneof_case_
  ~0u,  // no _weak_field_map_
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, m_rnti_),
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, m_symstart_),
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, m_numsym_),
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, m_tbsize_),
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, m_dstl2id_),
  PROTOBUF_FIELD_OFFSET(::ns3::NrSlMacPduTagProto, m_sfnsf_),
};
static const ::PROTOBUF_NAMESPACE_ID::internal::MigrationSchema schemas[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) = {
  { 0, -1, sizeof(::ns3::NrSlMacPduTagProto)},
};

static ::PROTOBUF_NAMESPACE_ID::Message const * const file_default_instances[] = {
  reinterpret_cast<const ::PROTOBUF_NAMESPACE_ID::Message*>(&::ns3::_NrSlMacPduTagProto_default_instance_),
};

const char descriptor_table_protodef_proto_2fsl_2dmac_2dpdu_2dtag_2eproto[] PROTOBUF_SECTION_VARIABLE(protodesc_cold) =
  "\n\032proto/sl-mac-pdu-tag.proto\022\003ns3\032\024proto"
  "/sl-sfnsf.proto\"\221\001\n\022NrSlMacPduTagProto\022\016"
  "\n\006m_rnti\030\001 \001(\r\022\022\n\nm_symStart\030\002 \001(\r\022\020\n\010m_"
  "numSym\030\003 \001(\r\022\020\n\010m_tbSize\030\004 \001(\r\022\021\n\tm_dstL"
  "2Id\030\005 \001(\r\022 \n\007m_sfnSf\030\006 \001(\0132\017.ns3.SfnSfPr"
  "otob\006proto3"
  ;
static const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable*const descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto_deps[1] = {
  &::descriptor_table_proto_2fsl_2dsfnsf_2eproto,
};
static ::PROTOBUF_NAMESPACE_ID::internal::SCCInfoBase*const descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto_sccs[1] = {
  &scc_info_NrSlMacPduTagProto_proto_2fsl_2dmac_2dpdu_2dtag_2eproto.base,
};
static ::PROTOBUF_NAMESPACE_ID::internal::once_flag descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto_once;
const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto = {
  false, false, descriptor_table_protodef_proto_2fsl_2dmac_2dpdu_2dtag_2eproto, "proto/sl-mac-pdu-tag.proto", 211,
  &descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto_once, descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto_sccs, descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto_deps, 1, 1,
  schemas, file_default_instances, TableStruct_proto_2fsl_2dmac_2dpdu_2dtag_2eproto::offsets,
  file_level_metadata_proto_2fsl_2dmac_2dpdu_2dtag_2eproto, 1, file_level_enum_descriptors_proto_2fsl_2dmac_2dpdu_2dtag_2eproto, file_level_service_descriptors_proto_2fsl_2dmac_2dpdu_2dtag_2eproto,
};

// Force running AddDescriptors() at dynamic initialization time.
static bool dynamic_init_dummy_proto_2fsl_2dmac_2dpdu_2dtag_2eproto = (static_cast<void>(::PROTOBUF_NAMESPACE_ID::internal::AddDescriptors(&descriptor_table_proto_2fsl_2dmac_2dpdu_2dtag_2eproto)), true);
namespace ns3 {

// ===================================================================

void NrSlMacPduTagProto::InitAsDefaultInstance() {
  ::ns3::_NrSlMacPduTagProto_default_instance_._instance.get_mutable()->m_sfnsf_ = const_cast< ::ns3::SfnSfProto*>(
      ::ns3::SfnSfProto::internal_default_instance());
}
class NrSlMacPduTagProto::_Internal {
 public:
  static const ::ns3::SfnSfProto& m_sfnsf(const NrSlMacPduTagProto* msg);
};

const ::ns3::SfnSfProto&
NrSlMacPduTagProto::_Internal::m_sfnsf(const NrSlMacPduTagProto* msg) {
  return *msg->m_sfnsf_;
}
void NrSlMacPduTagProto::clear_m_sfnsf() {
  if (GetArena() == nullptr && m_sfnsf_ != nullptr) {
    delete m_sfnsf_;
  }
  m_sfnsf_ = nullptr;
}
NrSlMacPduTagProto::NrSlMacPduTagProto(::PROTOBUF_NAMESPACE_ID::Arena* arena)
  : ::PROTOBUF_NAMESPACE_ID::Message(arena) {
  SharedCtor();
  RegisterArenaDtor(arena);
  // @@protoc_insertion_point(arena_constructor:ns3.NrSlMacPduTagProto)
}
NrSlMacPduTagProto::NrSlMacPduTagProto(const NrSlMacPduTagProto& from)
  : ::PROTOBUF_NAMESPACE_ID::Message() {
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  if (from._internal_has_m_sfnsf()) {
    m_sfnsf_ = new ::ns3::SfnSfProto(*from.m_sfnsf_);
  } else {
    m_sfnsf_ = nullptr;
  }
  ::memcpy(&m_rnti_, &from.m_rnti_,
    static_cast<size_t>(reinterpret_cast<char*>(&m_dstl2id_) -
    reinterpret_cast<char*>(&m_rnti_)) + sizeof(m_dstl2id_));
  // @@protoc_insertion_point(copy_constructor:ns3.NrSlMacPduTagProto)
}

void NrSlMacPduTagProto::SharedCtor() {
  ::PROTOBUF_NAMESPACE_ID::internal::InitSCC(&scc_info_NrSlMacPduTagProto_proto_2fsl_2dmac_2dpdu_2dtag_2eproto.base);
  ::memset(&m_sfnsf_, 0, static_cast<size_t>(
      reinterpret_cast<char*>(&m_dstl2id_) -
      reinterpret_cast<char*>(&m_sfnsf_)) + sizeof(m_dstl2id_));
}

NrSlMacPduTagProto::~NrSlMacPduTagProto() {
  // @@protoc_insertion_point(destructor:ns3.NrSlMacPduTagProto)
  SharedDtor();
  _internal_metadata_.Delete<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

void NrSlMacPduTagProto::SharedDtor() {
  GOOGLE_DCHECK(GetArena() == nullptr);
  if (this != internal_default_instance()) delete m_sfnsf_;
}

void NrSlMacPduTagProto::ArenaDtor(void* object) {
  NrSlMacPduTagProto* _this = reinterpret_cast< NrSlMacPduTagProto* >(object);
  (void)_this;
}
void NrSlMacPduTagProto::RegisterArenaDtor(::PROTOBUF_NAMESPACE_ID::Arena*) {
}
void NrSlMacPduTagProto::SetCachedSize(int size) const {
  _cached_size_.Set(size);
}
const NrSlMacPduTagProto& NrSlMacPduTagProto::default_instance() {
  ::PROTOBUF_NAMESPACE_ID::internal::InitSCC(&::scc_info_NrSlMacPduTagProto_proto_2fsl_2dmac_2dpdu_2dtag_2eproto.base);
  return *internal_default_instance();
}


void NrSlMacPduTagProto::Clear() {
// @@protoc_insertion_point(message_clear_start:ns3.NrSlMacPduTagProto)
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  if (GetArena() == nullptr && m_sfnsf_ != nullptr) {
    delete m_sfnsf_;
  }
  m_sfnsf_ = nullptr;
  ::memset(&m_rnti_, 0, static_cast<size_t>(
      reinterpret_cast<char*>(&m_dstl2id_) -
      reinterpret_cast<char*>(&m_rnti_)) + sizeof(m_dstl2id_));
  _internal_metadata_.Clear<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
}

const char* NrSlMacPduTagProto::_InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) {
#define CHK_(x) if (PROTOBUF_PREDICT_FALSE(!(x))) goto failure
  ::PROTOBUF_NAMESPACE_ID::Arena* arena = GetArena(); (void)arena;
  while (!ctx->Done(&ptr)) {
    ::PROTOBUF_NAMESPACE_ID::uint32 tag;
    ptr = ::PROTOBUF_NAMESPACE_ID::internal::ReadTag(ptr, &tag);
    CHK_(ptr);
    switch (tag >> 3) {
      // uint32 m_rnti = 1;
      case 1:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 8)) {
          m_rnti_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      // uint32 m_symStart = 2;
      case 2:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 16)) {
          m_symstart_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      // uint32 m_numSym = 3;
      case 3:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 24)) {
          m_numsym_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      // uint32 m_tbSize = 4;
      case 4:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 32)) {
          m_tbsize_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      // uint32 m_dstL2Id = 5;
      case 5:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 40)) {
          m_dstl2id_ = ::PROTOBUF_NAMESPACE_ID::internal::ReadVarint32(&ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      // .ns3.SfnSfProto m_sfnSf = 6;
      case 6:
        if (PROTOBUF_PREDICT_TRUE(static_cast<::PROTOBUF_NAMESPACE_ID::uint8>(tag) == 50)) {
          ptr = ctx->ParseMessage(_internal_mutable_m_sfnsf(), ptr);
          CHK_(ptr);
        } else goto handle_unusual;
        continue;
      default: {
      handle_unusual:
        if ((tag & 7) == 4 || tag == 0) {
          ctx->SetLastTag(tag);
          goto success;
        }
        ptr = UnknownFieldParse(tag,
            _internal_metadata_.mutable_unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(),
            ptr, ctx);
        CHK_(ptr != nullptr);
        continue;
      }
    }  // switch
  }  // while
success:
  return ptr;
failure:
  ptr = nullptr;
  goto success;
#undef CHK_
}

::PROTOBUF_NAMESPACE_ID::uint8* NrSlMacPduTagProto::_InternalSerialize(
    ::PROTOBUF_NAMESPACE_ID::uint8* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const {
  // @@protoc_insertion_point(serialize_to_array_start:ns3.NrSlMacPduTagProto)
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  // uint32 m_rnti = 1;
  if (this->m_rnti() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteUInt32ToArray(1, this->_internal_m_rnti(), target);
  }

  // uint32 m_symStart = 2;
  if (this->m_symstart() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteUInt32ToArray(2, this->_internal_m_symstart(), target);
  }

  // uint32 m_numSym = 3;
  if (this->m_numsym() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteUInt32ToArray(3, this->_internal_m_numsym(), target);
  }

  // uint32 m_tbSize = 4;
  if (this->m_tbsize() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteUInt32ToArray(4, this->_internal_m_tbsize(), target);
  }

  // uint32 m_dstL2Id = 5;
  if (this->m_dstl2id() != 0) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::WriteUInt32ToArray(5, this->_internal_m_dstl2id(), target);
  }

  // .ns3.SfnSfProto m_sfnSf = 6;
  if (this->has_m_sfnsf()) {
    target = stream->EnsureSpace(target);
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::
      InternalWriteMessage(
        6, _Internal::m_sfnsf(this), target, stream);
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    target = ::PROTOBUF_NAMESPACE_ID::internal::WireFormat::InternalSerializeUnknownFieldsToArray(
        _internal_metadata_.unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(::PROTOBUF_NAMESPACE_ID::UnknownFieldSet::default_instance), target, stream);
  }
  // @@protoc_insertion_point(serialize_to_array_end:ns3.NrSlMacPduTagProto)
  return target;
}

size_t NrSlMacPduTagProto::ByteSizeLong() const {
// @@protoc_insertion_point(message_byte_size_start:ns3.NrSlMacPduTagProto)
  size_t total_size = 0;

  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  // Prevent compiler warnings about cached_has_bits being unused
  (void) cached_has_bits;

  // .ns3.SfnSfProto m_sfnSf = 6;
  if (this->has_m_sfnsf()) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::MessageSize(
        *m_sfnsf_);
  }

  // uint32 m_rnti = 1;
  if (this->m_rnti() != 0) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::UInt32Size(
        this->_internal_m_rnti());
  }

  // uint32 m_symStart = 2;
  if (this->m_symstart() != 0) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::UInt32Size(
        this->_internal_m_symstart());
  }

  // uint32 m_numSym = 3;
  if (this->m_numsym() != 0) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::UInt32Size(
        this->_internal_m_numsym());
  }

  // uint32 m_tbSize = 4;
  if (this->m_tbsize() != 0) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::UInt32Size(
        this->_internal_m_tbsize());
  }

  // uint32 m_dstL2Id = 5;
  if (this->m_dstl2id() != 0) {
    total_size += 1 +
      ::PROTOBUF_NAMESPACE_ID::internal::WireFormatLite::UInt32Size(
        this->_internal_m_dstl2id());
  }

  if (PROTOBUF_PREDICT_FALSE(_internal_metadata_.have_unknown_fields())) {
    return ::PROTOBUF_NAMESPACE_ID::internal::ComputeUnknownFieldsSize(
        _internal_metadata_, total_size, &_cached_size_);
  }
  int cached_size = ::PROTOBUF_NAMESPACE_ID::internal::ToCachedSize(total_size);
  SetCachedSize(cached_size);
  return total_size;
}

void NrSlMacPduTagProto::MergeFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) {
// @@protoc_insertion_point(generalized_merge_from_start:ns3.NrSlMacPduTagProto)
  GOOGLE_DCHECK_NE(&from, this);
  const NrSlMacPduTagProto* source =
      ::PROTOBUF_NAMESPACE_ID::DynamicCastToGenerated<NrSlMacPduTagProto>(
          &from);
  if (source == nullptr) {
  // @@protoc_insertion_point(generalized_merge_from_cast_fail:ns3.NrSlMacPduTagProto)
    ::PROTOBUF_NAMESPACE_ID::internal::ReflectionOps::Merge(from, this);
  } else {
  // @@protoc_insertion_point(generalized_merge_from_cast_success:ns3.NrSlMacPduTagProto)
    MergeFrom(*source);
  }
}

void NrSlMacPduTagProto::MergeFrom(const NrSlMacPduTagProto& from) {
// @@protoc_insertion_point(class_specific_merge_from_start:ns3.NrSlMacPduTagProto)
  GOOGLE_DCHECK_NE(&from, this);
  _internal_metadata_.MergeFrom<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(from._internal_metadata_);
  ::PROTOBUF_NAMESPACE_ID::uint32 cached_has_bits = 0;
  (void) cached_has_bits;

  if (from.has_m_sfnsf()) {
    _internal_mutable_m_sfnsf()->::ns3::SfnSfProto::MergeFrom(from._internal_m_sfnsf());
  }
  if (from.m_rnti() != 0) {
    _internal_set_m_rnti(from._internal_m_rnti());
  }
  if (from.m_symstart() != 0) {
    _internal_set_m_symstart(from._internal_m_symstart());
  }
  if (from.m_numsym() != 0) {
    _internal_set_m_numsym(from._internal_m_numsym());
  }
  if (from.m_tbsize() != 0) {
    _internal_set_m_tbsize(from._internal_m_tbsize());
  }
  if (from.m_dstl2id() != 0) {
    _internal_set_m_dstl2id(from._internal_m_dstl2id());
  }
}

void NrSlMacPduTagProto::CopyFrom(const ::PROTOBUF_NAMESPACE_ID::Message& from) {
// @@protoc_insertion_point(generalized_copy_from_start:ns3.NrSlMacPduTagProto)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

void NrSlMacPduTagProto::CopyFrom(const NrSlMacPduTagProto& from) {
// @@protoc_insertion_point(class_specific_copy_from_start:ns3.NrSlMacPduTagProto)
  if (&from == this) return;
  Clear();
  MergeFrom(from);
}

bool NrSlMacPduTagProto::IsInitialized() const {
  return true;
}

void NrSlMacPduTagProto::InternalSwap(NrSlMacPduTagProto* other) {
  using std::swap;
  _internal_metadata_.Swap<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(&other->_internal_metadata_);
  ::PROTOBUF_NAMESPACE_ID::internal::memswap<
      PROTOBUF_FIELD_OFFSET(NrSlMacPduTagProto, m_dstl2id_)
      + sizeof(NrSlMacPduTagProto::m_dstl2id_)
      - PROTOBUF_FIELD_OFFSET(NrSlMacPduTagProto, m_sfnsf_)>(
          reinterpret_cast<char*>(&m_sfnsf_),
          reinterpret_cast<char*>(&other->m_sfnsf_));
}

::PROTOBUF_NAMESPACE_ID::Metadata NrSlMacPduTagProto::GetMetadata() const {
  return GetMetadataStatic();
}


// @@protoc_insertion_point(namespace_scope)
}  // namespace ns3
PROTOBUF_NAMESPACE_OPEN
template<> PROTOBUF_NOINLINE ::ns3::NrSlMacPduTagProto* Arena::CreateMaybeMessage< ::ns3::NrSlMacPduTagProto >(Arena* arena) {
  return Arena::CreateMessageInternal< ::ns3::NrSlMacPduTagProto >(arena);
}
PROTOBUF_NAMESPACE_CLOSE

// @@protoc_insertion_point(global_scope)
#include <google/protobuf/port_undef.inc>
