# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sl-slot-alloc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import sl_sfnsf_pb2 as sl__sfnsf__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='sl-slot-alloc.proto',
  package='ns3',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x13sl-slot-alloc.proto\x12\x03ns3\x1a\x0esl-sfnsf.proto\"/\n\x11SlRlcPduInfoProto\x12\x0c\n\x04lcid\x18\x01 \x01(\r\x12\x0c\n\x04size\x18\x02 \x01(\r\"\x9c\x03\n\x12NrSlSlotAllocProto\x12\x1c\n\x03sfn\x18\x10 \x01(\x0b\x32\x0f.ns3.SfnSfProto\x12\x0f\n\x07\x64stL2Id\x18\x0f \x01(\r\x12\x0b\n\x03ndi\x18\x0e \x01(\r\x12\n\n\x02rv\x18\r \x01(\r\x12\x10\n\x08priority\x18\x0c \x01(\r\x12,\n\x0cslRlcPduInfo\x18\x11 \x03(\x0b\x32\x16.ns3.SlRlcPduInfoProto\x12\x0b\n\x03mcs\x18\x0b \x01(\r\x12\x15\n\rnumSlPscchRbs\x18\n \x01(\r\x12\x17\n\x0fslPscchSymStart\x18\t \x01(\r\x12\x18\n\x10slPscchSymLength\x18\x08 \x01(\r\x12\x17\n\x0fslPsschSymStart\x18\x07 \x01(\r\x12\x18\n\x10slPsschSymLength\x18\x06 \x01(\r\x12\x19\n\x11slPsschSubChStart\x18\x05 \x01(\r\x12\x1a\n\x12slPsschSubChLength\x18\x01 \x01(\r\x12\x18\n\x10maxNumPerReserve\x18\x02 \x01(\r\x12\x0f\n\x07txSci1A\x18\x03 \x01(\x08\x12\x12\n\nslotNumInd\x18\x04 \x01(\rb\x06proto3')
  ,
  dependencies=[sl__sfnsf__pb2.DESCRIPTOR,])




_SLRLCPDUINFOPROTO = _descriptor.Descriptor(
  name='SlRlcPduInfoProto',
  full_name='ns3.SlRlcPduInfoProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lcid', full_name='ns3.SlRlcPduInfoProto.lcid', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size', full_name='ns3.SlRlcPduInfoProto.size', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=91,
)


_NRSLSLOTALLOCPROTO = _descriptor.Descriptor(
  name='NrSlSlotAllocProto',
  full_name='ns3.NrSlSlotAllocProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sfn', full_name='ns3.NrSlSlotAllocProto.sfn', index=0,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dstL2Id', full_name='ns3.NrSlSlotAllocProto.dstL2Id', index=1,
      number=15, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ndi', full_name='ns3.NrSlSlotAllocProto.ndi', index=2,
      number=14, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rv', full_name='ns3.NrSlSlotAllocProto.rv', index=3,
      number=13, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='priority', full_name='ns3.NrSlSlotAllocProto.priority', index=4,
      number=12, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slRlcPduInfo', full_name='ns3.NrSlSlotAllocProto.slRlcPduInfo', index=5,
      number=17, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mcs', full_name='ns3.NrSlSlotAllocProto.mcs', index=6,
      number=11, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='numSlPscchRbs', full_name='ns3.NrSlSlotAllocProto.numSlPscchRbs', index=7,
      number=10, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slPscchSymStart', full_name='ns3.NrSlSlotAllocProto.slPscchSymStart', index=8,
      number=9, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slPscchSymLength', full_name='ns3.NrSlSlotAllocProto.slPscchSymLength', index=9,
      number=8, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slPsschSymStart', full_name='ns3.NrSlSlotAllocProto.slPsschSymStart', index=10,
      number=7, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slPsschSymLength', full_name='ns3.NrSlSlotAllocProto.slPsschSymLength', index=11,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slPsschSubChStart', full_name='ns3.NrSlSlotAllocProto.slPsschSubChStart', index=12,
      number=5, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slPsschSubChLength', full_name='ns3.NrSlSlotAllocProto.slPsschSubChLength', index=13,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='maxNumPerReserve', full_name='ns3.NrSlSlotAllocProto.maxNumPerReserve', index=14,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='txSci1A', full_name='ns3.NrSlSlotAllocProto.txSci1A', index=15,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='slotNumInd', full_name='ns3.NrSlSlotAllocProto.slotNumInd', index=16,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=94,
  serialized_end=506,
)

_NRSLSLOTALLOCPROTO.fields_by_name['sfn'].message_type = sl__sfnsf__pb2._SFNSFPROTO
_NRSLSLOTALLOCPROTO.fields_by_name['slRlcPduInfo'].message_type = _SLRLCPDUINFOPROTO
DESCRIPTOR.message_types_by_name['SlRlcPduInfoProto'] = _SLRLCPDUINFOPROTO
DESCRIPTOR.message_types_by_name['NrSlSlotAllocProto'] = _NRSLSLOTALLOCPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SlRlcPduInfoProto = _reflection.GeneratedProtocolMessageType('SlRlcPduInfoProto', (_message.Message,), dict(
  DESCRIPTOR = _SLRLCPDUINFOPROTO,
  __module__ = 'sl_slot_alloc_pb2'
  # @@protoc_insertion_point(class_scope:ns3.SlRlcPduInfoProto)
  ))
_sym_db.RegisterMessage(SlRlcPduInfoProto)

NrSlSlotAllocProto = _reflection.GeneratedProtocolMessageType('NrSlSlotAllocProto', (_message.Message,), dict(
  DESCRIPTOR = _NRSLSLOTALLOCPROTO,
  __module__ = 'sl_slot_alloc_pb2'
  # @@protoc_insertion_point(class_scope:ns3.NrSlSlotAllocProto)
  ))
_sym_db.RegisterMessage(NrSlSlotAllocProto)


# @@protoc_insertion_point(module_scope)
