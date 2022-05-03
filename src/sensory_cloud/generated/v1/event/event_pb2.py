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
  serialized_options=b'\n\034ai.sensorycloud.api.v1.eventB\026SensoryApiV1EventProtoP\001Z:gitlab.com/sensory-cloud/server/titan.git/pkg/api/v1/event',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14v1/event/event.proto\x12\x14sensory.api.v1.event\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17validate/validate.proto\x1a\x13\x63ommon/common.proto\"M\n\x19PublishUsageEventsRequest\x12\x30\n\x06\x65vents\x18\x01 \x03(\x0b\x32 .sensory.api.v1.event.UsageEvent\"\xe6\x02\n\nUsageEvent\x12\x37\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xfa\x42\x05\xb2\x01\x02\x08\x01\x12\x19\n\x08\x64uration\x18\x02 \x01(\x03\x42\x07\xfa\x42\x04\"\x02(\x00\x12\x14\n\x02id\x18\x03 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\x12\x1b\n\x08\x63lientId\x18\x04 \x01(\tB\t\xfa\x42\x06r\x04\x10\x01\x18\x7f\x12:\n\x04type\x18\x05 \x01(\x0e\x32\".sensory.api.common.UsageEventTypeB\x08\xfa\x42\x05\x82\x01\x02\x10\x01\x12\x19\n\x05route\x18\x06 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\xff\x03\x12\x38\n\x0ctechnologies\x18\x07 \x03(\x0e\x32\".sensory.api.common.TechnologyType\x12\x0e\n\x06models\x18\x08 \x03(\t\x12\x17\n\x0f\x61udioDurationMs\x18\t \x01(\x03\x12\x17\n\x0fvideoFrameCount\x18\n \x01(\x03\"\x1c\n\x1aPublishUsageEventsResponse2\x89\x01\n\x0c\x45ventService\x12y\n\x12PublishUsageEvents\x12/.sensory.api.v1.event.PublishUsageEventsRequest\x1a\x30.sensory.api.v1.event.PublishUsageEventsResponse\"\x00\x42t\n\x1c\x61i.sensorycloud.api.v1.eventB\x16SensoryApiV1EventProtoP\x01Z:gitlab.com/sensory-cloud/server/titan.git/pkg/api/v1/eventb\x06proto3'
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
  serialized_end=563,
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
  serialized_start=565,
  serialized_end=593,
)

_PUBLISHUSAGEEVENTSREQUEST.fields_by_name['events'].message_type = _USAGEEVENT
_USAGEEVENT.fields_by_name['timestamp'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_USAGEEVENT.fields_by_name['type'].enum_type = common_dot_common__pb2._USAGEEVENTTYPE
_USAGEEVENT.fields_by_name['technologies'].enum_type = common_dot_common__pb2._TECHNOLOGYTYPE
DESCRIPTOR.message_types_by_name['PublishUsageEventsRequest'] = _PUBLISHUSAGEEVENTSREQUEST
DESCRIPTOR.message_types_by_name['UsageEvent'] = _USAGEEVENT
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

_EVENTSERVICE = _descriptor.ServiceDescriptor(
  name='EventService',
  full_name='sensory.api.v1.event.EventService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=596,
  serialized_end=733,
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
])
_sym_db.RegisterServiceDescriptor(_EVENTSERVICE)

DESCRIPTOR.services_by_name['EventService'] = _EVENTSERVICE

# @@protoc_insertion_point(module_scope)
