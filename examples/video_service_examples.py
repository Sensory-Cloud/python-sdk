import cv2
import os
import dotenv
from io import BytesIO
from PIL import Image
import threading
import time


from sensory_cloud.config import Config
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.services.video_service import VideoService, RequestIterator


from sensory_cloud.generated.v1.video.video_pb2 import (
    CreateEnrollmentResponse,
    GetModelsRequest,
    GetModelsResponse,
    CreateEnrollmentConfig,
    CreateEnrollmentRequest,
    AuthenticateConfig,
    AuthenticateRequest,
    AuthenticateResponse,
    LivenessRecognitionResponse,
    RecognitionThreshold,
    ValidateRecognitionConfig,
    ValidateRecognitionRequest,
)


from credential_store import CredentialStore


dotenv.load_dotenv(override=True)

is_connection_secure = True
is_liveness_enabled = False
model_name = "face_biometric_hektor_gpu"
device_name = 'jhersch-python-sdk-dev'
enrollment_description = "jhersch-video-enrollment"

fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
tenant_id = os.environ.get("TENANT_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
device_id = os.environ.get("DEVICE_ID")
device_credential = os.environ.get("DEVICE_CREDENTIAL")
user_id = os.environ.get("USER_ID")
enrollment_id = os.environ.get("VIDEO_ENROLLMENT_ID")


class VideoStreamIterator:
    _camera = cv2.VideoCapture(0)

    def __iter__(self):
        return self

    def __next__(self):
        success, frame = self._camera.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            buffer = BytesIO()
            Image.fromarray(frame).save(buffer, format="JPEG", quality=95)
            return buffer.getvalue()
        else:
            raise StopIteration

    def close(self):
        self._camera.release()


def view_camera():
    camera = cv2.VideoCapture(0)
    while show_camera:
        success, frame = camera.read()

        cv2.imshow('frame', frame)

    camera.release()
    cv2.destroyAllWindows()


def example_enroll_with_video():
    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name, 
        is_connection_secure=is_connection_secure, 
        tenant_id=tenant_id
    )
    config.connect()

    cred_store = CredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    video_service = VideoService(config=config, token_manager=token_manager)

    video_stream_iterator = VideoStreamIterator()

    enrollment_stream = video_service.stream_enrollment(
        description=enrollment_description,
        user_id=user_id,
        device_id=device_id,
        model_name=model_name,
        is_liveness_enabled=is_liveness_enabled,
        video_stream_iterator=video_stream_iterator
    )
    
    print("Recording enrollment...")
    percent_complete = 0
    enrollment_id = None
    print(f"percent complete = {percent_complete}")
    for response in enrollment_stream:
        if response.percentComplete != percent_complete:
            percent_complete = response.percentComplete
            print(f"percent complete = {percent_complete}")
        if response.percentComplete >= 100:
            break
    enrollment_id = response.enrollmentId
    print("Enrollment complete!")
    print(f"Enrollment Id = {enrollment_id}")

    video_stream_iterator.close()
    enrollment_stream.cancel()

    return enrollment_id


if __name__ == "__main__":
    show_camera = True

    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name, 
        is_connection_secure=is_connection_secure, 
        tenant_id=tenant_id
    )
    config.connect()

    cred_store = CredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    video_service = VideoService(config=config, token_manager=token_manager)

    video_stream_iterator = VideoStreamIterator()

    authenticate_stream = video_service.stream_authentication(
        enrollment_id=enrollment_id, is_liveness_enabled=False, video_stream_iterator=video_stream_iterator
    )

    print("Authenticating...")
    for response in authenticate_stream:
        if response.success:
            show_camera = False
            break
    print("Authentication successful!")


    video_stream_iterator.close()
    authenticate_stream.cancel()