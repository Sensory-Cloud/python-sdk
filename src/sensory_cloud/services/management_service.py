import typing

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata
from sensory_cloud.generated.v1.management.enrollment_pb2_grpc import (
    EnrollmentServiceStub,
)
from sensory_cloud.generated.v1.management.enrollment_pb2 import (
    GetEnrollmentsRequest,
    GetEnrollmentsResponse,
    GetEnrollmentGroupsResponse,
    CreateEnrollmentGroupRequest,
    EnrollmentGroupResponse,
    AppendEnrollmentGroupRequest,
    DeleteEnrollmentRequest,
    EnrollmentResponse,
    DeleteEnrollmentGroupRequest,
)


class ManagementService:
    def __init__(self, config: Config, token_manager: ITokenManager):

        self._config = config
        self._token_manager = token_manager
        self._enrollment_client = EnrollmentServiceStub(config.channel)

    def get_enrollments(self, user_id: str) -> GetEnrollmentsResponse:

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: GetEnrollmentsRequest = GetEnrollmentsRequest(userId=user_id)

        return self._enrollment_client.GetEnrollments(
            request=request, metadata=metadata
        )

    def get_enrollment_groups(self, user_id: str) -> GetEnrollmentGroupsResponse:

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: GetEnrollmentsRequest = GetEnrollmentsRequest(userId=user_id)

        return self._enrollment_client.GetEnrollmentGroups(
            request=request, metadata=metadata
        )

    def create_enrollment_group(
        self,
        user_id: str,
        group_id: str,
        group_name: str,
        description: str,
        model_name: str,
        enrollment_ids: typing.List[str],
    ) -> EnrollmentGroupResponse:

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: CreateEnrollmentGroupRequest = CreateEnrollmentGroupRequest(
            userId=user_id,
            id=group_id,
            name=group_name,
            description=description,
            modelName=model_name,
            enrollmentIds=enrollment_ids,
        )

        return self._enrollment_client.CreateEnrollmentGroup(
            request=request, metadata=metadata
        )

    def append_enrollment_group(
        self, group_id: str, enrollment_ids: typing.List[str]
    ) -> EnrollmentGroupResponse:

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: AppendEnrollmentGroupRequest = AppendEnrollmentGroupRequest(
            groupId=group_id
        )
        request.enrollmentIds += enrollment_ids

        return self._enrollment_client.AppendEnrollmentGroup(
            request=request, metadata=metadata
        )

    def delete_enrollment(self, id: str) -> EnrollmentResponse:

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: DeleteEnrollmentRequest = DeleteEnrollmentRequest(id=id)

        return self._enrollment_client.DeleteEnrollment(
            request=request, metadata=metadata
        )

    def delete_enrollment_group(self, group_id: str) -> EnrollmentGroupResponse:

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: DeleteEnrollmentGroupRequest = DeleteEnrollmentGroupRequest(
            id=group_id
        )

        return self._enrollment_client.DeleteEnrollmentGroup(
            request=request, metadata=metadata
        )
