"""
Predict TTS Duration Example (Async)

This example demonstrates how to asynchronously predict the duration of text-to-speech
conversion. Useful for non-blocking duration estimation in async applications.
"""

import asyncio
import os
from supertone import Supertone
from supertone import models


async def main():
    # Get API key from environment variable
    api_key = os.getenv("SUPERTONE_API_KEY")
    if not api_key:
        print("❌ Error: SUPERTONE_API_KEY environment variable not set")
        print("\n🔧 Setup:")
        print("   export SUPERTONE_API_KEY='your-api-key-here'")
        return

    # Initialize the SDK with async context manager
    async with Supertone(api_key=api_key) as client:
        # Replace with your voice ID
        VOICE_ID = "your-voice-id-here"

        # Text to estimate duration for
        text = (
            "Hello! This is a sample text to estimate the TTS duration asynchronously."
        )

        try:
            # Predict TTS duration asynchronously
            response = await client.text_to_speech.predict_duration_async(
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

            print("✅ Duration Predicted Successfully (Async)")
            print(f"   Estimated Duration: {response.duration} seconds")
            print(f"   Text: {text[:50]}...")
            print("\n💡 Perfect for async workflows and parallel processing")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
