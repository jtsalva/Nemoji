# Nemoji
An application supporting radio broadcasters and podcasters alike when receiving phone calls from their audiences. Incoming phone calls are first transcribed, sentiment analysis is then performed on the text to summarise the general vibe. Vibes are split into five sections: very negative vibe, negative vibe, neutral vibe, positive vibe, and very positive vibe. These help presenters quickly skim through what would be a lengthy process to broadcast the best comments from their viewers.

We've hosted a web application on Google Cloud Compute Engine using Tornado Python which receives incoming Nexmo calls. The calls are saved as .wav files, the audio is transcribed using Google Speech-To-Text, and further analysed using the Google Natural Language API.

## Flow of processes
1. Call number and say something
2. Recorded temporarily as 'static/audio.raw'
3. Raw file is converted to 'static/timestamp.wav'
3. The '.wav' is transcribed
4. Transcription is sentimentally analysed given a number between -1 (negative) and 1 (positive)
5. Caller number, transcription, timestamp, and sentiment value is stored into an sqlite database using github.com/jtsalva/Bull-SQLite.

## Prerequisites to run
1. To have enabled Google Speech-To-Text and Natural Language Processing from the Google Cloud Console, then generate and download 'credentials.json'.

2. Install client libraries `pip3 install google-cloud-speech google-cloud-language tornado`

## Run it
Only tested using Python 3 `GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json python3 server.py`

When calling you will be greeted via 'Hello stranger, tell me something' to end the call you must manually hang up.
