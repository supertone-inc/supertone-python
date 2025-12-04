"""
Create Cloned Voice Example (Sync)

This example demonstrates how to create a custom cloned voice from audio samples.
You need to provide audio files that contain clear voice samples.
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
        # Path to your audio file(s) for voice cloning
        AUDIO_FILE = "path/to/your/voice_sample.wav"

        try:
            # Read audio file
            with open(AUDIO_FILE, "rb") as f:
                audio_data = f.read()

            # Create a cloned voice
            response = client.custom_voices.create_cloned_voice(
                request_body=models.CustomVoicesCreateClonedVoiceRequestBody(
                    name="My Custom Voice",
                    description="A cloned voice created from audio samples",
                    audio_file=audio_data,
                    language=models.APICloneVoiceRequestLanguage.EN,
                )
            )

            print("✅ Custom Voice Created Successfully")
            print(f"   Voice ID: {response.voice_id}")
            print(f"   Name: {response.name}")
            print("   💡 You can now use this voice_id for TTS!")

        except FileNotFoundError:
            print(f"❌ Audio file not found: {AUDIO_FILE}")
            print("   Please update AUDIO_FILE with a valid path")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
