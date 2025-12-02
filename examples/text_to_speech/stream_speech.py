"""
Stream Speech Example (Sync)

This example demonstrates how to stream text-to-speech audio in real-time.
Streaming is ideal for low-latency applications and long texts.
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

    # Text to convert
    text = "This is a streaming text-to-speech example. The audio is generated and delivered in real-time."

    try:
        # Stream text to speech
        response = client.text_to_speech.stream_speech(
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

        # Stream audio chunks to file
        output_file = "output_stream.wav"
        chunk_count = 0

        with open(output_file, "wb") as f:
            # Process streaming response
            if hasattr(response.result, "iter_bytes"):
                for chunk in response.result.iter_bytes():
                    f.write(chunk)
                    chunk_count += 1
                    if chunk_count % 10 == 0:
                        print(f"   Received {chunk_count} chunks...")

        print("✅ Streaming Speech Completed")
        print(f"   Output File: {output_file}")
        print(f"   Total Chunks: {chunk_count}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
