import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config
from sensory_cloud.generated.v1.management.enrollment_pb2 import (
    CreateEnrollmentGroupRequest,
    EnrollmentGroupResponse,
    EnrollmentResponse,
    GetEnrollmentGroupsResponse,
    GetEnrollmentsResponse,
)
from sensory_cloud.services.management_service import ManagementService
from sensory_cloud.generated.v1.management.enrollment_pb2_grpc import (
    EnrollmentServiceStub,
)
from sensory_cloud.token_manager import ITokenManager, Metadata


class MockTokenManager(ITokenManager):
    def __init__(self, token: str = "token"):
        self._token = token

    def get_token(self) -> str:
        return self._token

    def get_authorization_metadata(self) -> Metadata:
        token: str = self.get_token()
        return (("authorization", f"Bearer {token}"),)


class MockManagementService(ManagementService):
    def __init__(
        self,
        config: Config,
        token_manager: ITokenManager,
        enrollment_client: EnrollmentServiceStub,
    ):

        self._config = config
        self._token_manager = token_manager
        self._enrollment_client = enrollment_client


class ManagmentServiceTest(unittest.TestCase):

    config: Config = Config(
        fully_qualified_domain_name="domain.name", tenant_id="tenant-id"
    )
    config.connect()

    enrollment_client: EnrollmentServiceStub = EnrollmentServiceStub(
        channel=config.channel
    )

    token_manager: MockTokenManager = MockTokenManager()

    def test_get_enrollments(self):
        self.config.connect()

        response: GetEnrollmentsResponse = GetEnrollmentsResponse(
            enrollments=[
                EnrollmentResponse(
                    description="enrollment", didEnrollWithLiveness=False
                )
            ]
        )

        self.enrollment_client.GetEnrollments = MagicMock(return_value=response)

        management_service: MockManagementService = MockManagementService(
            config=self.config,
            token_manager=self.token_manager,
            enrollment_client=self.enrollment_client,
        )

        enrollment_response: GetEnrollmentsResponse = (
            management_service.get_enrollments(user_id="user-id")
        )

        self.assertEqual(response, enrollment_response)

        self.config.channel.close()

    def test_get_enrollment_groups(self):
        self.config.connect()

        user_id: str = "user-id"

        response: GetEnrollmentGroupsResponse = GetEnrollmentGroupsResponse(
            enrollmentGroups=[
                EnrollmentGroupResponse(
                    description="enrollment group", modelName="my-model"
                )
            ]
        )

        self.enrollment_client.GetEnrollmentGroups = MagicMock(return_value=response)

        management_service: MockManagementService = MockManagementService(
            config=self.config,
            token_manager=self.token_manager,
            enrollment_client=self.enrollment_client,
        )

        enrollment_group_response: GetEnrollmentGroupsResponse = (
            management_service.get_enrollment_groups(user_id="user-id")
        )

        self.assertEqual(response, enrollment_group_response)

        self.config.channel.close()

    def test_create_enrollment_group(self):
        self.config.connect()

        response: EnrollmentGroupResponse = EnrollmentGroupResponse(
            description="enrollment group", modelName="my-model"
        )

        self.enrollment_client.CreateEnrollmentGroup = MagicMock(return_value=response)

        management_service: MockManagementService = MockManagementService(
            config=self.config,
            token_manager=self.token_manager,
            enrollment_client=self.enrollment_client,
        )

        enrollment_group_response: EnrollmentGroupResponse = (
            management_service.create_enrollment_group(
                user_id="user-id",
                group_id="group-id",
                group_name="group-name",
                description="enrollment group",
                model_name="model-name",
                enrollment_ids=["foo", "bar", "baz"],
            )
        )

        self.assertEqual(response, enrollment_group_response)

        self.config.channel.close()

    def test_append_enrollment_group(self):
        self.config.connect()

        response: EnrollmentGroupResponse = EnrollmentGroupResponse(
            description="enrollment group", modelName="my-model"
        )

        self.enrollment_client.AppendEnrollmentGroup = MagicMock(return_value=response)

        management_service: MockManagementService = MockManagementService(
            config=self.config,
            token_manager=self.token_manager,
            enrollment_client=self.enrollment_client,
        )

        enrollment_group_response: EnrollmentGroupResponse = (
            management_service.append_enrollment_group(
                group_id="group-id", enrollment_ids=["foo", "bar", "baz"]
            )
        )

        self.assertEqual(response, enrollment_group_response)

        self.config.channel.close()

    def test_delete_enrollment(self):
        self.config.connect()

        response: EnrollmentResponse = EnrollmentResponse(
            description="enrollment", modelName="my-model"
        )

        self.enrollment_client.DeleteEnrollment = MagicMock(return_value=response)

        management_service: MockManagementService = MockManagementService(
            config=self.config,
            token_manager=self.token_manager,
            enrollment_client=self.enrollment_client,
        )

        delete_enrollment_response: EnrollmentResponse = (
            management_service.delete_enrollment(id="id")
        )

        self.assertEqual(response, delete_enrollment_response)

        self.config.channel.close()

    def test_delete_enrollment_group(self):
        self.config.connect()

        response: EnrollmentGroupResponse = EnrollmentGroupResponse(
            description="enrollment", modelName="my-model"
        )

        self.enrollment_client.DeleteEnrollmentGroup = MagicMock(return_value=response)

        management_service: MockManagementService = MockManagementService(
            config=self.config,
            token_manager=self.token_manager,
            enrollment_client=self.enrollment_client,
        )

        delete_enrollment_group_response: EnrollmentGroupResponse = (
            management_service.delete_enrollment_group(group_id="group-id")
        )

        self.assertEqual(response, delete_enrollment_group_response)

        self.config.channel.close()


if __name__ == "__main__":
    unittest.main()
