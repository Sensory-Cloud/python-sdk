# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: oauth/oauth.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from sensory_cloud.generated.validate import validate_pb2 as validate_dot_validate__pb2
from sensory_cloud.generated.common import common_pb2 as common_dot_common__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='oauth/oauth.proto',
  package='sensory.api.oauth',
  syntax='proto3',
  serialized_options=b'\n\031ai.sensorycloud.api.oauthB\024SensoryApiOauthProtoP\001Z7gitlab.com/sensory-cloud/server/titan.git/pkg/api/oauth\242\002\004SENG',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11oauth/oauth.proto\x12\x11sensory.api.oauth\x1a\x17validate/validate.proto\x1a\x13\x63ommon/common.proto\":\n\x0cTokenRequest\x12\x1a\n\x08\x63lientId\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\x12\x0e\n\x06secret\x18\x02 \x01(\t\"\xdf\x01\n\x10SignTokenRequest\x12\x1a\n\x07subject\x18\x01 \x01(\tB\t\xfa\x42\x06r\x04\x10\x01\x18\x7f\x12G\n\x05scope\x18\x02 \x01(\x0e\x32..sensory.api.oauth.SignTokenRequest.TokenScopeB\x08\xfa\x42\x05\x82\x01\x02\x10\x01\"f\n\nTokenScope\x12\x08\n\x04USER\x10\x00\x12\x0f\n\x0bSUPER_ADMIN\x10\x01\x12\x11\n\rBILLING_ADMIN\x10\x02\x12\x13\n\x0fREAD_ONLY_ADMIN\x10\x03\x12\x15\n\x11\x45MAIL_SELF_VERIFY\x10\x04\"\x0f\n\rWhoAmIRequest\"4\n\x0eWhoAmIResponse\x12\x10\n\x08\x63lientId\x18\x01 \x01(\t\x12\x10\n\x08tenantId\x18\x02 \x01(\t\"+\n\x10PublicKeyRequest\x12\x17\n\x05keyId\x18\x01 \x01(\tB\x08\xfa\x42\x05r\x03\xb0\x01\x01\"T\n\x11PublicKeyResponse\x12\x11\n\tpublicKey\x18\x01 \x01(\x0c\x12,\n\x07keyType\x18\x02 \x01(\x0e\x32\x1b.sensory.api.common.KeyType2\xe8\x02\n\x0cOauthService\x12P\n\x08GetToken\x12\x1f.sensory.api.oauth.TokenRequest\x1a!.sensory.api.common.TokenResponse\"\x00\x12U\n\tSignToken\x12#.sensory.api.oauth.SignTokenRequest\x1a!.sensory.api.common.TokenResponse\"\x00\x12R\n\tGetWhoAmI\x12 .sensory.api.oauth.WhoAmIRequest\x1a!.sensory.api.oauth.WhoAmIResponse\"\x00\x12[\n\x0cGetPublicKey\x12#.sensory.api.oauth.PublicKeyRequest\x1a$.sensory.api.oauth.PublicKeyResponse\"\x00\x42s\n\x19\x61i.sensorycloud.api.oauthB\x14SensoryApiOauthProtoP\x01Z7gitlab.com/sensory-cloud/server/titan.git/pkg/api/oauth\xa2\x02\x04SENGb\x06proto3'
  ,
  dependencies=[validate_dot_validate__pb2.DESCRIPTOR,common_dot_common__pb2.DESCRIPTOR,])



_SIGNTOKENREQUEST_TOKENSCOPE = _descriptor.EnumDescriptor(
  name='TokenScope',
  full_name='sensory.api.oauth.SignTokenRequest.TokenScope',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='USER', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SUPER_ADMIN', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BILLING_ADMIN', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='READ_ONLY_ADMIN', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='EMAIL_SELF_VERIFY', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=268,
  serialized_end=370,
)
_sym_db.RegisterEnumDescriptor(_SIGNTOKENREQUEST_TOKENSCOPE)


_TOKENREQUEST = _descriptor.Descriptor(
  name='TokenRequest',
  full_name='sensory.api.oauth.TokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientId', full_name='sensory.api.oauth.TokenRequest.clientId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005r\003\260\001\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='secret', full_name='sensory.api.oauth.TokenRequest.secret', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=86,
  serialized_end=144,
)


_SIGNTOKENREQUEST = _descriptor.Descriptor(
  name='SignTokenRequest',
  full_name='sensory.api.oauth.SignTokenRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='subject', full_name='sensory.api.oauth.SignTokenRequest.subject', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\006r\004\020\001\030\177', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scope', full_name='sensory.api.oauth.SignTokenRequest.scope', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\202\001\002\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SIGNTOKENREQUEST_TOKENSCOPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=370,
)


_WHOAMIREQUEST = _descriptor.Descriptor(
  name='WhoAmIRequest',
  full_name='sensory.api.oauth.WhoAmIRequest',
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
  serialized_start=372,
  serialized_end=387,
)


_WHOAMIRESPONSE = _descriptor.Descriptor(
  name='WhoAmIResponse',
  full_name='sensory.api.oauth.WhoAmIResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientId', full_name='sensory.api.oauth.WhoAmIResponse.clientId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.oauth.WhoAmIResponse.tenantId', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=389,
  serialized_end=441,
)


_PUBLICKEYREQUEST = _descriptor.Descriptor(
  name='PublicKeyRequest',
  full_name='sensory.api.oauth.PublicKeyRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='keyId', full_name='sensory.api.oauth.PublicKeyRequest.keyId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005r\003\260\001\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=443,
  serialized_end=486,
)


_PUBLICKEYRESPONSE = _descriptor.Descriptor(
  name='PublicKeyResponse',
  full_name='sensory.api.oauth.PublicKeyResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='publicKey', full_name='sensory.api.oauth.PublicKeyResponse.publicKey', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='keyType', full_name='sensory.api.oauth.PublicKeyResponse.keyType', index=1,
      number=2, type=14, cpp_type=8, label=1,
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
  serialized_start=488,
  serialized_end=572,
)

_SIGNTOKENREQUEST.fields_by_name['scope'].enum_type = _SIGNTOKENREQUEST_TOKENSCOPE
_SIGNTOKENREQUEST_TOKENSCOPE.containing_type = _SIGNTOKENREQUEST
_PUBLICKEYRESPONSE.fields_by_name['keyType'].enum_type = common_dot_common__pb2._KEYTYPE
DESCRIPTOR.message_types_by_name['TokenRequest'] = _TOKENREQUEST
DESCRIPTOR.message_types_by_name['SignTokenRequest'] = _SIGNTOKENREQUEST
DESCRIPTOR.message_types_by_name['WhoAmIRequest'] = _WHOAMIREQUEST
DESCRIPTOR.message_types_by_name['WhoAmIResponse'] = _WHOAMIRESPONSE
DESCRIPTOR.message_types_by_name['PublicKeyRequest'] = _PUBLICKEYREQUEST
DESCRIPTOR.message_types_by_name['PublicKeyResponse'] = _PUBLICKEYRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TokenRequest = _reflection.GeneratedProtocolMessageType('TokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _TOKENREQUEST,
  '__module__' : 'oauth.oauth_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.oauth.TokenRequest)
  })
_sym_db.RegisterMessage(TokenRequest)

SignTokenRequest = _reflection.GeneratedProtocolMessageType('SignTokenRequest', (_message.Message,), {
  'DESCRIPTOR' : _SIGNTOKENREQUEST,
  '__module__' : 'oauth.oauth_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.oauth.SignTokenRequest)
  })
_sym_db.RegisterMessage(SignTokenRequest)

WhoAmIRequest = _reflection.GeneratedProtocolMessageType('WhoAmIRequest', (_message.Message,), {
  'DESCRIPTOR' : _WHOAMIREQUEST,
  '__module__' : 'oauth.oauth_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.oauth.WhoAmIRequest)
  })
_sym_db.RegisterMessage(WhoAmIRequest)

WhoAmIResponse = _reflection.GeneratedProtocolMessageType('WhoAmIResponse', (_message.Message,), {
  'DESCRIPTOR' : _WHOAMIRESPONSE,
  '__module__' : 'oauth.oauth_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.oauth.WhoAmIResponse)
  })
_sym_db.RegisterMessage(WhoAmIResponse)

PublicKeyRequest = _reflection.GeneratedProtocolMessageType('PublicKeyRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUBLICKEYREQUEST,
  '__module__' : 'oauth.oauth_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.oauth.PublicKeyRequest)
  })
_sym_db.RegisterMessage(PublicKeyRequest)

PublicKeyResponse = _reflection.GeneratedProtocolMessageType('PublicKeyResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUBLICKEYRESPONSE,
  '__module__' : 'oauth.oauth_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.oauth.PublicKeyResponse)
  })
_sym_db.RegisterMessage(PublicKeyResponse)


DESCRIPTOR._options = None
_TOKENREQUEST.fields_by_name['clientId']._options = None
_SIGNTOKENREQUEST.fields_by_name['subject']._options = None
_SIGNTOKENREQUEST.fields_by_name['scope']._options = None
_PUBLICKEYREQUEST.fields_by_name['keyId']._options = None

_OAUTHSERVICE = _descriptor.ServiceDescriptor(
  name='OauthService',
  full_name='sensory.api.oauth.OauthService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=575,
  serialized_end=935,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetToken',
    full_name='sensory.api.oauth.OauthService.GetToken',
    index=0,
    containing_service=None,
    input_type=_TOKENREQUEST,
    output_type=common_dot_common__pb2._TOKENRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SignToken',
    full_name='sensory.api.oauth.OauthService.SignToken',
    index=1,
    containing_service=None,
    input_type=_SIGNTOKENREQUEST,
    output_type=common_dot_common__pb2._TOKENRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetWhoAmI',
    full_name='sensory.api.oauth.OauthService.GetWhoAmI',
    index=2,
    containing_service=None,
    input_type=_WHOAMIREQUEST,
    output_type=_WHOAMIRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetPublicKey',
    full_name='sensory.api.oauth.OauthService.GetPublicKey',
    index=3,
    containing_service=None,
    input_type=_PUBLICKEYREQUEST,
    output_type=_PUBLICKEYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_OAUTHSERVICE)

DESCRIPTOR.services_by_name['OauthService'] = _OAUTHSERVICE

# @@protoc_insertion_point(module_scope)
