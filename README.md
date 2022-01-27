# Python SDK
Sensory Cloud is built using python 3.8, but it is compatible with python 3.6 and higher

## General Information
Before getting started, you must spin up a Sensory Cloud inference server or have Sensory spin one up for you. You must also have the following pieces of information:
- Your inference server URL (fully_qualified_domain_name)
- Your Sensory Tenant ID (UUID)
- Your configured secret key (device_credential) used to register OAuth clients and devices

## Code Examples
The [examples](https://github.com/Sensory-Cloud/python-sdk/tree/main/examples) section of this repository shows the user how to do the following:
- Set client credentials and register devices
- Create enrollments and enrollment groups for the audio and video services
- Authenticate against enrollments and enrollment groups
- Detect audio events such as coughing or door knocks
- Transcribe speech to text
- Detect video liveness
- Monitor server health
