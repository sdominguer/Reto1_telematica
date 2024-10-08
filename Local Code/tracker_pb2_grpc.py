# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import tracker_pb2 as tracker__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in tracker_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class TrackerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterPeer = channel.unary_unary(
                '/TrackerService/RegisterPeer',
                request_serializer=tracker__pb2.RegisterPeerRequest.SerializeToString,
                response_deserializer=tracker__pb2.RegisterPeerResponse.FromString,
                _registered_method=True)
        self.SearchFile = channel.unary_unary(
                '/TrackerService/SearchFile',
                request_serializer=tracker__pb2.SearchFileRequest.SerializeToString,
                response_deserializer=tracker__pb2.SearchFileResponse.FromString,
                _registered_method=True)
        self.LeavePeer = channel.unary_unary(
                '/TrackerService/LeavePeer',
                request_serializer=tracker__pb2.LeavePeerRequest.SerializeToString,
                response_deserializer=tracker__pb2.LeavePeerResponse.FromString,
                _registered_method=True)


class TrackerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterPeer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LeavePeer(self, request, context):
        """Missing associated documentation comment in .proto file."""
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
    server.add_registered_method_handlers('TrackerService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class TrackerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterPeer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TrackerService/RegisterPeer',
            tracker__pb2.RegisterPeerRequest.SerializeToString,
            tracker__pb2.RegisterPeerResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SearchFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TrackerService/SearchFile',
            tracker__pb2.SearchFileRequest.SerializeToString,
            tracker__pb2.SearchFileResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def LeavePeer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/TrackerService/LeavePeer',
            tracker__pb2.LeavePeerRequest.SerializeToString,
            tracker__pb2.LeavePeerResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
