# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: tarefas.proto
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
    'tarefas.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rtarefas.proto\x12\x07tarefas\"G\n\x06Tarefa\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06titulo\x18\x02 \x01(\t\x12\x11\n\tdescricao\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\"7\n\x12\x43riarTarefaRequest\x12\x0e\n\x06titulo\x18\x01 \x01(\t\x12\x11\n\tdescricao\x18\x02 \x01(\t\"1\n\x0eTarefaResponse\x12\x1f\n\x06tarefa\x18\x01 \x01(\x0b\x32\x0f.tarefas.Tarefa\"\x16\n\x14ListarTarefasRequest\"9\n\x15ListarTarefasResponse\x12 \n\x07tarefas\x18\x01 \x03(\x0b\x32\x0f.tarefas.Tarefa2\xa5\x01\n\x0eTarefasService\x12\x43\n\x0b\x43riarTarefa\x12\x1b.tarefas.CriarTarefaRequest\x1a\x17.tarefas.TarefaResponse\x12N\n\rListarTarefas\x12\x1d.tarefas.ListarTarefasRequest\x1a\x1e.tarefas.ListarTarefasResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tarefas_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TAREFA']._serialized_start=26
  _globals['_TAREFA']._serialized_end=97
  _globals['_CRIARTAREFAREQUEST']._serialized_start=99
  _globals['_CRIARTAREFAREQUEST']._serialized_end=154
  _globals['_TAREFARESPONSE']._serialized_start=156
  _globals['_TAREFARESPONSE']._serialized_end=205
  _globals['_LISTARTAREFASREQUEST']._serialized_start=207
  _globals['_LISTARTAREFASREQUEST']._serialized_end=229
  _globals['_LISTARTAREFASRESPONSE']._serialized_start=231
  _globals['_LISTARTAREFASRESPONSE']._serialized_end=288
  _globals['_TAREFASSERVICE']._serialized_start=291
  _globals['_TAREFASSERVICE']._serialized_end=456
# @@protoc_insertion_point(module_scope)
