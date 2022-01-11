# Sensory Cloud Python SDK Examples
The following examples show some sample implmentations of each service provided by Sensory Cloud.
Each of these example files will read in some environment variables that are set from a .env file
and retrieved using the [`python-dotenv`](https://pypi.org/project/python-dotenv/) package.  The `python-dotenv` package is not a dependency of
the `sensory-cloud` library so these examples must be run in a python environment with both packages installed.

## Audio Service Examples
The audio service examples use the [`pyaudio`](https://pypi.org/project/PyAudio/) library to interface with the device microphone.  Similar to
`python-dotenv`, this library must be installed in addition to `sensory-cloud` in order for the example code to run.

## Video Service Examples
The video service examples use the [`opencv-python`](https://pypi.org/project/opencv-python/) library to interface with the device camera.  As with
`pyaudio` and `python-dotenv`, this library must be installed in addition to `sensory-cloud` in order for the example code to run. 