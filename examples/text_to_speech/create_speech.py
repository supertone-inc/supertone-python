"""
Create Speech Example (Sync)

This example demonstrates how to convert text to speech and save it as an audio file.
The SDK automatically handles long texts (>300 characters) by chunking and merging.
"""

import os
from supertone import Supertone
from supertone import models


def main():
    # Get API key from environment variable
    api_key = os.getenv("SUPERTONE_API_KEY")
    if not api_key:
        print("❌ Error: SUPERTONE_API_KEY environment variable not set")
        print("\n🔧 Setup:")
        print("   export SUPERTONE_API_KEY='your-api-key-here'")
        return

    # Initialize the SDK with context manager
    with Supertone(api_key=api_key) as client:
        # Replace with your voice ID
        VOICE_ID = "your-voice-id-here"

        # Text to convert (supports long texts automatically)
        text = "Hello! This is a text-to-speech example using the SDK."

        try:
            # Convert text to speech
            response = client.text_to_speech.create_speech(
                voice_id=VOICE_ID,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                # Format options:
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                # output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,  # For smaller file size
                # Voice customization (optional):
                # pitch_shift=0.95,  # Range: 0.5-2.0 (lower/higher pitch)
                # speed=0.9,         # Range: 0.5-2.0 (slower/faster)
                # Advanced options (optional):
                # include_phonemes=True,  # Get phoneme data for lip-sync/animation
            )

            # Save audio to file
            output_file = "output_speech.wav"
            with open(output_file, "wb") as f:
                f.write(response.result.read())

            print("✅ Speech Created Successfully")
            print(f"   Output File: {output_file}")
            print(f"   Text: {text[:50]}...")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
