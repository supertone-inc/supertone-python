"""
Quick Start Example (Async)

This is the async version of the quick start example.
Use async for better performance in web applications and when processing multiple requests.
"""

import asyncio
import os
from supertone import Supertone
from supertone import models


async def main():
    # Step 1: Get API key from environment variable
    api_key = os.getenv("SUPERTONE_API_KEY")
    if not api_key:
        print("❌ Error: SUPERTONE_API_KEY environment variable not set")
        print("\n🔧 Setup:")
        print("   export SUPERTONE_API_KEY='your-api-key-here'")
        return

    # Step 2: Initialize the SDK with async context manager
    async with Supertone(api_key=api_key) as client:
        # Step 3: Replace with your voice ID
        VOICE_ID = "your-voice-id-here"

        # Step 4: Your text
        text = "Hello! This is the async version of the Text-to-Speech SDK example."

        try:
            # Step 5: Convert text to speech asynchronously
            print("🎤 Converting text to speech (async)...")
            response = await client.text_to_speech.create_speech_async(
                voice_id=VOICE_ID,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Step 6: Save the audio file
            output_file = "quickstart_output_async.wav"
            with open(output_file, "wb") as f:
                f.write(response.result.read())

            print(f"✅ Success! Audio saved to: {output_file}")
            print("\n💡 Next steps:")
            print("   • Try streaming: examples/text_to_speech/stream_speech_async.py")
            print("   • Explore custom voices: examples/custom_voices/")
            print("   • Read the docs: examples/README.md")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n🔧 Troubleshooting:")
            print("   1. Set your API key: export SUPERTONE_API_KEY='your-key'")
            print("   2. Get a voice ID: python examples/voices/list_voices_async.py")
            print("   3. Update VOICE_ID in this script")


if __name__ == "__main__":
    asyncio.run(main())
