"""
List Voices Example (Sync)

This example demonstrates how to retrieve a list of available voices.
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

    try:
        # List available voices with pagination
        response = client.voices.list_voices(
            page=1, page_size=10  # Number of voices per page (10-100)
        )

        print("✅ Voices Retrieved")
        print(f"   Total Voices: {response.total_items}")
        print(f"   Current Page: {response.page}/{response.total_pages}")

        # Display voice information
        if response.data:
            print("\n🎤 Available Voices:")
            for i, voice in enumerate(response.data, 1):
                print(f"\n   {i}. {voice.name}")
                print(f"      ID: {voice.voice_id}")
                print(f"      Language: {voice.language}")
                if hasattr(voice, "tags") and voice.tags:
                    print(f"      Tags: {', '.join(voice.tags)}")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        client.close()


if __name__ == "__main__":
    main()
