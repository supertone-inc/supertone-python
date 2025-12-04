"""
Get Usage Statistics Example (Sync)

This example demonstrates how to retrieve detailed usage statistics for your account.
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
            # Get usage statistics with pagination
            response = client.usage.get_usage(
                page=1, page_size=20  # Get up to 20 records per page
            )

            print("✅ Usage Statistics Retrieved")
            print(f"   Total Items: {response.total_items}")
            print(f"   Current Page: {response.page}")
            print(f"   Total Pages: {response.total_pages}")

            # Display first few usage records
            if response.data:
                print("\n📊 Recent Usage:")
                for i, usage in enumerate(response.data[:5], 1):
                    print(f"   {i}. Credits Used: {usage.credits_used}")
                    print(f"      Date: {usage.created_at}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
