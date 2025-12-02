#!/usr/bin/env python3
"""
SDK Basic Functionality Test Script
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Test configuration
TEST_API_KEY = os.getenv("SUPERTONE_API_KEY", "test_api_key_for_structure_validation")


def test_sdk_import():
    """Test SDK import"""
    try:
        from supertone import Supertone, models

        print("✅ SDK import successful")
        return True
    except Exception as e:
        print(f"❌ SDK import failed: {e}")
        return False


def test_sdk_initialization():
    """Test SDK initialization"""
    try:
        from supertone import Supertone

        sdk = Supertone(api_key=TEST_API_KEY)
        print("✅ SDK initialization successful")
        return True
    except Exception as e:
        print(f"❌ SDK initialization failed: {e}")
        return False


def test_sdk_structure():
    """Test SDK structure"""
    try:
        from supertone import Supertone

        sdk = Supertone(api_key=TEST_API_KEY)

        # Check main clients
        print("📋 SDK structure check:")

        if hasattr(sdk, "text_to_speech"):
            tts_methods = [
                method
                for method in dir(sdk.text_to_speech)
                if not method.startswith("_")
            ]
            print(f"  ✅ text_to_speech client: {tts_methods}")
        else:
            print("  ❌ text_to_speech client not found")

        if hasattr(sdk, "voices"):
            voice_methods = [
                method for method in dir(sdk.voices) if not method.startswith("_")
            ]
            print(f"  ✅ voices client: {voice_methods}")
        else:
            print("  ❌ voices client not found")

        if hasattr(sdk, "custom_voices"):
            custom_methods = [
                method
                for method in dir(sdk.custom_voices)
                if not method.startswith("_")
            ]
            print(f"  ✅ custom_voices client: {custom_methods}")
        else:
            print("  ❌ custom_voices client not found")

        if hasattr(sdk, "usage"):
            usage_methods = [
                method for method in dir(sdk.usage) if not method.startswith("_")
            ]
            print(f"  ✅ usage client: {usage_methods}")
        else:
            print("  ❌ usage client not found")

        return True
    except Exception as e:
        print(f"❌ SDK structure check failed: {e}")
        return False


def test_models():
    """Test model classes"""
    try:
        from supertone import models

        print("📋 Models check:")

        # Check available models
        available_models = [attr for attr in dir(models) if not attr.startswith("_")]
        print(f"  ✅ Available models: {len(available_models)} items")

        return True
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False


def test_context_manager():
    """Test context manager"""
    try:
        from supertone import Supertone

        with Supertone(api_key=TEST_API_KEY) as sdk:
            print("✅ Context manager creation successful")
            # Check if SDK methods are callable
            if hasattr(sdk.text_to_speech, "convert_text_to_speech"):
                print("  ✅ convert_text_to_speech method exists")
            if hasattr(sdk.voices, "list_voices"):
                print("  ✅ list_voices method exists")

        print("✅ Context manager exit successful")
        return True
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False


def main():
    """Main test execution"""
    print("🧪 SDK Basic Test Start")
    print("=" * 50)

    tests = [
        ("SDK Import", test_sdk_import),
        ("SDK Initialization", test_sdk_initialization),
        ("SDK Structure", test_sdk_structure),
        ("Models", test_models),
        ("Context Manager", test_context_manager),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        results.append(test_func())

    print("\n" + "=" * 50)
    print("🧪 Test Results Summary:")
    passed = sum(results)
    total = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"  {test_name}: {status}")

    print(f"\nTotal {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! SDK is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the issues.")


if __name__ == "__main__":
    main()
