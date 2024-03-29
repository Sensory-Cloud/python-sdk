# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: v1/file/file.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from sensory_cloud.generated.validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='v1/file/file.proto',
  package='sensory.api.v1.file',
  syntax='proto3',
  serialized_options=b'\n\033ai.sensorycloud.api.v1.fileB\025SensoryApiV1FileProtoP\001Z9gitlab.com/sensory-cloud/server/titan.git/pkg/api/v1/file\242\002\004SENG',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x12v1/file/file.proto\x12\x13sensory.api.v1.file\x1a\x17validate/validate.proto\"u\n\x0b\x46ileRequest\x12\x18\n\x04\x66ile\x18\x01 \x01(\tB\n\xfa\x42\x07r\x05\x10\x01\x18\xff\x0f\x12<\n\x08\x63\x61tegory\x18\x02 \x01(\x0b\x32*.sensory.api.v1.file.VersionedFileCategory\x12\x0e\n\x06offset\x18\x03 \x01(\x03\"\x95\x01\n\x0c\x46ileResponse\x12-\n\x04info\x18\x01 \x01(\x0b\x32\x1d.sensory.api.v1.file.FileInfoH\x00\x12/\n\x05\x63hunk\x18\x02 \x01(\x0b\x32\x1e.sensory.api.v1.file.FileChunkH\x00\x12\x10\n\x08\x63omplete\x18\x03 \x01(\x08\x42\x13\n\x11streamingResponse\"^\n\x12\x46ileCatalogRequest\x12H\n\ncategories\x18\x01 \x03(\x0b\x32*.sensory.api.v1.file.VersionedFileCategoryB\x08\xfa\x42\x05\x92\x01\x02\x08\x01\".\n\x1a\x46ileCompleteCatalogRequest\x12\x10\n\x08tenantId\x18\x01 \x01(\t\"H\n\x13\x46ileCatalogResponse\x12\x31\n\x07\x63\x61talog\x18\x01 \x03(\x0b\x32 .sensory.api.v1.file.FileCatalog\"*\n\tFileChunk\x12\r\n\x05\x62ytes\x18\x01 \x01(\x0c\x12\x0e\n\x06offset\x18\x02 \x01(\x03\"q\n\x08\x46ileInfo\x12\x0c\n\x04\x66ile\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x62solutePath\x18\x02 \x01(\t\x12\x0c\n\x04size\x18\x03 \x01(\x03\x12\x13\n\x0b\x63ontentType\x18\x04 \x01(\t\x12\x0c\n\x04hash\x18\x05 \x01(\t\x12\x10\n\x08tenantId\x18\x06 \x01(\t\"y\n\x0b\x46ileCatalog\x12,\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x1d.sensory.api.v1.file.FileInfo\x12<\n\x08\x63\x61tegory\x18\x02 \x01(\x0b\x32*.sensory.api.v1.file.VersionedFileCategory\"g\n\x15VersionedFileCategory\x12=\n\x08\x63\x61tegory\x18\x01 \x01(\x0e\x32!.sensory.api.v1.file.FileCategoryB\x08\xfa\x42\x05\x82\x01\x02\x10\x01\x12\x0f\n\x07version\x18\x02 \x01(\t*K\n\x0c\x46ileCategory\x12\x0e\n\nTSSV_MODEL\x10\x00\x12\x0f\n\x0b\x41TLAS_MODEL\x10\x01\x12\r\n\tTNL_MODEL\x10\x02\x12\x0b\n\x07UNKNOWN\x10\x64\x32\xff\x02\n\x04\x46ile\x12L\n\x07GetInfo\x12 .sensory.api.v1.file.FileRequest\x1a\x1d.sensory.api.v1.file.FileInfo\"\x00\x12\x61\n\nGetCatalog\x12\'.sensory.api.v1.file.FileCatalogRequest\x1a(.sensory.api.v1.file.FileCatalogResponse\"\x00\x12q\n\x12GetCompleteCatalog\x12/.sensory.api.v1.file.FileCompleteCatalogRequest\x1a(.sensory.api.v1.file.FileCatalogResponse\"\x00\x12S\n\x08\x44ownload\x12 .sensory.api.v1.file.FileRequest\x1a!.sensory.api.v1.file.FileResponse\"\x00\x30\x01\x42x\n\x1b\x61i.sensorycloud.api.v1.fileB\x15SensoryApiV1FileProtoP\x01Z9gitlab.com/sensory-cloud/server/titan.git/pkg/api/v1/file\xa2\x02\x04SENGb\x06proto3'
  ,
  dependencies=[validate_dot_validate__pb2.DESCRIPTOR,])

_FILECATEGORY = _descriptor.EnumDescriptor(
  name='FileCategory',
  full_name='sensory.api.v1.file.FileCategory',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TSSV_MODEL', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ATLAS_MODEL', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TNL_MODEL', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=3, number=100,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=944,
  serialized_end=1019,
)
_sym_db.RegisterEnumDescriptor(_FILECATEGORY)

FileCategory = enum_type_wrapper.EnumTypeWrapper(_FILECATEGORY)
TSSV_MODEL = 0
ATLAS_MODEL = 1
TNL_MODEL = 2
UNKNOWN = 100



_FILEREQUEST = _descriptor.Descriptor(
  name='FileRequest',
  full_name='sensory.api.v1.file.FileRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file', full_name='sensory.api.v1.file.FileRequest.file', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\007r\005\020\001\030\377\017', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='category', full_name='sensory.api.v1.file.FileRequest.category', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='sensory.api.v1.file.FileRequest.offset', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  serialized_start=68,
  serialized_end=185,
)


_FILERESPONSE = _descriptor.Descriptor(
  name='FileResponse',
  full_name='sensory.api.v1.file.FileResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='sensory.api.v1.file.FileResponse.info', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chunk', full_name='sensory.api.v1.file.FileResponse.chunk', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='complete', full_name='sensory.api.v1.file.FileResponse.complete', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
    _descriptor.OneofDescriptor(
      name='streamingResponse', full_name='sensory.api.v1.file.FileResponse.streamingResponse',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=188,
  serialized_end=337,
)


_FILECATALOGREQUEST = _descriptor.Descriptor(
  name='FileCatalogRequest',
  full_name='sensory.api.v1.file.FileCatalogRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='categories', full_name='sensory.api.v1.file.FileCatalogRequest.categories', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\222\001\002\010\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=339,
  serialized_end=433,
)


_FILECOMPLETECATALOGREQUEST = _descriptor.Descriptor(
  name='FileCompleteCatalogRequest',
  full_name='sensory.api.v1.file.FileCompleteCatalogRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.v1.file.FileCompleteCatalogRequest.tenantId', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=435,
  serialized_end=481,
)


_FILECATALOGRESPONSE = _descriptor.Descriptor(
  name='FileCatalogResponse',
  full_name='sensory.api.v1.file.FileCatalogResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='catalog', full_name='sensory.api.v1.file.FileCatalogResponse.catalog', index=0,
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
  serialized_start=483,
  serialized_end=555,
)


_FILECHUNK = _descriptor.Descriptor(
  name='FileChunk',
  full_name='sensory.api.v1.file.FileChunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bytes', full_name='sensory.api.v1.file.FileChunk.bytes', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='sensory.api.v1.file.FileChunk.offset', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=557,
  serialized_end=599,
)


_FILEINFO = _descriptor.Descriptor(
  name='FileInfo',
  full_name='sensory.api.v1.file.FileInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file', full_name='sensory.api.v1.file.FileInfo.file', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='absolutePath', full_name='sensory.api.v1.file.FileInfo.absolutePath', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='sensory.api.v1.file.FileInfo.size', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='contentType', full_name='sensory.api.v1.file.FileInfo.contentType', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hash', full_name='sensory.api.v1.file.FileInfo.hash', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tenantId', full_name='sensory.api.v1.file.FileInfo.tenantId', index=5,
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
  serialized_start=601,
  serialized_end=714,
)


_FILECATALOG = _descriptor.Descriptor(
  name='FileCatalog',
  full_name='sensory.api.v1.file.FileCatalog',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='files', full_name='sensory.api.v1.file.FileCatalog.files', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='category', full_name='sensory.api.v1.file.FileCatalog.category', index=1,
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
  serialized_start=716,
  serialized_end=837,
)


_VERSIONEDFILECATEGORY = _descriptor.Descriptor(
  name='VersionedFileCategory',
  full_name='sensory.api.v1.file.VersionedFileCategory',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='category', full_name='sensory.api.v1.file.VersionedFileCategory.category', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\372B\005\202\001\002\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='sensory.api.v1.file.VersionedFileCategory.version', index=1,
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
  serialized_start=839,
  serialized_end=942,
)

_FILEREQUEST.fields_by_name['category'].message_type = _VERSIONEDFILECATEGORY
_FILERESPONSE.fields_by_name['info'].message_type = _FILEINFO
_FILERESPONSE.fields_by_name['chunk'].message_type = _FILECHUNK
_FILERESPONSE.oneofs_by_name['streamingResponse'].fields.append(
  _FILERESPONSE.fields_by_name['info'])
_FILERESPONSE.fields_by_name['info'].containing_oneof = _FILERESPONSE.oneofs_by_name['streamingResponse']
_FILERESPONSE.oneofs_by_name['streamingResponse'].fields.append(
  _FILERESPONSE.fields_by_name['chunk'])
_FILERESPONSE.fields_by_name['chunk'].containing_oneof = _FILERESPONSE.oneofs_by_name['streamingResponse']
_FILECATALOGREQUEST.fields_by_name['categories'].message_type = _VERSIONEDFILECATEGORY
_FILECATALOGRESPONSE.fields_by_name['catalog'].message_type = _FILECATALOG
_FILECATALOG.fields_by_name['files'].message_type = _FILEINFO
_FILECATALOG.fields_by_name['category'].message_type = _VERSIONEDFILECATEGORY
_VERSIONEDFILECATEGORY.fields_by_name['category'].enum_type = _FILECATEGORY
DESCRIPTOR.message_types_by_name['FileRequest'] = _FILEREQUEST
DESCRIPTOR.message_types_by_name['FileResponse'] = _FILERESPONSE
DESCRIPTOR.message_types_by_name['FileCatalogRequest'] = _FILECATALOGREQUEST
DESCRIPTOR.message_types_by_name['FileCompleteCatalogRequest'] = _FILECOMPLETECATALOGREQUEST
DESCRIPTOR.message_types_by_name['FileCatalogResponse'] = _FILECATALOGRESPONSE
DESCRIPTOR.message_types_by_name['FileChunk'] = _FILECHUNK
DESCRIPTOR.message_types_by_name['FileInfo'] = _FILEINFO
DESCRIPTOR.message_types_by_name['FileCatalog'] = _FILECATALOG
DESCRIPTOR.message_types_by_name['VersionedFileCategory'] = _VERSIONEDFILECATEGORY
DESCRIPTOR.enum_types_by_name['FileCategory'] = _FILECATEGORY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FileRequest = _reflection.GeneratedProtocolMessageType('FileRequest', (_message.Message,), {
  'DESCRIPTOR' : _FILEREQUEST,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileRequest)
  })
_sym_db.RegisterMessage(FileRequest)

FileResponse = _reflection.GeneratedProtocolMessageType('FileResponse', (_message.Message,), {
  'DESCRIPTOR' : _FILERESPONSE,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileResponse)
  })
_sym_db.RegisterMessage(FileResponse)

FileCatalogRequest = _reflection.GeneratedProtocolMessageType('FileCatalogRequest', (_message.Message,), {
  'DESCRIPTOR' : _FILECATALOGREQUEST,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileCatalogRequest)
  })
_sym_db.RegisterMessage(FileCatalogRequest)

FileCompleteCatalogRequest = _reflection.GeneratedProtocolMessageType('FileCompleteCatalogRequest', (_message.Message,), {
  'DESCRIPTOR' : _FILECOMPLETECATALOGREQUEST,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileCompleteCatalogRequest)
  })
_sym_db.RegisterMessage(FileCompleteCatalogRequest)

FileCatalogResponse = _reflection.GeneratedProtocolMessageType('FileCatalogResponse', (_message.Message,), {
  'DESCRIPTOR' : _FILECATALOGRESPONSE,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileCatalogResponse)
  })
_sym_db.RegisterMessage(FileCatalogResponse)

FileChunk = _reflection.GeneratedProtocolMessageType('FileChunk', (_message.Message,), {
  'DESCRIPTOR' : _FILECHUNK,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileChunk)
  })
_sym_db.RegisterMessage(FileChunk)

FileInfo = _reflection.GeneratedProtocolMessageType('FileInfo', (_message.Message,), {
  'DESCRIPTOR' : _FILEINFO,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileInfo)
  })
_sym_db.RegisterMessage(FileInfo)

FileCatalog = _reflection.GeneratedProtocolMessageType('FileCatalog', (_message.Message,), {
  'DESCRIPTOR' : _FILECATALOG,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.FileCatalog)
  })
_sym_db.RegisterMessage(FileCatalog)

VersionedFileCategory = _reflection.GeneratedProtocolMessageType('VersionedFileCategory', (_message.Message,), {
  'DESCRIPTOR' : _VERSIONEDFILECATEGORY,
  '__module__' : 'v1.file.file_pb2'
  # @@protoc_insertion_point(class_scope:sensory.api.v1.file.VersionedFileCategory)
  })
_sym_db.RegisterMessage(VersionedFileCategory)


DESCRIPTOR._options = None
_FILEREQUEST.fields_by_name['file']._options = None
_FILECATALOGREQUEST.fields_by_name['categories']._options = None
_VERSIONEDFILECATEGORY.fields_by_name['category']._options = None

_FILE = _descriptor.ServiceDescriptor(
  name='File',
  full_name='sensory.api.v1.file.File',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1022,
  serialized_end=1405,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetInfo',
    full_name='sensory.api.v1.file.File.GetInfo',
    index=0,
    containing_service=None,
    input_type=_FILEREQUEST,
    output_type=_FILEINFO,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCatalog',
    full_name='sensory.api.v1.file.File.GetCatalog',
    index=1,
    containing_service=None,
    input_type=_FILECATALOGREQUEST,
    output_type=_FILECATALOGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetCompleteCatalog',
    full_name='sensory.api.v1.file.File.GetCompleteCatalog',
    index=2,
    containing_service=None,
    input_type=_FILECOMPLETECATALOGREQUEST,
    output_type=_FILECATALOGRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Download',
    full_name='sensory.api.v1.file.File.Download',
    index=3,
    containing_service=None,
    input_type=_FILEREQUEST,
    output_type=_FILERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FILE)

DESCRIPTOR.services_by_name['File'] = _FILE

# @@protoc_insertion_point(module_scope)
