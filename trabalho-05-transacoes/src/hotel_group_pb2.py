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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11hotel_group.proto\"$\n\x04Room\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"\x1d\n\x05Rooms\x12\x14\n\x05rooms\x18\x01 \x03(\x0b\x32\x05.Room\"#\n\x10HotelGroupStatus\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x11\n\x0fHotelGroupEmpty2\x94\x01\n\nHotelGroup\x12&\n\tbookRooms\x12\x06.Rooms\x1a\x11.HotelGroupStatus\x12/\n\x12\x63\x61ncelReservations\x12\x06.Rooms\x1a\x11.HotelGroupStatus\x12-\n\x11getRoomsAvailable\x12\x10.HotelGroupEmpty\x1a\x06.Roomsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hotel_group_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ROOM']._serialized_start=21
  _globals['_ROOM']._serialized_end=57
  _globals['_ROOMS']._serialized_start=59
  _globals['_ROOMS']._serialized_end=88
  _globals['_HOTELGROUPSTATUS']._serialized_start=90
  _globals['_HOTELGROUPSTATUS']._serialized_end=125
  _globals['_HOTELGROUPEMPTY']._serialized_start=127
  _globals['_HOTELGROUPEMPTY']._serialized_end=144
  _globals['_HOTELGROUP']._serialized_start=147
  _globals['_HOTELGROUP']._serialized_end=295
# @@protoc_insertion_point(module_scope)
