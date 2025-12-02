"""
Get Voice Details Example (Sync)

This example demonstrates how to retrieve detailed information about a specific voice.
"""

import os
from supertone import Supertone


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

    # Replace with an actual voice ID from your account
    VOICE_ID = "your-voice-id-here"

    try:
        # Get detailed information about a specific voice
        voice = client.voices.get_voice(voice_id=VOICE_ID)

        print("✅ Voice Details Retrieved")
        print("\n🎤 Voice Information:")
        print(f"   Name: {voice.name}")
        print(f"   ID: {voice.voice_id}")
        print(f"   Language: {voice.language}")

        if hasattr(voice, "description") and voice.description:
            print(f"   Description: {voice.description}")

        if hasattr(voice, "tags") and voice.tags:
            print(f"   Tags: {', '.join(voice.tags)}")

        if hasattr(voice, "created_at"):
            print(f"   Created: {voice.created_at}")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Tip: Make sure to replace VOICE_ID with a valid voice ID")

    finally:
        client.close()


if __name__ == "__main__":
    main()
