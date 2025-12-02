"""
Get Credit Balance Example (Async)

This example demonstrates how to retrieve your account's credit balance asynchronously.
Async operations are ideal for web servers, APIs, and applications handling multiple requests.
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

    # Initialize the SDK
    async with Supertone(api_key=api_key) as client:
        try:
            # Get current credit balance asynchronously
            response = await client.usage.get_credit_balance_async()

            print("✅ Credit Balance Retrieved")
            print(f"   Credits: {response.credits}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
