import typing

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata

import sensory_cloud.generated.v1.management.enrollment_pb2_grpc as enrollment_pb2_grpc
import sensory_cloud.generated.v1.management.enrollment_pb2 as enrollment_pb2


class ManagementService:
    """
    Class to handle all typical CRUD functions
    """

    def __init__(self, config: Config, token_manager: ITokenManager):
        """
        Constructor method for the ManagementService class

        Arguments:
            config: Config object containing the relevant grpc connection information
            token_manager: ITokenManager object that generates and returns JWT metadata
        """

        self._config = config
        self._token_manager = token_manager
        self._enrollment_client = enrollment_pb2_grpc.EnrollmentServiceStub(
            config.channel
        )

    def get_enrollments(self, user_id: str) -> enrollment_pb2.GetEnrollmentsResponse:
        """
        Method that obtains all of the active enrollments given the user_id

        Arguments:
            user_id: String containing the user id

        Returns:
            A GetEnrollmentsResponse object
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: enrollment_pb2.GetEnrollmentsRequest = (
            enrollment_pb2.GetEnrollmentsRequest(userId=user_id)
        )

        return self._enrollment_client.GetEnrollments(
            request=request, metadata=metadata
        )

    def get_enrollment_groups(
        self, user_id: str
    ) -> enrollment_pb2.GetEnrollmentGroupsResponse:
        """
        Method that obtains all of the active enrollment groups registered by this user_id

        Arguments:
            user_id: String containing the user id

        Returns:
            A GetEnrollmentGroupsResponse object
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: enrollment_pb2.GetEnrollmentsRequest = (
            enrollment_pb2.GetEnrollmentsRequest(userId=user_id)
        )

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
    ) -> enrollment_pb2.EnrollmentGroupResponse:
        """
        Method that registers a new enrollment group. Enrollment groups can contain up to 10 enrollments,
        and they enable multiple users to be recognized with the same request.

        Arguments:
            user_id: String containing the user id
            group_id: String containing the enrollment group id
            group_name: String containing the name of the enrollment group
            description: String containing a brief description of this group
            model_name: String containing the exact name of the model tied to this enrollment group
            enrollment_ids: List of enrollment id strings to add to the new enrollment group
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: enrollment_pb2.CreateEnrollmentGroupRequest = (
            enrollment_pb2.CreateEnrollmentGroupRequest(
                userId=user_id,
                id=group_id,
                name=group_name,
                description=description,
                modelName=model_name,
                enrollmentIds=enrollment_ids,
            )
        )

        return self._enrollment_client.CreateEnrollmentGroup(
            request=request, metadata=metadata
        )

    def append_enrollment_group(
        self, group_id: str, enrollment_ids: typing.List[str]
    ) -> enrollment_pb2.EnrollmentGroupResponse:
        """
        Method that adds a new enrollment to an enrollment group

        Arguments:
            group_id: String containing the enrollment group id
            enrollment_ids: List of enrollment id strings the enrollmentIds to
                be associated with this group. Max 10.

        Returns:
            An EnrollmentGroupResponse object
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: enrollment_pb2.AppendEnrollmentGroupRequest = (
            enrollment_pb2.AppendEnrollmentGroupRequest(groupId=group_id)
        )
        request.enrollmentIds.extend(enrollment_ids)

        return self._enrollment_client.AppendEnrollmentGroup(
            request=request, metadata=metadata
        )

    def delete_enrollment(self, id: str) -> enrollment_pb2.EnrollmentResponse:
        """
        Removes an enrollment from the system

        Arguments:
            id: String containing the enrollment id to be removed

        Returns:
            An EnrollmentResponse object
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: enrollment_pb2.DeleteEnrollmentRequest = (
            enrollment_pb2.DeleteEnrollmentRequest(id=id)
        )

        return self._enrollment_client.DeleteEnrollment(
            request=request, metadata=metadata
        )

    def delete_enrollment_group(
        self, group_id: str
    ) -> enrollment_pb2.EnrollmentGroupResponse:
        """
        Method that removes an enrollment group from the system

        Arguments:
            group_id: String containing the enrollment group to be removed

        Returns:
            An EnrollmentGroupResponse object
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: enrollment_pb2.DeleteEnrollmentGroupRequest = (
            enrollment_pb2.DeleteEnrollmentGroupRequest(id=group_id)
        )

        return self._enrollment_client.DeleteEnrollmentGroup(
            request=request, metadata=metadata
        )
