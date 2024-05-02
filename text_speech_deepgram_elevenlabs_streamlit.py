import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import streamlit as st

# Load environment variables
os.environ["DG_API_KEY"] = st.secrets["DG_API_KEY"]
os.environ["ELEVENLABS_API_KEY"] = st.secrets["ELEVENLABS_API_KEY"]

def speech_to_text(url):
    from deepgram import (
        DeepgramClient,
        PrerecordedOptions,
    )

    # URL to the audio file
    AUDIO_URL = {
        "url": url
    }

    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(DG_API_KEY)

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        # STEP 3: Call the transcribe_url method with the audio payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)

        # STEP 4: Print the response
        transcript = response.results["channels"][0]["alternatives"][0]["transcript"]
        print(transcript)
        
    except Exception as e:
        return f"Exception: {e}"

    return transcript

client = ElevenLabs(
    ELEVENLABS_API_KEY="623e37236fda749c8f75526b88530831"
)

def text_to_speech_file(text: str) -> str:
    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB", # Adam pre-made voice
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generating a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

def main():
    st.title("Text to Speech and back Conversion using Deepgram and ElevenLabs")
    url = st.text_input('Enter url of video: ')
    audio_file_path = text_to_speech_file(speech_to_text(url))
    audio_file = open(audio_file_path,'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)

if __name__ == "__main__":
    main()
    
