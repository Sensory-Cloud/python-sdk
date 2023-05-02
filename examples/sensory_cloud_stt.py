import yaml
import configparser
import argparse
import typing
import wave
import threading
import jiwer
import pandas as pd
from queue import Queue

from sensory_cloud.services.audio_service import AudioService, TranscriptAggregator
from sensory_cloud.services.oauth_service import OauthService
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.config import Config, CloudHost
from sensory_cloud.services.oauth_service import ISecureCredentialStore

import sensory_cloud.generated.v1.audio.audio_pb2 as audio_pb2


def get_options() -> typing.Tuple[dict, configparser.ConfigParser]:
    """
    Function that retrieves the stt config yaml path from the command line and loads the
    config arguments into a dictionary.  The sensory cloud config is also constructed and
    returned.

    Returns:
        a tuple containing the stt config dictionary and the config parser
        sensory cloud config
    """

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="sensorycloud_stt"
    )
    parser.add_argument(
        "--config_path",
        dest="config_path",
        type=str,
        required=True,
        help="path to yaml config file",
    )

    args: parser.Namespace = parser.parse_args()

    with open(args.config_path, "r") as config_file:
        stt_config: dict = yaml.safe_load(config_file)

    sensory_cloud_config: configparser.ConfigParser = configparser.ConfigParser()
    sensory_cloud_config.read(stt_config["stt-config"]["sensory_cloud_config_path"])

    return stt_config, sensory_cloud_config


class SecureCredentialStore(ISecureCredentialStore):
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret


def get_oauth_service() -> OauthService:
    """
    Function the creates an OauthService object using the credentials set in
    config.json

    Returns:
        An OauthService object
    """

    cloud_host: CloudHost = CloudHost(
        host=sensory_cloud_config.get("SDK-configuration", "fullyQualifiedDomainName"),
        is_connection_secure=sensory_cloud_config.getboolean(
            "SDK-configuration", "isSecure"
        ),
    )
    config: Config = Config(
        cloud_host=cloud_host,
        tenant_id=sensory_cloud_config.get("SDK-configuration", "tenantId"),
    )
    config.connect()

    credential_store: SecureCredentialStore = SecureCredentialStore(
        client_id=sensory_cloud_config.get("client-configuration", "clientId"),
        client_secret=sensory_cloud_config.get("client-configuration", "clientSecret"),
    )

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )

    return oauth_service


def get_token_manager() -> TokenManager:
    """
    Function that creates a TokenManager object using the credentials set in
    config.json

    Returns:
        A TokenManager object
    """

    oauth_service: OauthService = get_oauth_service()

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    return token_manager


def get_audio_service() -> AudioService:
    """
    Function that creates an AudioService object using the credentials set
    in config.json

    Returns:
        An AudioService object
    """

    token_manager: TokenManager = get_token_manager()

    audio_service: AudioService = AudioService(
        config=token_manager.oauth_service._config, token_manager=token_manager
    )

    return audio_service


def get_audio_config(sample_rate_hertz: int = 16000) -> audio_pb2.AudioConfig:
    """
    Function that creates an audio_pb2.AudioConfig object with
    Linear 16 encoding, one audio channel, 16 KHz sample rate, and
    uses US english

    Returns:
        An audio_pb2.AudioConfig object
    """

    audio_config: audio_pb2.AudioConfig = audio_pb2.AudioConfig(
        encoding=audio_pb2.AudioConfig.AudioEncoding.Value("LINEAR16"),
        audioChannelCount=1,
        sampleRateHertz=sample_rate_hertz,
        languageCode=stt_config["stt-config"]["language_code"],
    )

    return audio_config


class FileTranscriptionIterator:
    transcript = None
    responses = []
    _queue = Queue()
    _stop_event = threading.Event()

    def __init__(self):
        self._stop_event.set()

    def __iter__(self):
        return self

    def __next__(self):
        if self._stop_event.is_set():
            post_processing_action = None
            item = self._queue.get()
            self._queue.task_done()
            if item == "stop":
                post_processing_action = audio_pb2.AudioRequestPostProcessingAction(
                    action=audio_pb2.AudioPostProcessingAction.FINAL
                )
                item = b""
                self.stop()
            _next = (item, post_processing_action)
            return _next
        raise StopIteration

    def put(self, item):
        self._queue.put(item)

    def stop(self):
        self._stop_event.clear()


def transcribe_file(file_path: str) -> str:
    """
    Example of an audio transcription using the 'speech_recognition_en' speech
    to text model.  This function will read in a wave file and return the
    transcription as a string.

    Args:
        file_path: path to wave file to be transcribed

    Returns:
        A string containing a complete transcription
    """

    frames_per_buffer: int = int(
        stt_config["stt-config"]["chunkmsec"]
        * stt_config["stt-config"]["sample_rate_hertz"]
        / 1000
    )

    transcription_iterator: FileTranscriptionIterator = FileTranscriptionIterator()

    with wave.open(file_path, "rb") as wave_file:
        buffer: bytes = wave_file.readframes(frames_per_buffer)
        while buffer != b"":
            transcription_iterator.put(buffer)
            buffer: bytes = wave_file.readframes(frames_per_buffer)

    transcription_iterator.put("stop")

    audio_service: AudioService = get_audio_service()
    audio_config: audio_pb2.AudioConfig = get_audio_config(
        sample_rate_hertz=stt_config["stt-config"]["sample_rate_hertz"]
    )

    transcribe_stream = audio_service.stream_transcription(
        audio_config=audio_config,
        user_id=sensory_cloud_config.get("examples-configuration", "userId"),
        model_name=stt_config["stt-config"]["model_name"],
        enable_punctuation_capitalization=stt_config["stt-config"][
            "enable_punctuation_capitalization"
        ],
        audio_stream_iterator=transcription_iterator,
    )

    transcript_aggregator: TranscriptAggregator = TranscriptAggregator()

    try:
        for response in transcribe_stream:
            transcript_aggregator.process_response(response)
            full_transcript = transcript_aggregator.get_transcript()
            transcription_iterator.transcript = full_transcript
            transcription_iterator.responses.append(response)
    except Exception as e:
        print(f"Transcription failed with error: {str(e)}")
    finally:
        transcribe_stream.cancel()

    transcript: str = transcript_aggregator.get_transcript()

    return transcript


def transcribe_and_score(row: pd.Series) -> dict:
    audio_file = row["audio_file"]
    expected_transcript = row["expected_transcript"]
    hypothesis = transcribe_file(audio_file)

    score = -1
    if expected_transcript != "":
        score = score_func(expected_transcript, hypothesis)

    return {
        "audio_file": audio_file,
        "expected_transcript": expected_transcript,
        "hypothesis": hypothesis,
        "score": score,
    }


if __name__ == "__main__":
    stt_config, sensory_cloud_config = get_options()

    score_type = stt_config["stt-config"]["score_type"]
    if score_type == "wer":
        score_func = jiwer.wer
    elif score_type == "cer":
        score_func = jiwer.cer
    else:
        raise ValueError(
            f"'{score_type}' is an invalid score type, it must be 'wer' or 'cer'"
        )

    df_input = pd.read_csv(stt_config["io-config"]["input_path"])
    if "expected_transcript" not in df_input.columns:
        df_input["expected_transcript"] = ""

    output_records = [transcribe_and_score(row) for _, row in df_input.iterrows()]

    df_output = pd.DataFrame(output_records)
    df_output_with_expected = df_output.loc[df_output["score"] >= 0]

    expected_transcripts = list(
        df_output_with_expected["expected_transcript"].astype(str)
    )
    hypothesis = list(df_output_with_expected["hypothesis"].astype(str))
    if stt_config["stt-config"]["strip_spaces"]:
        expected_transcripts = [x.replace(" ", "") for x in expected_transcripts]
        hypothesis = [x.replace(" ", "") for x in hypothesis]

    try:
        corpus_score = score_func(expected_transcripts, hypothesis)
    except Exception as e:
        print(f"An error occured when calculting the corpus score - {str(e)}")
        corpus_score = -1

    df_output["corpus_score"] = corpus_score
    df_output.to_csv(stt_config["io-config"]["output_path"], index=False)
