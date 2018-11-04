# Nemoji
An application supporting radio broadcasters and podcasters alike when receiving phone calls from their audiences. Incoming phone calls are first transcribed, sentiment analysis is then performed on the text to summarise the general vibe. Vibes are split into five sections: very negative vibe, negative vibe, neutral vibe, positive vibe, and very positive vibe. These help presenters quickly skim through what would be a lengthy process to broadcast the best comments from their viewers.

We've hosted a web application on Google Cloud Computer Engine using Tornado Python which receives incoming Nexmo calls. The calls are saved as .wav files, the audio is transcribed using Google Speech-To-Text, and further analysed using the Google Natural Language API.
