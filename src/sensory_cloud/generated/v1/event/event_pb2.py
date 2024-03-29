# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/event/event.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from sensory_cloud.generated.validate import validate_pb2 as validate_dot_validate__pb2
from sensory_cloud.generated.common import common_pb2 as common_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='v1/event/event.proto',
  package='sensory.api.v1.event',
  syntax='proto3',
  serialized_options=b'\n\034ai.sensorycloud.api.v1.eventB\026SensoryApiV1EventProtoP\001Z:gitlab.com/sensory-cloud/server/titan.git/pkg/api/v1/event\242\002\004SENG',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14v1/event/event.proto\x12\x14sensory.api.v1.event\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17validate/validate.proto\x1a\x13\x63ommon/common.proto\"M\n\x19PublishUsageEventsRequest\x12\x30\n\x06\x65vents\x18\x01 \x03(\x0b\x32 .sensory.api.v1.event.UsageEvent\"\xc5\x03\n\nUsageEvent\x12\x37\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xfa\x42\x05\xb2\x01\x02\x08\x01\x12\x19\n\x08\x64uration\x18\x02 \x01(\x03\x42\x07\xfa\x42\x04\"\x02(\x00\x12\x14\n\x02id\x18\x03 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\x12\x1b\n\x08\x63lientId\x18\x04 \x01(\tB\t\xfa\x42\x06r\x04\x10\x01\x18\x7f\x12:\n\x04type\x18\x05 \x01(\x0e\x32\".sensory.api.common.UsageEventTypeB\x08\xfa\x42\x05\x82\x01\x02\x10\x01\x12\x19\n\x05route\x18\x06 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\xff\x03\x12\x38\n\x0ctechnologies\x18\x07 \x03(\x0e\x32\".sensory.api.common.TechnologyType\x12\x0e\n\x06models\x18\x08 \x03(\t\x12\x17\n\x0f\x61udioDurationMs\x18\t \x01(\x03\x12\x17\n\x0fvideoFrameCount\x18\n \x01(\x03\x12\x10\n\x08tenantId\x18\x0b \x01(\t\x12\x37\n\x10\x62illableFunction\x18\x0c \x01(\x0e\x32\x1d.sensory.api.common.ModelType\x12\x12\n\ntokenCount\x18\r \x01(\x03\"\xc6\x03\n\x12UsageEventResponse\x12\x37\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xfa\x42\x05\xb2\x01\x02\x08\x01\x12\x19\n\x08\x64uration\x18\x02 \x01(\x03\x42\x07\xfa\x42\x04\"\x02(\x00\x12\x14\n\x02id\x18\x03 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\x12\x1b\n\x08\x63lientId\x18\x04 \x01(\tB\t\xfa\x42\x06r\x04\x10\x01\x18\x7f\x12:\n\x04type\x18\x05 \x01(\x0e\x32\".sensory.api.common.UsageEventTypeB\x08\xfa\x42\x05\x82\x01\x02\x10\x01\x12\x19\n\x05route\x18\x06 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\xff\x03\x12\x38\n\x0ctechnologies\x18\x07 \x03(\x0e\x32\".sensory.api.common.TechnologyType\x12\x0e\n\x06models\x18\x08 \x03(\t\x12\x15\n\rbillableValue\x18\t \x01(\x03\x12\x15\n\rbillableUnits\x18\n \x01(\t\x12\x10\n\x08tenantId\x18\x0b \x01(\t\x12\x37\n\x10\x62illableFunction\x18\x0c \x01(\x0e\x32\x1d.sensory.api.common.ModelType\x12\x0f\n\x07\x63redits\x18\r \x01(\x01\"\xf5\x01\n\x15UsageEventListRequest\x12\x10\n\x08tenantId\x18\x01 \x01(\t\x12\x39\n\npagination\x18\x02 \x01(\x0b\x32%.sensory.api.common.PaginationOptions\x12)\n\x05\x61\x66ter\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06\x62\x65\x66ore\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x11\x62illableFunctions\x18\x05 \x03(\x0e\x32\x1d.sensory.api.common.ModelType\"\x8e\x01\n\x16UsageEventListResponse\x12\x38\n\x06\x65vents\x18\x01 \x03(\x0b\x32(.sensory.api.v1.event.UsageEventResponse\x12:\n\npagination\x18\x02 \x01(\x0b\x32&.sensory.api.common.PaginationResponse\"\xbd\x01\n\x19GlobalEventSummaryRequest\x12\x0f\n\x07tenants\x18\x01 \x03(\t\x12)\n\x05\x61\x66ter\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06\x62\x65\x66ore\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x38\n\x11\x62illableFunctions\x18\x05 \x03(\x0e\x32\x1d.sensory.api.common.ModelType\"T\n\x11UsageEventSummary\x12?\n\tsummaries\x18\x01 \x03(\x0b\x32,.sensory.api.v1.event.UsageEventModelSummary\"\xa1\x01\n\x16UsageEventModelSummary\x12\x37\n\x10\x62illableFunction\x18\x01 \x01(\x0e\x32\x1d.sensory.api.common.ModelType\x12\r\n\x05units\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x03\x12\r\n\x05\x63ount\x18\x04 \x01(\x03\x12\x0f\n\x07\x63redits\x18\x05 \x01(\x01\x12\x10\n\x08tenantId\x18\x06 \x01(\t\"\x1c\n\x1aPublishUsageEventsResponse2\xe0\x03\n\x0c\x45ventService\x12y\n\x12PublishUsageEvents\x12/.sensory.api.v1.event.PublishUsageEventsRequest\x1a\x30.sensory.api.v1.event.PublishUsageEventsResponse\"\x00\x12p\n\x11GetUsageEventList\x12+.sensory.api.v1.event.UsageEventListRequest\x1a,.sensory.api.v1.event.UsageEventListResponse\"\x00\x12n\n\x14GetUsageEventSummary\x12+.sensory.api.v1.event.UsageEventListRequest\x1a\'.sensory.api.v1.event.UsageEventSummary\"\x00\x12s\n\x15GetGlobalUsageSummary\x12/.sensory.api.v1.event.GlobalEventSummaryRequest\x1a\'.sensory.api.v1.event.UsageEventSummary\"\x00\x42{\n\x1c\x61i.sensorycloud.api.v1.eventB\x16SensoryApiV1EventProtoP\x01Z:gitlab.com/sensory-cloud/server/titan.git/pkg/api/v1/event\xa2\x02\x04SENGb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,validate_dot_validate__pb2.DESCRIPTOR,common_dot_common__pb2.DESCRIPTOR,])




_PUBLISHUSAGEEVENTSREQUEST = _descriptor.Descriptor(
  name='PublishUsageEventsRequest',
  full_name='sensory.api.v1.event.PublishUsageEventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='events', full_name='sensory.api.v1.event.PublishUsageEventsRequest.events', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=125,
  serialized_end=202,
)


_USAGEEVENT = _descriptor.Descriptor(
  name='UsageEvent',
  full_name='sensory.api.v1.event.UsageEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='sensory.api.v1.event.UsageEvent.timestamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\262\001\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='duration', full_name='sensory.api.v1.event.UsageEvent.duration', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\004\"\002(\000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='sensory.api.v1.event.UsageEvent.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005r\003\260\001\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clientId', full_name='sensory.api.v1.event.UsageEvent.clientId', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\006r\004\020\001\030\177', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='sensory.api.v1.event.UsageEvent.type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\202\001\002\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route', full_name='sensory.api.v1.event.UsageEvent.route', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\007r\005\020\001\030\377\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='technologies', full_name='sensory.api.v1.event.UsageEvent.technologies', index=6,
      number=7, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='models', full_name='sensory.api.v1.event.UsageEvent.models', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='audioDurationMs', full_name='sensory.api.v1.event.UsageEvent.audioDurationMs', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='videoFrameCount', full_name='sensory.api.v1.event.UsageEvent.videoFrameCount', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.v1.event.UsageEvent.tenantId', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billableFunction', full_name='sensory.api.v1.event.UsageEvent.billableFunction', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tokenCount', full_name='sensory.api.v1.event.UsageEvent.tokenCount', index=12,
      number=13, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=205,
  serialized_end=658,
)


_USAGEEVENTRESPONSE = _descriptor.Descriptor(
  name='UsageEventResponse',
  full_name='sensory.api.v1.event.UsageEventResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='sensory.api.v1.event.UsageEventResponse.timestamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\262\001\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='duration', full_name='sensory.api.v1.event.UsageEventResponse.duration', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\004\"\002(\000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='sensory.api.v1.event.UsageEventResponse.id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005r\003\260\001\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='clientId', full_name='sensory.api.v1.event.UsageEventResponse.clientId', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\006r\004\020\001\030\177', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='sensory.api.v1.event.UsageEventResponse.type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\202\001\002\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='route', full_name='sensory.api.v1.event.UsageEventResponse.route', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\007r\005\020\001\030\377\003', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='technologies', full_name='sensory.api.v1.event.UsageEventResponse.technologies', index=6,
      number=7, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='models', full_name='sensory.api.v1.event.UsageEventResponse.models', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billableValue', full_name='sensory.api.v1.event.UsageEventResponse.billableValue', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billableUnits', full_name='sensory.api.v1.event.UsageEventResponse.billableUnits', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.v1.event.UsageEventResponse.tenantId', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billableFunction', full_name='sensory.api.v1.event.UsageEventResponse.billableFunction', index=11,
      number=12, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='credits', full_name='sensory.api.v1.event.UsageEventResponse.credits', index=12,
      number=13, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=661,
  serialized_end=1115,
)


_USAGEEVENTLISTREQUEST = _descriptor.Descriptor(
  name='UsageEventListRequest',
  full_name='sensory.api.v1.event.UsageEventListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.v1.event.UsageEventListRequest.tenantId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pagination', full_name='sensory.api.v1.event.UsageEventListRequest.pagination', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='after', full_name='sensory.api.v1.event.UsageEventListRequest.after', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before', full_name='sensory.api.v1.event.UsageEventListRequest.before', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billableFunctions', full_name='sensory.api.v1.event.UsageEventListRequest.billableFunctions', index=4,
      number=5, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1118,
  serialized_end=1363,
)


_USAGEEVENTLISTRESPONSE = _descriptor.Descriptor(
  name='UsageEventListResponse',
  full_name='sensory.api.v1.event.UsageEventListResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='events', full_name='sensory.api.v1.event.UsageEventListResponse.events', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pagination', full_name='sensory.api.v1.event.UsageEventListResponse.pagination', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1366,
  serialized_end=1508,
)


_GLOBALEVENTSUMMARYREQUEST = _descriptor.Descriptor(
  name='GlobalEventSummaryRequest',
  full_name='sensory.api.v1.event.GlobalEventSummaryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tenants', full_name='sensory.api.v1.event.GlobalEventSummaryRequest.tenants', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='after', full_name='sensory.api.v1.event.GlobalEventSummaryRequest.after', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='before', full_name='sensory.api.v1.event.GlobalEventSummaryRequest.before', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='billableFunctions', full_name='sensory.api.v1.event.GlobalEventSummaryRequest.billableFunctions', index=3,
      number=5, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1511,
  serialized_end=1700,
)


_USAGEEVENTSUMMARY = _descriptor.Descriptor(
  name='UsageEventSummary',
  full_name='sensory.api.v1.event.UsageEventSummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='summaries', full_name='sensory.api.v1.event.UsageEventSummary.summaries', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1702,
  serialized_end=1786,
)


_USAGEEVENTMODELSUMMARY = _descriptor.Descriptor(
  name='UsageEventModelSummary',
  full_name='sensory.api.v1.event.UsageEventModelSummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='billableFunction', full_name='sensory.api.v1.event.UsageEventModelSummary.billableFunction', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='units', full_name='sensory.api.v1.event.UsageEventModelSummary.units', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='sensory.api.v1.event.UsageEventModelSummary.value', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='count', full_name='sensory.api.v1.event.UsageEventModelSummary.count', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='credits', full_name='sensory.api.v1.event.UsageEventModelSummary.credits', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.v1.event.UsageEventModelSummary.tenantId', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=1789,
  serialized_end=1950,
)


_PUBLISHUSAGEEVENTSRESPONSE = _descriptor.Descriptor(
  name='PublishUsageEventsResponse',
  full_name='sensory.api.v1.event.PublishUsageEventsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=1952,
  serialized_end=1980,
)

_PUBLISHUSAGEEVENTSREQUEST.fields_by_name['events'].message_type = _USAGEEVENT
_USAGEEVENT.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USAGEEVENT.fields_by_name['type'].enum_type = common_dot_common__pb2._USAGEEVENTTYPE
_USAGEEVENT.fields_by_name['technologies'].enum_type = common_dot_common__pb2._TECHNOLOGYTYPE
_USAGEEVENT.fields_by_name['billableFunction'].enum_type = common_dot_common__pb2._MODELTYPE
_USAGEEVENTRESPONSE.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USAGEEVENTRESPONSE.fields_by_name['type'].enum_type = common_dot_common__pb2._USAGEEVENTTYPE
_USAGEEVENTRESPONSE.fields_by_name['technologies'].enum_type = common_dot_common__pb2._TECHNOLOGYTYPE
_USAGEEVENTRESPONSE.fields_by_name['billableFunction'].enum_type = common_dot_common__pb2._MODELTYPE
_USAGEEVENTLISTREQUEST.fields_by_name['pagination'].message_type = common_dot_common__pb2._PAGINATIONOPTIONS
_USAGEEVENTLISTREQUEST.fields_by_name['after'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USAGEEVENTLISTREQUEST.fields_by_name['before'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USAGEEVENTLISTREQUEST.fields_by_name['billableFunctions'].enum_type = common_dot_common__pb2._MODELTYPE
_USAGEEVENTLISTRESPONSE.fields_by_name['events'].message_type = _USAGEEVENTRESPONSE
_USAGEEVENTLISTRESPONSE.fields_by_name['pagination'].message_type = common_dot_common__pb2._PAGINATIONRESPONSE
_GLOBALEVENTSUMMARYREQUEST.fields_by_name['after'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GLOBALEVENTSUMMARYREQUEST.fields_by_name['before'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GLOBALEVENTSUMMARYREQUEST.fields_by_name['billableFunctions'].enum_type = common_dot_common__pb2._MODELTYPE
_USAGEEVENTSUMMARY.fields_by_name['summaries'].message_type = _USAGEEVENTMODELSUMMARY
_USAGEEVENTMODELSUMMARY.fields_by_name['billableFunction'].enum_type = common_dot_common__pb2._MODELTYPE
DESCRIPTOR.message_types_by_name['PublishUsageEventsRequest'] = _PUBLISHUSAGEEVENTSREQUEST
DESCRIPTOR.message_types_by_name['UsageEvent'] = _USAGEEVENT
DESCRIPTOR.message_types_by_name['UsageEventResponse'] = _USAGEEVENTRESPONSE
DESCRIPTOR.message_types_by_name['UsageEventListRequest'] = _USAGEEVENTLISTREQUEST
DESCRIPTOR.message_types_by_name['UsageEventListResponse'] = _USAGEEVENTLISTRESPONSE
DESCRIPTOR.message_types_by_name['GlobalEventSummaryRequest'] = _GLOBALEVENTSUMMARYREQUEST
DESCRIPTOR.message_types_by_name['UsageEventSummary'] = _USAGEEVENTSUMMARY
DESCRIPTOR.message_types_by_name['UsageEventModelSummary'] = _USAGEEVENTMODELSUMMARY
DESCRIPTOR.message_types_by_name['PublishUsageEventsResponse'] = _PUBLISHUSAGEEVENTSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PublishUsageEventsRequest = _reflection.GeneratedProtocolMessageType('PublishUsageEventsRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHUSAGEEVENTSREQUEST,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.PublishUsageEventsRequest)
  })
_sym_db.RegisterMessage(PublishUsageEventsRequest)

UsageEvent = _reflection.GeneratedProtocolMessageType('UsageEvent', (_message.Message,), {
  'DESCRIPTOR' : _USAGEEVENT,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.UsageEvent)
  })
_sym_db.RegisterMessage(UsageEvent)

UsageEventResponse = _reflection.GeneratedProtocolMessageType('UsageEventResponse', (_message.Message,), {
  'DESCRIPTOR' : _USAGEEVENTRESPONSE,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.UsageEventResponse)
  })
_sym_db.RegisterMessage(UsageEventResponse)

UsageEventListRequest = _reflection.GeneratedProtocolMessageType('UsageEventListRequest', (_message.Message,), {
  'DESCRIPTOR' : _USAGEEVENTLISTREQUEST,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.UsageEventListRequest)
  })
_sym_db.RegisterMessage(UsageEventListRequest)

UsageEventListResponse = _reflection.GeneratedProtocolMessageType('UsageEventListResponse', (_message.Message,), {
  'DESCRIPTOR' : _USAGEEVENTLISTRESPONSE,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.UsageEventListResponse)
  })
_sym_db.RegisterMessage(UsageEventListResponse)

GlobalEventSummaryRequest = _reflection.GeneratedProtocolMessageType('GlobalEventSummaryRequest', (_message.Message,), {
  'DESCRIPTOR' : _GLOBALEVENTSUMMARYREQUEST,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.GlobalEventSummaryRequest)
  })
_sym_db.RegisterMessage(GlobalEventSummaryRequest)

UsageEventSummary = _reflection.GeneratedProtocolMessageType('UsageEventSummary', (_message.Message,), {
  'DESCRIPTOR' : _USAGEEVENTSUMMARY,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.UsageEventSummary)
  })
_sym_db.RegisterMessage(UsageEventSummary)

UsageEventModelSummary = _reflection.GeneratedProtocolMessageType('UsageEventModelSummary', (_message.Message,), {
  'DESCRIPTOR' : _USAGEEVENTMODELSUMMARY,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.UsageEventModelSummary)
  })
_sym_db.RegisterMessage(UsageEventModelSummary)

PublishUsageEventsResponse = _reflection.GeneratedProtocolMessageType('PublishUsageEventsResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHUSAGEEVENTSRESPONSE,
  '__module__' : 'v1.event.event_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.event.PublishUsageEventsResponse)
  })
_sym_db.RegisterMessage(PublishUsageEventsResponse)


DESCRIPTOR._options = None
_USAGEEVENT.fields_by_name['timestamp']._options = None
_USAGEEVENT.fields_by_name['duration']._options = None
_USAGEEVENT.fields_by_name['id']._options = None
_USAGEEVENT.fields_by_name['clientId']._options = None
_USAGEEVENT.fields_by_name['type']._options = None
_USAGEEVENT.fields_by_name['route']._options = None
_USAGEEVENTRESPONSE.fields_by_name['timestamp']._options = None
_USAGEEVENTRESPONSE.fields_by_name['duration']._options = None
_USAGEEVENTRESPONSE.fields_by_name['id']._options = None
_USAGEEVENTRESPONSE.fields_by_name['clientId']._options = None
_USAGEEVENTRESPONSE.fields_by_name['type']._options = None
_USAGEEVENTRESPONSE.fields_by_name['route']._options = None

_EVENTSERVICE = _descriptor.ServiceDescriptor(
  name='EventService',
  full_name='sensory.api.v1.event.EventService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1983,
  serialized_end=2463,
  methods=[
  _descriptor.MethodDescriptor(
    name='PublishUsageEvents',
    full_name='sensory.api.v1.event.EventService.PublishUsageEvents',
    index=0,
    containing_service=None,
    input_type=_PUBLISHUSAGEEVENTSREQUEST,
    output_type=_PUBLISHUSAGEEVENTSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetUsageEventList',
    full_name='sensory.api.v1.event.EventService.GetUsageEventList',
    index=1,
    containing_service=None,
    input_type=_USAGEEVENTLISTREQUEST,
    output_type=_USAGEEVENTLISTRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetUsageEventSummary',
    full_name='sensory.api.v1.event.EventService.GetUsageEventSummary',
    index=2,
    containing_service=None,
    input_type=_USAGEEVENTLISTREQUEST,
    output_type=_USAGEEVENTSUMMARY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetGlobalUsageSummary',
    full_name='sensory.api.v1.event.EventService.GetGlobalUsageSummary',
    index=3,
    containing_service=None,
    input_type=_GLOBALEVENTSUMMARYREQUEST,
    output_type=_USAGEEVENTSUMMARY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_EVENTSERVICE)

DESCRIPTOR.services_by_name['EventService'] = _EVENTSERVICE

# @@protoc_insertion_point(module_scope)
