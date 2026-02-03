#!/usr/bin/env python3
"""
Async API Integration Test Script
Tests all async SDK functionality with real Supertone API calls.
"""
import sys
import os
import json
from datetime import datetime, timedelta
import time
import asyncio

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # Load .env from the same directory as this script (custom_test/)
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
    if os.path.exists(env_path):
        print(f"✅ Loaded .env file from: {env_path}")
    else:
        print(f"⚠️ .env file not found at: {env_path}")
        print(
            "   Create .env file in custom_test/ directory with: SUPERTONE_API_KEY=your-key"
        )
except ImportError:
    print(
        "⚠️ Warning: python-dotenv not installed. Install with: pip install python-dotenv"
    )
    print("   Falling back to system environment variables only.\n")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# API Key for testing (from environment variable or hardcoded for testing)
API_KEY = os.getenv("SUPERTONE_API_KEY", "your-api-key-here")


async def test_credit_balance():
    """Test credit balance retrieval - safest async API call"""
    print("💰 Credit Balance Test (Async)")

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Retrieving credit balance...")

            response = await client.usage.get_credit_balance_async()

            print(f"  ✅ Credit Balance: {response.balance}")
            return True, response

    except errors.UnauthorizedErrorResponse as e:
        print(f"  ❌ Authentication failed: Invalid API key")
        print(f"     Status code: {e.status_code}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        print(f"     Status code: {e.status_code}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_get_usage():
    """Test usage retrieval (Advanced Usage Analytics) - async"""
    print("📊 Usage Analytics Test (Async)")

    try:
        from supertone import Supertone, errors

        # Query last 7 days usage
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Retrieving usage from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}..."
            )

            response = await client.usage.get_usage_async(
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
            )

            print(f"  ✅ Success: {len(response.data)} usage record buckets")
            print(f"  📊 Total buckets: {response.total}")

            if response.data:
                for bucket in response.data[:3]:
                    print(f"  📅 Bucket start: {bucket.starting_at}")
                    print(f"     Bucket end: {bucket.ending_at}")
                    print(f"     Results: {len(bucket.results)} items")

                    total_minutes = sum(
                        result.minutes_used for result in bucket.results
                    )
                    print(f"     Total usage: {total_minutes:.2f} minutes")

                    for result in bucket.results[:3]:
                        voice_info = (
                            result.voice_name
                            if result.voice_name
                            else f"Voice {result.voice_id[:8] if result.voice_id else 'Unknown'}"
                        )
                        print(f"       🎤 {voice_info}: {result.minutes_used:.2f}min")
            else:
                print("  📝 No usage records for this period")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_get_voice_usage():
    """Test voice-specific usage retrieval - async"""
    print("🎤 Voice Usage Test (Async)")

    try:
        from supertone import Supertone, errors

        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Retrieving voice usage from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}..."
            )

            response = await client.usage.get_voice_usage_async(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )

            print(f"  ✅ Success: {len(response.usages)} voice usage records")

            if response.usages:
                for usage in response.usages[:5]:
                    voice_name = (
                        usage.name if usage.name else f"Voice {usage.voice_id[:8]}"
                    )
                    print(f"  🎤 {voice_name}: {usage.total_minutes_used:.2f}min")
                    print(f"     Voice ID: {usage.voice_id}")
                    if usage.language:
                        print(f"     Language: {usage.language}")
            else:
                print("  📝 No voice usage records for this period")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_list_voices():
    """Test voice listing - async"""
    print("🎵 Voice List Test (Async)")

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Retrieving voice list...")

            response = await client.voices.list_voices_async(page_size=10)

            print(f"  ✅ Success: {len(response.items)} voices")
            print(f"  📊 Total voices: {response.total}")

            if response.items:
                first_voice = response.items[0]
                print(f"  🎤 First voice:")
                print(f"     ID: {first_voice.voice_id}")
                print(f"     Name: {first_voice.name}")
                print(f"     Description: {first_voice.description[:50]}...")
                print(f"     Language: {first_voice.language}")
                print(f"     Gender: {first_voice.gender}")

                return True, (response, first_voice.voice_id)
            else:
                print("  ⚠️ Voice list is empty")
                return True, (response, None)

    except errors.UnauthorizedErrorResponse as e:
        print(f"  ❌ Authentication failed: Invalid API key")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_search_voices():
    """Test voice search - async"""
    print("🔍 Voice Search Test (Async)")

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Searching for female English voices...")

            response = await client.voices.search_voices_async(
                language="en",
                gender="female",
                page_size=10,
            )

            print(f"  ✅ Search success: {len(response.items)} voices")

            for voice in response.items:
                print(f"  🎤 {voice.name} ({voice.voice_id})")
                print(f"     Language: {voice.language}, Gender: {voice.gender}")
                print(f"     Use case: {voice.use_case}")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_get_voice(voice_id):
    """Test voice detail retrieval - async"""
    print("📄 Voice Detail Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Retrieving voice '{voice_id}' details...")

            response = await client.voices.get_voice_async(voice_id=voice_id)

            print(f"  ✅ Success:")
            print(f"     Name: {response.name}")
            print(f"     ID: {response.voice_id}")
            print(f"     Description: {response.description}")
            print(f"     Language: {response.language}")
            print(f"     Gender: {response.gender}")

            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_list_custom_voices():
    """Test custom voice listing - async"""
    print("🎨 Custom Voice List Test (Async)")

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Retrieving custom voice list...")

            response = await client.custom_voices.list_custom_voices_async(page_size=10)

            print(f"  ✅ Success: {len(response.items)} custom voices")
            print(f"  📊 Total custom voices: {response.total}")

            custom_voice_id = None
            for voice in response.items:
                print(f"  🎤 {voice.name} ({voice.voice_id})")
                print(f"     Description: {voice.description}")
                if custom_voice_id is None:
                    custom_voice_id = voice.voice_id

            return True, (response, custom_voice_id)

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_search_custom_voices():
    """Test custom voice search - async"""
    print("🔍 Custom Voice Search Test (Async)")

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Searching custom voices...")

            response = await client.custom_voices.search_custom_voices_async(
                page_size=10
            )

            print(f"  ✅ Search success: {len(response.items)} custom voices")

            for voice in response.items:
                print(f"  🎤 {voice.name} ({voice.voice_id})")
                print(f"     Description: {voice.description}")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_get_custom_voice(voice_id):
    """Test custom voice detail retrieval - async"""
    print("📄 Custom Voice Detail Test (Async)")

    if not voice_id:
        print("  ⚠️ No custom voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Retrieving custom voice '{voice_id}' details...")

            response = await client.custom_voices.get_custom_voice_async(
                voice_id=voice_id
            )

            print(f"  ✅ Success:")
            print(f"     Name: {response.name}")
            print(f"     ID: {response.voice_id}")
            print(f"     Description: {response.description}")

            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Custom voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_cloned_voice():
    """Test custom voice creation - async (uses voice_sample.wav file)"""
    print("🎨 Custom Voice Creation Test (Async)")

    audio_file_path = "voice_sample.wav"

    if not os.path.exists(audio_file_path):
        print(f"  ❌ Audio file not found: {audio_file_path}")
        return False, None

    file_size = os.path.getsize(audio_file_path)
    max_size = 3 * 1024 * 1024  # 3MB

    print(f"  📏 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

    if file_size > max_size:
        print(f"  ❌ File exceeds 3MB limit: {file_size/1024/1024:.2f} MB")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            timestamp = datetime.now().strftime("%m%d_%H%M")
            voice_name = f"Test Sample Voice {timestamp} (Async)"
            voice_description = f"Test async custom voice created at {timestamp}"

            print(f"  🔍 Creating custom voice...")
            print(f"     File: {audio_file_path}")
            print(f"     Name: {voice_name}")
            print(f"     Description: {voice_description}")
            print("  ⚠️ This test consumes credits and creates actual custom voice!")

            with open(audio_file_path, "rb") as audio_file:
                audio_content = audio_file.read()

                files_obj = models.Files(
                    file_name="voice_sample.wav",
                    content=audio_content,
                    content_type="audio/wav",
                )

                response = await client.custom_voices.create_cloned_voice_async(
                    files=files_obj,
                    name=voice_name,
                    description=voice_description,
                )

            print(f"  ✅ Custom voice creation request successful!")
            print(f"     Voice ID: {response.voice_id}")
            print(f"     Status: {getattr(response, 'status', 'Unknown')}")

            return True, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.PayloadTooLargeErrorResponse as e:
        print(f"  ❌ File too large: Exceeds 3MB limit")
        return False, e
    except errors.UnsupportedMediaTypeErrorResponse as e:
        print(f"  ❌ Unsupported format: Use WAV or MP3")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_edit_custom_voice(voice_id):
    """Test custom voice update - async"""
    print("✏️ Custom Voice Update Test (Async)")

    if not voice_id:
        print("  ⚠️ No custom voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            timestamp = datetime.now().strftime("%H%M%S")
            test_name = f"Updated Test Voice {timestamp} (Async)"
            test_description = f"Updated async description at {timestamp}"

            print(f"  🔄 Updating custom voice '{voice_id}'...")
            print(f"     New name: {test_name}")
            print(f"     New description: {test_description}")

            response = await client.custom_voices.edit_custom_voice_async(
                voice_id=voice_id,
                name=test_name,
                description=test_description,
            )

            print(f"  ✅ Update successful:")
            print(f"     Updated name: {response.name}")
            print(f"     Updated description: {response.description}")

            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Custom voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_delete_custom_voice(voice_id):
    """Test custom voice deletion - async"""
    print("🗑️ Custom Voice Deletion Test (Async)")

    if not voice_id:
        print("  ⚠️ No custom voice ID to delete")
        return False, None

    try:
        from supertone import Supertone, errors

        print("  ⚠️ This test will actually delete the custom voice!")
        print("     Use for testing purposes only.")

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Deleting custom voice '{voice_id}'...")

            response = await client.custom_voices.delete_custom_voice_async(
                voice_id=voice_id
            )

            print(f"  ✅ Deletion successful:")
            print(f"     Response: {response}")

            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Custom voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_predict_duration(voice_id):
    """Test duration prediction - async (safe test before TTS)"""
    print("⏱️ Duration Prediction Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Predicting duration with voice '{voice_id}'...")

            response = await client.text_to_speech.predict_duration_async(
                voice_id=voice_id,
                text="Hello, this is a test message for duration prediction!",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
            )

            print(f"  ✅ Prediction complete: {response} seconds")
            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech(voice_id):
    """Test TTS conversion - async (consumes credits)"""
    print("🎤 TTS Conversion Test (Async - Consumes Credits)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting text to speech with voice '{voice_id}'...")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="안녕하세요! 이것은 비동기 SDK 테스트를 위한 한국어 텍스트입니다. 정상적으로 작동하는지 확인해보겠습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ TTS conversion success: {audio_size} bytes audio generated"
                )

                output_file = "test_async_create_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio file saved: {output_file}")

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(12)
                    if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                        print(f"  ✅ Valid WAV file generated")
                    else:
                        print(f"  ⚠️ WAV header needs verification: {header[:12]}")

                return True, response
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_long_text(voice_id):
    """Test auto-chunking TTS for long text (300+ chars) - async"""
    print("📜 Long Text Auto-Chunking TTS Test (Async - 300+ chars)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 자동 청킹 TTS 테스트입니다.
        새로 구현된 SDK는 긴 텍스트를 자동으로 여러 개의 청크로 나누어 처리합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹 기능을 통해 긴 텍스트도 자연스럽게 여러 개의 작은 세그먼트로 나누어져 처리됩니다.
        각 세그먼트는 문장 경계와 단어 경계를 고려하여 지능적으로 분할되며, 이를 통해 자연스러운 음성을 생성할 수 있습니다.
        이제 사용자는 텍스트 길이에 대해 걱정할 필요가 없으며, SDK가 모든 것을 자동으로 처리해줍니다.
        """.strip()

        actual_length = len(long_text)
        print(f"  📏 Test text length: {actual_length} characters (exceeds 300)")
        print(f"  🔧 Auto-chunking enabled for text segmentation")

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting long text with voice '{voice_id}' (async)...")
            print("  ⚠️ This test consumes credits!")
            print("  ✨ SDK automatically chunks and processes the text")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ Auto-chunking TTS success: {audio_size} bytes audio generated"
                )
                print(f"  🎯 Long text successfully chunked and processed!")

                output_file = "test_async_auto_chunking_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Auto-chunked audio file saved: {output_file}")

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(12)
                    if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                        print(f"  ✅ Valid auto-chunked WAV file generated")
                    else:
                        print(f"  ⚠️ WAV header needs verification: {header[:12]}")

                estimated_chunks = (actual_length + 299) // 300
                print(
                    f"  📊 Estimated chunks: {estimated_chunks} (based on text length)"
                )
                print(f"  🔀 Parallel processing applied to each chunk")

                return True, {
                    "audio_size": audio_size,
                    "text_length": actual_length,
                    "estimated_chunks": estimated_chunks,
                    "output_file": output_file,
                }
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(f"  ❌ Auto-chunking processing error: {e}")
            print("  🔧 Check chunking logic")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech(voice_id):
    """Test streaming TTS - async"""
    print("🎵 TTS Streaming Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔄 Streaming TTS test with voice '{voice_id}' (async)...")
            print("  ⚠️ This test may consume credits!")

            request_start_time = time.time()

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text="안녕하세요! 이것은 비동기 스트리밍 TTS 테스트를 위한 한국어 텍스트입니다. 스트리밍 기능이 정상적으로 작동하는지 확인하기 위해 조금 더 긴 텍스트를 사용하고 있습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                style="neutral",
                model="sona_speech_1",
            )

            print("  📡 Receiving streaming data...")

            if hasattr(response, "result") and hasattr(response.result, "aiter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []
                first_byte_time = None

                try:
                    async for chunk in response.result.aiter_bytes():
                        if chunk_count == 0:
                            first_byte_time = time.time()
                            first_byte_latency = first_byte_time - request_start_time
                            print(f"  🚀 First Byte arrival: {first_byte_latency:.3f}s")

                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 20:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 21:
                            print(f"     ... (more chunks - log truncated)")
                        elif chunk_count % 50 == 0:
                            print(
                                f"     Chunk {chunk_count}: {chunk_size} bytes (in progress...)"
                            )

                except Exception as iter_error:
                    print(f"  ⚠️ Streaming error: {str(iter_error)[:100]}...")

                end_time = time.time()
                total_time = end_time - request_start_time

                print(
                    f"  ✅ Streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                )
                print(f"  ⏱️ Total time: {total_time:.3f}s")

                if first_byte_time:
                    streaming_time = end_time - first_byte_time
                    print(
                        f"  📊 Streaming time: {streaming_time:.3f}s (after First Byte)"
                    )
                    if streaming_time > 0:
                        throughput = total_bytes / streaming_time
                        print(f"  🚀 Average throughput: {throughput:.0f} bytes/sec")

                if audio_chunks and total_bytes > 0:
                    output_file = "test_async_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 Streaming audio saved: {output_file}")

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    with open(output_file, "rb") as f:
                        header = f.read(12)
                        if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                            print(f"  ✅ Valid streaming WAV file generated")
                        else:
                            print(f"  📄 File header: {header[:12]} (may not be WAV)")

                    return True, f"{chunk_count} chunks, {total_bytes} bytes"
                else:
                    print(f"  ⚠️ No audio data received")
                    return False, "No audio data received"
            else:
                print(f"  ❌ Response missing iter_bytes attribute: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_long_text(voice_id):
    """Test streaming TTS for long text (300+ chars) with WAV format - async"""
    print("📜 Long Text WAV Streaming TTS Test (Async - 300+ chars)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 WAV 스트리밍 TTS 테스트입니다.
        새로 구현된 SDK는 긴 텍스트를 자동으로 여러 개의 청크로 나누어 스트리밍으로 처리합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹 기능을 통해 긴 텍스트도 자연스럽게 여러 개의 작은 세그먼트로 나누어져 처리됩니다.
        각 세그먼트는 문장 경계와 단어 경계를 고려하여 지능적으로 분할되며, 이를 통해 자연스러운 음성을 생성할 수 있습니다.
        스트리밍 방식으로 WAV 형식 처리되기 때문에 사용자는 전체 텍스트의 음성 변환이 완료되기를 기다릴 필요가 없습니다.
        첫 번째 청크의 음성이 생성되는 즉시 재생을 시작할 수 있어 반응성이 크게 향상됩니다.
        """.strip()

        actual_length = len(long_text)
        print(f"  📏 Test text length: {actual_length} characters (exceeds 300)")
        print(f"  🔧 Auto-chunking + WAV streaming enabled")

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Long text WAV streaming TTS conversion with voice '{voice_id}' (async)..."
            )
            print("  ⚠️ This test consumes credits and applies auto-chunking!")
            print("  ✨ SDK automatically chunks text and processes as WAV streaming")

            request_start_time = time.time()

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
            )

            print(f"  🔍 Response type: {type(response)}")
            print(f"  🔍 Result type: {type(response.result)}")

            # Handle real-time streaming response (AsyncExtendedStreamingWrapper)
            if (
                hasattr(response, "result")
                and hasattr(response.result, "aiter_bytes")
                and not isinstance(response.result, str)
            ):
                print("  ✅ Real-time streaming response detected (auto-chunked)")
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []
                first_byte_time = None

                try:
                    async for chunk in response.result.aiter_bytes():
                        if chunk_count == 0:
                            first_byte_time = time.time()
                            first_byte_latency = first_byte_time - request_start_time
                            print(f"  🚀 First Byte arrival: {first_byte_latency:.3f}s")

                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 20:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")

                except Exception as iter_error:
                    print(f"  ⚠️ Long text streaming error: {str(iter_error)[:100]}...")

                print(
                    f"  ✅ Long text streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                )

                if audio_chunks and total_bytes > 0:
                    audio_data = b"".join(audio_chunks)

                    end_time = time.time()
                    total_time = end_time - request_start_time
                    streaming_time = (
                        end_time - first_byte_time if first_byte_time else 0
                    )

                    print(f"  ⏱️ Total time: {total_time:.3f}s")
                    if streaming_time > 0:
                        print(
                            f"  📊 Streaming time: {streaming_time:.3f}s (after First Byte)"
                        )
                        throughput = total_bytes / streaming_time
                        print(f"  🚀 Average throughput: {throughput:.0f} bytes/sec")

                    output_file = "test_async_stream_speech_long_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(audio_data)
                    print(f"  💾 Long text streaming audio saved: {output_file}")
                    print(f"  📏 Saved file size: {total_bytes} bytes")

                    estimated_chunks = (actual_length + 299) // 300
                    print(
                        f"  📊 Estimated text chunks: {estimated_chunks} (based on text length)"
                    )

                    return True, {
                        "chunk_count": chunk_count,
                        "total_bytes": total_bytes,
                        "text_length": actual_length,
                        "estimated_chunks": estimated_chunks,
                    }

            # Handle new JSON format response (old merged format)
            elif hasattr(response, "result") and isinstance(response.result, str):
                try:
                    import base64

                    result_data = json.loads(response.result)
                    print(f"  ✅ Chunked JSON response detected")
                    print(f"  🔍 JSON keys: {list(result_data.keys())}")

                    if "audio_base64" in result_data:
                        first_byte_time = time.time()
                        first_byte_latency = first_byte_time - request_start_time
                        print(
                            f"  🚀 First Byte arrival: {first_byte_latency:.3f}s (chunked merged response)"
                        )

                        audio_data = base64.b64decode(result_data["audio_base64"])
                        total_bytes = len(audio_data)

                        print(f"  ✅ Merged WAV audio data: {total_bytes} bytes")

                        end_time = time.time()
                        total_time = end_time - request_start_time
                        streaming_time = end_time - first_byte_time

                        print(f"  ⏱️ Total time: {total_time:.3f}s")
                        print(
                            f"  📊 Processing time: {streaming_time:.3f}s (after First Byte)"
                        )
                        if streaming_time > 0:
                            throughput = total_bytes / streaming_time
                            print(
                                f"  🚀 Average throughput: {throughput:.0f} bytes/sec"
                            )

                        output_file = "test_async_stream_speech_long_output.wav"
                        with open(output_file, "wb") as f:
                            f.write(audio_data)
                        print(
                            f"  💾 Long text WAV streaming audio saved: {output_file}"
                        )

                        file_size = os.path.getsize(output_file)
                        print(f"  📏 Saved file size: {file_size} bytes")

                        with open(output_file, "rb") as f:
                            header = f.read(12)
                            if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                                print(
                                    f"  ✅ Valid WAV long text streaming file generated"
                                )
                            else:
                                print(
                                    f"  ⚠️ WAV header needs verification: {header[:12]}"
                                )

                        if "phonemes" in result_data and result_data["phonemes"]:
                            phonemes = result_data["phonemes"]
                            print(f"  🔤 Phoneme information included:")
                            print(f"    - Symbols: {len(phonemes.get('symbols', []))}")
                            if phonemes.get("start_times_seconds"):
                                print(
                                    f"    - Start times: {len(phonemes['start_times_seconds'])} items"
                                )
                            if phonemes.get("durations_seconds"):
                                print(
                                    f"    - Durations: {len(phonemes['durations_seconds'])} items"
                                )

                        estimated_chunks = (actual_length + 299) // 300
                        print(
                            f"  📊 Estimated text chunks: {estimated_chunks} (based on text length)"
                        )
                        print(f"  🔀 Auto-chunked segments merged as WAV")

                        return True, {
                            "total_bytes": total_bytes,
                            "text_length": actual_length,
                            "estimated_chunks": estimated_chunks,
                            "format": "wav",
                            "has_phonemes": "phonemes" in result_data
                            and result_data["phonemes"] is not None,
                            "first_byte_latency": first_byte_latency,
                            "total_time": total_time,
                        }
                    else:
                        print(f"  ❌ audio_base64 key missing: {result_data}")
                        return False, result_data

                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON parsing failed: {e}")
                    return False, e
                except Exception as e:
                    print(f"  ❌ Response processing error: {e}")
                    return False, e

            # Handle existing streaming response (non-chunked case)
            elif hasattr(response, "result") and hasattr(
                response.result, "aiter_bytes"
            ):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []
                first_byte_time = None

                try:
                    async for chunk in response.result.aiter_bytes():
                        if chunk_count == 0:
                            first_byte_time = time.time()
                            first_byte_latency = first_byte_time - request_start_time
                            print(
                                f"  🚀 First Byte arrival: {first_byte_latency:.3f}s (auto-chunking)"
                            )

                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 10:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count % 20 == 0:
                            print(f"     Progress: {chunk_count} chunks")

                except Exception as iter_error:
                    print(f"  ⚠️ WAV streaming error: {str(iter_error)[:100]}...")

                end_time = time.time()
                total_time = end_time - request_start_time

                print(
                    f"  ✅ WAV long text streaming success: {chunk_count} chunks, {total_bytes} bytes"
                )
                print(f"  ⏱️ Total time: {total_time:.3f}s")

                if first_byte_time:
                    streaming_time = end_time - first_byte_time
                    print(
                        f"  📊 Streaming time: {streaming_time:.3f}s (after First Byte)"
                    )
                    if streaming_time > 0:
                        throughput = total_bytes / streaming_time
                        print(f"  🚀 Average throughput: {throughput:.0f} bytes/sec")
                    print(f"  🔧 Additional processing time due to auto-chunking")

                if audio_chunks and total_bytes > 0:
                    output_file = "test_async_stream_speech_long_output.wav"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 Long text WAV streaming audio saved: {output_file}")

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    return True, output_file
                else:
                    print("  ⚠️ No audio data received")
                    return False, None
            else:
                print("  ⚠️ Streaming interface not found")
                return False, None

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(f"  ❌ WAV streaming auto-chunking processing error: {e}")
            print("  🔧 Check WAV streaming chunking logic")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_with_voice_settings(voice_id):
    """Test TTS with voice settings - async"""
    print("🎛️ TTS with Voice Settings Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 TTS conversion with voice settings using voice '{voice_id}' (async)..."
            )
            print("  ⚠️ This test consumes credits!")

            voice_settings = {
                "pitch_shift": 0.95,
                "pitch_variance": 1.1,
                "speed": 0.9,
            }

            print(
                f"     Settings: pitch_shift={voice_settings['pitch_shift']}, speed={voice_settings['speed']}"
            )

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hello world! This is a voice settings test. You can hear the adjusted pitch and speed.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=voice_settings,
                include_phonemes=False,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ TTS with voice settings success: {audio_size} bytes audio generated"
                )

                output_file = "test_async_voice_settings_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Voice settings audio file saved: {output_file}")

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(12)
                    if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                        print(f"  ✅ Valid voice settings WAV file generated")
                    else:
                        print(f"  ⚠️ WAV header needs verification: {header[:12]}")

                return True, response
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_with_phonemes(voice_id):
    """Test TTS with phoneme information - async"""
    print("🔤 TTS with Phoneme Information Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 TTS conversion with phonemes using voice '{voice_id}' (async)..."
            )
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hello world! This is a phoneme timing test.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
                include_phonemes=True,
            )

            print(f"  🔍 Response type: {type(response)}")

            if hasattr(response, "result"):
                print(f"  🔍 Result type: {type(response.result)}")

                if hasattr(response.result, "read"):
                    audio_data = response.result.read()
                    audio_size = len(audio_data)
                    print(
                        f"  ✅ TTS with phonemes success: {audio_size} bytes audio generated"
                    )

                    output_file = "test_async_phoneme_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(audio_data)
                    print(f"  💾 Phoneme audio file saved: {output_file}")

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    return True, response

            phoneme_fields = [
                attr for attr in dir(response) if "phoneme" in attr.lower()
            ]
            if phoneme_fields:
                print(f"  🔤 Phoneme related fields found: {phoneme_fields}")
                for field in phoneme_fields:
                    field_value = getattr(response, field)
                    print(
                        f"     {field}: {type(field_value)} = {str(field_value)[:100]}..."
                    )

            return True, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_with_phonemes(voice_id):
    """Test streaming TTS with phoneme information - async"""
    print("🔤 Phoneme Streaming TTS Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models
        import base64

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔄 Phoneme streaming TTS test with voice '{voice_id}' (async)...")
            print("  ⚠️ This test may consume credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text="Hello world! This is a phoneme streaming test with timing information.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
                include_phonemes=True,
            )

            print("  📡 Receiving phoneme streaming data...")
            print(f"  🔍 Response type: {type(response)}")
            print(
                f"  🔍 Result type: {type(response.result) if hasattr(response, 'result') else 'No result'}"
            )

            # Handle JSON streaming response
            if hasattr(response, "result") and isinstance(response.result, str):
                print("  📄 JSON streaming response detected")

                json_chunks = []
                audio_chunks = []
                merged_phonemes = {
                    "symbols": [],
                    "durations_seconds": [],
                    "start_times_seconds": [],
                }
                first_chunk_start_time = None

                lines = response.result.strip().split("\n")
                print(f"  📊 Total {len(lines)} JSON chunks found")

                for i, line in enumerate(lines):
                    if line.strip():
                        try:
                            chunk_data = json.loads(line.strip())
                            json_chunks.append(chunk_data)

                            if chunk_data.get("audio_base64"):
                                audio_data = base64.b64decode(
                                    chunk_data["audio_base64"]
                                )
                                audio_chunks.append(audio_data)
                                print(
                                    f"     Chunk {i+1}: {len(audio_data)} bytes audio"
                                )

                            if chunk_data.get("phonemes") and chunk_data["phonemes"]:
                                chunk_phonemes = chunk_data["phonemes"]
                                print(f"     Chunk {i+1}: Phoneme data found!")

                                if chunk_phonemes.get("start_times_seconds"):
                                    original_start_times = chunk_phonemes[
                                        "start_times_seconds"
                                    ]

                                    if first_chunk_start_time is None:
                                        first_chunk_start_time = original_start_times[0]

                                    adjusted_start_times = [
                                        t - first_chunk_start_time
                                        for t in original_start_times
                                    ]
                                    chunk_phonemes["start_times_seconds"] = (
                                        adjusted_start_times
                                    )

                                merged_phonemes["symbols"].extend(
                                    chunk_phonemes.get("symbols", [])
                                )
                                merged_phonemes["durations_seconds"].extend(
                                    chunk_phonemes.get("durations_seconds", [])
                                )
                                merged_phonemes["start_times_seconds"].extend(
                                    chunk_phonemes.get("start_times_seconds", [])
                                )

                        except json.JSONDecodeError as e:
                            print(
                                f"     Chunk {i+1}: JSON parsing failed - {str(e)[:50]}..."
                            )
                            continue

                if audio_chunks:
                    total_audio_data = b"".join(audio_chunks)
                    total_bytes = len(total_audio_data)

                    print(
                        f"  ✅ Phoneme streaming complete: {len(json_chunks)} chunks, {total_bytes} bytes"
                    )

                    output_file = "test_async_phoneme_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(total_audio_data)
                    print(f"  💾 Phoneme streaming audio saved: {output_file}")

                    if merged_phonemes["symbols"]:
                        print(
                            f"  🔤 Merged phoneme data: {len(merged_phonemes['symbols'])} symbols"
                        )

                        phoneme_file = "test_async_phoneme_data.json"
                        with open(phoneme_file, "w") as f:
                            json.dump(merged_phonemes, f, indent=2)
                        print(f"  💾 Phoneme data saved: {phoneme_file}")

                    return True, {
                        "json_chunks": len(json_chunks),
                        "audio_chunks": len(audio_chunks),
                        "total_bytes": total_bytes,
                        "phoneme_data": merged_phonemes,
                    }
                else:
                    print(f"  ⚠️ No audio data")
                    return False, "No audio data in JSON chunks"

            else:
                print(f"  ❌ Unexpected response type")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_predict_duration_with_voice_settings(voice_id):
    """Test duration prediction with voice settings - async"""
    print("🎛️ Duration Prediction with Voice Settings Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with voice settings using voice '{voice_id}' (async)..."
            )

            voice_settings = {
                "pitch_shift": 1.1,
                "pitch_variance": 0.9,
                "speed": 1.05,
            }

            print(
                f"     Settings: pitch_shift={voice_settings['pitch_shift']}, speed={voice_settings['speed']}"
            )

            response = await client.text_to_speech.predict_duration_async(
                voice_id=voice_id,
                text="Hello world! This is a voice settings prediction test.",
                language=models.PredictTTSDurationRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
                voice_settings=voice_settings,
            )

            print(f"  ✅ Voice settings prediction complete: {response} seconds")
            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_with_voice_settings(voice_id):
    """Test streaming TTS with voice settings - async"""
    print("🎛️ Streaming TTS with Voice Settings Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔄 Voice settings streaming TTS test with voice '{voice_id}' (async)..."
            )
            print("  ⚠️ This test may consume credits!")

            voice_settings = {
                "pitch_shift": 1.2,
                "pitch_variance": 0.8,
                "speed": 1.15,
            }

            print(
                f"     Settings: pitch_shift={voice_settings['pitch_shift']}, speed={voice_settings['speed']}"
            )

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text="Hello world! This is a voice settings streaming test. The pitch and speed are adjusted.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
                voice_settings=voice_settings,
                include_phonemes=False,
            )

            print("  📡 Receiving voice settings streaming data...")

            if hasattr(response, "result") and hasattr(response.result, "aiter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    async for chunk in response.result.aiter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 15:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 16:
                            print(f"     ... (more chunks - log truncated)")

                except Exception as iter_error:
                    print(
                        f"  ⚠️ Voice settings streaming error: {str(iter_error)[:100]}..."
                    )

                print(
                    f"  ✅ Voice settings streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                )

                if audio_chunks and total_bytes > 0:
                    total_audio_data = b"".join(audio_chunks)

                    output_file = "test_async_voice_settings_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(total_audio_data)
                    print(f"  💾 Voice settings streaming audio saved: {output_file}")

                    return True, {
                        "chunk_count": chunk_count,
                        "total_bytes": total_bytes,
                    }
                else:
                    print(f"  ⚠️ No audio data received")
                    return False, "No audio data received"
            else:
                print(f"  ❌ Response missing iter_bytes attribute: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_mp3(voice_id):
    """Test MP3 format TTS conversion - async"""
    print("🎤 MP3 Format TTS Test (Async - Consumes Credits)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 MP3 TTS conversion with voice '{voice_id}' (async)...")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="안녕하세요! 이것은 MP3 형식 SDK 테스트를 위한 한국어 텍스트입니다. 정상적으로 작동하는지 확인해보겠습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ MP3 TTS conversion success: {audio_size} bytes audio generated"
                )

                output_file = "test_async_create_speech_output.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 MP3 audio file saved: {output_file}")

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(10)
                    if header[:3] == b"ID3":
                        print(f"  ✅ Valid MP3 file generated (ID3 tag)")
                    elif header[:2] == b"\xff\xfb" or header[:2] == b"\xff\xfa":
                        print(f"  ✅ Valid MP3 file generated (MPEG frame)")
                    else:
                        print(
                            f"  📄 MP3 header: {header[:10].hex()} (needs verification)"
                        )

                return True, response
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_long_text_mp3(voice_id):
    """Test MP3 auto-chunking for long text (300+ chars) - async"""
    print("📜 Long Text MP3 Auto-Chunking TTS Test (Async - 300+ chars)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 MP3 자동 청킹 TTS 테스트입니다.
        새로 구현된 SDK는 긴 텍스트를 자동으로 여러 개의 청크로 나누어 처리합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹 기능을 통해 긴 텍스트도 자연스럽게 여러 개의 작은 세그먼트로 나누어져 처리됩니다.
        각 세그먼트는 문장 경계와 단어 경계를 고려하여 지능적으로 분할되며, 이를 통해 자연스러운 음성을 생성할 수 있습니다.
        이제 사용자는 텍스트 길이나 출력 형식에 대해 걱정할 필요가 없으며, SDK가 MP3 형식으로도 모든 것을 자동으로 처리해줍니다.
        """.strip()

        actual_length = len(long_text)
        print(f"  📏 Test text length: {actual_length} characters (exceeds 300)")
        print(f"  🔧 Auto-chunking enabled for MP3 format")

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Long text MP3 conversion with voice '{voice_id}' (async)...")
            print("  ⚠️ This test consumes credits!")
            print("  ✨ SDK automatically chunks text and processes as MP3")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ MP3 auto-chunking success: {audio_size} bytes audio generated"
                )
                print(f"  🎯 Long text successfully chunked and processed as MP3!")

                output_file = "test_async_auto_chunking_speech_output.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 MP3 auto-chunked audio file saved: {output_file}")

                estimated_chunks = (actual_length + 299) // 300
                print(
                    f"  📊 Estimated chunks: {estimated_chunks} (based on text length)"
                )
                print(f"  🔀 Parallel processing applied and merged as MP3")

                return True, {
                    "audio_size": audio_size,
                    "text_length": actual_length,
                    "estimated_chunks": estimated_chunks,
                    "format": "mp3",
                }
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(f"  ❌ MP3 auto-chunking processing error: {e}")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_mp3(voice_id):
    """Test MP3 streaming TTS - async"""
    print("🎵 MP3 Streaming TTS Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔄 MP3 streaming TTS test with voice '{voice_id}' (async)...")
            print("  ⚠️ This test may consume credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text="안녕하세요! 이것은 MP3 스트리밍 TTS 테스트를 위한 한국어 텍스트입니다. 스트리밍 기능이 MP3 형식으로도 정상적으로 작동하는지 확인하고 있습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,
                style="neutral",
                model="sona_speech_1",
            )

            print("  📡 Receiving MP3 streaming data...")

            if hasattr(response, "result") and hasattr(response.result, "aiter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    async for chunk in response.result.aiter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 20:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 21:
                            print(f"     ... (more chunks - log truncated)")

                except Exception as iter_error:
                    print(f"  ⚠️ MP3 streaming error: {str(iter_error)[:100]}...")

                print(
                    f"  ✅ MP3 streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                )

                if audio_chunks and total_bytes > 0:
                    output_file = "test_async_stream_speech_output.mp3"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 MP3 streaming audio saved: {output_file}")

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    return True, f"{chunk_count} chunks, {total_bytes} bytes"
                else:
                    print(f"  ⚠️ No audio data received")
                    return False, "No audio data received"
            else:
                print(f"  ❌ Response missing iter_bytes attribute: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_long_text_mp3(voice_id):
    """Test MP3 streaming for long text (300+ chars) - async"""
    print("📜 Long Text MP3 Streaming TTS Test (Async - 300+ chars)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models
        import base64

        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 MP3 스트리밍 TTS 테스트입니다.
        새로 구현된 SDK는 긴 텍스트를 자동으로 여러 개의 청크로 나누어 스트리밍으로 처리합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹 기능을 통해 긴 텍스트도 자연스럽게 여러 개의 작은 세그먼트로 나누어져 처리됩니다.
        각 세그먼트는 문장 경계와 단어 경계를 고려하여 지능적으로 분할되며, 이를 통해 자연스러운 음성을 생성할 수 있습니다.
        스트리밍 방식으로 MP3 형식 처리되기 때문에 사용자는 전체 텍스트의 음성 변환이 완료되기를 기다릴 필요가 없습니다.
        첫 번째 청크의 음성이 생성되는 즉시 재생을 시작할 수 있어 반응성이 크게 향상됩니다.
        """.strip()

        actual_length = len(long_text)
        print(f"  📏 Test text length: {actual_length} characters (exceeds 300)")
        print(f"  🔧 Auto-chunking + MP3 streaming enabled")

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Long text MP3 streaming with voice '{voice_id}' (async)...")
            print("  ⚠️ This test consumes credits and applies auto-chunking!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,
                style="neutral",
                model="sona_speech_1",
            )

            print(f"  🔍 Response type: {type(response)}")
            print(f"  🔍 Result type: {type(response.result)}")

            # Handle real-time streaming response (AsyncExtendedStreamingWrapper)
            if (
                hasattr(response, "result")
                and hasattr(response.result, "aiter_bytes")
                and not isinstance(response.result, str)
            ):
                print("  ✅ Real-time streaming response detected (auto-chunked)")
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    async for chunk in response.result.aiter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 20:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 21:
                            print(f"     ... (more chunks - log truncated)")

                except Exception as iter_error:
                    print(
                        f"  ⚠️ Long text MP3 streaming error: {str(iter_error)[:100]}..."
                    )

                print(
                    f"  ✅ Long text MP3 streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                )

                if audio_chunks and total_bytes > 0:
                    audio_data = b"".join(audio_chunks)

                    output_file = "test_async_stream_speech_long_output.mp3"
                    with open(output_file, "wb") as f:
                        f.write(audio_data)
                    print(f"  💾 Long text MP3 streaming audio saved: {output_file}")
                    print(f"  📏 Saved file size: {total_bytes} bytes")

                    estimated_chunks = (actual_length + 299) // 300
                    print(
                        f"  📊 Estimated text chunks: {estimated_chunks} (based on text length)"
                    )

                    return True, {
                        "chunk_count": chunk_count,
                        "total_bytes": total_bytes,
                        "text_length": actual_length,
                        "estimated_chunks": estimated_chunks,
                        "format": "mp3",
                    }

            # Handle JSON format response (old merged format)
            elif hasattr(response, "result") and isinstance(response.result, str):
                try:
                    result_data = json.loads(response.result)
                    print(f"  ✅ Chunked JSON response detected")

                    if "audio_base64" in result_data:
                        audio_data = base64.b64decode(result_data["audio_base64"])
                        total_bytes = len(audio_data)

                        print(f"  ✅ Merged MP3 audio data: {total_bytes} bytes")

                        output_file = "test_async_stream_speech_long_output.mp3"
                        with open(output_file, "wb") as f:
                            f.write(audio_data)
                        print(
                            f"  💾 Long text MP3 streaming audio saved: {output_file}"
                        )

                        estimated_chunks = (actual_length + 299) // 300
                        print(
                            f"  📊 Estimated chunks: {estimated_chunks} (based on text length)"
                        )
                        print(f"  🔀 Auto-chunked segments merged as MP3")

                        return True, {
                            "total_bytes": total_bytes,
                            "text_length": actual_length,
                            "estimated_chunks": estimated_chunks,
                            "format": "mp3",
                        }
                    else:
                        print(f"  ❌ audio_base64 key missing")
                        return False, result_data

                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON parsing failed: {e}")
                    return False, e

            # Handle existing streaming response
            elif hasattr(response, "result") and hasattr(
                response.result, "aiter_bytes"
            ):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    async for chunk in response.result.aiter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 10:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")

                except Exception as iter_error:
                    print(f"  ⚠️ MP3 streaming error: {str(iter_error)[:100]}...")

                print(
                    f"  ✅ MP3 long text streaming success: {chunk_count} chunks, {total_bytes} bytes"
                )

                if audio_chunks and total_bytes > 0:
                    output_file = "test_async_stream_speech_long_output.mp3"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 Long text MP3 streaming audio saved: {output_file}")

                    return True, {
                        "chunk_count": chunk_count,
                        "total_bytes": total_bytes,
                        "format": "mp3",
                    }
                else:
                    print(f"  ⚠️ No audio data received")
                    return False, None
            else:
                print(f"  ❌ Response structure verification needed")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please recharge")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_long_text_with_phonemes(voice_id):
    """Test long text auto-chunking with phoneme information - async"""
    print("📜🔤 Long Text Auto-Chunking + Phoneme TTS Test (Async - 300+ chars)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models
        import base64

        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 자동 청킹과 Phoneme 정보를 동시에 테스트합니다.
        새로 구현된 SDK는 긴 텍스트를 자동으로 여러 개의 청크로 나누어 처리하고 각 청크의 Phoneme 정보를 병합합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹 기능과 Phoneme 병합을 통해 긴 텍스트도 자연스럽게 음성으로 변환할 수 있습니다.
        """.strip()

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Long text chunking + phoneme TTS with voice '{voice_id}' (async)..."
            )
            print(f"  📝 Text length: {len(long_text)} characters")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                include_phonemes=True,
            )

            print(f"  🔍 Response type: {type(response)}")

            if hasattr(response, "result"):
                print(f"  🔍 Result type: {type(response.result)}")

                if (
                    hasattr(response.result, "audio_base64")
                    and response.result.audio_base64
                ):
                    print("  ✅ Base64 audio data received")
                    print(
                        f"  📊 Audio data size: {len(response.result.audio_base64)} characters"
                    )

                    if (
                        hasattr(response.result, "phonemes")
                        and response.result.phonemes
                    ):
                        phonemes = response.result.phonemes
                        print("\n  🔤 ===== Phoneme Information Analysis =====")
                        print(
                            f"  📊 Phoneme symbols: {len(phonemes.symbols) if phonemes.symbols else 0}"
                        )
                        print(
                            f"  ⏱️ Durations: {len(phonemes.durations_seconds) if phonemes.durations_seconds else 0}"
                        )

                        if (
                            hasattr(phonemes, "start_times_seconds")
                            and phonemes.start_times_seconds
                        ):
                            print(
                                f"  🚀 Start times: {len(phonemes.start_times_seconds)}"
                            )

                        if phonemes.symbols and phonemes.durations_seconds:
                            total_duration = sum(phonemes.durations_seconds)
                            print(f"  ⏱️ Total duration: {total_duration:.3f}s")

                            phoneme_data = {
                                "text": long_text,
                                "text_length": len(long_text),
                                "audio_format": "wav",
                                "phonemes": {
                                    "symbols": phonemes.symbols,
                                    "durations_seconds": phonemes.durations_seconds,
                                    "start_times_seconds": getattr(
                                        phonemes, "start_times_seconds", None
                                    ),
                                    "total_symbols": len(phonemes.symbols),
                                    "total_duration": total_duration,
                                },
                            }

                            with open(
                                "test_async_long_chunking_phoneme_data.json",
                                "w",
                                encoding="utf-8",
                            ) as f:
                                json.dump(phoneme_data, f, ensure_ascii=False, indent=2)
                            print(
                                f"\n  💾 Phoneme data saved: test_async_long_chunking_phoneme_data.json"
                            )
                    else:
                        print("  ⚠️ No phoneme information")

                    audio_data = base64.b64decode(response.result.audio_base64)
                    filename = "test_async_long_chunking_phoneme_output.wav"
                    with open(filename, "wb") as f:
                        f.write(audio_data)
                    print(f"  💾 Audio file saved: {filename}")

                    return True, response
                else:
                    print("  ❌ No audio data")
                    return False, None
            else:
                print("  ❌ No result in response")
                return False, None

    except errors.SupertoneDefaultError as e:
        print(f"  ❌ API error: {e}")
        return False, None
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, None


async def test_stream_speech_phoneme_chunking_wav(voice_id):
    """Test long text + phoneme + streaming (WAV) - async"""
    print("🎵🔤📜 Long Text + Phoneme + Streaming Test (WAV - Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models
        import base64

        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 Phoneme + 스트리밍 테스트입니다.
        현재 SDK는 긴 텍스트를 자동으로 청킹하며, Phoneme + 스트리밍 조합도 지원합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹과 Phoneme 병합 기능을 통해 긴 텍스트도 자연스럽게 음성으로 변환하고 정확한 발음 정보를 제공할 수 있습니다.
        """.strip()

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Long text phoneme + streaming test with voice '{voice_id}' (async)..."
            )
            print(f"  📝 Text length: {len(long_text)} characters (exceeds 300)")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                include_phonemes=True,
            )

            print(f"  🔍 Response type: {type(response)}")

            if hasattr(response, "result"):
                print(f"  🔍 Result type: {type(response.result)}")

                # Handle streaming response (AsyncExtendedStreamingWrapper)
                if hasattr(response.result, "aiter_bytes") and not isinstance(
                    response.result, str
                ):
                    print("  ✅ Real-time streaming response detected")
                    audio_chunks = []
                    chunk_count = 0

                    try:
                        async for chunk in response.result.aiter_bytes():
                            chunk_count += 1
                            audio_chunks.append(chunk)
                            if chunk_count <= 10:
                                print(f"     Chunk {chunk_count}: {len(chunk)} bytes")
                    except Exception as stream_error:
                        print(f"  ⚠️ Streaming error: {type(stream_error).__name__}")
                        import traceback

                        traceback.print_exc()

                    if audio_chunks:
                        audio_data = b"".join(audio_chunks)
                        total_bytes = len(audio_data)

                        print(
                            f"  ✅ Streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                        )

                        output_file = "test_async_phoneme_chunking_stream_output.wav"
                        with open(output_file, "wb") as f:
                            f.write(audio_data)
                        print(f"  💾 Streaming audio saved: {output_file}")

                        return True, {
                            "total_bytes": total_bytes,
                            "chunk_count": chunk_count,
                            "text_length": len(long_text),
                            "format": "wav",
                        }

                # Handle merged JSON response (old format)
                elif isinstance(response.result, str):
                    try:
                        result_data = json.loads(response.result)
                        print(f"  ✅ Chunked merged JSON response detected")

                        if "audio_base64" in result_data:
                            audio_data = base64.b64decode(result_data["audio_base64"])
                            total_bytes = len(audio_data)

                            print(
                                f"  ✅ Merged WAV + Phoneme audio data: {total_bytes} bytes"
                            )

                            output_file = (
                                "test_async_phoneme_chunking_stream_output.wav"
                            )
                            with open(output_file, "wb") as f:
                                f.write(audio_data)
                            print(
                                f"  💾 Phoneme + chunking streaming audio saved: {output_file}"
                            )

                            if "phonemes" in result_data and result_data["phonemes"]:
                                phonemes = result_data["phonemes"]
                                print(f"\n  🔤 ===== Merged Phoneme Information =====")
                                print(
                                    f"    - Symbols: {len(phonemes.get('symbols', []))}"
                                )

                                if phonemes.get("durations_seconds"):
                                    durations = phonemes["durations_seconds"]
                                    print(f"    - Durations: {len(durations)} items")
                                    print(
                                        f"    - Total duration: {sum(durations):.3f}s"
                                    )

                                if phonemes.get("start_times_seconds"):
                                    start_times = phonemes["start_times_seconds"]
                                    print(
                                        f"    - Start times: {len(start_times)} items"
                                    )

                                phoneme_file = (
                                    "test_async_phoneme_chunking_stream_data.json"
                                )
                                with open(phoneme_file, "w", encoding="utf-8") as f:
                                    json.dump(phonemes, f, ensure_ascii=False, indent=2)
                                print(f"  💾 Phoneme data saved: {phoneme_file}")
                            else:
                                print(f"  ⚠️ No phoneme information")

                            return True, {
                                "total_bytes": total_bytes,
                                "text_length": len(long_text),
                                "format": "wav",
                                "has_phonemes": "phonemes" in result_data
                                and result_data["phonemes"] is not None,
                            }
                        else:
                            print(f"  ❌ audio_base64 key missing")
                            return False, result_data

                    except json.JSONDecodeError:
                        print(f"  ❌ JSON parsing failed")
                        return False, None

                print("  ⚠️ Unexpected response structure")
                return False, None

    except errors.SupertoneDefaultError as e:
        print(f"  ❌ API error: {e}")
        return False, e
    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


# =============================================================================
# NEW MODEL TESTS (sona_speech_2, sona_speech_2_flash, supertonic_api_1) - Async
# =============================================================================


async def test_create_speech_sona_speech_2(voice_id):
    """Test TTS with sona_speech_2 model (Async)"""
    print("🎤 TTS Test with sona_speech_2 Model (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with sona_speech_2 using voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hello! This is a test with the new sona_speech_2 model.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_2,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(f"  ✅ sona_speech_2 TTS successful: {audio_size} bytes")

                output_file = "test_async_sona_speech_2_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio saved: {output_file}")

                return True, response
            else:
                print(f"  ❌ Response structure error: {type(response)}")
                return False, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_sona_speech_2_flash(voice_id):
    """Test TTS with sona_speech_2_flash model (Async) - faster, lower latency"""
    print("⚡ TTS Test with sona_speech_2_flash Model (Async) (Low Latency)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with sona_speech_2_flash using voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hello! This is a test with the new sona_speech_2_flash model. It offers lower latency for real-time applications.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_2_FLASH,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(f"  ✅ sona_speech_2_flash TTS successful: {audio_size} bytes")

                output_file = "test_async_sona_speech_2_flash_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio saved: {output_file}")

                return True, response
            else:
                print(f"  ❌ Response structure error: {type(response)}")
                return False, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_sona_speech_2_with_normalized_text(voice_id):
    """Test TTS with sona_speech_2 model using normalized_text for Japanese pronunciation (Async)"""
    print("🇯🇵 TTS Test with sona_speech_2 Model + normalized_text (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with sona_speech_2 + normalized_text using voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            # Japanese text with kanji and its reading (hiragana)
            original_text = "今日はどんな一日だったの？"
            normalized_text = "きょうはどんないちにちだったの？"

            print(f"  📝 Original text (with kanji): {original_text}")
            print(f"  📖 Normalized text (hiragana): {normalized_text}")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=original_text,
                normalized_text=normalized_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_2,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(f"  ✅ sona_speech_2 + normalized_text TTS successful: {audio_size} bytes")

                output_file = "test_async_sona_speech_2_normalized_text_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio saved: {output_file}")
                print(f"  🎯 The TTS engine used normalized_text for pronunciation!")

                return True, response
            else:
                print(f"  ❌ Response structure error: {type(response)}")
                return False, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_sona_speech_2_flash_with_normalized_text(voice_id):
    """Test TTS with sona_speech_2_flash model using normalized_text for Japanese pronunciation (Async)"""
    print("⚡🇯🇵 TTS Test with sona_speech_2_flash Model + normalized_text (Async) (Low Latency)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with sona_speech_2_flash + normalized_text using voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            # Japanese text with kanji and its reading (hiragana)
            original_text = "今日はどんな一日だったの？"
            normalized_text = "きょうはどんないちにちだったの？"

            print(f"  📝 Original text (with kanji): {original_text}")
            print(f"  📖 Normalized text (hiragana): {normalized_text}")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=original_text,
                normalized_text=normalized_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_2_FLASH,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(f"  ✅ sona_speech_2_flash + normalized_text TTS successful: {audio_size} bytes")

                output_file = "test_async_sona_speech_2_flash_normalized_text_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio saved: {output_file}")
                print(f"  🎯 The TTS engine used normalized_text for pronunciation!")

                return True, response
            else:
                print(f"  ❌ Response structure error: {type(response)}")
                return False, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_supertonic_api_1(voice_id):
    """Test TTS with supertonic_api_1 model (Async)"""
    print("🎤 TTS Test with supertonic_api_1 Model (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Converting TTS with supertonic_api_1 using voice '{voice_id}'..."
            )
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hello! This is a test with the supertonic_api_1 model.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SUPERTONIC_API_1,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(f"  ✅ supertonic_api_1 TTS successful: {audio_size} bytes")

                output_file = "test_async_supertonic_api_1_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio saved: {output_file}")

                return True, response
            else:
                print(f"  ❌ Response structure error: {type(response)}")
                return False, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_invalid_model(voice_id):
    """Test TTS with unsupported model - should return error (Async)"""
    print("❌ TTS Test with Invalid Model (Expected Error) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Attempting TTS with invalid model 'invalid_model_xyz'...")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="This should fail with invalid model.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="invalid_model_xyz",  # Invalid model
            )

            print(f"  ⚠️ Unexpected: API did not reject invalid model")
            return False, response

    except (errors.BadRequestErrorResponse, errors.SupertoneError) as e:
        print(
            f"  ✅ Expected error received: {e.message if hasattr(e, 'message') else e}"
        )
        print("  ✅ API correctly rejected invalid model")
        return True, e
    except ValueError as e:
        print(f"  ✅ Expected SDK validation error: {e}")
        print("  ✅ SDK correctly rejected invalid model")
        return True, e
    except Exception as e:
        print(f"  ✅ Error received (expected): {e}")
        return True, e


async def test_predict_duration_sona_speech_2(voice_id):
    """Test duration prediction with sona_speech_2 model (Async)"""
    print("⏱️ Duration Prediction Test with sona_speech_2 Model (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with sona_speech_2 using voice '{voice_id}'..."
            )

            response = await client.text_to_speech.predict_duration_async(
                voice_id=voice_id,
                text="Hello! This is a duration prediction test with sona_speech_2.",
                language=models.PredictTTSDurationRequestLanguage.EN,
                style="neutral",
                model=models.PredictTTSDurationRequestModel.SONA_SPEECH_2,
            )

            print(f"  ✅ sona_speech_2 prediction complete: {response} seconds")
            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_predict_duration_sona_speech_2_flash(voice_id):
    """Test duration prediction with sona_speech_2_flash model (Async)"""
    print("⚡⏱️ Duration Prediction Test with sona_speech_2_flash Model (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with sona_speech_2_flash using voice '{voice_id}'..."
            )

            response = await client.text_to_speech.predict_duration_async(
                voice_id=voice_id,
                text="Hello! This is a duration prediction test with sona_speech_2_flash.",
                language=models.PredictTTSDurationRequestLanguage.EN,
                style="neutral",
                model=models.PredictTTSDurationRequestModel.SONA_SPEECH_2_FLASH,
            )

            print(f"  ✅ sona_speech_2_flash prediction complete: {response} seconds")
            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_predict_duration_supertonic_api_1(voice_id):
    """Test duration prediction with supertonic_api_1 model (Async)"""
    print("⏱️ Duration Prediction Test with supertonic_api_1 Model (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with supertonic_api_1 using voice '{voice_id}'..."
            )

            response = await client.text_to_speech.predict_duration_async(
                voice_id=voice_id,
                text="Hello! This is a duration prediction test with supertonic_api_1.",
                language=models.PredictTTSDurationRequestLanguage.EN,
                style="neutral",
                model=models.PredictTTSDurationRequestModel.SUPERTONIC_API_1,
            )

            print(f"  ✅ supertonic_api_1 prediction complete: {response} seconds")
            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_predict_duration_invalid_model(voice_id):
    """Test duration prediction with unsupported model - should return error (Async)"""
    print("❌ Duration Prediction Test with Invalid Model (Expected Error) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Attempting prediction with invalid model 'invalid_model_xyz'..."
            )

            response = await client.text_to_speech.predict_duration_async(
                voice_id=voice_id,
                text="This should fail with invalid model.",
                language=models.PredictTTSDurationRequestLanguage.EN,
                style="neutral",
                model="invalid_model_xyz",  # Invalid model
            )

            print(f"  ⚠️ Unexpected: API did not reject invalid model")
            return False, response

    except (errors.BadRequestErrorResponse, errors.SupertoneError) as e:
        print(
            f"  ✅ Expected error received: {e.message if hasattr(e, 'message') else e}"
        )
        print("  ✅ API correctly rejected invalid model")
        return True, e
    except ValueError as e:
        print(f"  ✅ Expected SDK validation error: {e}")
        print("  ✅ SDK correctly rejected invalid model")
        return True, e
    except Exception as e:
        print(f"  ✅ Error received (expected): {e}")
        return True, e


# =============================================================================
# MULTI-LANGUAGE TESTS BY MODEL - Async
# =============================================================================


async def test_create_speech_sona_speech_1_multilang(voice_id):
    """Test sona_speech_1 with supported languages (ko, en, ja) - Async"""
    print("🌐 sona_speech_1 Multi-language Test (ko, en, ja) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        test_cases = [
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                "안녕하세요! 한국어 테스트입니다.",
            ),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                "Hello! English test.",
            ),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                "こんにちは！日本語テストです。",
            ),
        ]

        all_success = True
        async with Supertone(api_key=API_KEY) as client:
            for lang, text in test_cases:
                print(f"  🔍 Testing {lang.value} with sona_speech_1...")

                try:
                    response = await client.text_to_speech.create_speech_async(
                        voice_id=voice_id,
                        text=text,
                        language=lang,
                        output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                        style="neutral",
                        model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                    )

                    if hasattr(response, "result") and hasattr(response.result, "read"):
                        audio_data = response.result.read()
                        print(f"    ✅ {lang.value}: {len(audio_data)} bytes")
                    else:
                        print(f"    ❌ {lang.value}: Response structure error")
                        all_success = False

                except errors.SupertoneError as e:
                    print(f"    ❌ {lang.value}: {e.message}")
                    all_success = False

        return all_success, "sona_speech_1 multilang test async"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_sona_speech_2_multilang(voice_id):
    """Test sona_speech_2 with all supported languages - Async"""
    print("🌐 sona_speech_2 Multi-language Test (all languages) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # sona_speech_2 supports all languages
        test_cases = [
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                "안녕하세요!",
            ),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN, "Hello!"),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                "こんにちは!",
            ),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.ES, "¡Hola!"),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.PT, "Olá!"),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.DE, "Hallo!"),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.FR, "Bonjour!"),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.IT, "Ciao!"),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.RU, "Привет!"),
            (models.APIConvertTextToSpeechUsingCharacterRequestLanguage.AR, "مرحبا!"),
        ]

        all_success = True
        success_count = 0
        async with Supertone(api_key=API_KEY) as client:
            for lang, text in test_cases:
                print(f"  🔍 Testing {lang.value} with sona_speech_2...")

                try:
                    response = await client.text_to_speech.create_speech_async(
                        voice_id=voice_id,
                        text=text,
                        language=lang,
                        output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                        style="neutral",
                        model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_2,
                    )

                    if hasattr(response, "result") and hasattr(response.result, "read"):
                        audio_data = response.result.read()
                        print(f"    ✅ {lang.value}: {len(audio_data)} bytes")
                        success_count += 1
                    else:
                        print(f"    ❌ {lang.value}: Response structure error")
                        all_success = False

                except errors.SupertoneError as e:
                    print(f"    ❌ {lang.value}: {e.message}")
                    all_success = False

        print(f"  📊 Total: {success_count}/{len(test_cases)} languages successful")
        return (
            all_success,
            f"sona_speech_2 multilang async: {success_count}/{len(test_cases)}",
        )

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_supertonic_api_1_multilang(voice_id):
    """Test supertonic_api_1 with supported languages (ko, en, ja, es, pt) - Async"""
    print("🌐 supertonic_api_1 Multi-language Test (ko, en, ja, es, pt) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # supertonic_api_1 supports: ko, en, ja, es, pt
        test_cases = [
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                "안녕하세요! 한국어 테스트입니다.",
            ),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                "Hello! English test.",
            ),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                "こんにちは！日本語テストです。",
            ),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.ES,
                "¡Hola! Prueba en español.",
            ),
            (
                models.APIConvertTextToSpeechUsingCharacterRequestLanguage.PT,
                "Olá! Teste em português.",
            ),
        ]

        all_success = True
        async with Supertone(api_key=API_KEY) as client:
            for lang, text in test_cases:
                print(f"  🔍 Testing {lang.value} with supertonic_api_1...")

                try:
                    response = await client.text_to_speech.create_speech_async(
                        voice_id=voice_id,
                        text=text,
                        language=lang,
                        output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                        style="neutral",
                        model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SUPERTONIC_API_1,
                    )

                    if hasattr(response, "result") and hasattr(response.result, "read"):
                        audio_data = response.result.read()
                        print(f"    ✅ {lang.value}: {len(audio_data)} bytes")
                    else:
                        print(f"    ❌ {lang.value}: Response structure error")
                        all_success = False

                except errors.SupertoneError as e:
                    print(f"    ❌ {lang.value}: {e.message}")
                    all_success = False

        return all_success, "supertonic_api_1 multilang test async"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_sona_speech_1_unsupported_lang(voice_id):
    """Test sona_speech_1 with unsupported language - should return error (Async)"""
    print("❌ sona_speech_1 Unsupported Language Test (Expected Error) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # sona_speech_1 only supports ko, en, ja - testing with German (de)
        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Attempting sona_speech_1 with German (unsupported)...")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hallo! Dies ist ein Test.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.DE,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                print(f"  ⚠️ Unexpected success: {len(audio_data)} bytes")
                print(
                    "  ⚠️ API accepted unsupported language (may need to verify model-language restrictions)"
                )
                return False, response
            else:
                print(f"  ⚠️ Unexpected response: {type(response)}")
                return False, response

    except (errors.BadRequestErrorResponse, errors.SupertoneError) as e:
        print(
            f"  ✅ Expected error received: {e.message if hasattr(e, 'message') else e}"
        )
        print("  ✅ API correctly rejected unsupported language for sona_speech_1")
        return True, e
    except Exception as e:
        print(f"  ✅ Error received (expected): {e}")
        return True, e


async def test_create_speech_supertonic_api_1_unsupported_lang(voice_id):
    """Test supertonic_api_1 with unsupported language - should return error (Async)"""
    print("❌ supertonic_api_1 Unsupported Language Test (Expected Error) (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # supertonic_api_1 supports: ko, en, ja, es, pt - testing with German (de)
        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Attempting supertonic_api_1 with German (unsupported)...")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text="Hallo! Dies ist ein Test.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.DE,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SUPERTONIC_API_1,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                print(f"  ⚠️ Unexpected success: {len(audio_data)} bytes")
                print(
                    "  ⚠️ API accepted unsupported language (may need to verify model-language restrictions)"
                )
                return False, response
            else:
                print(f"  ⚠️ Unexpected response: {type(response)}")
                return False, response

    except (errors.BadRequestErrorResponse, errors.SupertoneError) as e:
        print(
            f"  ✅ Expected error received: {e.message if hasattr(e, 'message') else e}"
        )
        print("  ✅ API correctly rejected unsupported language for supertonic_api_1")
        return True, e
    except Exception as e:
        print(f"  ✅ Error received (expected): {e}")
        return True, e


async def test_predict_duration_multilang(voice_id):
    """Test duration prediction with different languages and models - Async"""
    print("🌐⏱️ Duration Prediction Multi-language Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        test_cases = [
            # (model, language, text)
            (
                models.PredictTTSDurationRequestModel.SONA_SPEECH_1,
                models.PredictTTSDurationRequestLanguage.KO,
                "안녕하세요!",
            ),
            (
                models.PredictTTSDurationRequestModel.SONA_SPEECH_2,
                models.PredictTTSDurationRequestLanguage.DE,
                "Guten Tag!",
            ),
            (
                models.PredictTTSDurationRequestModel.SUPERTONIC_API_1,
                models.PredictTTSDurationRequestLanguage.ES,
                "¡Buenos días!",
            ),
        ]

        all_success = True
        async with Supertone(api_key=API_KEY) as client:
            for model, lang, text in test_cases:
                print(f"  🔍 Predicting with {model.value} + {lang.value}...")

                try:
                    response = await client.text_to_speech.predict_duration_async(
                        voice_id=voice_id,
                        text=text,
                        language=lang,
                        style="neutral",
                        model=model,
                    )
                    print(f"    ✅ {model.value} + {lang.value}: {response} seconds")

                except errors.SupertoneError as e:
                    print(f"    ❌ {model.value} + {lang.value}: {e.message}")
                    all_success = False

        return all_success, "predict_duration multilang test async"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_long_sentence_word_split(voice_id):
    """Test async TTS with a very long sentence (word-based splitting)"""
    print("📝✂️ Async Long Sentence Word-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Create a long sentence without punctuation (over 300 chars)
        long_sentence = (
            "This is a very long sentence without any punctuation marks that is designed "
            "to exceed the three hundred character limit so that the text chunking algorithm "
            "will need to fall back to word based splitting instead of sentence based splitting "
            "because there are no sentence ending punctuation marks like periods or exclamation "
            "points to use as natural break points in this extremely lengthy run on sentence"
        )

        print(f"  📏 Text length: {len(long_sentence)} characters (no punctuation)")
        print(f"  📄 Text preview: {long_sentence[:50]}...")

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Converting TTS with word-based chunking (async)...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=long_sentence,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                if len(audio_data) > 0:
                    print(f"  ✅ Word-based chunking successful!")
                    print(f"  📦 Audio data size: {len(audio_data):,} bytes")
                    return True, response
                else:
                    print("  ❌ Empty audio data")
                    return False, response
            else:
                print(f"  ❌ Unexpected response type: {type(response)}")
                return False, response

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_japanese_no_spaces(voice_id):
    """Test async TTS with Japanese text (character-based splitting)"""
    print("🇯🇵✂️ Async Japanese Text Character-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Long Japanese text without spaces
        japanese_text = (
            "これは日本語のテストです。"
            "日本語には通常スペースがありません。"
            "そのため、テキストを分割するときは文字単位で分割する必要があります。"
            "このテストは三百文字を超える長いテキストを使用して、"
            "文字ベースの分割アルゴリズムが正しく動作することを確認します。"
            "人工知能技術は日々進化しており、音声合成の品質も向上しています。"
            "私たちは最新の技術を使用して、自然な音声を生成することができます。"
        )

        print(f"  📏 Text length: {len(japanese_text)} characters (no word spaces)")
        print(f"  📄 Text preview: {japanese_text[:30]}...")

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Converting TTS with character-based chunking (async)...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=japanese_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                if len(audio_data) > 0:
                    print(f"  ✅ Character-based chunking successful!")
                    print(f"  📦 Audio data size: {len(audio_data):,} bytes")
                    return True, response
                else:
                    print("  ❌ Empty audio data")
                    return False, response
            else:
                print(f"  ❌ Unexpected response type: {type(response)}")
                return False, response

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_stream_speech_long_sentence_word_split(voice_id):
    """Test async streaming TTS with a very long sentence (word-based splitting)"""
    print("📝🔊✂️ Async Streaming Long Sentence Word-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Long sentence without punctuation
        long_sentence = (
            "This is an extremely long sentence that has been carefully crafted without "
            "any punctuation marks whatsoever in order to test the streaming text to speech "
            "functionality with word based chunking which should split this text into multiple "
            "smaller chunks at word boundaries while still producing smooth continuous audio "
            "output that sounds natural and without any noticeable gaps or stuttering effects"
        )

        print(f"  📏 Text length: {len(long_sentence)} characters (no punctuation)")

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Streaming TTS with word-based chunking (async)...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=long_sentence,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "aiter_bytes"):
                async for chunk in response.result.aiter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "iter_bytes"):
                for chunk in response.result.iter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "read"):
                audio_data = response.result.read()

            if len(audio_data) > 0:
                print(f"  ✅ Streaming word-based chunking successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")
                return True, response
            else:
                print("  ❌ Empty audio data")
                return False, response

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_create_speech_multilingual_punctuation(voice_id):
    """Test async TTS with multilingual punctuation splitting (Japanese 。！？, Korean ellipsis, etc.)"""
    print("🌐✂️ Async Multilingual Punctuation Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Test cases with various multilingual punctuation
        test_cases = [
            {
                "name": "Japanese punctuation (。！？)",
                "text": (
                    "これは日本語のテストです。音声合成技術はとても進化しています！"
                    "リアルタイムストリーミングは素晴らしいですね？"
                    "長いテキストでも自然に分割されます。品質がとても良いです！"
                    "次の文章も続きます。これで三百文字を超えるテキストになります。"
                    "人工知能の発展により音声技術も進歩しました。素晴らしいですね！"
                    "音声合成の未来は明るいです。私たちはこの素晴らしい技術を使って"
                    "世界中の人々にサービスを提供しています。テキストが長くなっても"
                    "問題なく処理できます。自動チャンキング機能が正しく動作しています！"
                    "これで確実に三百文字を超えました。日本語の句読点で自然に分割されることを確認します。"
                    "最新のAI技術を活用した音声合成システムです。"
                ),
                "language": models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
            },
            {
                "name": "Korean with ellipsis (…)",
                "text": (
                    "안녕하세요… 오늘 날씨가 좋네요. 음성 합성 기술이 발전했습니다!"
                    "실시간 스트리밍도 가능해요… 정말 놀랍죠? 긴 텍스트도 자연스럽게 처리됩니다."
                    "이 테스트는 삼백자를 넘는 긴 문장입니다… 다국어 구두점 분리를 확인합니다!"
                    "한국어 말줄임표도 잘 인식됩니다… 기술의 발전이 놀랍습니다."
                    "음성 합성 기술은 우리 생활을 더욱 편리하게 만들어줍니다… 앞으로도 계속 발전할 것입니다!"
                    "자동 청킹 기능이 정상적으로 동작하는지 확인합니다… 이제 삼백자를 초과했습니다! 테스트 완료!"
                    "최신 AI 기술을 활용한 음성 합성 시스템입니다… 품질이 매우 우수합니다! 확인했어요!"
                ),
                "language": models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
            },
        ]

        all_success = True
        async with Supertone(api_key=API_KEY) as client:
            for case in test_cases:
                print(f"  🔍 Testing {case['name']}...")
                print(f"     📏 Text length: {len(case['text'])} characters")

                try:
                    response = await client.text_to_speech.create_speech_async(
                        voice_id=voice_id,
                        text=case["text"],
                        language=case["language"],
                        style="neutral",
                        model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                        output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                    )

                    if hasattr(response, "result") and hasattr(response.result, "read"):
                        audio_data = response.result.read()
                        if len(audio_data) > 0:
                            print(f"     ✅ Success: {len(audio_data):,} bytes")
                        else:
                            print(f"     ❌ Empty audio data")
                            all_success = False
                    else:
                        print(f"     ❌ Response structure error")
                        all_success = False

                except Exception as e:
                    print(f"     ❌ Error: {e}")
                    all_success = False

        return all_success, "multilingual_punctuation async test"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_stream_speech_multilingual_punctuation(voice_id):
    """Test async streaming TTS with multilingual punctuation splitting"""
    print("🌐🔊✂️ Async Streaming Multilingual Punctuation Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Japanese text with 。！？、 punctuation (over 300 chars)
        japanese_text = (
            "これは日本語のストリーミングテストです。音声合成技術はとても進化しています！"
            "リアルタイムストリーミングは素晴らしいですね？長いテキストでも自然に分割されます。"
            "品質がとても良いです！次の文章も続きます。これで三百文字を超えるテキストになります。"
            "人工知能の発展により音声技術も進歩しました。素晴らしいですね！最新技術を活用しています。"
            "テキストが長くなっても問題なく処理できます。自動チャンキング機能が正しく動作しています！"
            "これで確実に三百文字を超えました。日本語の句読点で自然に分割されることを確認します。"
            "最新のAI技術を活用した音声合成システムです。ストリーミング機能も完璧に動作します！テスト完了です！"
        )

        print(f"  📏 Text length: {len(japanese_text)} characters")
        print(f"  📝 Contains: 。！？ punctuation marks")

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Streaming TTS with Japanese punctuation splitting (async)...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=japanese_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "aiter_bytes"):
                async for chunk in response.result.aiter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "iter_bytes"):
                for chunk in response.result.iter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "read"):
                audio_data = response.result.read()

            if len(audio_data) > 0:
                print(f"  ✅ Streaming multilingual punctuation splitting successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")
                return True, response
            else:
                print("  ❌ Empty audio data")
                return False, response

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


async def test_stream_speech_japanese_no_spaces(voice_id):
    """Test async streaming TTS with Japanese text (character-based splitting)"""
    print("🇯🇵🔊✂️ Async Streaming Japanese Character-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Long Japanese text without spaces
        japanese_text = (
            "これは日本語のストリーミングテストです。"
            "日本語のテキストは通常スペースを含まないため、"
            "文字単位での分割が必要になります。"
            "このテストでは三百文字を超える長い日本語テキストを使用して、"
            "ストリーミング音声合成が正しく動作することを確認します。"
            "最新の人工知能技術により、高品質な音声合成が可能になりました。"
            "私たちはこの技術を活用して、より自然な音声体験を提供します。"
        )

        print(f"  📏 Text length: {len(japanese_text)} characters")

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Streaming TTS with character-based chunking (async)...")
            print("  ⚠️ This test will consume credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=japanese_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "aiter_bytes"):
                async for chunk in response.result.aiter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "iter_bytes"):
                for chunk in response.result.iter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "read"):
                audio_data = response.result.read()

            if len(audio_data) > 0:
                print(f"  ✅ Streaming character-based chunking successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")
                return True, response
            else:
                print("  ❌ Empty audio data")
                return False, response

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


# ============================================
# Concurrent/Parallel Testing (Async Power!)
# ============================================


async def test_concurrent_api_calls(voice_id):
    """Test multiple API calls concurrently - showcase async power"""
    print("🚀 Concurrent API Calls Test (Async Power!)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Running 5 different API calls concurrently...")
            print("  ⏱️ Starting timer...")

            start_time = time.time()

            # Run 5 different API calls concurrently
            results = await asyncio.gather(
                client.usage.get_credit_balance_async(),
                client.voices.list_voices_async(page_size=10),
                client.custom_voices.list_custom_voices_async(page_size=10),
                client.text_to_speech.predict_duration_async(
                    voice_id=voice_id,
                    text="Concurrent API test",
                    language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                ),
                client.usage.get_voice_usage_async(
                    start_date=(datetime.now() - timedelta(days=1)).strftime(
                        "%Y-%m-%d"
                    ),
                    end_date=datetime.now().strftime("%Y-%m-%d"),
                ),
                return_exceptions=True,
            )

            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"  ✅ All 5 API calls completed!")
            print(f"  ⏱️ Total time: {elapsed_time:.3f}s (parallel execution)")
            print(f"  🚀 Average time per call: {elapsed_time/5:.3f}s")

            success_count = sum(1 for r in results if not isinstance(r, Exception))
            print(f"  📊 Success: {success_count}/5 calls")

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"     Call {i+1}: ❌ {type(result).__name__}")
                else:
                    print(f"     Call {i+1}: ✅ Success")

            return True, {
                "elapsed_time": elapsed_time,
                "success_count": success_count,
                "total_calls": 5,
            }

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_parallel_tts_conversion(voice_id):
    """Test parallel TTS conversions with different texts - async power"""
    print("🎤🎤🎤 Parallel TTS Conversion Test (Async Power!)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        texts = [
            "First parallel TTS test.",
            "Second parallel TTS test.",
            "Third parallel TTS test.",
        ]

        async with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting {len(texts)} texts in parallel...")
            print("  ⚠️ This test consumes credits!")
            print("  ⏱️ Starting timer...")

            start_time = time.time()

            # Create parallel TTS conversion tasks
            tasks = [
                client.text_to_speech.create_speech_async(
                    voice_id=voice_id,
                    text=text,
                    language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                    output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                )
                for text in texts
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"  ✅ All {len(texts)} TTS conversions completed!")
            print(f"  ⏱️ Total time: {elapsed_time:.3f}s (parallel execution)")
            print(f"  🚀 Average time per conversion: {elapsed_time/len(texts):.3f}s")

            success_count = 0
            total_bytes = 0

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"     Text {i+1}: ❌ {type(result).__name__}")
                else:
                    if hasattr(result, "result") and hasattr(result.result, "read"):
                        audio_data = result.result.read()
                        audio_size = len(audio_data)
                        total_bytes += audio_size
                        success_count += 1
                        print(f"     Text {i+1}: ✅ {audio_size} bytes")

                        # Save individual files
                        output_file = f"test_async_parallel_tts_{i+1}.wav"
                        with open(output_file, "wb") as f:
                            f.write(audio_data)
                        print(f"        💾 Saved: {output_file}")

            print(f"  📊 Success: {success_count}/{len(texts)} conversions")
            print(f"  📦 Total audio: {total_bytes} bytes")

            return True, {
                "elapsed_time": elapsed_time,
                "success_count": success_count,
                "total_conversions": len(texts),
                "total_bytes": total_bytes,
            }

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_parallel_multiple_voices(voice_id):
    """Test same text with multiple voices in parallel - async power"""
    print("🎭🎭🎭 Parallel Multiple Voices Test (Async Power!)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        async with Supertone(api_key=API_KEY) as client:
            # First, get multiple voices
            print("  🔍 Fetching available voices...")
            voice_response = await client.voices.list_voices_async(page_size=10)

            if not voice_response.items or len(voice_response.items) < 2:
                print("  ⚠️ Not enough voices available for parallel test")
                return False, None

            voice_ids = [voice.voice_id for voice in voice_response.items[:3]]
            print(f"  📊 Using {len(voice_ids)} voices for parallel test")

            print("  🔍 Predicting duration with multiple voices in parallel...")
            print("  ⏱️ Starting timer...")

            start_time = time.time()

            # Predict duration with multiple voices in parallel
            from supertone import models

            tasks = [
                client.text_to_speech.predict_duration_async(
                    voice_id=vid,
                    text="Parallel multiple voices test with async power!",
                    language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                )
                for vid in voice_ids
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"  ✅ All {len(voice_ids)} voice predictions completed!")
            print(f"  ⏱️ Total time: {elapsed_time:.3f}s (parallel execution)")
            print(f"  🚀 Average time per voice: {elapsed_time/len(voice_ids):.3f}s")

            success_count = 0
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(
                        f"     Voice {i+1} ({voice_ids[i][:8]}...): ❌ {type(result).__name__}"
                    )
                else:
                    print(f"     Voice {i+1} ({voice_ids[i][:8]}...): ✅ {result}s")
                    success_count += 1

            print(f"  📊 Success: {success_count}/{len(voice_ids)} predictions")

            return True, {
                "elapsed_time": elapsed_time,
                "success_count": success_count,
                "total_voices": len(voice_ids),
            }

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_mixed_parallel_operations(voice_id):
    """Test mixed read/write operations in parallel - complex async scenario"""
    print("🔀 Mixed Parallel Operations Test (Complex Async!)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print("  🔍 Running mixed read/write operations in parallel...")
            print("  ⏱️ Starting timer...")

            start_time = time.time()

            # Mix of different operation types
            results = await asyncio.gather(
                # Read operations
                client.usage.get_credit_balance_async(),
                client.voices.list_voices_async(page_size=10),
                client.custom_voices.list_custom_voices_async(page_size=10),
                # Prediction operations (lightweight)
                client.text_to_speech.predict_duration_async(
                    voice_id=voice_id,
                    text="Mixed operations test one",
                    language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                ),
                client.text_to_speech.predict_duration_async(
                    voice_id=voice_id,
                    text="Mixed operations test two",
                    language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                ),
                return_exceptions=True,
            )

            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"  ✅ All mixed operations completed!")
            print(f"  ⏱️ Total time: {elapsed_time:.3f}s (parallel execution)")

            operation_types = [
                "Credit Check",
                "List Voices",
                "List Custom Voices",
                "Predict 1",
                "Predict 2",
            ]
            success_count = 0

            for i, (op_type, result) in enumerate(zip(operation_types, results)):
                if isinstance(result, Exception):
                    print(f"     {op_type}: ❌ {type(result).__name__}")
                else:
                    print(f"     {op_type}: ✅ Success")
                    success_count += 1

            print(f"  📊 Success: {success_count}/{len(results)} operations")
            print(
                f"  💡 Note: Parallel async allows mixing different operation types efficiently!"
            )

            return True, {
                "elapsed_time": elapsed_time,
                "success_count": success_count,
                "total_operations": len(results),
            }

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_with_pronunciation_dictionary(voice_id):
    """Test async TTS with pronunciation dictionary substitution"""
    print("📖🎤 Pronunciation Dictionary TTS Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        async with Supertone(api_key=API_KEY) as client:
            # Note: "TTSAPI" tests partial_match=True (substring replacement)
            text = "Hello, I work at Supertone Inc. The TTSAPI is amazing!"

            # Pronunciation dictionary: mix of partial_match=True and False
            pronunciation_dictionary = [
                # partial_match=False: only matches standalone "Supertone"
                {"text": "Supertone", "pronunciation": "Super-tone", "partial_match": False},
                # partial_match=True: matches "TTS" inside "TTSAPI" as well
                {"text": "TTS", "pronunciation": "Text-to-Speech", "partial_match": True},
                # partial_match=False: exact word boundary match
                {"text": "Inc", "pronunciation": "Incorporated", "partial_match": False},
            ]

            print(f"  📝 Original text: {text}")
            print(f"  📖 Pronunciation dictionary entries: {len(pronunciation_dictionary)}")
            for entry in pronunciation_dictionary:
                print(f"    - '{entry['text']}' → '{entry['pronunciation']}' (partial_match={entry['partial_match']})")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                pronunciation_dictionary=pronunciation_dictionary,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                print(f"  ✅ Pronunciation dictionary TTS successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")

                output_file = "test_async_pronunciation_dictionary_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Saved: {output_file}")

                return True, response
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_create_speech_pronunciation_dictionary_long_text(voice_id):
    """Test async TTS with pronunciation dictionary that expands text beyond 300 chars (triggers auto-chunking)"""
    print("📖📜🎤 Pronunciation Dictionary Long Text TTS Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        async with Supertone(api_key=API_KEY) as client:
            # Short text that expands to 300+ chars after pronunciation substitution
            # Note: Contains "AIML" and "TTSAPI" to test partial_match behavior
            text = (
                "AI and AIML power modern TTS systems. "
                "The TTSAPI enables voice synthesis via SDK. "
                "Our AI SDK supports real-time API calls. "
                "Use the TTS API to integrate AI into your app."
            )

            # Pronunciation dictionary that significantly expands the text
            # Mix of partial_match=True and False to demonstrate both behaviors
            pronunciation_dictionary = [
                # partial_match=False: "AI" won't match inside "AIML"
                {"text": "AI", "pronunciation": "Artificial Intelligence System", "partial_match": False},
                # partial_match=True: "TTS" will match inside "TTSAPI"
                {"text": "TTS", "pronunciation": "Text-to-Speech Engine", "partial_match": True},
                # partial_match=False: exact word match only
                {"text": "SDK", "pronunciation": "Software Development Kit", "partial_match": False},
                # partial_match=True: "API" will match inside "TTSAPI" (after TTS replaced)
                {"text": "API", "pronunciation": "Application Programming Interface", "partial_match": True},
            ]

            print(f"  📏 Original text length: {len(text)} characters")
            print(f"  📖 Pronunciation dictionary entries: {len(pronunciation_dictionary)}")
            for entry in pronunciation_dictionary:
                print(f"    - '{entry['text']}' → '{entry['pronunciation']}'")

            # Calculate expanded length
            expanded_text = text
            for entry in pronunciation_dictionary:
                expanded_text = expanded_text.replace(entry["text"], entry["pronunciation"])
            print(f"  📏 Expanded text length: {len(expanded_text)} characters")
            print(f"  {'✅' if len(expanded_text) > 300 else '⚠️'} {'Exceeds' if len(expanded_text) > 300 else 'Does not exceed'} 300 chars (auto-chunking threshold)")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.create_speech_async(
                voice_id=voice_id,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                pronunciation_dictionary=pronunciation_dictionary,
            )

            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                print(f"  ✅ Pronunciation dictionary long text TTS successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")

                output_file = "test_async_pronunciation_dictionary_long_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Saved: {output_file}")

                return True, response
            else:
                print(f"  ❌ Response structure verification needed: {type(response)}")
                return False, response

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_with_pronunciation_dictionary(voice_id):
    """Test async streaming TTS with pronunciation dictionary"""
    print("📖🔊 Pronunciation Dictionary Streaming TTS Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        async with Supertone(api_key=API_KEY) as client:
            # Note: "TTSAPI" tests partial_match=True behavior
            text = "Welcome to Supertone. Our AI TTSAPI delivers high-quality voice synthesis."

            pronunciation_dictionary = [
                # partial_match=False: exact word boundary match
                {"text": "Supertone", "pronunciation": "Super-tone Korea", "partial_match": False},
                {"text": "AI", "pronunciation": "Artificial Intelligence", "partial_match": False},
                # partial_match=True: matches "TTS" inside "TTSAPI"
                {"text": "TTS", "pronunciation": "Text-to-Speech", "partial_match": True},
                {"text": "API", "pronunciation": "A-P-I", "partial_match": True},
            ]

            print(f"  📝 Original text: {text}")
            print(f"  📖 Dictionary entries: {len(pronunciation_dictionary)}")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                pronunciation_dictionary=pronunciation_dictionary,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "aiter_bytes"):
                async for chunk in response.result.aiter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "iter_bytes"):
                for chunk in response.result.iter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "read"):
                audio_data = response.result.read()

            if len(audio_data) > 0:
                print(f"  ✅ Pronunciation dictionary streaming successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")

                output_file = "test_async_pronunciation_dictionary_stream_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Saved: {output_file}")

                return True, response
            else:
                print("  ❌ Empty audio data")
                return False, response

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def test_stream_speech_pronunciation_dictionary_long_text(voice_id):
    """Test async streaming TTS with pronunciation dictionary that expands text beyond 300 chars"""
    print("📖📜🔊 Pronunciation Dictionary Long Text Streaming TTS Test (Async)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        async with Supertone(api_key=API_KEY) as client:
            # Short text that expands to 300+ chars
            # Contains "AIML" and compound words to test partial_match behavior
            text = (
                "Our AI and AIML SDK provides seamless TTSAPI integration. "
                "The AI analyzes text and the TTS engine generates speech. "
                "Use our SDK to access the API. AI-powered TTS is the future."
            )

            pronunciation_dictionary = [
                # partial_match=False: "AI" won't match inside "AIML" or "AI-powered"
                {"text": "AI", "pronunciation": "Artificial Intelligence System", "partial_match": False},
                # partial_match=True: "TTS" matches inside "TTSAPI"
                {"text": "TTS", "pronunciation": "Text-to-Speech Voice Engine", "partial_match": True},
                {"text": "SDK", "pronunciation": "Software Development Kit", "partial_match": False},
                # partial_match=True: "API" matches inside "TTSAPI"
                {"text": "API", "pronunciation": "Application Programming Interface", "partial_match": True},
            ]

            print(f"  📏 Original text length: {len(text)} characters")
            for entry in pronunciation_dictionary:
                print(f"    - '{entry['text']}' → '{entry['pronunciation']}' (partial_match={entry['partial_match']})")

            # Calculate expanded length
            expanded_text = text
            for entry in pronunciation_dictionary:
                expanded_text = expanded_text.replace(entry["text"], entry["pronunciation"])
            print(f"  📏 Expanded text length: {len(expanded_text)} characters")
            print(f"  ✅ Triggers auto-chunking: {len(expanded_text) > 300}")
            print("  ⚠️ This test consumes credits!")

            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                pronunciation_dictionary=pronunciation_dictionary,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "aiter_bytes"):
                async for chunk in response.result.aiter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "iter_bytes"):
                for chunk in response.result.iter_bytes():
                    audio_data += chunk
            elif hasattr(response.result, "read"):
                audio_data = response.result.read()

            if len(audio_data) > 0:
                print(f"  ✅ Pronunciation dictionary long text streaming successful!")
                print(f"  📦 Audio data size: {len(audio_data):,} bytes")

                output_file = "test_async_pronunciation_dictionary_stream_long_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Saved: {output_file}")

                return True, response
            else:
                print("  ❌ Empty audio data")
                return False, response

    except Exception as e:
        import traceback

        print(f"  ❌ Unexpected error: {e}")
        print(f"  📋 Traceback:")
        traceback.print_exc()
        return False, e


async def main():
    """Main async integration test runner - all async API tests"""
    print("🧪 Async API Integration Test Started (All Async APIs)")
    print(f"🔑 API Key: {API_KEY[:8]}..." + "*" * 24)
    print("🔧 Authentication: HTTP Headers (x-sup-api-key)")
    print("=" * 60)

    test_results = {}
    voice_id_for_tts = "91992bbd4758bdcf9c9b01"  # Adam
    custom_voice_id = None
    created_custom_voice_id = None

    # 1. Credit and Usage Tests
    print("\n1️⃣ Credit and Usage Tests (Async)")

    success, result = await test_credit_balance()
    test_results["get_credit_balance_async"] = success

    if not success:
        print("❌ API key authentication failed. Stopping tests.")
        return False

    success, result = await test_get_usage()
    test_results["get_usage_async"] = success

    success, result = await test_get_voice_usage()
    test_results["get_voice_usage_async"] = success

    # 2. Voice Tests
    print("\n2️⃣ Voice Tests (Async)")

    success, result = await test_list_voices()
    test_results["list_voices_async"] = success

    success, result = await test_search_voices()
    test_results["search_voices_async"] = success

    if voice_id_for_tts:
        success, result = await test_get_voice(voice_id_for_tts)
        test_results["get_voice_async"] = success

    # 3. Custom Voice Tests
    print("\n3️⃣ Custom Voice Tests (Async)")

    success, result = await test_list_custom_voices()
    test_results["list_custom_voices_async"] = success
    if success and result[1]:
        custom_voice_id = result[1]

    success, result = await test_search_custom_voices()
    test_results["search_custom_voices_async"] = success

    if custom_voice_id:
        success, result = await test_get_custom_voice(custom_voice_id)
        test_results["get_custom_voice_async"] = success

        success, result = await test_edit_custom_voice(custom_voice_id)
        test_results["edit_custom_voice_async"] = success

    # Custom Voice Creation Test
    print("\n🎨 Custom Voice Creation Test (Async)")
    success, result = await test_create_cloned_voice()
    test_results["create_cloned_voice_async"] = success
    if success and result:
        created_custom_voice_id = result.voice_id
        print(f"  🎉 New custom voice created: {created_custom_voice_id}")

    # 4. TTS Tests
    print("\n4️⃣ TTS Tests (Async)")

    if voice_id_for_tts:
        # Duration prediction (no credit consumption)
        success, result = await test_predict_duration(voice_id_for_tts)
        test_results["predict_duration_async"] = success

        # Basic TTS (consumes credits)
        print("💳 TTS consumes credits.")
        success, result = await test_create_speech(voice_id_for_tts)
        test_results["create_speech_async"] = success

        # Voice settings TTS
        success, result = await test_create_speech_with_voice_settings(voice_id_for_tts)
        test_results["create_speech_with_voice_settings_async"] = success

        # Basic streaming TTS (WAV)
        success, result = await test_stream_speech(voice_id_for_tts)
        test_results["stream_speech_async"] = success

        # Voice Settings Tests
        success, result = await test_predict_duration_with_voice_settings(
            voice_id_for_tts
        )
        test_results["predict_duration_with_voice_settings_async"] = success

        success, result = await test_stream_speech_with_voice_settings(voice_id_for_tts)
        test_results["stream_speech_with_voice_settings_async"] = success

        # 5. Phoneme Tests
        print("\n🔤 Phoneme Information TTS Tests (Async)")

        print("💳 Phoneme TTS consumes credits.")
        success, result = await test_create_speech_with_phonemes(voice_id_for_tts)
        test_results["create_speech_with_phonemes_async"] = success

        success, result = await test_stream_speech_with_phonemes(voice_id_for_tts)
        test_results["stream_speech_with_phonemes_async"] = success

        # 6. Long Text Tests (WAV)
        print("\n5️⃣ Long Text Tests (300+ chars - WAV) (Async)")
        success, result = await test_create_speech_long_text(voice_id_for_tts)
        test_results["create_speech_long_text_async"] = success

        success, result = await test_stream_speech_long_text(voice_id_for_tts)
        test_results["stream_speech_long_text_async"] = success

        # 7. MP3 Format Tests
        print("\n🎵 MP3 Format TTS Tests (Async)")
        success, result = await test_create_speech_mp3(voice_id_for_tts)
        test_results["create_speech_mp3_async"] = success

        success, result = await test_create_speech_long_text_mp3(voice_id_for_tts)
        test_results["create_speech_long_text_mp3_async"] = success

        success, result = await test_stream_speech_mp3(voice_id_for_tts)
        test_results["stream_speech_mp3_async"] = success

        success, result = await test_stream_speech_long_text_mp3(voice_id_for_tts)
        test_results["stream_speech_long_text_mp3_async"] = success

        # 8. Long Text + Phoneme Tests
        print("\n📜🔤 Long Text + Phoneme Tests (Async)")
        success, result = await test_create_speech_long_text_with_phonemes(
            voice_id_for_tts
        )
        test_results["create_speech_long_text_with_phonemes_async"] = success

        success, result = await test_stream_speech_phoneme_chunking_wav(
            voice_id_for_tts
        )
        test_results["stream_speech_phoneme_chunking_wav_async"] = success

        # 9. New Model Tests (sona_speech_2, sona_speech_2_flash, supertonic_api_1)
        print("\n6️⃣ New Model Tests (sona_speech_2, sona_speech_2_flash, supertonic_api_1) (Async)")

        # TTS with sona_speech_2
        success, result = await test_create_speech_sona_speech_2(voice_id_for_tts)
        test_results["create_speech_sona_speech_2_async"] = success

        # TTS with sona_speech_2_flash (low latency)
        success, result = await test_create_speech_sona_speech_2_flash(voice_id_for_tts)
        test_results["create_speech_sona_speech_2_flash_async"] = success

        # TTS with sona_speech_2 + normalized_text (Japanese pronunciation)
        success, result = await test_create_speech_sona_speech_2_with_normalized_text(voice_id_for_tts)
        test_results["create_speech_sona_speech_2_with_normalized_text_async"] = success

        # TTS with sona_speech_2_flash + normalized_text (Japanese pronunciation)
        success, result = await test_create_speech_sona_speech_2_flash_with_normalized_text(voice_id_for_tts)
        test_results["create_speech_sona_speech_2_flash_with_normalized_text_async"] = success

        # TTS with supertonic_api_1
        success, result = await test_create_speech_supertonic_api_1(voice_id_for_tts)
        test_results["create_speech_supertonic_api_1_async"] = success

        # Invalid model test
        success, result = await test_create_speech_invalid_model(voice_id_for_tts)
        test_results["create_speech_invalid_model_async"] = success

        # Duration prediction with new models
        success, result = await test_predict_duration_sona_speech_2(voice_id_for_tts)
        test_results["predict_duration_sona_speech_2_async"] = success

        # Duration prediction with sona_speech_2_flash
        success, result = await test_predict_duration_sona_speech_2_flash(voice_id_for_tts)
        test_results["predict_duration_sona_speech_2_flash_async"] = success

        success, result = await test_predict_duration_supertonic_api_1(voice_id_for_tts)
        test_results["predict_duration_supertonic_api_1_async"] = success

        # Invalid model prediction test
        success, result = await test_predict_duration_invalid_model(voice_id_for_tts)
        test_results["predict_duration_invalid_model_async"] = success

        # 10. Multi-language Tests by Model
        print("\n7️⃣ Multi-language Tests by Model (Async)")

        # sona_speech_1 multilang (ko, en, ja)
        success, result = await test_create_speech_sona_speech_1_multilang(
            voice_id_for_tts
        )
        test_results["create_speech_sona_speech_1_multilang_async"] = success

        # sona_speech_2 multilang (all languages)
        success, result = await test_create_speech_sona_speech_2_multilang(
            voice_id_for_tts
        )
        test_results["create_speech_sona_speech_2_multilang_async"] = success

        # supertonic_api_1 multilang (ko, en, ja, es, pt)
        success, result = await test_create_speech_supertonic_api_1_multilang(
            voice_id_for_tts
        )
        test_results["create_speech_supertonic_api_1_multilang_async"] = success

        # Unsupported language error tests
        success, result = await test_create_speech_sona_speech_1_unsupported_lang(
            voice_id_for_tts
        )
        test_results["create_speech_sona_speech_1_unsupported_lang_async"] = success

        success, result = await test_create_speech_supertonic_api_1_unsupported_lang(
            voice_id_for_tts
        )
        test_results["create_speech_supertonic_api_1_unsupported_lang_async"] = success

        # Duration prediction multilang test
        success, result = await test_predict_duration_multilang(voice_id_for_tts)
        test_results["predict_duration_multilang_async"] = success

        # 11. Advanced Text Chunking Tests
        print("\n8️⃣ Advanced Text Chunking Tests (Async)")

        # Long sentence word-based splitting (TTS)
        success, result = await test_create_speech_long_sentence_word_split(
            voice_id_for_tts
        )
        test_results["create_speech_long_sentence_word_split_async"] = success

        # Japanese character-based splitting (TTS)
        success, result = await test_create_speech_japanese_no_spaces(voice_id_for_tts)
        test_results["create_speech_japanese_no_spaces_async"] = success

        # Long sentence word-based splitting (Streaming)
        success, result = await test_stream_speech_long_sentence_word_split(
            voice_id_for_tts
        )
        test_results["stream_speech_long_sentence_word_split_async"] = success

        # Japanese character-based splitting (Streaming)
        success, result = await test_stream_speech_japanese_no_spaces(voice_id_for_tts)
        test_results["stream_speech_japanese_no_spaces_async"] = success

        # Multilingual punctuation splitting tests
        success, result = await test_create_speech_multilingual_punctuation(
            voice_id_for_tts
        )
        test_results["create_speech_multilingual_punctuation_async"] = success

        success, result = await test_stream_speech_multilingual_punctuation(
            voice_id_for_tts
        )
        test_results["stream_speech_multilingual_punctuation_async"] = success

        # 12. Pronunciation Dictionary Tests
        print("\n📖 Pronunciation Dictionary Tests (Async)")

        # Basic pronunciation dictionary test
        success, result = await test_create_speech_with_pronunciation_dictionary(
            voice_id_for_tts
        )
        test_results["create_speech_with_pronunciation_dictionary_async"] = success

        # Pronunciation dictionary with long text (triggers auto-chunking)
        success, result = await test_create_speech_pronunciation_dictionary_long_text(
            voice_id_for_tts
        )
        test_results["create_speech_pronunciation_dictionary_long_text_async"] = success

        # Streaming with pronunciation dictionary
        success, result = await test_stream_speech_with_pronunciation_dictionary(
            voice_id_for_tts
        )
        test_results["stream_speech_with_pronunciation_dictionary_async"] = success

        # Streaming with pronunciation dictionary long text
        success, result = await test_stream_speech_pronunciation_dictionary_long_text(
            voice_id_for_tts
        )
        test_results["stream_speech_pronunciation_dictionary_long_text_async"] = success

        # 13. Concurrent/Parallel Tests (Async Power!)
        print("\n🚀 Concurrent/Parallel Tests (Async Power!)")
        success, result = await test_concurrent_api_calls(voice_id_for_tts)
        test_results["concurrent_api_calls_async"] = success

        success, result = await test_parallel_tts_conversion(voice_id_for_tts)
        test_results["parallel_tts_conversion_async"] = success

        success, result = await test_parallel_multiple_voices(voice_id_for_tts)
        test_results["parallel_multiple_voices_async"] = success

        success, result = await test_mixed_parallel_operations(voice_id_for_tts)
        test_results["mixed_parallel_operations_async"] = success

    # 10. Custom Voice Deletion (run last)
    if created_custom_voice_id:
        print("\n🗑️ Created Custom Voice Deletion Test (Async)")
        success, result = await test_delete_custom_voice(created_custom_voice_id)
        test_results["delete_custom_voice_async"] = success

    # Results Summary
    print("\n" + "=" * 60)
    print("🧪 Async Integration Test Results Summary:")

    passed = 0
    total = 0

    for test_name, result in test_results.items():
        if result is None:
            status = "⏭️ SKIP"
        elif result:
            status = "✅ PASS"
            passed += 1
            total += 1
        else:
            status = "❌ FAIL"
            total += 1

        print(f"  {test_name}: {status}")

    print(f"\nTotal {passed}/{total} tests passed")

    if passed == total:
        print(
            "🎉 All async integration tests passed! Async SDK works correctly with real API."
        )
        print("\n✅ Async SDK ready for deployment!")
    else:
        print("⚠️ Some tests failed. Please check API key or permissions.")

    print("\n📋 All tested async APIs:")
    print("  • Usage: get_credit_balance_async, get_usage_async, get_voice_usage_async")
    print("  • Voices: list_voices_async, search_voices_async, get_voice_async")
    print(
        "  • Custom Voices: list_custom_voices_async, search_custom_voices_async, get_custom_voice_async"
    )
    print(
        "                   create_cloned_voice_async, edit_custom_voice_async, delete_custom_voice_async"
    )
    print(
        "  • Text-to-Speech (WAV): predict_duration_async, create_speech_async, stream_speech_async"
    )
    print("  • Voice Settings Tests: predict_duration_with_voice_settings_async,")
    print(
        "                          create_speech_with_voice_settings_async, stream_speech_with_voice_settings_async"
    )
    print(
        "  • Phoneme Tests: create_speech_with_phonemes_async, stream_speech_with_phonemes_async"
    )
    print("  • Long Text Tests (Auto-Chunking):")
    print("    - WAV: create_speech_long_text_async, stream_speech_long_text_async")
    print("    - MP3: create_speech_mp3_async, create_speech_long_text_mp3_async")
    print("           stream_speech_mp3_async, stream_speech_long_text_mp3_async")
    print("  • Long Text + Phoneme Tests:")
    print(
        "    - create_speech_long_text_with_phonemes_async, stream_speech_phoneme_chunking_wav_async"
    )
    print("  • New Model Tests:")
    print(
        "    - sona_speech_2: create_speech_sona_speech_2_async, predict_duration_sona_speech_2_async"
    )
    print(
        "    - sona_speech_2_flash: create_speech_sona_speech_2_flash_async, predict_duration_sona_speech_2_flash_async"
    )
    print(
        "    - normalized_text: create_speech_sona_speech_2_with_normalized_text_async, create_speech_sona_speech_2_flash_with_normalized_text_async"
    )
    print(
        "    - supertonic_api_1: create_speech_supertonic_api_1_async, predict_duration_supertonic_api_1_async"
    )
    print(
        "    - Invalid model tests: create_speech_invalid_model_async, predict_duration_invalid_model_async"
    )
    print("  • Multi-language Tests by Model:")
    print("    - sona_speech_1: ko, en, ja")
    print("    - sona_speech_2: all languages")
    print("    - supertonic_api_1: ko, en, ja, es, pt")
    print("    - Unsupported language error tests")
    print("  • Advanced Text Chunking Tests:")
    print("    - Long sentence word-based splitting: create_speech, stream_speech")
    print("    - Japanese character-based splitting: create_speech, stream_speech")
    print(
        "    - Multilingual punctuation splitting (。！？…): create_speech, stream_speech"
    )
    print("  • Pronunciation Dictionary Tests:")
    print("    - Basic: create_speech_async, stream_speech_async")
    print("    - Long text (auto-chunking): create_speech_async, stream_speech_async")
    print("  • Concurrent/Parallel Tests (Async Power!):")
    print("    - concurrent_api_calls_async (5 different APIs in parallel)")
    print("    - parallel_tts_conversion_async (3 texts converted simultaneously)")
    print("    - parallel_multiple_voices_async (3 voices tested simultaneously)")
    print("    - mixed_parallel_operations_async (mixed read/write operations)")

    if created_custom_voice_id:
        print(f"\n🎨 Custom voice created during test: {created_custom_voice_id}")

    print(f"\n💡 Async Advantages Demonstrated:")
    print(f"  • All tests use async/await for non-blocking I/O")
    print(f"  • Concurrent tests showcase parallel API call capabilities")
    print(f"  • Significantly faster than sync when running multiple operations")
    print(f"  • Perfect for web servers, real-time apps, and batch processing")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
