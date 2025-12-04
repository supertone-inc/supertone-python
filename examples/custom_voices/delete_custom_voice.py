"""
Delete Custom Voice Example (Sync)

This example demonstrates how to permanently delete a custom cloned voice.
⚠️ WARNING: This action is irreversible! The voice will be permanently deleted.
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
        # Replace with an actual custom voice ID from your account
        CUSTOM_VOICE_ID = "your-custom-voice-id-here"

        try:
            # ⚠️ WARNING: This will permanently delete the custom voice
            print("⚠️  WARNING: You are about to permanently delete a custom voice!")
            print(f"   Voice ID: {CUSTOM_VOICE_ID}")
            
            # Uncomment the following lines to actually delete the voice
            # confirmation = input("\n   Type 'DELETE' to confirm: ")
            # if confirmation != "DELETE":
            #     print("   Deletion cancelled.")
            #     return

            # Delete the custom voice
            client.custom_voices.delete_custom_voice(voice_id=CUSTOM_VOICE_ID)

            print("✅ Custom Voice Deleted Successfully")
            print(f"   Deleted Voice ID: {CUSTOM_VOICE_ID}")
            print("\n⚠️  This action cannot be undone!")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Tip: Make sure to replace CUSTOM_VOICE_ID with a valid custom voice ID")
            print("   Run: python examples/custom_voices/list_custom_voices.py")


if __name__ == "__main__":
    main()

