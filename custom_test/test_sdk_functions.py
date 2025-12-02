#!/usr/bin/env python3
"""
SDK Function Test Script (Dynamic Discovery Version)
Automatically detects and validates all SDK functionality without knowing function names.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# API key configuration (from environment variable or test key)
TEST_API_KEY = os.getenv("SUPERTONE_API_KEY", "your-api-key-here")
TEST_VOICE_ID = "voice_emma_001"


def analyze_method_signature(obj, method_name: str) -> dict:
    """Analyze method signature"""
    try:
        import inspect

        method = getattr(obj, method_name)
        sig = inspect.signature(method)

        # Analyze parameters
        params = []
        required_params = []
        optional_params = []

        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue

            param_info = {
                "name": param_name,
                "type": (
                    str(param.annotation) if param.annotation != param.empty else "Any"
                ),
                "default": str(param.default) if param.default != param.empty else None,
                "required": param.default == param.empty,
            }

            params.append(param_info)
            if param_info["required"]:
                required_params.append(param_name)
            else:
                optional_params.append(param_name)

        return {
            "params": params,
            "required_params": required_params,
            "optional_params": optional_params,
            "param_count": len(params),
            "docstring": getattr(method, "__doc__", "No documentation"),
            "return_type": (
                str(sig.return_annotation)
                if sig.return_annotation != sig.empty
                else "Any"
            ),
        }

    except Exception as e:
        return {
            "error": str(e),
            "params": [],
            "required_params": [],
            "optional_params": [],
            "param_count": 0,
            "docstring": "Analysis failed",
            "return_type": "Unknown",
        }


def discover_client_methods(client_obj, client_name: str) -> dict:
    """Discover all public methods of client object (excluding specific internal methods)"""
    if not hasattr(client_obj, "__dict__") and not hasattr(client_obj, "__class__"):
        return {}

    excluded_methods = {"do_request", "do_request_async", "sdk_configuration"}

    # Extract only public methods (exclude private/protected and specific internal methods)
    methods = [
        name
        for name in dir(client_obj)
        if not name.startswith("_")
        and callable(getattr(client_obj, name, None))
        and name not in excluded_methods
    ]

    method_details = {}
    successful_methods = []
    failed_methods = []

    for method_name in methods:
        try:
            method = getattr(client_obj, method_name)
            docstring = getattr(method, "__doc__", "")

            # 시그니처 분석
            signature_info = analyze_method_signature(client_obj, method_name)

            method_info = {
                "name": method_name,
                "client": client_name,
                "signature": signature_info,
                "is_async": method_name.endswith("_async"),
                "docstring_preview": (
                    docstring[:100] + "..."
                    if docstring and len(docstring) > 100
                    else docstring
                ),
            }

            successful_methods.append(method_info)
            method_details[method_name] = method_info

        except Exception as e:
            failed_method = {
                "name": method_name,
                "client": client_name,
                "error": str(e),
                "is_async": method_name.endswith("_async"),
            }
            failed_methods.append(failed_method)

    return {
        "successful_methods": successful_methods,
        "failed_methods": failed_methods,
        "details": method_details,
        "total_methods": len(methods),
        "success_count": len(successful_methods),
        "failure_count": len(failed_methods),
    }


def test_dynamic_sdk_discovery():
    """Dynamic SDK structure discovery test"""
    print("🔍 SDK Structure Dynamic Discovery Test Start")

    try:
        from supertone import Supertone, models

        with Supertone(api_key=TEST_API_KEY) as client:
            print("  📋 Detecting available clients:")

            # Client mappings (per user request)
            client_mappings = {
                "text_to_speech": "TTS",
                "voices": "Voices",
                "custom_voices": "Custom Voices",
                "usage": "Usage",
            }

            # Find all client attributes
            client_attrs = [
                name
                for name in dir(client)
                if not name.startswith("_")
                and hasattr(getattr(client, name), "__dict__")
                and name in client_mappings
            ]

            all_methods = {}
            total_methods_found = 0
            total_success = 0
            total_failures = 0

            for attr_name in client_attrs:
                client_obj = getattr(client, attr_name)
                display_name = client_mappings[attr_name]

                print(f"    🔍 Analyzing {display_name} ({attr_name}) client...")

                methods_info = discover_client_methods(client_obj, attr_name)
                all_methods[attr_name] = methods_info

                total_methods_found += methods_info["total_methods"]
                total_success += methods_info["success_count"]
                total_failures += methods_info["failure_count"]

                print(f"      ✅ {methods_info['success_count']} methods successful")
                if methods_info["failure_count"] > 0:
                    print(f"      ❌ {methods_info['failure_count']} methods failed")

                # List successful methods
                if methods_info["successful_methods"]:
                    method_names = [
                        m["name"] for m in methods_info["successful_methods"]
                    ]
                    print(f"        📂 Methods: {method_names}")

            print(f"\n  📊 Overall Detection Results:")
            print(f"    🎯 Total methods: {total_methods_found}")
            print(f"    ✅ Analysis successful: {total_success}")
            print(f"    ❌ Analysis failed: {total_failures}")

            return all_methods

    except Exception as e:
        print(f"  ❌ Dynamic discovery failed: {e}")
        return {}


def test_method_signatures(methods_data: dict):
    """Test signatures of detected methods"""
    print("📝 Method Signature Validation Test Start")

    try:
        signature_results = {
            "total_methods": 0,
            "valid_signatures": 0,
            "invalid_signatures": 0,
            "methods_with_required_params": 0,
            "async_methods": 0,
            "clients": {},
        }

        client_display_names = {
            "text_to_speech": "TTS",
            "voices": "Voices",
            "custom_voices": "Custom Voices",
            "usage": "Usage",
        }

        for client_name, client_data in methods_data.items():
            display_name = client_display_names.get(client_name, client_name)
            print(f"  📋 {display_name} Method Signature Validation:")

            client_stats = {
                "total": 0,
                "valid": 0,
                "invalid": 0,
                "async": 0,
                "with_required_params": 0,
            }

            # Validate successful methods
            for method_info in client_data["successful_methods"]:
                method_name = method_info["name"]
                signature = method_info["signature"]

                client_stats["total"] += 1
                signature_results["total_methods"] += 1

                if "error" in signature:
                    print(f"    ❌ {method_name}: {signature['error']}")
                    signature_results["invalid_signatures"] += 1
                    client_stats["invalid"] += 1
                else:
                    print(f"    ✅ {method_name}:")
                    print(
                        f"      📥 Required parameters ({len(signature['required_params'])}): {signature['required_params']}"
                    )
                    print(
                        f"      📤 Optional parameters ({len(signature['optional_params'])}): {signature['optional_params']}"
                    )

                    signature_results["valid_signatures"] += 1
                    client_stats["valid"] += 1

                    if signature["required_params"]:
                        signature_results["methods_with_required_params"] += 1
                        client_stats["with_required_params"] += 1

                    if method_info["is_async"]:
                        signature_results["async_methods"] += 1
                        client_stats["async"] += 1

            # Count failed methods too
            for failed_method in client_data["failed_methods"]:
                print(
                    f"    ❌ {failed_method['name']}: Method access failed - {failed_method['error']}"
                )
                signature_results["invalid_signatures"] += 1
                client_stats["invalid"] += 1
                client_stats["total"] += 1
                signature_results["total_methods"] += 1

            signature_results["clients"][client_name] = client_stats

        # Results summary
        print(f"\n  📊 Signature Validation Final Results:")
        print(f"    🎯 Total methods: {signature_results['total_methods']}")
        print(f"    ✅ Valid signatures: {signature_results['valid_signatures']}")
        print(f"    ❌ Invalid signatures: {signature_results['invalid_signatures']}")
        print(f"    ⚡ Async methods: {signature_results['async_methods']}")
        print(
            f"    📋 Methods with required params: {signature_results['methods_with_required_params']}"
        )

        # Calculate success rate
        if signature_results["total_methods"] > 0:
            success_rate = (
                signature_results["valid_signatures"]
                / signature_results["total_methods"]
            ) * 100
            print(f"    📈 Overall success rate: {success_rate:.1f}%")

        return signature_results

    except Exception as e:
        print(f"  ❌ Signature validation failed: {e}")
        return {}


def test_models_discovery():
    """Models dynamic discovery test"""
    print("📦 Models Dynamic Discovery Test Start")

    try:
        from supertone import models

        # Find all model classes
        model_classes = []
        enums = []
        other_objects = []

        for name in dir(models):
            if name.startswith("_"):
                continue

            try:
                obj = getattr(models, name)

                # Check if it's a class
                if hasattr(obj, "__bases__"):
                    # Check if it's an Enum
                    if hasattr(obj, "__members__"):
                        enum_values = list(obj.__members__.keys())
                        enum_items = [(k, v.value) for k, v in obj.__members__.items()]

                        enums.append(
                            {
                                "name": name,
                                "values": enum_values,
                                "items": enum_items,
                                "count": len(enum_values),
                            }
                        )
                    else:
                        # Model class
                        fields = []
                        if hasattr(obj, "__fields__"):
                            fields = list(obj.__fields__.keys())
                        elif hasattr(obj, "model_fields"):
                            fields = list(obj.model_fields.keys())

                        model_classes.append(
                            {"name": name, "fields": fields, "field_count": len(fields)}
                        )
                else:
                    other_objects.append(
                        {"name": name, "type": str(type(obj).__name__)}
                    )

            except Exception as e:
                other_objects.append({"name": name, "type": f"Error: {str(e)}"})

        print(f"  📊 Models Detection Results:")
        print(f"    📋 Model classes: {len(model_classes)}")
        print(f"    🔢 Enum classes: {len(enums)}")
        print(f"    📦 Other objects: {len(other_objects)}")

        # Detailed output of important models
        if model_classes:
            print(f"\n  📋 Major Model Classes (sorted by field count):")
            sorted_models = sorted(
                model_classes, key=lambda x: x["field_count"], reverse=True
            )
            for model in sorted_models[:10]:
                print(f"    ✅ {model['name']}: {model['field_count']} fields")
                if model["fields"]:
                    preview_fields = model["fields"][:3]
                    more_text = (
                        f"... (+{len(model['fields'])-3} more)"
                        if len(model["fields"]) > 3
                        else ""
                    )
                    print(f"      Fields: {preview_fields}{more_text}")

        if enums:
            print(f"\n  🔢 Enum Classes:")
            for enum in enums:
                print(f"    ✅ {enum['name']}: {enum['count']} values")
                print(f"      Values: {enum['items']}")

        return {
            "models": model_classes,
            "enums": enums,
            "others": other_objects,
            "total_models": len(model_classes),
            "total_enums": len(enums),
            "total_others": len(other_objects),
        }

    except Exception as e:
        print(f"  ❌ Models discovery failed: {e}")
        return {}


def test_comprehensive_functionality():
    """Comprehensive functionality test"""
    print("🧪 Comprehensive Functionality Test Start")

    results = {}

    # 1. Dynamic SDK discovery
    print("\n" + "=" * 50)
    methods_data = test_dynamic_sdk_discovery()
    results["methods"] = methods_data

    if not methods_data:
        print("❌ SDK discovery failed, stopping comprehensive test")
        return False

    # 2. Signature validation
    print("\n" + "=" * 50)
    signature_results = test_method_signatures(methods_data)
    results["signatures"] = signature_results

    # 3. Models discovery
    print("\n" + "=" * 50)
    models_data = test_models_discovery()
    results["models"] = models_data

    # 4. Results summary
    print("\n" + "=" * 50)
    print("🎉 Comprehensive Test Complete!")

    # Calculate statistics
    total_clients = len(methods_data)
    total_methods = sum(data["total_methods"] for data in methods_data.values())
    successful_methods = sum(data["success_count"] for data in methods_data.values())

    print(f"\n📊 Final Statistics:")
    print(f"  🏗️  Clients: {total_clients}")
    print(f"  ⚙️  Total methods: {total_methods}")
    print(f"  ✅ Successfully analyzed methods: {successful_methods}")

    if models_data:
        print(f"  📋 Model classes: {models_data['total_models']}")
        print(f"  🔢 Enum classes: {models_data['total_enums']}")

    if signature_results and signature_results["total_methods"] > 0:
        success_rate = (
            signature_results["valid_signatures"] / signature_results["total_methods"]
        ) * 100
        print(f"  📈 Overall success rate: {success_rate:.1f}%")
        print(f"  ⚡ Async methods: {signature_results['async_methods']}")

    # Detailed statistics by client
    print(f"\n📋 Details by Client:")
    client_names = {
        "text_to_speech": "TTS",
        "voices": "Voices",
        "custom_voices": "Custom Voices",
        "usage": "Usage",
    }

    for client_key, client_data in methods_data.items():
        display_name = client_names.get(client_key, client_key)
        print(f"  🔸 {display_name}: {client_data['success_count']} methods")

    return True


def main():
    """Main test execution"""
    print("🧪 SDK Dynamic Analysis Test Start")
    print("=" * 60)
    print(
        "💡 Excluding only specific internal methods (do_request, do_request_async, sdk_configuration)"
    )
    print("   All other SDK features are automatically detected!")
    print("=" * 60)

    try:
        success = test_comprehensive_functionality()

        if success:
            print("\n🎉 All dynamic analysis tests complete!")
        else:
            print("⚠️ Some tests failed. Please check the issues.")

        return success

    except Exception as e:
        print(f"❌ Error occurred during test execution: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
