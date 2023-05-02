import os
import json
import binascii
import typing
import base64
import configparser
import uuid
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from sensory_cloud.config import (
    Config,
    CloudHost,
    EnrollmentType,
    SDKConfig,
)
from sensory_cloud.services.oauth_service import (
    OauthClient,
    OauthService,
    ISecureCredentialStore,
    GenericCredentialStore,
)

import sensory_cloud.generated.v1.management.device_pb2 as device_pb2


class FileSystemCredentialStore:
    """A file-system--based credential storage manager."""

    def __init__(self, root_path: str, package: str = "sensory-cloud"):
        """Initialize a new secure credential storage interface."""
        self._root_path = root_path
        self._package = package

    def __setitem__(self, key: str, value: str):
        """Emplace or replace a key/value pair in the secure credential store.

        Unlike most key-value store abstractions in the STL, this implementation of
        emplace will overwrite existing values in the key-value store.
        """
        with open(self._key_path(key), "w") as output_file:
            output_file.write(value)

    def __contains__(self, key: str) -> bool:
        """Return True if the key exists in the secure credential store."""
        return os.path.isfile(self._key_path(key))

    def __getitem__(self, key: str) -> str:
        """Look-up a secret value in the secure credential store."""
        with open(self._key_path(key)) as input_file:
            return input_file.read().strip()

    def __delitem__(self, key: str):
        """Remove a secret key-value pair in the secure credential store."""
        os.remove(self._key_path(key))

    def _key_path(self, key: str) -> str:
        """Return the path of the given key."""
        return os.path.join(self._root_path, f"{self._package}.{key}")


class Initializer:
    """
    Initialization class used to register a device
    """

    _enrollment_type_map: dict = {
        "none": EnrollmentType.none,
        "sharedSecret": EnrollmentType.shared_secret,
        "jwt": EnrollmentType.jwt,
    }

    def __init__(
        self,
        init_config: typing.Union[str, SDKConfig],
        secure_credential_store: ISecureCredentialStore = None,
        keychain: FileSystemCredentialStore = None,
    ):
        """
        Constructor method to generate an Initializer object

        Arguments:
            init_config (str or SDKConfig): The init_config argument can either be a string
                containing the path to a .ini config file or an SDKConfig object containing
                the required configuration information
            secure_credential_store (ISecureCredentialStore): The secure_credential_store
                argument is an ISecureCredentialStore abstract class object.  If it is set to
                None then the client credentials will be written to a GenericCredentialStore
                object
            keychain (FileSystemCredentialStore): The keychain will store the location of
                and the values of the device id and device name if they are not set as
                environment variables
        """

        self.init_config: typing.Union[str, SDKConfig] = init_config
        self.secure_credential_store: ISecureCredentialStore = secure_credential_store
        self.keychain = keychain
        self.sdk_config: SDKConfig = None
        self.config_parser: configparser.ConfigParser = None
        self.device_id = None
        self.device_name = None

    def _get_device_information(self) -> None:
        """
        Private method that first checks environment variables for device information.
        If the device information is not set as environment variables then the device information
        will be retrieved from the keychain initialization argument.  If the keychain does not 
        contain the device information then it will be randomly generated and written to the current
        working directory.
        """
        
        device_id = os.environ.get("SENSORYCLOUD_DEVICE_ID")
        device_name = os.environ.get("SENSORYCLOUD_DEVICE_NAME")
        
        if device_id is None:
            if self.keychain is None:
                self.keychain = FileSystemCredentialStore(root_path=os.getcwd())
                
            if 'deviceID' in self.keychain:
                device_id = self.keychain["deviceID"]
            else:
                device_id = str(uuid.uuid1())
                self.keychain["deviceID"] = device_id
                
            if 'deviceName' in self.keychain:
                device_name = self.keychain["deviceName"]
            else:
                device_name = str(uuid.uuid1())
                self.keychain["deviceName"] = device_name
                
        self.device_id = device_id
        self.device_name = device_name

    def _read_config_from_file(self) -> None:
        """
        Private method that sets the sdk_config attribute in the case that the init_config
        attribute is a path to a config file
        """

        self.config_parser: configparser.ConfigParser = configparser.ConfigParser()
        self.config_parser.read(self.init_config)

        sdk_config_parser: configparser.SectionProxy = self.config_parser[
            "SDK-configuration"
        ]

        self.sdk_config: SDKConfig = SDKConfig(
            fully_qualified_domain_name=sdk_config_parser.get(
                "fullyQualifiedDomainName"
            ),
            tenant_id=sdk_config_parser.get("tenantId"),
            is_connection_secure=sdk_config_parser.getboolean("isSecure"),
            enrollment_type=self._enrollment_type_map[
                sdk_config_parser.get("enrollmentType")
            ],
            credential=sdk_config_parser.get("credential"),
        )

        if (
            "client-configuration" in self.config_parser
            and self.secure_credential_store is None
        ):
            client_config_parser: configparser.SectionProxy = self.config_parser[
                "client-configuration"
            ]
            self.secure_credential_store: GenericCredentialStore = (
                GenericCredentialStore(
                    client_id=client_config_parser.get("clientId"),
                    client_secret=client_config_parser.get("clientSecret"),
                )
            )

    def _get_config(self) -> Config:
        """
        Private method that creates a Config object from the sdk_config attribute

        Returns:
            Config object used to construct an OauthService object
        """

        cloud_host: CloudHost = CloudHost(
            host=self.sdk_config.fully_qualified_domain_name,
            is_connection_secure=self.sdk_config.is_connection_secure,
        )

        config: Config = Config(
            tenant_id=self.sdk_config.tenant_id, cloud_host=cloud_host
        )
        config.connect()

        return config

    def _get_credential(self) -> str:
        """
        Private method that generates a credential string depending on the
        enrollment type

        Returns:
            Credential string used to enroll the device
        """

        if self.sdk_config.enrollment_type == EnrollmentType.none:
            credential: str = ""
        elif self.sdk_config.enrollment_type == EnrollmentType.shared_secret:
            credential: str = self.sdk_config.credential
        elif self.sdk_config.enrollment_type == EnrollmentType.jwt:
            credential: str = self._generate_jwt(private_key=self.sdk_config.credential)

        return credential

    def _generate_jwt(self, private_key: str) -> str:
        """
        Private method that generates a jwt token in the case that the enrollment
        type is 'jwt'

        Returns:
            A jwt token used as the enrollment credential
        """

        header: dict = {
            "alg": "EdDSA",
            "typ": "JWT",
        }
        payload: dict = {
            "name": self.sdk_config.device_name,
            "tenant": self.sdk_config.tenant_id,
            "client": self.secure_credential_store.client_id,
        }

        signing_key: Ed25519PrivateKey = Ed25519PrivateKey.from_private_bytes(
            binascii.unhexlify(private_key.encode("utf-8"))
        )

        header_base64: bytes = base64.urlsafe_b64encode(
            json.dumps(header).encode("utf-8")
        )
        payload_base64: bytes = base64.urlsafe_b64encode(
            json.dumps(payload).encode("utf-8")
        )
        to_sign: bytes = header_base64 + b"." + payload_base64

        signature: bytes = base64.urlsafe_b64encode(signing_key.sign(to_sign))

        token: str = (
            b".".join([header_base64, payload_base64, signature])
            .decode()
            .replace("+", "-")
            .replace("/", "_")
            .replace("=", "")
        )

        return token

    def _update_config_file(self) -> None:
        """
        Private method that updates the config file with the client id and the
        client secret upon successful enrollment of the device
        """

        if "client-configuration" not in self.config_parser:
            self.config_parser.add_section("client-configuration")

        self.config_parser.set(
            "client-configuration", "clientId", self.secure_credential_store.client_id
        )
        self.config_parser.set(
            "client-configuration",
            "clientSecret",
            self.secure_credential_store.client_secret,
        )

        with open(self.init_config, "w") as config_file:
            self.config_parser.write(config_file)

    def initialize(self) -> typing.Union[device_pb2.DeviceResponse, Exception]:
        """
        Public method that uses the sdk and client credentials to enroll a
        new device

        Returns:
            If the device enrollment is successful then a device_pb2.DeviceResponse
            object will be returned.  If the device is already enrolled or another
            device is enrolled with the client credentials specified, then an
            Exception will be returned.
        """

        self._get_device_information()

        if isinstance(self.init_config, str):
            if not os.path.exists(self.init_config):
                raise Exception(f"The path, {self.init_config}, does not exist")
            self._read_config_from_file()
        elif isinstance(self.init_config, SDKConfig):
            self.sdk_config = self.init_config
        else:
            raise Exception(
                "The init_config attribute must be a string containing the config file path or an SDKConfig object"
            )

        if self.secure_credential_store is None:
            client_credentials: OauthClient = OauthService.generate_credentials()
            self.secure_credential_store: GenericCredentialStore = (
                GenericCredentialStore(
                    client_id=client_credentials.client_id,
                    client_secret=client_credentials.client_secret,
                )
            )

        config: Config = self._get_config()
        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=self.secure_credential_store
        )

        try:
            device_response = oauth_service.get_who_am_i()
            device_is_registered = self.device_id == device_response.deviceId
            if not device_is_registered:
                err: str = f"Another device with deviceId = {device_response.deviceId} is already enrolled with this client"
                print(err)
                return Exception(err)
        except Exception as e:
            device_is_registered = False

        if not device_is_registered:
            credential: str = self._get_credential()
            response: device_pb2.DeviceResponse = oauth_service.register(
                device_id=self.device_id,
                device_name=self.device_name,
                credential=credential,
            )
            if self.config_parser is not None:
                self._update_config_file()
        else:
            err: str = "This device is already enrolled"
            print(err)
            response: Exception = Exception(err)

        return response
