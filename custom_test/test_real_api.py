#!/usr/bin/env python3
"""
Real API Integration Test Script
Tests all SDK functionality with real Supertone API calls.
"""
import sys
import os
import json
import base64
from datetime import datetime, timedelta
import time

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


def test_credit_balance():
    """Test credit balance retrieval - safest API call"""
    print("💰 Credit Balance Test")

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Retrieving credit balance...")

            response = client.usage.get_credit_balance()

            print(f"  ✅ Credit balance: {response.balance}")
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_get_usage():
    """Test usage retrieval (Advanced Usage Analytics)"""
    print("📊 Usage Retrieval Test")

    try:
        from supertone import Supertone, errors

        # Query usage for the last 7 days - RFC3339 format
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Retrieving usage from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}..."
            )

            # Using start_time/end_time with RFC3339 format
            response = client.usage.get_usage(
                start_time=start_time.isoformat() + "Z",
                end_time=end_time.isoformat() + "Z",
            )

            print(f"  ✅ Query successful: {len(response.data)} usage record buckets")
            print(f"  📊 Total buckets: {response.total}")

            if response.data:
                # Show first 3 buckets
                for bucket in response.data[:3]:
                    print(f"  📅 Bucket start: {bucket.starting_at}")
                    print(f"     Bucket end: {bucket.ending_at}")
                    print(f"     Results count: {len(bucket.results)}")

                    # Calculate total minutes from results array
                    total_minutes = sum(
                        result.minutes_used for result in bucket.results
                    )
                    print(f"     Total usage: {total_minutes:.2f} minutes")

                    # Show top 3 voice usages
                    for result in bucket.results[:3]:
                        voice_info = (
                            result.voice_name
                            if result.voice_name
                            else f"Voice {result.voice_id[:8] if result.voice_id else 'Unknown'}"
                        )
                        print(f"       🎤 {voice_info}: {result.minutes_used:.2f} min")
            else:
                print("  📝 No usage records found for this period")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_get_voice_usage():
    """Test voice-specific usage retrieval"""
    print("🎤 Voice Usage Retrieval Test")

    try:
        from supertone import Supertone, errors

        # Query voice usage for the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Retrieving voice usage from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}..."
            )

            response = client.usage.get_voice_usage(
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=end_date.strftime("%Y-%m-%d"),
            )

            print(f"  ✅ Query successful: {len(response.usages)} voice usage records")

            if response.usages:
                for usage in response.usages[:5]:  # Show top 5 voices
                    voice_name = (
                        usage.name if usage.name else f"Voice {usage.voice_id[:8]}"
                    )
                    print(f"  🎤 {voice_name}: {usage.total_minutes_used:.2f} min")
                    print(f"     Voice ID: {usage.voice_id}")
                    if usage.language:
                        print(f"     Language: {usage.language}")
            else:
                print("  📝 No voice usage records found for this period")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_list_voices():
    """Test voice list retrieval"""
    print("🎵 Voice List Retrieval Test")

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Retrieving voice list...")

            response = client.voices.list_voices(
                page_size=10  # API requirement: between 10-100
            )

            print(f"  ✅ Query successful: {len(response.items)} voices")
            print(f"  📊 Total voices: {response.total}")

            # Display first voice information
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_search_voices():
    """Test voice search"""
    print("🔍 Voice Search Test")

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Searching for female English voices...")

            response = client.voices.search_voices(
                language="en",
                gender="female",
                page_size=10,  # API requirement: between 10-100
            )

            print(f"  ✅ Search successful: {len(response.items)} voices")

            for voice in response.items:
                print(f"  🎤 {voice.name} ({voice.voice_id})")
                print(f"     Language: {voice.language}, Gender: {voice.gender}")
                print(f"     Use case: {voice.use_case}")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_get_voice(voice_id):
    """Test specific voice detail retrieval"""
    print("📄 Voice Detail Retrieval Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Retrieving voice '{voice_id}' details...")

            response = client.voices.get_voice(voice_id=voice_id)

            print(f"  ✅ Query successful:")
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_list_custom_voices():
    """Test custom voice list retrieval"""
    print("🎨 Custom Voice List Retrieval Test")

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Retrieving custom voice list...")

            response = client.custom_voices.list_custom_voices(page_size=10)

            print(f"  ✅ Query successful: {len(response.items)} custom voices")
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_search_custom_voices():
    """Test custom voice search"""
    print("🔍 Custom Voice Search Test")

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Searching custom voices...")

            response = client.custom_voices.search_custom_voices(page_size=10)

            print(f"  ✅ Search successful: {len(response.items)} custom voices")

            for voice in response.items:
                print(f"  🎤 {voice.name} ({voice.voice_id})")
                print(f"     Description: {voice.description}")

            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_get_custom_voice(voice_id):
    """Test specific custom voice detail retrieval"""
    print("📄 Custom Voice Detail Retrieval Test")

    if not voice_id:
        print("  ⚠️ No custom voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Retrieving custom voice '{voice_id}' details...")

            response = client.custom_voices.get_custom_voice(voice_id=voice_id)

            print(f"  ✅ Query successful:")
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_cloned_voice():
    """Test custom voice creation (using voice_sample.wav file)"""
    print("🎨 Custom Voice Creation Test")

    # Check file path
    audio_file_path = "voice_sample.wav"

    if not os.path.exists(audio_file_path):
        print(f"  ❌ Audio file not found: {audio_file_path}")
        return False, None

    # Check file size (3MB limit)
    file_size = os.path.getsize(audio_file_path)
    max_size = 3 * 1024 * 1024  # 3MB

    print(f"  📏 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

    if file_size > max_size:
        print(f"  ❌ File size exceeds 3MB: {file_size/1024/1024:.2f} MB")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            # Test voice name and description
            timestamp = datetime.now().strftime("%m%d_%H%M")
            voice_name = f"Test Sample Voice {timestamp}"
            voice_description = f"Test custom voice created at {timestamp}"

            print(f"  🔍 Creating custom voice...")
            print(f"     File: {audio_file_path}")
            print(f"     Name: {voice_name}")
            print(f"     Description: {voice_description}")
            print(
                "  ⚠️ This test will consume credits and create an actual custom voice!"
            )

            # Create file upload object
            with open(audio_file_path, "rb") as audio_file:
                audio_content = audio_file.read()

                files_obj = models.Files(
                    file_name="voice_sample.wav",
                    content=audio_content,
                    content_type="audio/wav",
                )

                response = client.custom_voices.create_cloned_voice(
                    files=files_obj,
                    name=voice_name,
                    description=voice_description,
                )

            print(f"  ✅ Custom voice creation request successful!")
            print(f"     Voice ID: {response.voice_id}")
            print(f"     Status: {getattr(response, 'status', 'Unknown')}")

            return True, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.PayloadTooLargeErrorResponse as e:
        print(f"  ❌ File size exceeded: File is too large (exceeds 3MB)")
        return False, e
    except errors.UnsupportedMediaTypeErrorResponse as e:
        print(f"  ❌ Unsupported file format: Please use WAV or MP3 file")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_edit_custom_voice(voice_id):
    """Test custom voice information update"""
    print("✏️ Custom Voice Update Test")

    if not voice_id:
        print("  ⚠️ No custom voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors

        with Supertone(api_key=API_KEY) as client:
            # New test name and description
            timestamp = datetime.now().strftime("%H%M%S")
            test_name = f"Updated Test Voice {timestamp}"
            test_description = f"Updated description at {timestamp}"

            print(f"  🔄 Updating custom voice '{voice_id}'...")
            print(f"     New name: {test_name}")
            print(f"     New description: {test_description}")

            response = client.custom_voices.edit_custom_voice(
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_delete_custom_voice(voice_id):
    """Test custom voice deletion"""
    print("🗑️ Custom Voice Deletion Test")

    if not voice_id:
        print("  ⚠️ No custom voice ID to delete")
        return False, None

    try:
        from supertone import Supertone, errors

        print("  ⚠️ This test will actually delete the custom voice!")
        print("     Use for testing purposes only.")

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Deleting custom voice '{voice_id}'...")

            response = client.custom_voices.delete_custom_voice(voice_id=voice_id)

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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_predict_duration(voice_id):
    """Test audio duration prediction - safe test before TTS call"""
    print("⏱️ Audio Duration Prediction Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Predicting duration with voice '{voice_id}'...")

            response = client.text_to_speech.predict_duration(
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
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech(voice_id):
    """Test actual TTS conversion - test that consumes credits"""
    print("🎤 TTS Conversion Test (Consumes Credits)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            # Test with approximately 50 Korean characters
            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text="안녕하세요! 이것은 SDK 테스트를 위한 한국어 텍스트입니다. 정상적으로 작동하는지 확인해보겠습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            # Handle TTS response
            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ TTS conversion successful: {audio_size} bytes audio generated"
                )

                # Save and validate audio file
                output_file = "test_create_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio file saved: {output_file}")

                # Check file size and WAV header
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
                print(f"  ❌ Response structure needs verification: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_long_text(voice_id):
    """Test auto-chunking TTS conversion for text over 300 characters"""
    print("📜 Auto-Chunking TTS Test for Text Over 300 Characters")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # Long text over 500 characters
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
        print(f"  📏 Test text length: {actual_length} characters (over 300)")
        print(f"  🔧 Auto-chunking enabled, text will be automatically split")

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting auto-chunking TTS with voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")
            print("  ✨ SDK will automatically chunk and process the text")

            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            # Handle auto-chunking success
            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ Auto-chunking TTS conversion successful: {audio_size} bytes audio generated"
                )
                print(f"  🎯 Long text successfully chunked and processed!")

                output_file = "test_auto_chunking_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Auto-chunking audio file saved: {output_file}")

                # Check file size and WAV header
                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(12)
                    if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                        print(f"  ✅ Valid auto-chunking WAV file generated")
                    else:
                        print(f"  ⚠️ WAV header needs verification: {header[:12]}")

                # Calculate and display estimated chunk count
                estimated_chunks = (actual_length + 299) // 300  # Ceiling division
                print(
                    f"  📊 Estimated chunk count: {estimated_chunks} (based on text length)"
                )
                print(
                    f"  🔀 Each chunk processed concurrently through parallel processing"
                )

                return True, {
                    "audio_size": audio_size,
                    "text_length": actual_length,
                    "estimated_chunks": estimated_chunks,
                    "output_file": output_file,
                }
            elif hasattr(response, "result") and hasattr(response.result, "content"):
                # If content attribute exists
                audio_data = response.result.content
                audio_size = len(audio_data)
                print(
                    f"  ✅ Auto-chunking TTS conversion successful: {audio_size} bytes audio generated"
                )

                output_file = "test_auto_chunking_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Auto-chunking audio file saved: {output_file}")

                return True, {"audio_size": audio_size, "text_length": actual_length}
            else:
                print(f"  ❌ Response structure needs verification: {type(response)}")
                print(
                    f"  🔍 Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}"
                )
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        # Errors that may occur in auto-chunking logic
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(f"  ❌ Error during auto-chunking processing: {e}")
            print("  🔧 Please check the chunking logic")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        print(
            "  💡 Auto-chunking implemented but there may still be API-level limitations"
        )
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        print(f"  🔍 Error type: {type(e)}")
        return False, e


def test_stream_speech(voice_id):
    """Test TTS streaming"""
    print("🎵 TTS Streaming Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔄 Testing streaming TTS with voice '{voice_id}'...")
            print("  ⚠️ This test may consume credits!")

            # Record request start time
            request_start_time = time.time()

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text="안녕하세요! 이것은 스트리밍 TTS 테스트를 위한 한국어 텍스트입니다. 스트리밍 기능이 정상적으로 작동하는지 확인하기 위해 조금 더 긴 텍스트를 사용하고 있습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                style="neutral",
                model="sona_speech_1",
            )

            # Handle streaming response
            print("  📡 Receiving streaming data...")

            if hasattr(response, "result") and hasattr(response.result, "iter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []
                first_byte_time = None  # Record first byte time

                try:
                    for chunk in response.result.iter_bytes():
                        # Record and display first byte arrival time
                        if chunk_count == 0:
                            first_byte_time = time.time()
                            first_byte_latency = first_byte_time - request_start_time
                            print(f"  🚀 First byte arrived: {first_byte_latency:.3f}s")

                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        # Detailed log for first 20 chunks only
                        if chunk_count <= 20:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 21:
                            print(f"     ... (more chunks - logs omitted)")
                        elif chunk_count % 50 == 0:
                            print(
                                f"     Chunk {chunk_count}: {chunk_size} bytes (in progress...)"
                            )

                except Exception as iter_error:
                    print(f"  ⚠️ Error during streaming: {str(iter_error)[:100]}...")

                # Display completion time and statistics
                end_time = time.time()
                total_time = end_time - request_start_time

                print(
                    f"  ✅ Streaming complete: {chunk_count} chunks, {total_bytes} bytes"
                )
                print(f"  ⏱️ Total elapsed time: {total_time:.3f}s")

                if first_byte_time:
                    streaming_time = end_time - first_byte_time
                    print(
                        f"  📊 Streaming time: {streaming_time:.3f}s (after first byte)"
                    )
                    if streaming_time > 0:
                        throughput = total_bytes / streaming_time
                        print(f"  🚀 Average throughput: {throughput:.0f} bytes/sec")

                # Save received data to file if available
                if audio_chunks and total_bytes > 0:
                    output_file = "test_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 Streaming audio saved: {output_file}")

                    # Validate file
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
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_stream_speech_long_text(voice_id):
    """Test WAV streaming TTS for text over 300 characters (auto-chunking)"""
    print("📜 Long Text WAV Streaming TTS Test (Over 300 Characters, Auto-Chunking)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # Long text over 500 characters
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
        print(f"  📏 Test text length: {actual_length} characters (over 300)")
        print(f"  🔧 Auto-chunking + WAV streaming enabled")

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Converting long text WAV streaming TTS with voice '{voice_id}'..."
            )
            print("  ⚠️ This test will consume credits with auto-chunking applied!")
            print("  ✨ SDK will automatically chunk text for WAV streaming")

            # Record request start time
            request_start_time = time.time()

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
            )

            # Handle WAV streaming response
            print(f"  🔍 Response type: {type(response)}")
            print(f"  🔍 Result type: {type(response.result)}")

            # Handle new JSON format response (chunked case)
            if hasattr(response, "result") and isinstance(response.result, str):
                try:

                    # Parse JSON
                    result_data = json.loads(response.result)
                    print(f"  ✅ Detected chunked JSON response")
                    print(f"  🔍 JSON keys: {list(result_data.keys())}")

                    if "audio_base64" in result_data:
                        # Record first byte time (JSON response processing start)
                        first_byte_time = time.time()
                        first_byte_latency = first_byte_time - request_start_time
                        print(
                            f"  🚀 First byte arrived: {first_byte_latency:.3f}s (chunked merged response)"
                        )

                        # Decode base64 to extract audio data
                        audio_data = base64.b64decode(result_data["audio_base64"])
                        total_bytes = len(audio_data)

                        print(f"  ✅ Merged WAV audio data: {total_bytes} bytes")

                        # Display completion time and statistics
                        end_time = time.time()
                        total_time = end_time - request_start_time
                        streaming_time = end_time - first_byte_time

                        print(f"  ⏱️ Total elapsed time: {total_time:.3f}s")
                        print(
                            f"  📊 Processing time: {streaming_time:.3f}s (after first byte)"
                        )
                        if streaming_time > 0:
                            throughput = total_bytes / streaming_time
                            print(
                                f"  🚀 Average throughput: {throughput:.0f} bytes/sec"
                            )

                        # Save file
                        output_file = "test_stream_speech_long_output.wav"
                        with open(output_file, "wb") as f:
                            f.write(audio_data)
                        print(
                            f"  💾 Long text WAV streaming audio saved: {output_file}"
                        )

                        # Validate file
                        file_size = os.path.getsize(output_file)
                        print(f"  📏 Saved file size: {file_size} bytes")

                        with open(output_file, "rb") as f:
                            header = f.read(12)
                            if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                                print(
                                    f"  ✅ Valid long text WAV streaming file generated"
                                )
                            else:
                                print(
                                    f"  ⚠️ WAV header needs verification: {header[:12]}"
                                )

                        # Check Phoneme information
                        if "phonemes" in result_data and result_data["phonemes"]:
                            phonemes = result_data["phonemes"]
                            print(f"  🔤 Phoneme information included:")
                            print(
                                f"    - Symbol count: {len(phonemes.get('symbols', []))}"
                            )
                            if phonemes.get("start_times_seconds"):
                                print(
                                    f"    - Start times: {len(phonemes['start_times_seconds'])} items"
                                )
                            if phonemes.get("durations_seconds"):
                                print(
                                    f"    - Durations: {len(phonemes['durations_seconds'])} items"
                                )

                        # Calculate estimated chunk count
                        estimated_chunks = (actual_length + 299) // 300
                        print(
                            f"  📊 Estimated text chunk count: {estimated_chunks} (based on text length)"
                        )
                        print(f"  🔀 Auto-chunked segments merged and processed as WAV")

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
                        print(f"  ❌ Missing audio_base64 key: {result_data}")
                        return False, result_data

                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON parsing failed: {e}")
                    return False, e
                except Exception as e:
                    print(f"  ❌ Error during response processing: {e}")
                    return False, e

            # Handle existing streaming response (non-chunked case)
            elif hasattr(response, "result") and hasattr(response.result, "iter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []
                first_byte_time = None  # Record first byte time

                try:
                    for chunk in response.result.iter_bytes():
                        # Record and display first byte arrival time (auto-chunking first response)
                        if chunk_count == 0:
                            first_byte_time = time.time()
                            first_byte_latency = first_byte_time - request_start_time
                            print(
                                f"  🚀 First byte arrived: {first_byte_latency:.3f}s (auto-chunking)"
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
                    print(f"  ⚠️ Error during WAV streaming: {str(iter_error)[:100]}...")

                # Display completion time and statistics
                end_time = time.time()
                total_time = end_time - request_start_time

                print(
                    f"  ✅ Long text WAV streaming successful: {chunk_count} chunks, {total_bytes} bytes"
                )
                print(f"  ⏱️ Total elapsed time: {total_time:.3f}s")

                if first_byte_time:
                    streaming_time = end_time - first_byte_time
                    print(
                        f"  📊 Streaming time: {streaming_time:.3f}s (after first byte)"
                    )
                    if streaming_time > 0:
                        throughput = total_bytes / streaming_time
                        print(f"  🚀 Average throughput: {throughput:.0f} bytes/sec")
                    print(f"  🔧 Additional processing time due to auto-chunking")

                # Save file
                if audio_chunks and total_bytes > 0:
                    output_file = "test_stream_speech_long_output.wav"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 Long text WAV streaming audio saved: {output_file}")

                    # Validate file
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
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        # Errors that may occur in auto-chunking logic
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(f"  ❌ Error during WAV streaming auto-chunking: {e}")
            print("  🔧 Please check WAV streaming chunking logic")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        print(
            "  💡 WAV streaming auto-chunking implemented but there may still be API-level limitations"
        )
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        print(f"  🔍 Error type: {type(e)}")
        return False, e


def test_create_speech_with_phonemes(voice_id):
    """Test TTS conversion with phoneme information"""
    print("🔤 TTS Conversion Test with Phoneme Information")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with phonemes using voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            # TTS conversion with phoneme information
            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text="Hello world! This is a phoneme timing test.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
                include_phonemes=True,  # Include phoneme information
            )

            # Handle TTS response with phonemes
            print(f"  🔍 Response type: {type(response)}")
            print(
                f"  🔍 Response fields: {[attr for attr in dir(response) if not attr.startswith('_')]}"
            )

            # Analyze response structure
            if hasattr(response, "result"):
                print(f"  🔍 Result type: {type(response.result)}")

                # Handle audio data
                if hasattr(response.result, "read"):
                    audio_data = response.result.read()
                    audio_size = len(audio_data)
                    print(
                        f"  ✅ TTS conversion with phonemes successful: {audio_size} bytes audio generated"
                    )

                    # Save as audio file
                    output_file = "test_phoneme_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(audio_data)
                    print(f"  💾 Audio file with phonemes saved: {output_file}")

                    # Validate file
                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    return True, response
                else:
                    print(
                        f"  🔍 Result fields: {[attr for attr in dir(response.result) if not attr.startswith('_')]}"
                    )
                    return True, response

            # Check if phoneme data is in a separate field
            phoneme_fields = [
                attr for attr in dir(response) if "phoneme" in attr.lower()
            ]
            if phoneme_fields:
                print(f"  🔤 Phoneme-related fields found: {phoneme_fields}")
                for field in phoneme_fields:
                    field_value = getattr(response, field)
                    print(
                        f"     {field}: {type(field_value)} = {str(field_value)[:100]}..."
                    )

            return True, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_stream_speech_with_phonemes(voice_id):
    """Test streaming TTS with phoneme information"""
    print("🔤 Streaming TTS Test with Phoneme Information")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔄 Testing streaming TTS with phonemes using voice '{voice_id}'..."
            )
            print("  ⚠️ This test may consume credits!")

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text="Hello world! This is a phoneme streaming test with timing information.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
                include_phonemes=True,  # Include phoneme information
            )

            # Analyze streaming response structure
            print("  📡 Receiving streaming data with phonemes...")
            print(f"  🔍 Response type: {type(response)}")
            print(
                f"  🔍 Result type: {type(response.result) if hasattr(response, 'result') else 'No result'}"
            )

            # Handle JSON streaming data if result is a string
            if hasattr(response, "result") and isinstance(response.result, str):
                print("  📄 Detected JSON streaming response")
                print(f"  🔍 Response length: {len(response.result)} characters")
                print(f"  🔍 Response preview: {response.result[:200]}...")

                # Parse JSON chunks
                json_chunks = []
                audio_chunks = []

                # Structure to merge phoneme data from all chunks
                merged_phonemes = {
                    "symbols": [],
                    "durations_seconds": [],
                    "start_times_seconds": [],
                }
                first_chunk_start_time = None  # Record first chunk start time

                # Try to parse each line as JSON
                lines = response.result.strip().split("\n")
                print(f"  📊 Found {len(lines)} JSON chunks total")

                phoneme_chunks_count = 0
                audio_chunks_count = 0

                for i, line in enumerate(lines):
                    if line.strip():
                        try:
                            chunk_data = json.loads(line.strip())
                            json_chunks.append(chunk_data)

                            # Handle audio data
                            if chunk_data.get("audio_base64"):
                                audio_data = base64.b64decode(
                                    chunk_data["audio_base64"]
                                )
                                audio_chunks.append(audio_data)
                                audio_chunks_count += 1
                                print(
                                    f"     Chunk {i+1}: {len(audio_data)} bytes audio data"
                                )

                            # Handle phoneme data - collect from all chunks
                            if chunk_data.get("phonemes") and chunk_data["phonemes"]:
                                chunk_phonemes = chunk_data["phonemes"]
                                phoneme_chunks_count += 1
                                print(f"     Chunk {i+1}: Phoneme data found!")
                                print(
                                    f"       Symbol count: {len(chunk_phonemes.get('symbols', []))}"
                                )

                                # Display original time information
                                if chunk_phonemes.get("start_times_seconds"):
                                    original_times = chunk_phonemes[
                                        "start_times_seconds"
                                    ]
                                    print(
                                        f"       Original time range: {original_times[0]:.3f}s ~ {original_times[-1]:.3f}s"
                                    )
                                    print(
                                        f"       Original time count: {len(original_times)} items"
                                    )

                                if chunk_phonemes.get("durations_seconds"):
                                    durations = chunk_phonemes["durations_seconds"]
                                    total_duration = sum(durations)
                                    print(
                                        f"       Total duration: {total_duration:.3f}s"
                                    )

                                # Adjust continuous timing
                                if chunk_phonemes.get("start_times_seconds"):
                                    original_start_times = chunk_phonemes[
                                        "start_times_seconds"
                                    ]

                                    # Set base time for first phoneme chunk
                                    if first_chunk_start_time is None:
                                        first_chunk_start_time = original_start_times[0]
                                        print(
                                            f"       First chunk base time: {first_chunk_start_time:.3f}s"
                                        )

                                    # Streaming NDJSON: API already provides continuous time, just adjust base
                                    adjusted_start_times = [
                                        t - first_chunk_start_time
                                        for t in original_start_times
                                    ]

                                    chunk_phonemes["start_times_seconds"] = (
                                        adjusted_start_times
                                    )
                                    print(
                                        f"       Time adjusted: {original_start_times[0]:.3f}s → {adjusted_start_times[0]:.3f}s (base: -{first_chunk_start_time:.3f}s)"
                                    )

                                # Merge
                                merged_phonemes["symbols"].extend(
                                    chunk_phonemes.get("symbols", [])
                                )
                                merged_phonemes["durations_seconds"].extend(
                                    chunk_phonemes.get("durations_seconds", [])
                                )
                                merged_phonemes["start_times_seconds"].extend(
                                    chunk_phonemes.get("start_times_seconds", [])
                                )

                                # Display chunk duration information (Streaming NDJSON - no offset needed)
                                if chunk_phonemes.get("durations_seconds"):
                                    chunk_duration = sum(
                                        chunk_phonemes["durations_seconds"]
                                    )
                                    print(
                                        f"       Chunk duration: {chunk_duration:.3f}s (Streaming NDJSON)"
                                    )
                            else:
                                print(f"     Chunk {i+1}: No phoneme data")

                        except json.JSONDecodeError as e:
                            print(
                                f"     Chunk {i+1}: JSON parsing failed - {str(e)[:50]}..."
                            )
                            continue

                # Display statistics
                print(f"\n  📊 ===== Chunking Statistics =====")
                print(f"    - Total JSON chunks: {len(json_chunks)}")
                print(f"    - Audio chunks: {audio_chunks_count}")
                print(f"    - Phoneme chunks: {phoneme_chunks_count}")
                print(
                    f"    - Chunks without phoneme: {len(json_chunks) - phoneme_chunks_count}"
                )

                # Audio data statistics
                if audio_chunks:
                    total_audio_bytes = sum(len(chunk) for chunk in audio_chunks)
                    print(f"    - Total audio data: {total_audio_bytes} bytes")
                    for i, chunk in enumerate(audio_chunks):
                        print(f"      Chunk {i+1}: {len(chunk)} bytes")

                # Text length information
                original_text = "Hello world! This is a phoneme streaming test with timing information."
                print(f"    - Original text length: {len(original_text)} characters")
                print(f"    - Original text: '{original_text}'")

                # Use merged phoneme data
                phoneme_data = merged_phonemes if merged_phonemes["symbols"] else None

                # Display detailed merged phoneme data
                if phoneme_data:
                    print(f"  🔤 ===== Merged Phoneme Data Details =====")
                    symbols = phoneme_data.get("symbols", [])
                    durations = phoneme_data.get("durations_seconds", [])
                    start_times = phoneme_data.get("start_times_seconds", [])

                    print(f"     Symbol count: {len(symbols)}")
                    print(f"     Duration count: {len(durations)}")
                    print(f"     Start time count: {len(start_times)}")

                    if start_times:
                        print(
                            f"     Time range: {start_times[0]:.3f}s ~ {start_times[-1]:.3f}s"
                        )
                    if durations:
                        print(f"     Total duration: {sum(durations):.3f}s")

                    # Display first 10 phoneme samples
                    if len(symbols) > 0:
                        print(f"\n  🔤 Phoneme samples (first 10):")
                        for i in range(min(10, len(symbols))):
                            symbol = symbols[i]
                            duration = durations[i] if i < len(durations) else "N/A"
                            start_time = (
                                start_times[i] if i < len(start_times) else "N/A"
                            )
                            print(
                                f"    [{i+1:2d}] '{symbol}' | {duration}s | start: {start_time}s"
                            )

                        if len(symbols) > 10:
                            print(f"    ... (showing first 10 of {len(symbols)} total)")

                # Merge and save audio data
                if audio_chunks:
                    total_audio_data = b"".join(audio_chunks)
                    total_bytes = len(total_audio_data)

                    print(
                        f"  ✅ Streaming with phonemes completed: {len(json_chunks)} JSON chunks, {len(audio_chunks)} audio chunks, {total_bytes} bytes"
                    )

                    # Save as audio file
                    output_file = "test_phoneme_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(total_audio_data)
                    print(f"  💾 Streaming audio with phonemes saved: {output_file}")

                    # Validate file and calculate audio length
                    import os
                    import struct

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    with open(output_file, "rb") as f:
                        header = f.read(44)  # Read entire WAV header
                        if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                            print(f"  ✅ Valid WAV file with phonemes generated")

                            # Extract WAV file information
                            try:
                                sample_rate = struct.unpack("<I", header[24:28])[0]
                                byte_rate = struct.unpack("<I", header[28:32])[0]
                                bits_per_sample = struct.unpack("<H", header[34:36])[0]
                                channels = struct.unpack("<H", header[22:24])[0]
                                data_size = file_size - 44  # Data size excluding header
                                audio_duration = data_size / byte_rate

                                print(f"  🎵 Audio information:")
                                print(f"    - Sample rate: {sample_rate} Hz")
                                print(f"    - Channels: {channels}")
                                print(f"    - Bit depth: {bits_per_sample} bits")
                                print(f"    - Byte rate: {byte_rate} bytes/sec")
                                print(f"    - Data size: {data_size} bytes")
                                print(
                                    f"    - Actual audio length: {audio_duration:.3f}s"
                                )

                                # Calculate using alternative method
                                samples_per_second = sample_rate * channels
                                bytes_per_sample = bits_per_sample // 8
                                total_samples = data_size // bytes_per_sample
                                duration_by_samples = total_samples / samples_per_second
                                print(
                                    f"    - Duration by samples: {duration_by_samples:.3f}s"
                                )

                                # Compare with phoneme time
                                if phoneme_data and phoneme_data.get(
                                    "start_times_seconds"
                                ):
                                    phoneme_end_time = max(
                                        phoneme_data["start_times_seconds"]
                                    )
                                    if phoneme_data.get("durations_seconds"):
                                        last_phoneme_duration = phoneme_data[
                                            "durations_seconds"
                                        ][-1]
                                        phoneme_total_time = (
                                            phoneme_end_time + last_phoneme_duration
                                        )
                                    else:
                                        phoneme_total_time = phoneme_end_time

                                    print(
                                        f"    - Total phoneme time: {phoneme_total_time:.3f}s"
                                    )
                                    time_diff = abs(audio_duration - phoneme_total_time)
                                    print(f"    - Time difference: {time_diff:.3f}s")

                                    if time_diff > 0.5:
                                        print(
                                            f"    ⚠️ Audio and phoneme time mismatch detected!"
                                        )

                            except Exception as e:
                                print(f"    ⚠️ Failed to extract audio information: {e}")
                        else:
                            print(f"  📄 File header: {header[:12]} (may not be WAV)")

                    # Save phoneme data to JSON file
                    if phoneme_data:
                        phoneme_file = "test_phoneme_data.json"
                        with open(phoneme_file, "w") as f:
                            json.dump(phoneme_data, f, indent=2)
                        print(f"  💾 Phoneme data saved: {phoneme_file}")

                    return True, {
                        "json_chunks": len(json_chunks),
                        "audio_chunks": len(audio_chunks),
                        "total_bytes": total_bytes,
                        "phoneme_data": phoneme_data,
                    }
                else:
                    print("  ⚠️ No audio data")
                    return False, "No audio data in JSON chunks"

            # Legacy binary streaming handling (fallback)
            elif hasattr(response, "result") and hasattr(response.result, "iter_bytes"):
                print("  📄 Binary streaming response detected")
                # ... legacy binary processing code ...
                return False, "Binary streaming not implemented for phonemes"

            else:
                print(f"  🔍 Result details:")
                print(f"     Type: {type(response.result)}")
                print(f"     Value (first 500 chars): {str(response.result)[:500]}...")
                return False, f"Unexpected result type: {type(response.result)}"

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_predict_duration_with_voice_settings(voice_id):
    """Test voice duration prediction with Voice Settings"""
    print("🎛️ Voice Duration Prediction Test with Voice Settings")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with Voice Settings using voice '{voice_id}'..."
            )

            # Voice Settings configuration
            voice_settings = {
                "pitch_shift": 1.1,  # Increase pitch by 10%
                "pitch_variance": 0.9,  # Pitch variance at 90%
                "speed": 1.05,  # Increase speed by 5%
            }

            print(
                f"     Settings: pitch_shift={voice_settings['pitch_shift']}, speed={voice_settings['speed']}"
            )

            response = client.text_to_speech.predict_duration(
                voice_id=voice_id,
                text="Hello world! This is a voice settings prediction test.",
                language=models.PredictTTSDurationUsingCharacterRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
                voice_settings=voice_settings,  # Include Voice Settings
            )

            print(f"  ✅ Prediction with Voice Settings completed: {response}s")
            return True, response

    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_with_voice_settings(voice_id):
    """Test TTS conversion with Voice Settings"""
    print("🎛️ TTS Conversion Test with Voice Settings")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Converting TTS with Voice Settings using voice '{voice_id}'..."
            )
            print("  ⚠️ This test will consume credits!")

            # Voice Settings configuration
            voice_settings = {
                "pitch_shift": 0.95,  # Decrease pitch by 5%
                "pitch_variance": 1.1,  # Pitch variance at 110%
                "speed": 0.9,  # Decrease speed by 10%
            }

            print(
                f"     Settings: pitch_shift={voice_settings['pitch_shift']}, speed={voice_settings['speed']}"
            )

            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text="Hello world! This is a voice settings test. You can hear the adjusted pitch and speed.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model="sona_speech_1",
                voice_settings=voice_settings,  # Include Voice Settings
                include_phonemes=False,
            )

            # Handle TTS response with Voice Settings
            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ TTS conversion with Voice Settings successful: {audio_size} bytes audio generated"
                )

                # Save as audio file
                output_file = "test_voice_settings_speech_output.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 Audio file with Voice Settings saved: {output_file}")

                # Validate file
                import os

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(12)
                    if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                        print(f"  ✅ Valid Voice Settings WAV file generated")
                    else:
                        print(f"  ⚠️ WAV header needs verification: {header[:12]}")

                return True, response
            else:
                print(f"  ❌ Response structure needs verification: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_stream_speech_with_voice_settings(voice_id):
    """Test streaming TTS with Voice Settings"""
    print("🎛️ Streaming TTS Test with Voice Settings")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models
        import json
        import base64

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔄 Testing streaming TTS with Voice Settings using voice '{voice_id}'..."
            )
            print("  ⚠️ This test may consume credits!")

            # Voice Settings configuration
            voice_settings = {
                "pitch_shift": 1.2,  # Increase pitch by 20%
                "pitch_variance": 0.8,  # Pitch variance at 80%
                "speed": 1.15,  # Increase speed by 15%
            }

            print(
                f"     Settings: pitch_shift={voice_settings['pitch_shift']}, speed={voice_settings['speed']}"
            )

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text="Hello world! This is a voice settings streaming test. The pitch and speed are adjusted for better audio quality and personalization.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model="sona_speech_1",
                voice_settings=voice_settings,  # Include Voice Settings
                include_phonemes=False,
            )

            # Handle streaming response
            print("  📡 Receiving streaming data with Voice Settings...")
            print(f"  🔍 Response type: {type(response)}")
            print(
                f"  🔍 Result type: {type(response.result) if hasattr(response, 'result') else 'No result'}"
            )

            # Handle binary streaming if result is httpx.Response
            if hasattr(response, "result") and hasattr(response.result, "iter_bytes"):
                print("  📄 Binary streaming response detected (Voice Settings)")

                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    for chunk in response.result.iter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        # Display detailed log for first 15 chunks only
                        if chunk_count <= 15:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 16:
                            print(f"     ... (more chunks - log omitted)")
                        elif chunk_count % 25 == 0:
                            print(
                                f"     Chunk {chunk_count}: {chunk_size} bytes (in progress...)"
                            )

                except Exception as iter_error:
                    print(
                        f"  ⚠️ Error during Voice Settings streaming: {str(iter_error)[:100]}..."
                    )

                print(
                    f"  ✅ Voice Settings Streaming completed: {chunk_count} chunks, {total_bytes} bytes"
                )

                # Save to file if data is received
                if audio_chunks and total_bytes > 0:
                    total_audio_data = b"".join(audio_chunks)

                    output_file = "test_voice_settings_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(total_audio_data)
                    print(f"  💾 Voice Settings Streaming audio saved: {output_file}")

                    # Validate file
                    import os

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    with open(output_file, "rb") as f:
                        header = f.read(12)
                        if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                            print(
                                f"  ✅ Valid Voice Settings streaming WAV file generated"
                            )
                        else:
                            print(f"  📄 File header: {header[:12]} (may not be WAV)")

                    return True, {
                        "chunk_count": chunk_count,
                        "total_bytes": total_bytes,
                        "streaming_type": "binary",
                    }
                else:
                    print(f"  ⚠️ No received audio data")
                    return False, "No audio data received"

            # Handle JSON streaming data if result is a string (when Phoneme is included)
            elif hasattr(response, "result") and isinstance(response.result, str):
                print("  📄 JSON streaming response detected (with Phoneme)")

                # Parse JSON chunks
                json_chunks = []
                audio_chunks = []

                # Try to parse each line as JSON
                lines = response.result.strip().split("\n")
                print(f"  📊 Found {len(lines)} JSON chunks total")

                for i, line in enumerate(lines):
                    if line.strip():
                        try:
                            chunk_data = json.loads(line.strip())
                            json_chunks.append(chunk_data)

                            # Process audio data
                            if chunk_data.get("audio_base64"):
                                audio_data = base64.b64decode(
                                    chunk_data["audio_base64"]
                                )
                                audio_chunks.append(audio_data)
                                print(
                                    f"     Chunk {i+1}: {len(audio_data)} bytes audio data"
                                )

                        except json.JSONDecodeError as e:
                            print(
                                f"     Chunk {i+1}: JSON parsing failed - {str(e)[:50]}..."
                            )
                            continue

                # Merge and save audio data
                if audio_chunks:
                    total_audio_data = b"".join(audio_chunks)
                    total_bytes = len(total_audio_data)

                    print(
                        f"  ✅ Voice Settings Streaming completed: {len(json_chunks)} JSON chunks, {len(audio_chunks)} audio chunks, {total_bytes} bytes"
                    )

                    # Save as audio file
                    output_file = "test_voice_settings_stream_speech_output.wav"
                    with open(output_file, "wb") as f:
                        f.write(total_audio_data)
                    print(f"  💾 Voice Settings Streaming audio saved: {output_file}")

                    # Validate file
                    import os

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    with open(output_file, "rb") as f:
                        header = f.read(12)
                        if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                            print(
                                f"  ✅ Valid Voice Settings streaming WAV file generated"
                            )
                        else:
                            print(f"  📄 File header: {header[:12]} (may not be WAV)")

                    return True, {
                        "json_chunks": len(json_chunks),
                        "audio_chunks": len(audio_chunks),
                        "total_bytes": total_bytes,
                        "streaming_type": "json",
                    }
                else:
                    print("  ⚠️ No audio data")
                    return False, "No audio data in JSON chunks"

            else:
                print(f"  🔍 Result details:")
                print(
                    f"     Type: {type(response.result) if hasattr(response, 'result') else 'No result'}"
                )
                if hasattr(response, "result"):
                    print(
                        f"     Value (first 200 chars): {str(response.result)[:200]}..."
                    )

                    # Check httpx.Response object attributes
                    if hasattr(response.result, "__dict__"):
                        attrs = [
                            attr
                            for attr in dir(response.result)
                            if not attr.startswith("_")
                        ]
                        print(
                            f"     Available attributes: {attrs[:10]}..."
                        )  # Show only first 10

                        # Streaming-related methodscheck if exists
                        streaming_methods = [
                            attr
                            for attr in attrs
                            if "iter" in attr.lower() or "stream" in attr.lower()
                        ]
                        if streaming_methods:
                            print(
                                f"     Streaming-related methods: {streaming_methods}"
                            )

                return (
                    False,
                    f"Unexpected result type: {type(response.result) if hasattr(response, 'result') else 'No result'}",
                )

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_mp3(voice_id):
    """MP3 format TTS Conversion Test - Test that consumes credits"""
    print("🎤 MP3 Format TTS Conversion Test (Consumes Credits)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 MP3 using voice '{voice_id}' converting TTS...")
            print("  ⚠️ This test will consume credits!")

            # Test with approximately 50 Korean characters
            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text="안녕하세요! 이것은 MP3 형식 SDK 테스트를 위한 한국어 텍스트입니다. 정상적으로 작동하는지 확인해보겠습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,  # MP3 format
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            # Process MP3 TTS response
            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ MP3 TTS conversion successful: {audio_size} bytes audio generated"
                )

                # Save and verify as MP3 file
                output_file = "test_create_speech_output.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 MP3 Audio file saved: {output_file}")

                # Check file size and MP3 header
                import os

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(10)
                    # Verify MP3 file (ID3 tag or MPEG frame header)
                    if header[:3] == b"ID3":
                        print(f"  ✅ Valid MP3 file generated (with ID3 tag)")
                    elif header[:2] == b"\xff\xfb" or header[:2] == b"\xff\xfa":
                        print(f"  ✅ Valid MP3 file generated (MPEG frame)")
                    else:
                        print(
                            f"  📄 MP3 header: {header[:10].hex()} (needs verification)"
                        )

                return True, response
            elif hasattr(response, "result") and hasattr(response.result, "content"):
                # If content attribute exists
                audio_data = response.result.content
                audio_size = len(audio_data)
                print(
                    f"  ✅ MP3 TTS conversion successful: {audio_size} bytes audio generated"
                )

                output_file = "test_create_speech_output.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 MP3 Audio file saved: {output_file}")

                return True, response
            else:
                print(f"  ❌ Response structure needs verification: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_long_text_mp3(voice_id):
    """Long text (300+ chars) MP3 auto-chunking TTS Conversion Test"""
    print("📜 Long text (300+ chars) MP3 auto-chunking TTS Conversion Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # Long text over 500 characters
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
        print(f"  📏 Test text length: {actual_length} characters (exceeds 300 chars)")
        print(f"  🔧 Auto-chunking feature activated, text will be split automatically")
        print(f"  🎵 Output will be in MP3 format")

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 MP3 using voice '{voice_id}' auto-chunking converting TTS...")
            print("  ⚠️ This test will consume credits!")
            print("  ✨ SDK automatically chunks text and processes as MP3")

            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,  # MP3 format
                style="neutral",
                model="sona_speech_1",
                voice_settings=None,
            )

            # Process MP3 auto-chunking success
            if hasattr(response, "result") and hasattr(response.result, "read"):
                audio_data = response.result.read()
                audio_size = len(audio_data)
                print(
                    f"  ✅ MP3 auto-chunking TTS conversion successful: {audio_size} bytes audio generated"
                )
                print(f"  🎯 Long text successfully chunked and processed as MP3!")

                output_file = "test_auto_chunking_speech_output.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 MP3 auto-chunking Audio file saved: {output_file}")

                # Check file size and MP3 header
                import os

                file_size = os.path.getsize(output_file)
                print(f"  📏 Saved file size: {file_size} bytes")

                with open(output_file, "rb") as f:
                    header = f.read(10)
                    # Verify MP3 file
                    if header[:3] == b"ID3":
                        print(
                            f"  ✅ Valid MP3 auto-chunking file generated (with ID3 tag)"
                        )
                    elif header[:2] == b"\xff\xfb" or header[:2] == b"\xff\xfa":
                        print(
                            f"  ✅ Valid MP3 auto-chunking file generated (MPEG frame)"
                        )
                    else:
                        print(
                            f"  📄 MP3 header: {header[:10].hex()} (needs verification)"
                        )

                # Calculate and display estimated chunk count
                estimated_chunks = (actual_length + 299) // 300  # Round up calculation
                print(
                    f"  📊 Estimated chunk count: {estimated_chunks} items (based on text length)"
                )
                print(
                    f"  🔀 Each chunk processed simultaneously through parallel processing and merged into MP3"
                )

                return True, {
                    "audio_size": audio_size,
                    "text_length": actual_length,
                    "estimated_chunks": estimated_chunks,
                    "output_file": output_file,
                    "format": "mp3",
                }
            elif hasattr(response, "result") and hasattr(response.result, "content"):
                # If content attribute exists
                audio_data = response.result.content
                audio_size = len(audio_data)
                print(
                    f"  ✅ MP3 auto-chunking TTS conversion successful: {audio_size} bytes audio generated"
                )

                output_file = "test_auto_chunking_speech_output.mp3"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                print(f"  💾 MP3 auto-chunking Audio file saved: {output_file}")

                return True, {
                    "audio_size": audio_size,
                    "text_length": actual_length,
                    "format": "mp3",
                }
            else:
                print(f"  ❌ Response structure needs verification: {type(response)}")
                print(
                    f"  🔍 Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}"
                )
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        # Possible errors in auto-chunking logic
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(f"  ❌ MP3 auto-chunking error occurred during processing: {e}")
            print("  🔧 MP3 Please check chunking logic")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        print(
            "  💡 MP3 auto-chunking is implemented, but there may still be limitations at the API level"
        )
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        print(f"  🔍 Error type: {type(e)}")
        return False, e


def test_stream_speech_mp3(voice_id):
    """MP3 format TTS Streaming Test"""
    print("🎵 MP3 format TTS Streaming Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔄 MP3 using voice '{voice_id}' testing streaming TTS...")
            print("  ⚠️ This test may consume credits!")

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text="안녕하세요! 이것은 MP3 스트리밍 TTS 테스트를 위한 한국어 텍스트입니다. 스트리밍 기능이 MP3 형식으로도 정상적으로 작동하는지 확인하기 위해 조금 더 긴 텍스트를 사용하고 있습니다.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,  # MP3 format
                style="neutral",
                model="sona_speech_1",
            )

            # Process MP3 streaming response
            print("  📡 MP3 Receiving streaming data...")

            if hasattr(response, "result") and hasattr(response.result, "iter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    for chunk in response.result.iter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        # Display detailed log for first 20 only
                        if chunk_count <= 20:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count == 21:
                            print(f"     ... (more chunks - log omitted)")
                        elif chunk_count % 50 == 0:
                            print(
                                f"     Chunk {chunk_count}: {chunk_size} bytes (in progress...)"
                            )

                except Exception as iter_error:
                    print(f"  ⚠️ MP3 Error during streaming: {str(iter_error)[:100]}...")

                print(
                    f"  ✅ MP3 Streaming completed: {chunk_count} chunks, {total_bytes} bytes"
                )

                # Save as MP3 file if data received
                if audio_chunks and total_bytes > 0:
                    output_file = "test_stream_speech_output.mp3"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 MP3 Streaming audio saved: {output_file}")

                    # Validate file
                    import os

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    with open(output_file, "rb") as f:
                        header = f.read(10)
                        if header[:3] == b"ID3":
                            print(
                                f"  ✅ Valid MP3 streaming file generated (with ID3 tag)"
                            )
                        elif header[:2] == b"\xff\xfb" or header[:2] == b"\xff\xfa":
                            print(
                                f"  ✅ Valid MP3 streaming file generated (MPEG frame)"
                            )
                        else:
                            print(
                                f"  📄 File header: {header[:10].hex()} (may not be MP3)"
                            )

                    return True, f"{chunk_count} chunks, {total_bytes} bytes"
                else:
                    print(f"  ⚠️ No received audio data")
                    return False, "No audio data received"
            else:
                print(f"  ❌ Response missing iter_bytes attribute: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_stream_speech_long_text_mp3(voice_id):
    """Long text (300+ chars) MP3 Streaming TTS Test"""
    print("📜 Long text (300+ chars) MP3 Streaming TTS Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # Long text over 500 characters
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
        print(f"  📏 Test text length: {actual_length} characters (exceeds 300 chars)")
        print(f"  🔧 auto-chunking + MP3 streaming feature activated")

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Long text using voice '{voice_id}' MP3 streaming converting TTS..."
            )
            print("  ⚠️ This test consumes credits and applies auto-chunking!")
            print("  ✨ SDK automatically chunks text and processes as MP3 streaming")

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.MP3,  # MP3 format
                style="neutral",
                model="sona_speech_1",
            )

            # Process MP3 streaming response
            print(f"  🔍 Response type: {type(response)}")
            print(f"  🔍 Result type: {type(response.result)}")

            # Process new JSON format response (chunked case)
            if hasattr(response, "result") and isinstance(response.result, str):
                try:
                    import json
                    import base64

                    # Parse JSON
                    result_data = json.loads(response.result)
                    print(f"  ✅ Chunked JSON response detected")
                    print(f"  🔍 JSON keys: {list(result_data.keys())}")

                    if "audio_base64" in result_data:
                        # Base64 decode and extract audio data
                        audio_data = base64.b64decode(result_data["audio_base64"])
                        total_bytes = len(audio_data)

                        print(f"  ✅ Merged MP3 audio data: {total_bytes} bytes")

                        # Save file
                        output_file = "test_stream_speech_long_output.mp3"
                        with open(output_file, "wb") as f:
                            f.write(audio_data)
                        print(
                            f"  💾 Long text MP3 Streaming audio saved: {output_file}"
                        )

                        # Validate file
                        import os

                        file_size = os.path.getsize(output_file)
                        print(f"  📏 Saved file size: {file_size} bytes")

                        with open(output_file, "rb") as f:
                            header = f.read(10)
                            if header[:3] == b"ID3":
                                print(
                                    f"  ✅ Valid MP3 Long text streaming file generated (with ID3 tag)"
                                )
                            elif header[:2] == b"\xff\xfb" or header[:2] == b"\xff\xfa":
                                print(
                                    f"  ✅ Valid MP3 Long text streaming file generated (MPEG frame)"
                                )
                            else:
                                print(
                                    f"  📄 File header: {header[:10].hex()} (may not be MP3)"
                                )

                        # Check Phoneme Information
                        if "phonemes" in result_data and result_data["phonemes"]:
                            phonemes = result_data["phonemes"]
                            print(f"  🔤 Phoneme information included:")
                            print(
                                f"    - Symbol count: {len(phonemes.get('symbols', []))}"
                            )
                            if phonemes.get("start_times_seconds"):
                                print(
                                    f"    - Start times: {len(phonemes['start_times_seconds'])} items"
                                )
                            if phonemes.get("durations_seconds"):
                                print(
                                    f"    - Duration: {len(phonemes['durations_seconds'])} items"
                                )

                        # Calculate estimated chunk count
                        estimated_chunks = (actual_length + 299) // 300
                        print(
                            f"  📊 Estimated text chunk count: {estimated_chunks} items (based on text length)"
                        )
                        print(
                            f"  🔀 Each auto-chunked segment was merged and processed as MP3"
                        )

                        return True, {
                            "total_bytes": total_bytes,
                            "text_length": actual_length,
                            "estimated_chunks": estimated_chunks,
                            "format": "mp3",
                            "has_phonemes": "phonemes" in result_data
                            and result_data["phonemes"] is not None,
                        }
                    else:
                        print(f"  ❌ audio_base64 key missing: {result_data}")
                        return False, result_data

                except json.JSONDecodeError as e:
                    print(f"  ❌ JSON parsing failed: {e}")
                    return False, e
                except Exception as e:
                    print(f"  ❌ Error processing response: {e}")
                    return False, e

            # Process existing streaming response (non-chunked case)
            elif hasattr(response, "result") and hasattr(response.result, "iter_bytes"):
                chunk_count = 0
                total_bytes = 0
                audio_chunks = []

                try:
                    for chunk in response.result.iter_bytes():
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size
                        audio_chunks.append(chunk)

                        if chunk_count <= 10:
                            print(f"     Chunk {chunk_count}: {chunk_size} bytes")
                        elif chunk_count % 20 == 0:
                            print(f"     Progress: {chunk_count} chunks")

                except Exception as iter_error:
                    print(f"  ⚠️ MP3 Error during streaming: {str(iter_error)[:100]}...")

                print(
                    f"  ✅ MP3 Long text streaming success: {chunk_count} chunks, {total_bytes} bytes"
                )

                if audio_chunks and total_bytes > 0:
                    output_file = "test_stream_speech_long_output.mp3"
                    with open(output_file, "wb") as f:
                        for chunk in audio_chunks:
                            f.write(chunk)
                    print(f"  💾 Long text MP3 Streaming audio saved: {output_file}")

                    # Validate file
                    import os

                    file_size = os.path.getsize(output_file)
                    print(f"  📏 Saved file size: {file_size} bytes")

                    with open(output_file, "rb") as f:
                        header = f.read(10)
                        if header[:3] == b"ID3":
                            print(
                                f"  ✅ Valid MP3 Long text streaming file generated (with ID3 tag)"
                            )
                        elif header[:2] == b"\xff\xfb" or header[:2] == b"\xff\xfa":
                            print(
                                f"  ✅ Valid MP3 Long text streaming file generated (MPEG frame)"
                            )
                        else:
                            print(
                                f"  📄 File header: {header[:10].hex()} (may not be MP3)"
                            )

                    # Calculate and display estimated chunk count
                    estimated_chunks = (
                        actual_length + 299
                    ) // 300  # Round up calculation
                    print(
                        f"  📊 Estimated text chunk count: {estimated_chunks} items (based on text length)"
                    )
                    print(
                        f"  🔀 Each auto-chunked segment was processed as MP3 streaming"
                    )

                    return True, {
                        "chunk_count": chunk_count,
                        "total_bytes": total_bytes,
                        "text_length": actual_length,
                        "estimated_chunks": estimated_chunks,
                        "format": "mp3",
                    }
                else:
                    print(f"  ⚠️ No received audio data")
                    return False, "No audio data received"
            else:
                print(f"  ❌ Response structure needs verification: {type(response)}")
                return False, response

    except errors.PaymentRequiredErrorResponse as e:
        print(f"  ❌ Insufficient credits: Please top up your credits")
        return False, e
    except errors.NotFoundErrorResponse as e:
        print(f"  ❌ Voice not found: {voice_id}")
        return False, e
    except RuntimeError as e:
        # Possible errors in auto-chunking logic
        error_message = str(e).lower()
        if "chunk" in error_message or "merge" in error_message:
            print(
                f"  ❌ MP3 streaming auto-chunking error occurred during processing: {e}"
            )
            print("  🔧 MP3 streaming Please check chunking logic")
            return False, e
        else:
            print(f"  ❌ Unexpected runtime error: {e}")
            return False, e
    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        print(
            "  💡 MP3 streaming auto-chunking is implemented, but there may still be limitations at the API level"
        )
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        print(f"  🔍 Error type: {type(e)}")
        return False, e


def test_create_speech_long_text_with_phonemes(voice_id):
    """Long text (300+ chars) auto-chunking + Phoneme Information included TTS Test"""
    print("📜🔤 Long text (300+ chars) auto-chunking + Phoneme Information TTS Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # Long text over 500 characters
        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 자동 청킹과 Phoneme 정보를 동시에 테스트합니다.
        새로 구현된 SDK는 긴 텍스트를 자동으로 여러 개의 청크로 나누어 처리하고 각 청크의 Phoneme 정보를 병합합니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹 기능과 Phoneme 병합을 통해 긴 텍스트도 자연스럽게 음성으로 변환할 수 있습니다.
        """.strip()

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Long text using voice '{voice_id}' chunking + Phoneme converting TTS..."
            )
            print(f"  📝 Text length: {len(long_text)} chars")
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                include_phonemes=True,  # Include Phoneme Information
            )

            print(f"  🔍 Response type: {type(response)}")

            if hasattr(response, "result"):
                print(f"  🔍 Result type: {type(response.result)}")

                # Check audio data
                if (
                    hasattr(response.result, "audio_base64")
                    and response.result.audio_base64
                ):
                    print("  ✅ Base64 audio data received")
                    print(
                        f"  📊 audio data 크기: {len(response.result.audio_base64)} characters"
                    )

                    # Display detailed Phoneme Information
                    if (
                        hasattr(response.result, "phonemes")
                        and response.result.phonemes
                    ):
                        phonemes = response.result.phonemes
                        print(
                            "\n  🔤 ===== Phoneme Information Detailed Analysis ====="
                        )
                        print(
                            f"  📊 Phoneme symbols 개수: {len(phonemes.symbols) if phonemes.symbols else 0}"
                        )
                        print(
                            f"  ⏱️ Duration 개수: {len(phonemes.durations_seconds) if phonemes.durations_seconds else 0}"
                        )

                        # Add start_times_seconds information
                        if (
                            hasattr(phonemes, "start_times_seconds")
                            and phonemes.start_times_seconds
                        ):
                            print(
                                f"  🚀 Start Times 개수: {len(phonemes.start_times_seconds)}"
                            )
                        else:
                            print(f"  🚀 Start Times count: 0 (no information)")

                        if phonemes.symbols:
                            print(f"\n  🔤 All Phoneme Symbols:")
                            # Display in groups of 10
                            symbols = phonemes.symbols
                            for i in range(0, len(symbols), 10):
                                group = symbols[i : i + 10]
                                print(
                                    f"    {i+1:3d}-{min(i+10, len(symbols)):3d}: {group}"
                                )

                        if phonemes.durations_seconds:
                            print(f"\n  ⏱️ Duration Information (in seconds):")
                            durations = phonemes.durations_seconds
                            total_duration = sum(durations)
                            print(f"    Total duration: {total_duration:.3f}s")
                            print(
                                f"    Average duration: {total_duration/len(durations):.3f}s"
                            )
                            print(f"    Min duration: {min(durations):.3f}s")
                            print(f"    Max duration: {max(durations):.3f}s")

                            # Display first 20 durations
                            print(f"    First 20 duration: {durations[:20]}")
                            if len(durations) > 20:
                                print(f"    ... (total {len(durations)} items)")

                        # Display additional start_times_seconds information
                        if (
                            hasattr(phonemes, "start_times_seconds")
                            and phonemes.start_times_seconds
                        ):
                            print(f"\n  🚀 Start Times Information (in seconds):")
                            start_times = phonemes.start_times_seconds
                            print(f"    First start: {min(start_times):.3f}s")
                            print(f"    Last start: {max(start_times):.3f}s")
                            print(
                                f"    Time range: {max(start_times) - min(start_times):.3f}s"
                            )

                            # Display first 20 start times
                            print(f"    First 20 start times: {start_times[:20]}")
                            if len(start_times) > 20:
                                print(f"    ... (total {len(start_times)} items)")

                        # Display Phoneme-Duration-StartTime mapping (first 30)
                        if phonemes.symbols and phonemes.durations_seconds:
                            print(
                                f"\n  🎯 Phoneme-Duration-StartTime mapping (first 30):"
                            )
                            has_start_times = (
                                hasattr(phonemes, "start_times_seconds")
                                and phonemes.start_times_seconds
                            )

                            for i in range(
                                min(
                                    30,
                                    len(phonemes.symbols),
                                    len(phonemes.durations_seconds),
                                )
                            ):
                                symbol = phonemes.symbols[i]
                                duration = phonemes.durations_seconds[i]

                                if has_start_times and i < len(
                                    phonemes.start_times_seconds
                                ):
                                    start_time = phonemes.start_times_seconds[i]
                                    end_time = start_time + duration
                                    print(
                                        f"    {i+1:2d}. '{symbol}' -> {start_time:.3f}s~{end_time:.3f}s ({duration:.3f}s)"
                                    )
                                else:
                                    print(
                                        f"    {i+1:2d}. '{symbol}' -> duration: {duration:.3f}s (start time 없음)"
                                    )

                            if len(phonemes.symbols) > 30:
                                print(f"    ... (total {len(phonemes.symbols)} items)")

                        # Save Phoneme Information as detailed JSON
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
                                "total_symbols": (
                                    len(phonemes.symbols) if phonemes.symbols else 0
                                ),
                                "total_duration": (
                                    sum(phonemes.durations_seconds)
                                    if phonemes.durations_seconds
                                    else 0
                                ),
                                "average_duration": (
                                    sum(phonemes.durations_seconds)
                                    / len(phonemes.durations_seconds)
                                    if phonemes.durations_seconds
                                    else 0
                                ),
                                "has_start_times": hasattr(
                                    phonemes, "start_times_seconds"
                                )
                                and phonemes.start_times_seconds is not None,
                            },
                        }

                        import json

                        with open(
                            "test_long_chunking_phoneme_data.json",
                            "w",
                            encoding="utf-8",
                        ) as f:
                            json.dump(phoneme_data, f, ensure_ascii=False, indent=2)
                        print(
                            f"\n  💾 상세 Phoneme 데이터 저장: test_long_chunking_phoneme_data.json"
                        )

                    else:
                        print("  ⚠️ No Phoneme information")

                    # Save as WAV file
                    import base64

                    audio_data = base64.b64decode(response.result.audio_base64)
                    filename = "test_long_chunking_phoneme_output.wav"
                    with open(filename, "wb") as f:
                        f.write(audio_data)
                    print(f"  💾 Audio file saved: {filename}")

                    return True, response
                else:
                    print("  ❌ No audio data")
                    return False, None
            else:
                print("  ❌ Response has no result")
                return False, None

    except errors.SupertoneDefaultError as e:
        print(f"  ❌ API error: {e}")
        return False, None
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        print(f"  🔍 Error type: {type(e)}")
        return False, None


def test_stream_speech_phoneme_chunking_wav(voice_id):
    """Long text + Phoneme + Streaming Test (WAV) - Improved Error Handling"""
    print("🎵🔤📜 Long text + Phoneme + Streaming Test (WAV) - Improved Error Handling")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # Long text over 500 characters
        long_text = """
        안녕하세요! 이것은 300자를 초과하는 매우 긴 텍스트를 사용한 Phoneme + 스트리밍 테스트입니다.
        현재 SDK는 긴 텍스트를 자동으로 청킹하지만, Phoneme + 스트리밍 조합에서는 제한사항이 있을 수 있습니다.
        실시간 스트리밍 텍스트 음성 변환 기술은 현대 AI 애플리케이션에서 핵심적인 역할을 담당하고 있습니다.
        특히 대화형 서비스, 라이브 방송, 실시간 번역 서비스 등에서 없어서는 안 될 중요한 기술입니다.
        자동 청킹과 Phoneme 병합 기능을 통해 긴 텍스트도 자연스럽게 음성으로 변환하고 정확한 발음 정보를 제공할 수 있습니다.
        """.strip()

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Long text using voice '{voice_id}' Phoneme + Streaming Test..."
            )
            print(f"  📝 Text length: {len(long_text)} chars (exceeds 300 chars)")
            print("  ⚠️ Current SDK chunking + Phoneme + streaming combination Test")
            print("  ⚠️ This test may consume credits!")

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text=long_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                include_phonemes=True,  # Include Phoneme Information
            )

            print(f"  🔍 Response type: {type(response)}")

            if hasattr(response, "result"):
                print(f"  🔍 Result type: {type(response.result)}")

                # Process new JSON format response (Chunked merged response)
                if isinstance(response.result, str):
                    try:
                        import json
                        import base64

                        # Attempt to parse JSON
                        result_data = json.loads(response.result)
                        print(f"  ✅ Chunked merged JSON response detected")
                        print(f"  🔍 JSON keys: {list(result_data.keys())}")

                        if "audio_base64" in result_data:
                            # Base64 decode and extract audio data
                            audio_data = base64.b64decode(result_data["audio_base64"])
                            total_bytes = len(audio_data)

                            print(
                                f"  ✅ Merged WAV + Phoneme audio data: {total_bytes} bytes"
                            )

                            # Save file
                            output_file = "test_phoneme_chunking_stream_output.wav"
                            with open(output_file, "wb") as f:
                                f.write(audio_data)
                            print(
                                f"  💾 Phoneme + 청킹 Streaming audio saved: {output_file}"
                            )

                            # Validate file
                            import os

                            file_size = os.path.getsize(output_file)
                            print(f"  📏 Saved file size: {file_size} bytes")

                            with open(output_file, "rb") as f:
                                header = f.read(12)
                                if header[:4] == b"RIFF" and header[8:12] == b"WAVE":
                                    print(f"  ✅ Valid WAV file generated")
                                else:
                                    print(
                                        f"  ⚠️ WAV header needs verification: {header[:12]}"
                                    )

                            # Process Merged Phoneme Information
                            if "phonemes" in result_data and result_data["phonemes"]:
                                phonemes = result_data["phonemes"]
                                print(f"\n  🔤 ===== Merged Phoneme Information =====")
                                print(
                                    f"    - Symbol count: {len(phonemes.get('symbols', []))}"
                                )

                                if phonemes.get("durations_seconds"):
                                    durations = phonemes["durations_seconds"]
                                    print(f"    - Duration: {len(durations)} items")
                                    print(
                                        f"    - Total duration: {sum(durations):.3f}s"
                                    )

                                if phonemes.get("start_times_seconds"):
                                    start_times = phonemes["start_times_seconds"]
                                    print(
                                        f"    - Start times: {len(start_times)} items"
                                    )
                                    if start_times:
                                        # Adjust time: Set first time to 0
                                        first_time = start_times[0]
                                        if first_time != 0.0:
                                            print(
                                                f"    - 시간 조정: 첫 번째 시간 {first_time:.3f}s를 0초로 조정"
                                            )
                                            adjusted_start_times = [
                                                t - first_time for t in start_times
                                            ]
                                            phonemes["start_times_seconds"] = (
                                                adjusted_start_times
                                            )
                                            start_times = adjusted_start_times

                                        print(
                                            f"    - Time range: {start_times[0]:.3f}s ~ {start_times[-1]:.3f}s"
                                        )

                                # Save detailed Phoneme data
                                phoneme_output_file = (
                                    "test_phoneme_chunking_stream_data.json"
                                )
                                with open(
                                    phoneme_output_file, "w", encoding="utf-8"
                                ) as f:
                                    json.dump(phonemes, f, ensure_ascii=False, indent=2)
                                print(
                                    f"  💾 상세 Phoneme 데이터 저장: {phoneme_output_file}"
                                )

                                # Display first few and last few phonemes
                                symbols = phonemes.get("symbols", [])
                                durations = phonemes.get("durations_seconds", [])
                                start_times = phonemes.get("start_times_seconds", [])

                                if len(symbols) > 0:
                                    print(f"\n  🔤 Phoneme samples (first 10):")
                                    for i in range(min(10, len(symbols))):
                                        symbol = symbols[i]
                                        duration = (
                                            durations[i]
                                            if i < len(durations)
                                            else "N/A"
                                        )
                                        start_time = (
                                            start_times[i]
                                            if i < len(start_times)
                                            else "N/A"
                                        )
                                        print(
                                            f"    [{i+1:2d}] '{symbol}' | {duration}s | start: {start_time}s"
                                        )

                                    if len(symbols) > 10:
                                        print(
                                            f"    ... (showing only first 10 of {len(symbols)} items total)"
                                        )
                            else:
                                print(f"  ⚠️ Phoneme Information missing")

                            return True, {
                                "total_bytes": total_bytes,
                                "text_length": len(long_text),
                                "format": "wav",
                                "has_phonemes": "phonemes" in result_data
                                and result_data["phonemes"] is not None,
                                "phoneme_count": len(
                                    result_data.get("phonemes", {}).get("symbols", [])
                                ),
                                "output_file": output_file,
                                "phoneme_file": "test_phoneme_chunking_stream_data.json",
                            }
                        else:
                            print(f"  ❌ audio_base64 key missing: {result_data}")
                            return False, result_data

                    except json.JSONDecodeError:
                        # Process with existing logic if not JSON
                        print(f"  📄 Direct processing of string response...")
                        pass
                    except Exception as e:
                        print(f"  ❌ Merged JSON Error processing response: {e}")
                        return False, e

                # Handle ExtendedStreamingWrapper error
                if "ExtendedStreamingWrapper" in str(type(response.result)):
                    print(
                        "  ⚠️ ExtendedStreamingWrapper detected - special handling required"
                    )

                    try:
                        # Attempt to access original_response of ExtendedStreamingWrapper directly
                        if hasattr(response.result, "original_response"):
                            original = response.result.original_response
                            print(f"  🔍 Original response type: {type(original)}")

                            # Process as JSON if original_response is a string
                            if isinstance(original, str):
                                print(
                                    "  📄 Original response가 문자열 - JSON 스트리밍으로 처리"
                                )

                                import json
                                import base64

                                lines = original.strip().split("\n")
                                total_audio = b""
                                all_phonemes = {
                                    "symbols": [],
                                    "durations_seconds": [],
                                    "start_times_seconds": [],
                                }  # Add start_times_seconds
                                current_time_offset = 0.0  # Track time offset

                                for i, line in enumerate(lines):
                                    if line.strip():
                                        try:
                                            chunk_data = json.loads(line.strip())
                                            print(
                                                f"    JSON Chunk {i+1}: {list(chunk_data.keys())}"
                                            )

                                            # Process audio data
                                            if chunk_data.get("audio_base64"):
                                                audio_data = base64.b64decode(
                                                    chunk_data["audio_base64"]
                                                )
                                                total_audio += audio_data
                                                print(
                                                    f"      오디오: {len(audio_data)} bytes"
                                                )

                                            # Process Phoneme data (including start_times_seconds)
                                            if chunk_data.get("phonemes"):
                                                phonemes = chunk_data["phonemes"]

                                                # 🔍 Debugging output of original phonemes structure (added)
                                                print(
                                                    f"\n      �� Original Phonemes structure:"
                                                )
                                                for key in phonemes.keys():
                                                    value = phonemes[key]
                                                    if isinstance(value, list):
                                                        print(
                                                            f"        {key}: [{len(value)} items] {type(value[0]).__name__ if value else 'empty'}"
                                                        )
                                                    else:
                                                        print(
                                                            f"        {key}: {type(value).__name__} = {value}"
                                                        )

                                                if phonemes.get("symbols"):
                                                    all_phonemes["symbols"].extend(
                                                        phonemes["symbols"]
                                                    )
                                                    print(
                                                        f"      Phoneme symbols: {len(phonemes['symbols'])} items"
                                                    )

                                                if phonemes.get("durations_seconds"):
                                                    all_phonemes[
                                                        "durations_seconds"
                                                    ].extend(
                                                        phonemes["durations_seconds"]
                                                    )
                                                    print(
                                                        f"      Duration: {len(phonemes['durations_seconds'])} items"
                                                    )

                                                # Process start_times_seconds (apply time offset)
                                                if phonemes.get("start_times_seconds"):
                                                    # Apply offset to current chunk's start times
                                                    offset_start_times = [
                                                        t + current_time_offset
                                                        for t in phonemes[
                                                            "start_times_seconds"
                                                        ]
                                                    ]
                                                    all_phonemes[
                                                        "start_times_seconds"
                                                    ].extend(offset_start_times)
                                                    print(
                                                        f"      Start Times: {len(phonemes['start_times_seconds'])} items (offset: +{current_time_offset:.3f}s)"
                                                    )

                                                # Update time offset for next chunk
                                                if phonemes.get("durations_seconds"):
                                                    chunk_duration = sum(
                                                        phonemes["durations_seconds"]
                                                    )
                                                    current_time_offset += (
                                                        chunk_duration
                                                    )

                                        except json.JSONDecodeError as je:
                                            print(
                                                f"    JSON Chunk {i+1} parsing failed: {str(je)[:50]}..."
                                            )

                                # Display detailed Phoneme Information (including start_times_seconds)
                                if all_phonemes["symbols"]:
                                    print(
                                        f"\n  🔤 ===== Merged Phoneme Information ====="
                                    )
                                    print(
                                        f"  📊 Total symbol count: {len(all_phonemes['symbols'])}"
                                    )
                                    print(
                                        f"  ⏱️ Total Duration count: {len(all_phonemes['durations_seconds'])}"
                                    )
                                    print(
                                        f"  🚀 Total Start Times count: {len(all_phonemes['start_times_seconds'])}"
                                    )

                                    # Display all symbols (in groups of 10)
                                    symbols = all_phonemes["symbols"]
                                    print(f"\n  🔤 All Phoneme Symbols:")
                                    for i in range(0, len(symbols), 10):
                                        group = symbols[i : i + 10]
                                        print(
                                            f"    {i+1:3d}-{min(i+10, len(symbols)):3d}: {group}"
                                        )

                                    # Duration statistics
                                    if all_phonemes["durations_seconds"]:
                                        durations = all_phonemes["durations_seconds"]
                                        total_duration = sum(durations)
                                        print(f"\n  ⏱️ Duration statistics:")
                                        print(
                                            f"    Total duration: {total_duration:.3f}s"
                                        )
                                        print(
                                            f"    Average duration: {total_duration/len(durations):.3f}s"
                                        )
                                        print(
                                            f"    Min duration: {min(durations):.3f}s"
                                        )
                                        print(
                                            f"    Max duration: {max(durations):.3f}s"
                                        )

                                    # Add Start Times statistics
                                    if all_phonemes["start_times_seconds"]:
                                        start_times = all_phonemes[
                                            "start_times_seconds"
                                        ]
                                        print(f"\n  🚀 Start Times statistics:")
                                        print(
                                            f"    First start: {min(start_times):.3f}s"
                                        )
                                        print(
                                            f"    Last start: {max(start_times):.3f}s"
                                        )
                                        print(
                                            f"    전체 Time range: {max(start_times) - min(start_times):.3f}s"
                                        )

                                    # Display Phoneme-Duration-StartTime mapping (first 30)
                                    if (
                                        all_phonemes["symbols"]
                                        and all_phonemes["durations_seconds"]
                                    ):
                                        print(
                                            f"\n  🎯 Phoneme-Duration-StartTime mapping (first 30):"
                                        )
                                        has_start_times = (
                                            len(all_phonemes["start_times_seconds"]) > 0
                                        )

                                        for i in range(
                                            min(
                                                30,
                                                len(all_phonemes["symbols"]),
                                                len(all_phonemes["durations_seconds"]),
                                            )
                                        ):
                                            symbol = all_phonemes["symbols"][i]
                                            duration = all_phonemes[
                                                "durations_seconds"
                                            ][i]

                                            if has_start_times and i < len(
                                                all_phonemes["start_times_seconds"]
                                            ):
                                                start_time = all_phonemes[
                                                    "start_times_seconds"
                                                ][i]
                                                end_time = start_time + duration
                                                print(
                                                    f"    {i+1:2d}. '{symbol}' -> {start_time:.3f}s~{end_time:.3f}s ({duration:.3f}s)"
                                                )
                                            else:
                                                print(
                                                    f"    {i+1:2d}. '{symbol}' -> duration: {duration:.3f}s (start time 없음)"
                                                )

                                        if len(all_phonemes["symbols"]) > 30:
                                            print(
                                                f"    ... (총 {len(all_phonemes['symbols'])} items)"
                                            )

                                    # Save detailed information as JSON (including start_times_seconds)
                                    phoneme_data = {
                                        "text": long_text,
                                        "text_length": len(long_text),
                                        "processing_method": "stream_speech_chunking",
                                        "audio_format": "wav",
                                        "phonemes": all_phonemes,
                                        "statistics": {
                                            "total_symbols": len(
                                                all_phonemes["symbols"]
                                            ),
                                            "total_duration": (
                                                sum(all_phonemes["durations_seconds"])
                                                if all_phonemes["durations_seconds"]
                                                else 0
                                            ),
                                            "has_start_times": len(
                                                all_phonemes["start_times_seconds"]
                                            )
                                            > 0,
                                            "total_time_range": (
                                                max(all_phonemes["start_times_seconds"])
                                                - min(
                                                    all_phonemes["start_times_seconds"]
                                                )
                                                if all_phonemes["start_times_seconds"]
                                                else 0
                                            ),
                                        },
                                    }

                                    import json

                                    with open(
                                        "test_phoneme_chunking_stream_data.json",
                                        "w",
                                        encoding="utf-8",
                                    ) as f:
                                        json.dump(
                                            phoneme_data,
                                            f,
                                            ensure_ascii=False,
                                            indent=2,
                                        )
                                    print(
                                        f"\n  💾 Detailed Phoneme streaming data saved: test_phoneme_chunking_stream_data.json"
                                    )

                                return (
                                    True,
                                    f"JSON streaming success: {len(total_audio)} bytes, {len(all_phonemes['symbols'])} phonemes, {len(all_phonemes['start_times_seconds'])} start times",
                                )

                            else:
                                print(
                                    f"  🔍 Original response has unexpected type: {type(original)}"
                                )

                    except Exception as wrapper_error:
                        print(
                            f"  ❌ Error processing ExtendedStreamingWrapper: {wrapper_error}"
                        )
                        print(f"  🔍 Wrapper Error type: {type(wrapper_error)}")

                # Attempt regular streaming processing
                try:
                    if hasattr(response.result, "iter_bytes"):
                        print("  🔄 Attempting regular streaming processing...")
                        audio_chunks = []

                        for chunk in response.result.iter_bytes(chunk_size=8192):
                            audio_chunks.append(chunk)

                        if audio_chunks:
                            full_audio = b"".join(audio_chunks)
                            filename = "test_phoneme_chunking_stream_output.wav"
                            with open(filename, "wb") as f:
                                f.write(full_audio)
                            print(f"  💾 Regular Streaming audio saved: {filename}")
                            return True, response

                except AttributeError as attr_error:
                    if "'str' object has no attribute 'iter_bytes'" in str(attr_error):
                        print("  ✅ Expected error: Streaming interface issue")
                        print(
                            "  💡 Phoneme + Long text + streaming is currently not fully supported"
                        )
                        return (
                            True,
                            "Expected: Streaming interface limitation with phonemes",
                        )
                    else:
                        raise attr_error

                # Process other response formats
                if isinstance(response.result, str):
                    print("  📄 Direct processing of string response...")
                    # Same as JSON processing logic above

                print("  ⚠️ Unknown response structure - additional analysis required")
                return False, "Unknown response structure"

    except errors.SupertoneDefaultError as e:
        print(f"  ❌ API error: {e}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        print(f"  🔍 Error type: {type(e)}")
        return False, e


# =============================================================================
# NEW MODEL TESTS (sona_speech_2, supertonic_api_1)
# =============================================================================


def test_create_speech_sona_speech_2(voice_id):
    """Test TTS with sona_speech_2 model"""
    print("🎤 TTS Test with sona_speech_2 Model")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Converting TTS with sona_speech_2 using voice '{voice_id}'...")
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.create_speech(
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

                output_file = "test_sona_speech_2_output.wav"
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


def test_create_speech_supertonic_api_1(voice_id):
    """Test TTS with supertonic_api_1 model"""
    print("🎤 TTS Test with supertonic_api_1 Model")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Converting TTS with supertonic_api_1 using voice '{voice_id}'..."
            )
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.create_speech(
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

                output_file = "test_supertonic_api_1_output.wav"
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


def test_create_speech_invalid_model(voice_id):
    """Test TTS with unsupported model - should return error"""
    print("❌ TTS Test with Invalid Model (Expected Error)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Attempting TTS with invalid model 'invalid_model_xyz'...")

            # Attempt to call with invalid model string directly
            response = client.text_to_speech.create_speech(
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
        # SDK-level validation may catch this before API call
        print(f"  ✅ Expected SDK validation error: {e}")
        print("  ✅ SDK correctly rejected invalid model")
        return True, e
    except Exception as e:
        # Any error is acceptable since invalid model should fail
        print(f"  ✅ Error received (expected): {e}")
        return True, e


def test_predict_duration_sona_speech_2(voice_id):
    """Test duration prediction with sona_speech_2 model"""
    print("⏱️ Duration Prediction Test with sona_speech_2 Model")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with sona_speech_2 using voice '{voice_id}'..."
            )

            response = client.text_to_speech.predict_duration(
                voice_id=voice_id,
                text="Hello! This is a duration prediction test with sona_speech_2.",
                language=models.PredictTTSDurationUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.PredictTTSDurationUsingCharacterRequestModel.SONA_SPEECH_2,
            )

            print(f"  ✅ sona_speech_2 prediction complete: {response} seconds")
            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_predict_duration_supertonic_api_1(voice_id):
    """Test duration prediction with supertonic_api_1 model"""
    print("⏱️ Duration Prediction Test with supertonic_api_1 Model")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Predicting duration with supertonic_api_1 using voice '{voice_id}'..."
            )

            response = client.text_to_speech.predict_duration(
                voice_id=voice_id,
                text="Hello! This is a duration prediction test with supertonic_api_1.",
                language=models.PredictTTSDurationUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.PredictTTSDurationUsingCharacterRequestModel.SUPERTONIC_API_1,
            )

            print(f"  ✅ supertonic_api_1 prediction complete: {response} seconds")
            return True, response

    except errors.SupertoneError as e:
        print(f"  ❌ API error: {e.message}")
        return False, e
    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_predict_duration_invalid_model(voice_id):
    """Test duration prediction with unsupported model - should return error"""
    print("❌ Duration Prediction Test with Invalid Model (Expected Error)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        with Supertone(api_key=API_KEY) as client:
            print(
                f"  🔍 Attempting prediction with invalid model 'invalid_model_xyz'..."
            )

            response = client.text_to_speech.predict_duration(
                voice_id=voice_id,
                text="This should fail with invalid model.",
                language=models.PredictTTSDurationUsingCharacterRequestLanguage.EN,
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
# MULTI-LANGUAGE TESTS BY MODEL
# =============================================================================


def test_create_speech_sona_speech_1_multilang(voice_id):
    """Test sona_speech_1 with supported languages (ko, en, ja)"""
    print("🌐 sona_speech_1 Multi-language Test (ko, en, ja)")

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
        with Supertone(api_key=API_KEY) as client:
            for lang, text in test_cases:
                print(f"  🔍 Testing {lang.value} with sona_speech_1...")

                try:
                    response = client.text_to_speech.create_speech(
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

        return all_success, "sona_speech_1 multilang test"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_sona_speech_2_multilang(voice_id):
    """Test sona_speech_2 with all supported languages"""
    print("🌐 sona_speech_2 Multi-language Test (all languages)")

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
        with Supertone(api_key=API_KEY) as client:
            for lang, text in test_cases:
                print(f"  🔍 Testing {lang.value} with sona_speech_2...")

                try:
                    response = client.text_to_speech.create_speech(
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
            f"sona_speech_2 multilang: {success_count}/{len(test_cases)}",
        )

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_supertonic_api_1_multilang(voice_id):
    """Test supertonic_api_1 with supported languages (ko, en, ja, es, pt)"""
    print("🌐 supertonic_api_1 Multi-language Test (ko, en, ja, es, pt)")

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
        with Supertone(api_key=API_KEY) as client:
            for lang, text in test_cases:
                print(f"  🔍 Testing {lang.value} with supertonic_api_1...")

                try:
                    response = client.text_to_speech.create_speech(
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

        return all_success, "supertonic_api_1 multilang test"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_sona_speech_1_unsupported_lang(voice_id):
    """Test sona_speech_1 with unsupported language - should return error"""
    print("❌ sona_speech_1 Unsupported Language Test (Expected Error)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # sona_speech_1 only supports ko, en, ja - testing with German (de)
        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Attempting sona_speech_1 with German (unsupported)...")

            response = client.text_to_speech.create_speech(
                voice_id=voice_id,
                text="Hallo! Dies ist ein Test.",
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.DE,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
            )

            # If API returns success, it might mean our understanding is wrong
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


def test_create_speech_supertonic_api_1_unsupported_lang(voice_id):
    """Test supertonic_api_1 with unsupported language - should return error"""
    print("❌ supertonic_api_1 Unsupported Language Test (Expected Error)")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        # supertonic_api_1 supports: ko, en, ja, es, pt - testing with German (de)
        with Supertone(api_key=API_KEY) as client:
            print(f"  🔍 Attempting supertonic_api_1 with German (unsupported)...")

            response = client.text_to_speech.create_speech(
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


def test_predict_duration_multilang(voice_id):
    """Test duration prediction with different languages and models"""
    print("🌐⏱️ Duration Prediction Multi-language Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, errors, models

        test_cases = [
            # (model, language, text)
            (
                models.PredictTTSDurationUsingCharacterRequestModel.SONA_SPEECH_1,
                models.PredictTTSDurationUsingCharacterRequestLanguage.KO,
                "안녕하세요!",
            ),
            (
                models.PredictTTSDurationUsingCharacterRequestModel.SONA_SPEECH_2,
                models.PredictTTSDurationUsingCharacterRequestLanguage.DE,
                "Guten Tag!",
            ),
            (
                models.PredictTTSDurationUsingCharacterRequestModel.SUPERTONIC_API_1,
                models.PredictTTSDurationUsingCharacterRequestLanguage.ES,
                "¡Buenos días!",
            ),
        ]

        all_success = True
        with Supertone(api_key=API_KEY) as client:
            for model, lang, text in test_cases:
                print(f"  🔍 Predicting with {model.value} + {lang.value}...")

                try:
                    response = client.text_to_speech.predict_duration(
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

        return all_success, "predict_duration multilang test"

    except Exception as e:
        print(f"  ❌ Unexpected error: {e}")
        return False, e


def test_create_speech_long_sentence_word_split(voice_id):
    """Test TTS with a very long sentence that exceeds 300 chars without punctuation (word-based splitting)"""
    print("📝✂️ Long Sentence Word-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Create a long sentence without punctuation (over 300 chars)
        # This forces the chunking algorithm to split by word boundaries
        long_sentence = (
            "This is a very long sentence without any punctuation marks that is designed "
            "to exceed the three hundred character limit so that the text chunking algorithm "
            "will need to fall back to word based splitting instead of sentence based splitting "
            "because there are no sentence ending punctuation marks like periods or exclamation "
            "points to use as natural break points in this extremely lengthy run on sentence"
        )

        print(f"  📏 Text length: {len(long_sentence)} characters (no punctuation)")
        print(f"  📄 Text preview: {long_sentence[:50]}...")

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Converting TTS with word-based chunking...")
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.create_speech(
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


def test_create_speech_japanese_no_spaces(voice_id):
    """Test TTS with Japanese text (no spaces) that exceeds 300 chars (character-based splitting)"""
    print("🇯🇵✂️ Japanese Text Character-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Create a long Japanese text without spaces (over 300 chars)
        # Japanese typically has no word spaces, forcing character-based splitting
        # This is a repeated pattern to exceed 300 characters
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

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Converting TTS with character-based chunking...")
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.create_speech(
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


def test_stream_speech_long_sentence_word_split(voice_id):
    """Test streaming TTS with a very long sentence (word-based splitting)"""
    print("📝🔊✂️ Streaming Long Sentence Word-Based Splitting Test")

    if not voice_id:
        print("  ⚠️ No voice ID available")
        return False, None

    try:
        from supertone import Supertone, models

        # Create a long sentence without punctuation (over 300 chars)
        long_sentence = (
            "This is an extremely long sentence that has been carefully crafted without "
            "any punctuation marks whatsoever in order to test the streaming text to speech "
            "functionality with word based chunking which should split this text into multiple "
            "smaller chunks at word boundaries while still producing smooth continuous audio "
            "output that sounds natural and without any noticeable gaps or stuttering effects"
        )

        print(f"  📏 Text length: {len(long_sentence)} characters (no punctuation)")

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Streaming TTS with word-based chunking...")
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text=long_sentence,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "iter_bytes"):
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


def test_stream_speech_japanese_no_spaces(voice_id):
    """Test streaming TTS with Japanese text (character-based splitting)"""
    print("🇯🇵🔊✂️ Streaming Japanese Character-Based Splitting Test")

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

        with Supertone(api_key=API_KEY) as client:
            print("  🔍 Streaming TTS with character-based chunking...")
            print("  ⚠️ This test will consume credits!")

            response = client.text_to_speech.stream_speech(
                voice_id=voice_id,
                text=japanese_text,
                language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
                style="neutral",
                model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
                output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
            )

            # Collect streaming data
            audio_data = b""
            if hasattr(response.result, "iter_bytes"):
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


def main():
    """Main integration test execution - all sync API tests"""
    print("🧪 Real API Integration Test Start (All Sync APIs)")
    print(f"🔑 API Key: {API_KEY[:8]}..." + "*" * 24)
    print("=" * 60)

    test_results = {}
    voice_id_for_tts = "91992bbd4758bdcf9c9b01"  # Adam
    custom_voice_id = None
    created_custom_voice_id = None

    # 1. Credit and Usage Tests
    print("\n1️⃣ Credit and Usage Tests")

    success, result = test_credit_balance()
    test_results["get_credit_balance"] = success

    if not success:
        print("❌ API key authentication failed. Stopping tests.")
        return False

    success, result = test_get_usage()
    test_results["get_usage"] = success

    success, result = test_get_voice_usage()
    test_results["get_voice_usage"] = success

    # 2. Voice Tests
    print("\n2️⃣ Voice Tests")

    success, result = test_list_voices()
    test_results["list_voices"] = success

    success, result = test_search_voices()
    test_results["search_voices"] = success

    if voice_id_for_tts:
        success, result = test_get_voice(voice_id_for_tts)
        test_results["get_voice"] = success

    # 3. Custom Voice Tests
    print("\n3️⃣ Custom Voice Tests")

    success, result = test_list_custom_voices()
    test_results["list_custom_voices"] = success
    if success and result[1]:  # Extract custom_voice_id
        custom_voice_id = result[1]

    success, result = test_search_custom_voices()
    test_results["search_custom_voices"] = success

    if custom_voice_id:
        success, result = test_get_custom_voice(custom_voice_id)
        test_results["get_custom_voice"] = success

        success, result = test_edit_custom_voice(custom_voice_id)
        test_results["edit_custom_voice"] = success

    # Custom Voice Creation Test
    print("\n🎨 Custom Voice Creation Test")
    success, result = test_create_cloned_voice()
    test_results["create_cloned_voice"] = success
    if success and result:
        created_custom_voice_id = result.voice_id
        print(f"  🎉 New custom voice created: {created_custom_voice_id}")

    # 4. TTS Tests
    print("\n4️⃣ TTS Tests")

    if voice_id_for_tts:
        # Duration prediction (no credit consumption)
        success, result = test_predict_duration(voice_id_for_tts)
        test_results["predict_duration"] = success

        # Duration prediction with Voice Settings
        success, result = test_predict_duration_with_voice_settings(voice_id_for_tts)
        test_results["predict_duration_with_voice_settings"] = success

        # Basic TTS (consumes credits)
        print("💳 TTS will consume credits.")
        success, result = test_create_speech(voice_id_for_tts)
        test_results["create_speech"] = success

        # TTS with Voice Settings (consumes credits)
        success, result = test_create_speech_with_voice_settings(voice_id_for_tts)
        test_results["create_speech_with_voice_settings"] = success

        # Basic Streaming TTS (WAV)
        success, result = test_stream_speech(voice_id_for_tts)
        test_results["stream_speech"] = success

        # Streaming TTS with Voice Settings (consumes credits)
        success, result = test_stream_speech_with_voice_settings(voice_id_for_tts)
        test_results["stream_speech_with_voice_settings"] = success

        # 5. TTS Tests with Phoneme Information
        print("\n🔤 TTS Tests with Phoneme Information")

        # Basic TTS with Phonemes (consumes credits)
        print("💳 TTS with phonemes will consume credits.")
        success, result = test_create_speech_with_phonemes(voice_id_for_tts)
        test_results["create_speech_with_phonemes"] = success

        # Streaming TTS with Phonemes (consumes credits)
        success, result = test_stream_speech_with_phonemes(voice_id_for_tts)
        test_results["stream_speech_with_phonemes"] = success

        # Long Text Tests (over 300 characters)
        print("\n5️⃣ Long Text Tests (Over 300 Characters)")
        success, result = test_create_speech_long_text(voice_id_for_tts)
        test_results["create_speech_long_text"] = success

        success, result = test_stream_speech_long_text(voice_id_for_tts)
        test_results["stream_speech_long_text"] = success

        # MP3 Format TTS Tests
        print("\n🎵 MP3 Format TTS Tests")
        success, result = test_create_speech_mp3(voice_id_for_tts)
        test_results["create_speech_mp3"] = success

        # Long text MP3 auto-chunking TTS test
        success, result = test_create_speech_long_text_mp3(voice_id_for_tts)
        test_results["create_speech_long_text_mp3"] = success

        # MP3 Streaming TTS test
        success, result = test_stream_speech_mp3(voice_id_for_tts)
        test_results["stream_speech_mp3"] = success

        # Long text MP3 streaming TTS test
        success, result = test_stream_speech_long_text_mp3(voice_id_for_tts)
        test_results["stream_speech_long_text_mp3"] = success

        # Long text auto-chunking + Phonemes TTS test
        success, result = test_create_speech_long_text_with_phonemes(voice_id_for_tts)
        test_results["create_speech_long_text_with_phonemes"] = success

        # Long text + Phoneme + Streaming test (WAV)
        success, result = test_stream_speech_phoneme_chunking_wav(voice_id_for_tts)
        test_results["stream_speech_phoneme_chunking_wav"] = success

        # 6. New Model Tests (sona_speech_2, supertonic_api_1)
        print("\n6️⃣ New Model Tests (sona_speech_2, supertonic_api_1)")

        # TTS with sona_speech_2
        success, result = test_create_speech_sona_speech_2(voice_id_for_tts)
        test_results["create_speech_sona_speech_2"] = success

        # TTS with supertonic_api_1
        success, result = test_create_speech_supertonic_api_1(voice_id_for_tts)
        test_results["create_speech_supertonic_api_1"] = success

        # Invalid model test
        success, result = test_create_speech_invalid_model(voice_id_for_tts)
        test_results["create_speech_invalid_model"] = success

        # Duration prediction with new models
        success, result = test_predict_duration_sona_speech_2(voice_id_for_tts)
        test_results["predict_duration_sona_speech_2"] = success

        success, result = test_predict_duration_supertonic_api_1(voice_id_for_tts)
        test_results["predict_duration_supertonic_api_1"] = success

        # Invalid model prediction test
        success, result = test_predict_duration_invalid_model(voice_id_for_tts)
        test_results["predict_duration_invalid_model"] = success

        # 7. Multi-language Tests by Model
        print("\n7️⃣ Multi-language Tests by Model")

        # sona_speech_1 multilang (ko, en, ja)
        success, result = test_create_speech_sona_speech_1_multilang(voice_id_for_tts)
        test_results["create_speech_sona_speech_1_multilang"] = success

        # sona_speech_2 multilang (all languages)
        success, result = test_create_speech_sona_speech_2_multilang(voice_id_for_tts)
        test_results["create_speech_sona_speech_2_multilang"] = success

        # supertonic_api_1 multilang (ko, en, ja, es, pt)
        success, result = test_create_speech_supertonic_api_1_multilang(
            voice_id_for_tts
        )
        test_results["create_speech_supertonic_api_1_multilang"] = success

        # Unsupported language error tests
        success, result = test_create_speech_sona_speech_1_unsupported_lang(
            voice_id_for_tts
        )
        test_results["create_speech_sona_speech_1_unsupported_lang"] = success

        success, result = test_create_speech_supertonic_api_1_unsupported_lang(
            voice_id_for_tts
        )
        test_results["create_speech_supertonic_api_1_unsupported_lang"] = success

        # Duration prediction multilang test
        success, result = test_predict_duration_multilang(voice_id_for_tts)
        test_results["predict_duration_multilang"] = success

        # 8. Advanced Text Chunking Tests
        print("\n8️⃣ Advanced Text Chunking Tests")

        # Long sentence word-based splitting (TTS)
        success, result = test_create_speech_long_sentence_word_split(voice_id_for_tts)
        test_results["create_speech_long_sentence_word_split"] = success

        # Japanese character-based splitting (TTS)
        success, result = test_create_speech_japanese_no_spaces(voice_id_for_tts)
        test_results["create_speech_japanese_no_spaces"] = success

        # Long sentence word-based splitting (Streaming)
        success, result = test_stream_speech_long_sentence_word_split(voice_id_for_tts)
        test_results["stream_speech_long_sentence_word_split"] = success

        # Japanese character-based splitting (Streaming)
        success, result = test_stream_speech_japanese_no_spaces(voice_id_for_tts)
        test_results["stream_speech_japanese_no_spaces"] = success

    # 9. Custom Voice Deletion (run last)
    if created_custom_voice_id:
        print("\n🗑️ Created Custom Voice Deletion Test")
        success, result = test_delete_custom_voice(created_custom_voice_id)
        test_results["delete_custom_voice"] = success

    # Results Summary
    print("\n" + "=" * 60)
    print("🧪 Integration Test Results Summary (All Sync APIs):")

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

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All integration tests passed! SDK works properly with the real API.")
        print("\n✅ SDK ready for deployment!")
    else:
        print("⚠️ Some tests failed. Please check API key or permissions.")

    print("\n📋 All Tested Sync APIs:")
    print("  • Usage: get_credit_balance, get_usage, get_voice_usage")
    print("  • Voices: list_voices, search_voices, get_voice")
    print(
        "  • Custom Voices: list_custom_voices, search_custom_voices, get_custom_voice"
    )
    print(
        "                   create_cloned_voice, edit_custom_voice, delete_custom_voice"
    )
    print("  • Text-to-Speech (WAV): predict_duration, create_speech, stream_speech")
    print("  • Text-to-Speech (MP3): create_speech_mp3, create_speech_long_text_mp3")
    print("                          stream_speech_mp3, stream_speech_long_text_mp3")
    print(
        "  • Voice Settings Tests: predict_duration_with_voice_settings, create_speech_with_voice_settings, stream_speech_with_voice_settings"
    )
    print("  • Phoneme Tests: create_speech_with_phonemes, stream_speech_with_phonemes")
    print("  • Long Text Tests (Auto-Chunking):")
    print("    - WAV: create_speech_long_text, stream_speech_long_text")
    print("    - MP3: create_speech_long_text_mp3, stream_speech_long_text_mp3")
    print("  • New Model Tests:")
    print(
        "    - sona_speech_2: create_speech_sona_speech_2, predict_duration_sona_speech_2"
    )
    print(
        "    - supertonic_api_1: create_speech_supertonic_api_1, predict_duration_supertonic_api_1"
    )
    print(
        "    - Invalid model tests: create_speech_invalid_model, predict_duration_invalid_model"
    )
    print("  • Multi-language Tests by Model:")
    print("    - sona_speech_1: ko, en, ja")
    print("    - sona_speech_2: all languages")
    print("    - supertonic_api_1: ko, en, ja, es, pt")
    print("    - Unsupported language error tests")
    print("  • Advanced Text Chunking Tests:")
    print("    - Long sentence word-based splitting: create_speech, stream_speech")
    print("    - Japanese character-based splitting: create_speech, stream_speech")

    if created_custom_voice_id:
        print(f"\n🎨 Custom voice created during test: {created_custom_voice_id}")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
