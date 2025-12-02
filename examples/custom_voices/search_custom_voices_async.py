"""
Search Custom Voices Example (Async)

This example demonstrates how to asynchronously search and filter your custom cloned voices.
Perfect for non-blocking search in async applications.
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
        try:
            # Search custom voices asynchronously
            response = await client.custom_voices.search_custom_voices_async(
                page_size=10,
                # Search filters (all optional):
                # name="John",               # Search by name (space-separated for AND)
                # description="professional", # Search by description (space-separated for AND)
            )

            print("✅ Custom Voice Search Completed (Async)")
            print(f"   Total Results: {response.total_items}")
            print(f"   Page Size: {response.page_size}")

            # Display search results
            if response.data:
                print("\n🎭 Search Results:")
                for i, voice in enumerate(response.data, 1):
                    print(f"\n   {i}. {voice.name}")
                    print(f"      ID: {voice.voice_id}")
                    if hasattr(voice, "description") and voice.description:
                        print(f"      Description: {voice.description}")
                    if hasattr(voice, "created_at") and voice.created_at:
                        print(f"      Created: {voice.created_at}")
            else:
                print("\n   No custom voices found matching the search criteria.")

            # Pagination support
            if hasattr(response, "next_page_token") and response.next_page_token:
                print(f"\n📄 More results available. Use next_page_token: {response.next_page_token[:20]}...")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

