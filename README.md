# Curiosities Podcast Generator

Application that generates a radio podcast about curiosities.

Using: 

- **GPT-3 API** from OpenAI for the generation of the content of the podcast.

- **AWS Polly API** for the generation of the audio of the podcast.

## What does it do?
It generates a folder in the root of the project with the following structure:

- theme_name
    - content.txt (text file with the content of the podcast)
    - podcast.mp3 (audio file with the content of the podcast)
    - audios (folder)
        - multiple audio files (one for each sentence of the podcast)
