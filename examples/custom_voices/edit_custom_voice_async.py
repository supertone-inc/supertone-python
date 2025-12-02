"""
Edit Custom Voice Example (Async)

This example demonstrates how to asynchronously update a custom cloned voice's
name and/or description.
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
            # Update custom voice details asynchronously (partial update)
            response = await client.custom_voices.edit_custom_voice_async(
                voice_id=CUSTOM_VOICE_ID,
                name="Updated Voice Name",  # Optional: new name
                description="Updated description for this custom voice",  # Optional: new description
            )

            print("✅ Custom Voice Updated Successfully (Async)")
            print(f"   Voice ID: {response.voice_id}")
            print(f"   New Name: {response.name}")
            if hasattr(response, "description") and response.description:
                print(f"   New Description: {response.description}")
            if hasattr(response, "updated_at") and response.updated_at:
                print(f"   Updated At: {response.updated_at}")

            print("\n💡 Perfect for batch updates in async workflows")

        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Tip: Make sure to replace CUSTOM_VOICE_ID with a valid custom voice ID")
            print("   Run: python examples/custom_voices/list_custom_voices_async.py")


if __name__ == "__main__":
    asyncio.run(main())

