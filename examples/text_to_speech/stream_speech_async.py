"""
Stream Speech Example (Async)

This example demonstrates how to stream text-to-speech audio asynchronously in real-time.
Async streaming is perfect for web applications, chatbots, and real-time communication systems.
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

    # Initialize the SDK
    async with Supertone(api_key=api_key) as client:
        # Replace with your voice ID
        VOICE_ID = "your-voice-id-here"

        # Text to convert
        text = "This is an async streaming text-to-speech example. The audio is generated and delivered in real-time."

        try:
            # Stream text to speech asynchronously
            response = await client.text_to_speech.stream_speech_async(
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
            output_file = "output_stream_async.wav"
            chunk_count = 0

            with open(output_file, "wb") as f:
                # Process streaming response asynchronously
                if hasattr(response.result, "aiter_bytes"):
                    async for chunk in response.result.aiter_bytes():
                        f.write(chunk)
                        chunk_count += 1
                        if chunk_count % 10 == 0:
                            print(f"   Received {chunk_count} chunks...")

            print("✅ Async Streaming Speech Completed")
            print(f"   Output File: {output_file}")
            print(f"   Total Chunks: {chunk_count}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
