# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import tracker_pb2 as tracker__pb2


class TrackerServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RegisterPeer = channel.unary_unary(
        '/TrackerService/RegisterPeer',
        request_serializer=tracker__pb2.RegisterPeerRequest.SerializeToString,
        response_deserializer=tracker__pb2.RegisterPeerResponse.FromString,
        )
    self.SearchFile = channel.unary_unary(
        '/TrackerService/SearchFile',
        request_serializer=tracker__pb2.SearchFileRequest.SerializeToString,
        response_deserializer=tracker__pb2.SearchFileResponse.FromString,
        )
    self.LeavePeer = channel.unary_unary(
        '/TrackerService/LeavePeer',
        request_serializer=tracker__pb2.LeavePeerRequest.SerializeToString,
        response_deserializer=tracker__pb2.LeavePeerResponse.FromString,
        )


class TrackerServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RegisterPeer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SearchFile(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def LeavePeer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TrackerServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RegisterPeer': grpc.unary_unary_rpc_method_handler(
          servicer.RegisterPeer,
          request_deserializer=tracker__pb2.RegisterPeerRequest.FromString,
          response_serializer=tracker__pb2.RegisterPeerResponse.SerializeToString,
      ),
      'SearchFile': grpc.unary_unary_rpc_method_handler(
          servicer.SearchFile,
          request_deserializer=tracker__pb2.SearchFileRequest.FromString,
          response_serializer=tracker__pb2.SearchFileResponse.SerializeToString,
      ),
      'LeavePeer': grpc.unary_unary_rpc_method_handler(
          servicer.LeavePeer,
          request_deserializer=tracker__pb2.LeavePeerRequest.FromString,
          response_serializer=tracker__pb2.LeavePeerResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'TrackerService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
