"""
List Custom Voices Example (Sync)

This example demonstrates how to retrieve a list of your custom cloned voices.
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

    # Initialize the SDK with context manager
    with Supertone(api_key=api_key) as client:
        try:
            # List your custom voices
            response = client.custom_voices.list_custom_voices(page=1, page_size=10)

            print("✅ Custom Voices Retrieved")
            print(f"   Total Voices: {response.total_items}")
            print(f"   Current Page: {response.page}/{response.total_pages}")

            # Display custom voice information
            if response.data:
                print("\n🎭 Your Custom Voices:")
                for i, voice in enumerate(response.data, 1):
                    print(f"\n   {i}. {voice.name}")
                    print(f"      ID: {voice.voice_id}")
                    if hasattr(voice, "created_at"):
                        print(f"      Created: {voice.created_at}")
            else:
                print("\n   No custom voices found.")
                print("   💡 Create a custom voice using create_cloned_voice()")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
