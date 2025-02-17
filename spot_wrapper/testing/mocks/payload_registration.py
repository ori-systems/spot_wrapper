# Copyright (c) 2023 Boston Dynamics AI Institute LLC. See LICENSE file for more info.

import typing

import grpc
from bosdyn.api.payload_pb2 import Payload
from bosdyn.api.payload_registration_pb2 import (
    GetPayloadAuthTokenRequest,
    GetPayloadAuthTokenResponse,
    RegisterPayloadRequest,
    RegisterPayloadResponse,
    UpdatePayloadAttachedRequest,
    UpdatePayloadAttachedResponse,
    UpdatePayloadVersionRequest,
    UpdatePayloadVersionResponse,
)
from bosdyn.api.payload_registration_service_pb2_grpc import (
    PayloadRegistrationServiceServicer,
)


class MockPayloadRegistrationService(PayloadRegistrationServiceServicer):
    """
    A mock Spot payload registration service.

    It bookkeeps all payloads but enforces nothing.
    """

    def __init__(self, **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)
        self._payloads: typing.Dict[str, Payload] = {}

    def RegisterPayload(
        self, request: RegisterPayloadRequest, context: grpc.ServicerContext
    ) -> RegisterPayloadResponse:
        response = RegisterPayloadResponse()
        if request.payload.GUID in self._payloads:
            response.status = RegisterPayloadResponse.Status.STATUS_ALREADY_EXISTS
            return response
        payload = Payload()
        payload.CopyFrom(request.payload)
        self._payloads[payload.GUID] = payload
        response.status = RegisterPayloadResponse.Status.STATUS_OK
        return response

    def UpdatePayloadVersion(
        self, request: UpdatePayloadVersionRequest, context: grpc.ServicerContext
    ) -> UpdatePayloadVersionResponse:
        response = UpdatePayloadVersionResponse()
        if request.payload_credentials.guid not in self._payloads:
            response.status = UpdatePayloadAttachedResponse.Status.STATUS_DOES_NOT_EXIST
            return response
        response.status = UpdatePayloadAttachedResponse.Status.STATUS_OK
        return response

    def GetPayloadAuthToken(
        self, request: GetPayloadAuthTokenRequest, context: grpc.ServicerContext
    ) -> GetPayloadAuthTokenResponse:
        response = GetPayloadAuthTokenResponse()
        if request.payload_credentials.guid not in self._payloads:
            response.status = (
                GetPayloadAuthTokenResponse.Status.STATUS_INVALID_CREDENTIALS
            )
            return response
        response.status = GetPayloadAuthTokenResponse.Status.STATUS_OK
        response.token = "mock-payload-token"
        return response

    def UpdatePayloadAttached(
        self, request: UpdatePayloadAttachedRequest, context: grpc.ServicerContext
    ) -> UpdatePayloadAttachedResponse:
        response = UpdatePayloadAttachedResponse()
        if request.payload_credentials.guid not in self._payloads:
            response.status = UpdatePayloadAttachedResponse.Status.STATUS_DOES_NOT_EXIST
            return response
        response.status = UpdatePayloadAttachedResponse.Status.STATUS_OK
        return response
