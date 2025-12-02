"""
Get Voice Usage Example (Async)

This example demonstrates how to asynchronously retrieve TTS API usage data
filtered by date range. All dates are in UTC+0 timezone.
"""

import asyncio
import os
from datetime import datetime, timedelta
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
            # Get usage data for the last 7 days
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=7)

            response = await client.usage.get_voice_usage_async(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )

            print("✅ Voice Usage Retrieved (Async)")
            print(f"   Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            print(f"   Total Items: {response.total_items}")

            # Display usage data
            if response.data:
                print("\n📊 Usage Details:")
                for i, usage in enumerate(response.data[:10], 1):  # Show first 10 records
                    print(f"\n   {i}. Date: {usage.created_at}")
                    if hasattr(usage, "voice_id"):
                        print(f"      Voice ID: {usage.voice_id}")
                    if hasattr(usage, "credits_used"):
                        print(f"      Credits Used: {usage.credits_used}")
                    if hasattr(usage, "text_length"):
                        print(f"      Text Length: {usage.text_length}")

                if len(response.data) > 10:
                    print(f"\n   ... and {len(response.data) - 10} more records")
            else:
                print("\n   No usage data found for the specified date range.")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

