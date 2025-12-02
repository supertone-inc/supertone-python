"""
Get Voice Usage Example (Sync)

This example demonstrates how to retrieve TTS API usage data filtered by date range.
All dates are in UTC+0 timezone.
"""

import os
from datetime import datetime, timedelta
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
        # Get usage data for the last 7 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=7)

        response = client.usage.get_voice_usage(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )

        print("✅ Voice Usage Retrieved")
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

    finally:
        client.close()


if __name__ == "__main__":
    main()

