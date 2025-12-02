"""
Predict TTS Duration Example (Sync)

This example demonstrates how to predict the duration of text-to-speech conversion
without actually generating the audio. This is useful for estimating processing time
and planning audio content.
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

    # Initialize the SDK
    client = Supertone(api_key=api_key)

    # Replace with your voice ID
    VOICE_ID = "your-voice-id-here"

    # Text to estimate duration for
    text = "Hello! This is a sample text to estimate the TTS duration."

    try:
        # Predict TTS duration
        response = client.text_to_speech.predict_duration(
            voice_id=VOICE_ID,
            text=text,
            language=models.PredictTTSDurationUsingCharacterRequestLanguage.EN,
            # Format options:
            output_format=models.PredictTTSDurationUsingCharacterRequestOutputFormat.WAV,
            # Voice customization (optional):
            # voice_settings=models.ConvertTextToSpeechParameters(
            #     pitch_shift=0.95,  # Range: 0.5-2.0
            #     speed=0.9,         # Range: 0.5-2.0
            # ),
        )

        print("✅ Duration Predicted Successfully")
        print(f"   Estimated Duration: {response.duration} seconds")
        print(f"   Text: {text[:50]}...")
        print("\n💡 Use this to estimate processing time before actual TTS generation")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
