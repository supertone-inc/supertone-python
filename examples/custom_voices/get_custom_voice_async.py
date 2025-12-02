"""
Get Custom Voice Details Example (Async)

This example demonstrates how to asynchronously retrieve detailed information
about a specific custom cloned voice.
"""

import asyncio
import os
from supertone import Supertone


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
        # Replace with an actual custom voice ID from your account
        CUSTOM_VOICE_ID = "your-custom-voice-id-here"

        try:
            # Get detailed information about a specific custom voice asynchronously
            voice = await client.custom_voices.get_custom_voice_async(
                voice_id=CUSTOM_VOICE_ID
            )

            print("✅ Custom Voice Details Retrieved (Async)")
            print("\n🎭 Voice Information:")
            print(f"   Name: {voice.name}")
            print(f"   ID: {voice.voice_id}")

            if hasattr(voice, "description") and voice.description:
                print(f"   Description: {voice.description}")

            if hasattr(voice, "language") and voice.language:
                print(f"   Language: {voice.language}")

            if hasattr(voice, "created_at") and voice.created_at:
                print(f"   Created: {voice.created_at}")

            if hasattr(voice, "updated_at") and voice.updated_at:
                print(f"   Updated: {voice.updated_at}")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Tip: Make sure to replace CUSTOM_VOICE_ID with a valid custom voice ID")
            print("   Run: python examples/custom_voices/list_custom_voices_async.py")


if __name__ == "__main__":
    asyncio.run(main())

