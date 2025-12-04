"""
Quick Start Example

This is the simplest example to get started with the SDK.
It demonstrates the basic workflow: initialize, convert text to speech, and save the result.
"""

import os
from supertone import Supertone
from supertone import models


def main():
    # Step 1: Get API key from environment variable
    api_key = os.getenv("SUPERTONE_API_KEY")
    if not api_key:
        print("❌ Error: SUPERTONE_API_KEY environment variable not set")
        print("\n🔧 Setup:")
        print("   export SUPERTONE_API_KEY='your-api-key-here'")
        return

    # Step 2: Initialize the SDK with context manager
    with Supertone(api_key=api_key) as client:
        # Step 3: Replace with your voice ID
        # Get available voices: python examples/voices/list_voices.py
        VOICE_ID = "your-voice-id-here"

        # Step 4: Your text
        text = "Hello! Welcome to the Text-to-Speech SDK. This is your first example."

        try:
            # Step 5: Convert text to speech
            print("🎤 Converting text to speech...")
            response = client.text_to_speech.create_speech(
                voice_id=VOICE_ID,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Step 6: Save the audio file
            output_file = "quickstart_output.wav"
            with open(output_file, "wb") as f:
                f.write(response.result.read())

            print(f"✅ Success! Audio saved to: {output_file}")
            print("\n💡 Next steps:")
            print("   • Explore more examples in examples/")
            print("   • Try async version: python examples/quickstart_async.py")
            print("   • Read the docs: examples/README.md")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n🔧 Troubleshooting:")
            print("   1. Set your API key: export SUPERTONE_API_KEY='your-key'")
            print("   2. Get a voice ID: python examples/voices/list_voices.py")
            print("   3. Update VOICE_ID in this script")


if __name__ == "__main__":
    main()
