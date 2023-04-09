import boto3
import credentials

polly_client = boto3.Session(
    aws_access_key_id=credentials.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=credentials.AWS_SECRET_ACCESS_KEY,
    aws_session_token=credentials.AWS_SESSION_TOKEN,
    region_name='us-east-1').client('polly')


def speech(person, text, theme, num_line):
    voice = ""
    engine = ""

    match person:
        case "Jose Luis":
            voice = "Sergio"
            engine = "neural"
        case "Juan":
            voice = "Enrique"
            engine = "standard"
        case "Lucía":
            voice = "Lucia"
            engine = "neural"
        case "Manolo":
            voice = "Andres"
            engine = "neural"

    response = polly_client.synthesize_speech(
        VoiceId=voice,
        OutputFormat='mp3',
        Text=text,
        Engine=engine,
    )

    file = open(f"programs/{theme}/audios/{num_line}", 'wb')
    file.write(response['AudioStream'].read())
    file.close()
