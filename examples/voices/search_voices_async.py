"""
Search Voices Example (Async)

This example demonstrates how to asynchronously search and filter voices.
Perfect for non-blocking voice search in async applications.
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
            # Search voices with filters asynchronously
            response = await client.voices.search_voices_async(
                page_size=10,
                # Search filters (all optional):
                # name="Alice",              # Search by name
                # description="professional", # Search by description
                language="en",             # Filter by language (comma-separated)
                # gender="female",           # Filter by gender (comma-separated)
                # age="young",               # Filter by age (comma-separated)
                # use_case="audiobook",      # Filter by use case (comma-separated)
                # style="calm",              # Filter by style (comma-separated for OR, semicolon for AND)
                # model="sona_speech_1",     # Filter by model (comma-separated)
            )

            print("✅ Voice Search Completed (Async)")
            print(f"   Total Results: {response.total_items}")
            print(f"   Page Size: {response.page_size}")

            # Display search results
            if response.data:
                print("\n🎤 Search Results:")
                for i, voice in enumerate(response.data, 1):
                    print(f"\n   {i}. {voice.name}")
                    print(f"      ID: {voice.voice_id}")
                    print(f"      Language: {voice.language}")
                    if hasattr(voice, "gender") and voice.gender:
                        print(f"      Gender: {voice.gender}")
                    if hasattr(voice, "age") and voice.age:
                        print(f"      Age: {voice.age}")
                    if hasattr(voice, "tags") and voice.tags:
                        print(f"      Tags: {', '.join(voice.tags)}")

            # Pagination support
            if hasattr(response, "next_page_token") and response.next_page_token:
                print(f"\n📄 More results available. Use next_page_token: {response.next_page_token[:20]}...")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

