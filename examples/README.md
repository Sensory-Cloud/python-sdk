# Sensory Cloud Python SDK Examples
Before starting with these examples you will need to create json config file called `config.json`  in this directory as shown below.

```
{
    "fully_qualified_domain_name": "my.unique.domain.com",
    "tenant_id": "my-tenant-id",
    "tenant_secret": "my-tenant-secret",
    "client_id": "",
    "client_secret": "",
    "device_id": "my-device-id",
    "device_name": "my-device-name",
    "user_id": "my-user-id",
    "audio_enrollment_id": "",
    "audio_enrollment_group_id": "",
    "audio_event_enrollment_group_id": "",
    "video_enrollment_id": "",
    "video_enrollment_group_id": ""
}
```
The `fully_qualified_domain_name`, `tenant_id`, and `tenant_secret` are obtained from Sensory upon registration and those credentials should
be placed in the `config.json` file.  The `device_id`, `device_name`, and `user_id` can be chosen by the user and added to the config
file as well.  The remaining configuration parameters will be set as we work through the examples.

## Registration
The first step in using the Sensory Cloud Python SDK is to setup client credentials and register your device.  An example of this process is covered
in [registration_examples.py](registration_examples.py).
