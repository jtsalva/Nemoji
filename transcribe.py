from google.cloud import speech_v1p1beta1 as speech

def transcribe(name):
    client = speech.SpeechClient()

    speech_file = 'static/{}.wav'.format(name)
    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-GB',
        enable_speaker_diarization=True,
        diarization_speaker_count=2)

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

    result = response.results[-1]

    words_info = result.alternatives[0].words

    text = ''
    last_speaker = None

    for word_info in words_info:
        if last_speaker != word_info.speaker_tag:
            text += '\n'
        else:
            text += ' '
        text += word_info.word
        last_speaker = word_info.speaker_tag

    return text.strip()
