# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: hotel_group.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'hotel_group.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11hotel_group.proto\"\x12\n\x04Room\x12\n\n\x02id\x18\x01 \x01(\x05\"#\n\x10HotelGroupStatus\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32V\n\nHotelGroup\x12 \n\x04\x62ook\x12\x05.Room\x1a\x11.HotelGroupStatus\x12&\n\ncancelBook\x12\x05.Room\x1a\x11.HotelGroupStatusb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hotel_group_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ROOM']._serialized_start=21
  _globals['_ROOM']._serialized_end=39
  _globals['_HOTELGROUPSTATUS']._serialized_start=41
  _globals['_HOTELGROUPSTATUS']._serialized_end=76
  _globals['_HOTELGROUP']._serialized_start=78
  _globals['_HOTELGROUP']._serialized_end=164
# @@protoc_insertion_point(module_scope)
