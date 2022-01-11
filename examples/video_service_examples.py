import cv2
import os
import dotenv
from io import BytesIO
from PIL import Image

from sensory_cloud.config import Config
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.services.video_service import VideoService

from secure_credential_store_example import SecureCredentialStore


dotenv.load_dotenv(override=True)

is_connection_secure = True
is_liveness_enabled = False
device_name = "jhersch-python-sdk-dev"
enrollment_description = "jhersch-video-enrollment-cpu"

fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
tenant_id = os.environ.get("TENANT_ID")
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
device_id = os.environ.get("DEVICE_ID")
device_credential = os.environ.get("DEVICE_CREDENTIAL")
user_id = os.environ.get("USER_ID")
enrollment_id = os.environ.get("VIDEO_ENROLLMENT_ID")


class VideoStreamIterator:
    def __init__(self):
        self._camera = cv2.VideoCapture(0)

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


def example_get_models():
    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    video_service = VideoService(config=config, token_manager=token_manager)

    return video_service.get_models()


def example_enroll_with_video() -> str:
    model_name = "face_recognition_mathilde"

    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
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
        video_stream_iterator=video_stream_iterator,
    )

    print("Recording enrollment...")
    percent_complete = 0
    enrollment_id = None
    try:
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
    except Exception as e:
        f"Enrollment failed with error: {str(e)}"
    finally:
        video_stream_iterator.close()
        enrollment_stream.cancel()

    return enrollment_id


def example_authenticate_with_video() -> bool:
    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    video_service = VideoService(config=config, token_manager=token_manager)

    video_stream_iterator = VideoStreamIterator()

    authenticate_stream = video_service.stream_authentication(
        enrollment_id=enrollment_id,
        is_liveness_enabled=False,
        video_stream_iterator=video_stream_iterator,
    )

    success = False
    try:
        print("Authenticating...")
        for response in authenticate_stream:
            print(response.success)
            if response.success:
                success = True
                break
        print("Authentication successful!")
    except Exception as e:
        print(f"Authentication failed with error {str(e)}")
    finally:
        video_stream_iterator.close()
        authenticate_stream.cancel()

    return success


def example_stream_liveness_recognition():
    model_name: str = "face_recognition_mathilde"

    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name,
        is_connection_secure=is_connection_secure,
        tenant_id=tenant_id,
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    video_service = VideoService(config=config, token_manager=token_manager)

    video_stream_iterator = VideoStreamIterator()

    recognition_stream = video_service.stream_liveness_recognition(
        user_id=user_id,
        model_name=model_name,
        video_stream_iterator=video_stream_iterator,
    )

    alive = False
    try:
        print("Running liveness recognition...")
        for response in recognition_stream:
            print(response.isAlive)
            if response.isAlive:
                alive = True
                break
        print("You're alive!")
    except Exception as e:
        print(f"Liveness recognition failed with error {str(e)}")
    finally:
        video_stream_iterator.close()
        recognition_stream.cancel()

    return alive


if __name__ == "__main__":
    alive = example_stream_liveness_recognition()
