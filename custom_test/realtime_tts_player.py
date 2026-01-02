#!/usr/bin/env python3
"""
Real-time Streaming TTS Audio Player
Example of automatic playback as chunks arrive
"""
import sys
import os
import asyncio
import struct
import wave
import io
from threading import Thread, Event
from queue import Queue
import time
import threading
import numpy as np
import sounddevice as sd
from queue import Queue, Empty
import time
import struct
import io

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # Load .env from the same directory as this script (custom_test/)
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # Silently fall back to system environment variables

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Real API Key
API_KEY = os.getenv("SUPERTONE_API_KEY", "your-api-key-here")

try:
    import sounddevice as sd
    import numpy as np

    AUDIO_AVAILABLE = True
    print("🔊 sounddevice library available")
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️ sounddevice installation required: pip install sounddevice numpy")
    print("   or brew install portaudio (macOS)")


class RealTimeAudioPlayer:
    """Real-time audio streaming player - Simple and stable version"""

    def __init__(self):
        self.audio_queue = Queue()
        self.stop_event = threading.Event()
        self.sample_rate = None
        self.channels = None
        self.sample_width = None
        self.is_playing = False

        # Continuous audio stream (simplified)
        self.audio_stream = io.BytesIO()
        self.stream_lock = threading.Lock()
        self.current_position = 0

        # sounddevice stream
        self.output_stream = None
        self.feeder_thread = None

        # Simple buffering (noise removal logic removed)
        self.buffer_size = 32768  # Increased from 16384 to 32768 (more stable)

        # Accumulation buffer for small chunk filtering
        self.chunk_accumulator = bytearray()
        self.accumulator_lock = threading.Lock()
        self.min_chunk_size = 4096  # Minimum chunk size (4KB)

    def audio_callback(self, outdata, frames, time, status):
        """sounddevice callback - Small chunk noise removal version"""
        if status:
            print(f"⚠️ Audio status: {status}")

        try:
            with self.stream_lock:
                # Read required data from current position
                self.audio_stream.seek(self.current_position)
                requested_bytes = frames * self.sample_width * self.channels

                # **Key improvement**: Check minimum buffer size
                available_bytes = self.audio_stream.seek(0, io.SEEK_END)
                self.audio_stream.seek(self.current_position)
                remaining_bytes = available_bytes - self.current_position

                # Play only when sufficient data is available (key noise solution)
                min_required = max(
                    requested_bytes, self.buffer_size // 4
                )  # At least 1/4 of buffer

                if remaining_bytes < min_required:
                    # Wait with silence when data is insufficient (prevent noise)
                    outdata.fill(0)
                    return

                audio_data = self.audio_stream.read(requested_bytes)

                if len(audio_data) >= requested_bytes:  # **Process only complete data**
                    # Sample boundary alignment
                    sample_boundary = (
                        len(audio_data)
                        // (self.sample_width * self.channels)
                        * (self.sample_width * self.channels)
                    )
                    if sample_boundary != len(audio_data):
                        audio_data = audio_data[:sample_boundary]

                    if len(audio_data) == 0:
                        outdata.fill(0)
                        return

                    # Type conversion (add clipping to prevent noise)
                    if self.sample_width == 2:
                        audio_array = np.frombuffer(audio_data, dtype=np.int16)
                        # **Add clipping**: Prevent range overflow
                        audio_array = np.clip(
                            audio_array.astype(np.float32) / 32768.0, -1.0, 1.0
                        )
                    else:
                        audio_array = np.frombuffer(audio_data, dtype=np.int32)
                        audio_array = np.clip(
                            audio_array.astype(np.float32) / 2147483648.0, -1.0, 1.0
                        )

                    # Channel handling (safer)
                    if self.channels == 2:
                        if len(audio_array) % 2 == 0:
                            audio_array = audio_array.reshape(-1, 2)
                        else:
                            # Remove last one if odd samples
                            audio_array = audio_array[:-1].reshape(-1, 2)

                    # **Output only complete frames**: Wait if partial frame
                    samples_available = len(audio_array)
                    if samples_available >= frames:  # **Only complete frames**
                        if self.channels == 1:
                            outdata[:frames, 0] = audio_array[:frames]
                        else:
                            outdata[:frames] = audio_array[:frames]

                        # Move position by used data
                        used_bytes = frames * self.sample_width * self.channels
                        self.current_position += used_bytes
                    else:
                        # Wait if incomplete frame (prevent noise)
                        outdata.fill(0)
                else:
                    outdata.fill(0)

        except Exception as e:
            print(f"⚠️ Callback error: {e}")
            outdata.fill(0)

    def audio_feeder_worker(self):
        """Simple audio feeder"""
        print("🎵 Audio feeder started")

        while not self.stop_event.is_set():
            try:
                audio_data = self.audio_queue.get(timeout=0.1)

                if audio_data is None:
                    break

                if not AUDIO_AVAILABLE:
                    continue

                # Wait for settings
                if (
                    self.sample_rate is None
                    or self.channels is None
                    or self.sample_width is None
                ):
                    self.audio_queue.put(audio_data)
                    time.sleep(0.01)
                    continue

                if len(audio_data) == 0:
                    continue

                # Minimal alignment only
                if self.sample_width == 2 and len(audio_data) % 2 != 0:
                    audio_data = audio_data[:-1]

                if len(audio_data) == 0:
                    continue

                # Add to stream immediately (remove complex buffering)
                with self.stream_lock:
                    self.audio_stream.seek(0, io.SEEK_END)
                    self.audio_stream.write(audio_data)

            except Empty:
                continue
            except Exception as e:
                print(f"⚠️ Feeder error: {e}")
                continue

        print("🛑 Audio feeder stopped")

    def start_streaming_playback(self):
        """Start simple sounddevice stream"""
        if not AUDIO_AVAILABLE or self.output_stream is not None:
            return

        try:
            print(f"🔊 Simple output stream starting")
            print(f"   Sample rate: {self.sample_rate} Hz, Channels: {self.channels}")

            self.output_stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self.audio_callback,
                dtype=np.float32,
                blocksize=4096,  # Appropriate size
                latency="high",  # Stability first
            )

            self.output_stream.start()
            print("✅ Simple stream started")

        except Exception as e:
            print(f"⚠️ Stream start error: {e}")

    def add_audio_chunk(self, chunk_data):
        """Add chunk with small chunk filtering applied"""
        if not self.is_playing:
            return

        # WAV header parsing (first chunk)
        if self.sample_rate is None:
            print(f"🔍 Header parsing: {len(chunk_data)} bytes")

            if (
                len(chunk_data) >= 44
                and chunk_data[:4] == b"RIFF"
                and chunk_data[8:12] == b"WAVE"
            ):
                try:
                    self.channels = struct.unpack("<H", chunk_data[22:24])[0]
                    self.sample_rate = struct.unpack("<I", chunk_data[24:28])[0]
                    self.sample_width = struct.unpack("<H", chunk_data[34:36])[0] // 8

                    print(
                        f"✅ Header: {self.sample_rate}Hz, {self.channels}ch, {self.sample_width*8}bit"
                    )

                    # Adjust minimum chunk size based on sample rate (0.1 seconds)
                    self.min_chunk_size = int(
                        0.1 * self.sample_rate * self.sample_width * self.channels
                    )
                    print(f"🎯 Minimum chunk size: {self.min_chunk_size} bytes")

                    # Find data chunk
                    pos = 36
                    audio_data = chunk_data[44:]  # Default

                    while pos < len(chunk_data) - 8:
                        chunk_id = chunk_data[pos : pos + 4]
                        chunk_size = struct.unpack("<I", chunk_data[pos + 4 : pos + 8])[
                            0
                        ]

                        if chunk_id == b"data":
                            audio_data = chunk_data[pos + 8 :]
                            break
                        pos += 8 + chunk_size

                    self.start_streaming_playback()

                    # Apply filtering to first audio data too
                    if audio_data and len(audio_data) > 0:
                        print(f"📡 First audio: {len(audio_data)} bytes")
                        self._add_chunk_with_filtering(audio_data)

                except Exception as e:
                    print(f"⚠️ Header error: {e}")
                    self._set_default_settings()
                    self._add_chunk_with_filtering(chunk_data)
            else:
                self._set_default_settings()
                self._add_chunk_with_filtering(chunk_data)
        else:
            # Subsequent chunks - apply filtering
            if len(chunk_data) > 0:
                self._add_chunk_with_filtering(chunk_data)

    def _add_chunk_with_filtering(self, chunk_data):
        """Small chunk filtering logic"""
        if len(chunk_data) == 0:
            return

        with self.accumulator_lock:
            # Add to accumulation buffer
            self.chunk_accumulator.extend(chunk_data)

            # Detect and log small chunks
            if len(chunk_data) < 1024:
                print(
                    f"🟡 Small chunk accumulated: {len(chunk_data)} bytes → Buffer: {len(self.chunk_accumulator)} bytes"
                )
            else:
                print(
                    f"📊 Chunk accumulated: {len(chunk_data)} bytes → Buffer: {len(self.chunk_accumulator)} bytes"
                )

            # Send to playback queue when sufficient size is accumulated
            while len(self.chunk_accumulator) >= self.min_chunk_size:
                # Extract stable size
                stable_chunk = bytes(self.chunk_accumulator[: self.min_chunk_size])
                self.chunk_accumulator = self.chunk_accumulator[self.min_chunk_size :]

                print(
                    f"✅ Stable chunk sent to playback queue: {len(stable_chunk)} bytes (Remaining buffer: {len(self.chunk_accumulator)} bytes)"
                )

                # Add to actual playback queue
                self.audio_queue.put(stable_chunk)

    def _set_default_settings(self):
        """Default settings"""
        self.sample_rate = 44100
        self.channels = 1
        self.sample_width = 2
        self.min_chunk_size = int(
            0.1 * self.sample_rate * self.sample_width * self.channels
        )  # 0.1 seconds
        print(f"🎛️ Default settings: {self.sample_rate}Hz, {self.channels}ch")
        print(f"🎯 Default minimum chunk size: {self.min_chunk_size} bytes")
        self.start_streaming_playback()

    def start_player(self):
        """Start player"""
        if not self.is_playing:
            self.stop_event.clear()
            self.feeder_thread = threading.Thread(
                target=self.audio_feeder_worker, daemon=True
            )
            self.feeder_thread.start()
            self.is_playing = True

    def stop_player(self):
        """Stop player (including remaining buffer processing)"""
        print("🛑 Stopping player...")

        # Process remaining accumulation buffer
        with self.accumulator_lock:
            if len(self.chunk_accumulator) > 0:
                print(
                    f"📤 Sending remaining buffer: {len(self.chunk_accumulator)} bytes"
                )
                self.audio_queue.put(bytes(self.chunk_accumulator))
                self.chunk_accumulator.clear()

        self.is_playing = False
        self.stop_event.set()
        self.audio_queue.put(None)

        if self.output_stream:
            try:
                self.output_stream.stop()
                self.output_stream.close()
                self.output_stream = None
            except:
                pass

        if self.feeder_thread:
            self.feeder_thread.join(timeout=2.0)

    def wait_for_playback_complete(self, timeout=10):
        """Wait for playback completion"""
        print("⏳ Waiting for playback completion...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            with self.stream_lock:
                total_bytes = self.audio_stream.tell()
                remaining = total_bytes - self.current_position

                if remaining <= 1024:  # Almost complete
                    break

            time.sleep(0.5)

        # Additional wait (safely)
        time.sleep(1.0)
        print("✅ Playback completed")


async def streaming_tts_with_realtime_playback(
    voice_id, text, pronunciation_dictionary=None, language="EN"
):
    """Streaming TTS + Real-time automatic playback"""
    print(f"🚀 Real-time playback streaming TTS started")
    print(f"🎤 Voice ID: {voice_id}")
    print(f"🌐 Language: {language}")
    print(f"📝 Text: {text[:50]}...")
    if pronunciation_dictionary:
        print(f"📖 Pronunciation dictionary: {len(pronunciation_dictionary)} entries")

    if not voice_id:
        print("❌ Valid voice ID required")
        return False

    player = RealTimeAudioPlayer()

    try:
        from supertone import Supertone, errors, models

        async with Supertone(api_key=API_KEY) as client:
            print("📡 Requesting streaming TTS...")
            start_time = time.time()

            # Map language string to enum
            language_map = {
                "KO": models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
                "EN": models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN,
                "JA": models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA,
            }
            lang_enum = language_map.get(
                language, models.APIConvertTextToSpeechUsingCharacterRequestLanguage.EN
            )

            # Fixed API call structure
            response = await client.text_to_speech.stream_speech_async(
                voice_id=voice_id,
                text=text,
                language=lang_enum,
                style="neutral",
                model="sona_speech_1",
                pronunciation_dictionary=pronunciation_dictionary,
            )

            request_time = time.time() - start_time
            print(f"✅ Streaming connection completed: {request_time:.3f}s")

            if hasattr(response, "result") and hasattr(response.result, "iter_bytes"):

                print("🎵 Starting audio player...")
                player.start_player()

                chunk_count = 0
                total_bytes = 0
                first_chunk_time = None

                print("🎵 Real-time playback started!")
                print("💡 Chunks will be played automatically as they arrive...")

                # Fixed iterator call - async stream only
                if hasattr(response.result, "aiter_bytes"):
                    # Async stream - use aiter_bytes
                    print("  🔄 Processing as async stream...")
                    async for chunk in response.result.aiter_bytes():
                        current_time = time.time()
                        chunk_count += 1
                        chunk_size = len(chunk)
                        total_bytes += chunk_size

                        if first_chunk_time is None:
                            first_chunk_time = current_time
                            first_playback_delay = first_chunk_time - start_time
                            print(
                                f"🎉 First chunk playback started! @ {first_playback_delay:.3f}s"
                            )

                        # Add to playback queue immediately
                        player.add_audio_chunk(chunk)

                        elapsed = current_time - start_time

                        if chunk_count <= 10:
                            print(
                                f"📡 Chunk {chunk_count}: {chunk_size} bytes → Playing immediately! @ {elapsed:.3f}s"
                            )
                        elif chunk_count == 11:
                            print("🎵 ... (Real-time playback continuing)")
                        elif chunk_count % 20 == 0:
                            print(
                                f"🎵 Progress: {chunk_count} chunks, {total_bytes} bytes @ {elapsed:.3f}s"
                            )

                        await asyncio.sleep(0.001)

                elif hasattr(response.result.iter_bytes, "__call__"):
                    # iter_bytes is callable method (fallback)
                    try:
                        # Try async for first
                        async for chunk in response.result.iter_bytes():
                            current_time = time.time()
                            chunk_count += 1
                            chunk_size = len(chunk)
                            total_bytes += chunk_size

                            if first_chunk_time is None:
                                first_chunk_time = current_time
                                first_playback_delay = first_chunk_time - start_time
                                print(
                                    f"🎉 First chunk playback started! @ {first_playback_delay:.3f}s"
                                )

                            # Add to playback queue immediately
                            player.add_audio_chunk(chunk)

                            elapsed = current_time - start_time

                            if chunk_count <= 10:
                                print(
                                    f"📡 Chunk {chunk_count}: {chunk_size} bytes → Playing immediately! @ {elapsed:.3f}s"
                                )
                            elif chunk_count == 11:
                                print("🎵 ... (Real-time playback continuing)")
                            elif chunk_count % 20 == 0:
                                print(
                                    f"🎵 Progress: {chunk_count} chunks, {total_bytes} bytes @ {elapsed:.3f}s"
                                )

                            await asyncio.sleep(0.001)

                    except TypeError:
                        # Fallback to sync for if async for fails (this case won't occur)
                        print("  🔄 Processing as sync stream...")
                        for chunk in response.result.iter_bytes():
                            current_time = time.time()
                            chunk_count += 1
                            chunk_size = len(chunk)
                            total_bytes += chunk_size

                            if first_chunk_time is None:
                                first_chunk_time = current_time
                                first_playback_delay = first_chunk_time - start_time
                                print(
                                    f"🎉 First chunk playback started! @ {first_playback_delay:.3f}s"
                                )

                            # Add to playback queue immediately
                            player.add_audio_chunk(chunk)

                            elapsed = current_time - start_time

                            if chunk_count <= 10:
                                print(
                                    f"📡 Chunk {chunk_count}: {chunk_size} bytes → Playing immediately! @ {elapsed:.3f}s"
                                )
                            elif chunk_count == 11:
                                print("🎵 ... (Real-time playback continuing)")
                            elif chunk_count % 20 == 0:
                                print(
                                    f"🎵 Progress: {chunk_count} chunks, {total_bytes} bytes @ {elapsed:.3f}s"
                                )

                            await asyncio.sleep(0.001)

                total_time = time.time() - start_time

                print(f"\n📥 Streaming reception completed!")
                print(f"📊 Total {chunk_count} chunks, {total_bytes} bytes")
                print(f"⏱️ Total reception time: {total_time:.3f}s")
                if first_chunk_time:
                    print(f"🚀 Time to first playback: {first_playback_delay:.3f}s")

                # **Simple wait**: Wait for estimated playback time
                if player.sample_rate and player.sample_width:
                    estimated_duration = (
                        total_bytes
                        / player.sample_rate
                        / player.sample_width
                        / (player.channels or 1)
                    )
                    wait_time = estimated_duration + 2  # 2 seconds margin
                    print(f"🎵 Estimated playback time: {estimated_duration:.1f}s")
                    print(f"⏳ Waiting {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                else:
                    await asyncio.sleep(5)

                return True

            else:
                print(
                    f"❌ Streaming response structure needs verification: {type(response)}"
                )
                return False

    except Exception as e:
        print(f"❌ Streaming playback error: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Cleanup player
        player.stop_player()


async def demo_realtime_streaming_scenarios():
    """Demo of various real-time streaming scenarios"""
    print("🎯 Real-time Streaming TTS Scenario Demo\n")

    # Voice ID to use
    voice_id = "91992bbd4758bdcf9c9b01"  # Default voice

    scenarios = [
        {
            "name": "Short message (70 chars)",
            "text": "안녕하세요! 실시간 스트리밍 TTS 기술을 테스트하고 있습니다. 빠른 응답성을 확인해보겠습니다.",
            "language": "KO",
            "description": "Measure immediate responsiveness and initial latency with short text",
        },
        {
            "name": "Regular sentence (150 chars)",
            "text": "오늘은 날씨가 참 좋네요. 실시간 음성 합성 기술이 발달하면서 다양한 애플리케이션에서 활용되고 있습니다. 특히 교육 분야에서는 접근성을 크게 향상시키는 중요한 역할을 하고 있어요. 기술의 발전이 정말 놀랍습니다.",
            "language": "KO",
            "description": "Check natural voice synthesis quality with typical conversation length",
        },
        {
            "name": "Medium explanation (280 chars)",
            "text": "실시간 스트리밍 TTS 기술은 전통적인 배치 처리 방식과는 다릅니다. 사용자가 텍스트를 입력하면 즉시 처리가 시작되고, 첫 번째 청크가 준비되는 즉시 오디오 스트림이 시작됩니다. 이를 통해 전체 텍스트 처리를 기다릴 필요 없이 빠른 피드백을 받을 수 있습니다. 특히 긴 문서를 읽을 때 사용자 경험이 크게 개선되며, 실시간 상호작용이 가능해집니다. 이는 현대적인 AI 서비스의 핵심 요소 중 하나입니다.",
            "language": "KO",
            "description": "Test chunking and performance near 300 character boundary",
        },
        {
            "name": "Long explanation (400 chars)",
            "text": "인공지능과 머신러닝 기술의 발전은 우리 사회의 많은 영역을 변화시키고 있습니다. 특히 자연어 처리와 음성 기술 분야에서는 놀라운 발전이 이루어지고 있어요. 텍스트를 자연스러운 음성으로 변환하는 TTS 기술은 이제 사람의 목소리와 구별하기 어려울 정도로 발전했습니다. 실시간 스트리밍 처리가 가능해지면서 사용자 경험도 크게 향상되었죠. 교육, 엔터테인먼트, 접근성 개선 등 다양한 분야에서 활용되고 있으며, 앞으로도 더 많은 혁신이 기대됩니다. 이러한 기술적 진보는 디지털 콘텐츠 소비 패턴까지 바꾸고 있습니다.",
            "language": "KO",
            "description": "Test auto-chunking feature and continuous streaming with 400 chars",
        },
        {
            "name": "Long document (600 chars)",
            "text": "현대 사회에서 인공지능 기술은 우리 일상생활의 모든 영역에 스며들고 있습니다. 특히 음성 합성 기술은 시각 장애인을 위한 접근성 도구에서부터 엔터테인먼트 산업의 콘텐츠 제작까지 광범위하게 활용되고 있습니다. 실시간 스트리밍 기술과 결합된 텍스트 음성 변환 시스템은 사용자 경험을 혁신적으로 개선합니다. 사용자는 전체 텍스트의 음성 변환이 완료되기를 기다릴 필요 없이, 첫 번째 청크가 처리되는 즉시 오디오를 들을 수 있습니다. 자동 청킹 알고리즘은 텍스트를 문맥과 문장 구조를 고려하여 적절한 크기로 분할하며, 각 청크는 병렬로 처리되어 전체 응답 시간을 대폭 단축시킵니다. 이러한 기술적 혁신은 교육 플랫폼의 강의 자료 음성화, 뉴스 기사의 실시간 읽기 서비스, 소셜 미디어 게시물의 오디오 변환 등 다양한 응용 분야에서 그 진가를 발휘하고 있습니다.",
            "language": "KO",
            "description": "Verify multi-chunking and memory efficiency with 600 char long document",
        },
        {
            "name": "Very long document (800+ chars)",
            "text": "디지털 트랜스포메이션 시대에 접어들면서 음성 기술의 중요성이 더욱 부각되고 있습니다. 특히 코로나19 팬데믹 이후 비대면 서비스와 원격 교육이 일반화되면서 텍스트 음성 변환 기술의 수요가 폭발적으로 증가했습니다. 실시간 스트리밍 TTS는 이러한 요구에 부응하는 핵심 기술로 자리잡고 있어요. 기존의 배치 처리 방식과 달리 스트리밍 방식은 지연 시간을 최소화하고 사용자 상호작용을 극대화합니다. 자동 청킹 알고리즘을 통해 긴 텍스트도 효율적으로 처리할 수 있게 되었고, 문장 경계를 고려한 지능적 분할로 자연스러운 음성을 생성합니다. 또한 병렬 처리를 통해 전체 응답 시간을 단축시키면서도 품질을 유지할 수 있습니다. 이는 온라인 강의, 오디오북 서비스, 뉴스 브리핑, 실시간 번역 등 다양한 서비스에서 활용되고 있으며, 접근성 측면에서도 시각 장애인들에게 큰 도움을 주고 있습니다. 앞으로는 더욱 자연스러운 감정 표현과 개인화된 음성 스타일까지 지원할 것으로 기대됩니다.",
            "language": "KO",
            "description": "Test maximum performance and stability with 800+ char very long text",
        },
        {
            "name": "Long sentence no punctuation (400+ chars, word-based splitting)",
            "text": "This is a very long sentence without any punctuation marks that is designed to exceed the three hundred character limit so that the text chunking algorithm will need to fall back to word based splitting instead of sentence based splitting because there are no sentence ending punctuation marks like periods or exclamation points to use as natural break points in this extremely lengthy run on sentence that keeps going and going without any stops",
            "language": "EN",
            "description": "Test word-based splitting fallback when no punctuation is available",
        },
        {
            "name": "Japanese long text (400+ chars, character-based splitting)",
            "text": "これは日本語のテストです。日本語には通常スペースがありません。そのためテキストを分割するときは文字単位で分割する必要があります。このテストは三百文字を超える長いテキストを使用して文字ベースの分割アルゴリズムが正しく動作することを確認します。人工知能技術は日々進化しており音声合成の品質も向上しています。私たちは最新の技術を使用して自然な音声を生成することができます。デジタル化の進展に伴い音声技術はますます重要になってきています。リアルタイムストリーミング技術と組み合わせることで低遅延で高品質な音声体験を提供できるようになりました。",
            "language": "JA",
            "description": "Test character-based splitting for languages without word spaces like Japanese",
        },
        {
            "name": "Japanese with 。！？ punctuation (350+ chars, multilingual punctuation splitting)",
            "text": "これは日本語のストリーミングテストです。音声合成技術はとても進化しています！リアルタイムストリーミングは素晴らしいですね？長いテキストでも自然に分割されます。品質がとても良いです！次の文章も続きます。これで三百文字を超えるテキストになります。人工知能の発展により音声技術も進歩しました。素晴らしいですね！最新技術を活用しています。日本語の句読点で自然に分割されることを確認します。これは非常に重要な機能です！音声合成の未来は明るいです。私たちはこの素晴らしい技術を使って世界中の人々にサービスを提供しています。テキストが長くなっても問題なく処理できます。自動チャンキング機能が正しく動作しています！これで確実に三百文字を超えました。",
            "language": "JA",
            "description": "Test multilingual punctuation splitting with Japanese 。！？ marks",
        },
        {
            "name": "Korean with ellipsis … (350+ chars, multilingual punctuation splitting)",
            "text": "안녕하세요… 오늘 날씨가 좋네요. 음성 합성 기술이 발전했습니다! 실시간 스트리밍도 가능해요… 정말 놀랍죠? 긴 텍스트도 자연스럽게 처리됩니다. 이 테스트는 삼백자를 넘는 긴 문장입니다… 다국어 구두점 분리를 확인합니다! 한국어 말줄임표도 잘 인식됩니다… 기술의 발전이 놀랍습니다. 실시간 오디오 스트리밍 테스트를 진행하고 있습니다… 품질이 정말 좋네요! 음성 합성 기술은 우리 생활을 더욱 편리하게 만들어줍니다… 앞으로도 계속 발전할 것입니다! 자동 청킹 기능이 정상적으로 동작하는지 확인합니다… 이제 삼백자를 초과했습니다! 테스트 완료!",
            "language": "KO",
            "description": "Test multilingual punctuation splitting with Korean ellipsis (…)",
        },
        # ============================================================
        # Pronunciation Dictionary Scenarios
        # ============================================================
        {
            "name": "Pronunciation Dictionary - Basic (partial_match mixed)",
            "text": "Welcome to Supertone Inc. Our TTSAPI provides high-quality voice synthesis.",
            "language": "EN",
            "pronunciation_dictionary": [
                # partial_match=False: exact word boundary match only
                {
                    "text": "Supertone",
                    "pronunciation": "Super-tone",
                    "partial_match": False,
                },
                {
                    "text": "Inc",
                    "pronunciation": "Incorporated",
                    "partial_match": False,
                },
                # partial_match=True: matches "TTS" inside "TTSAPI"
                {
                    "text": "TTS",
                    "pronunciation": "Text-to-Speech",
                    "partial_match": True,
                },
                {"text": "API", "pronunciation": "A-P-I", "partial_match": True},
            ],
            "description": "Test pronunciation dictionary with mixed partial_match settings",
        },
        {
            "name": "Pronunciation Dictionary - Long text with expansion (triggers auto-chunking)",
            "text": (
                "AI and AIML power modern TTS systems. "
                "The TTSAPI enables voice synthesis via SDK. "
                "Our AI SDK supports real-time API calls. "
                "Use the TTS API to integrate AI into your app. "
                "The SDK documentation covers all API endpoints."
            ),
            "language": "EN",
            "pronunciation_dictionary": [
                # partial_match=False: "AI" won't match inside "AIML"
                {
                    "text": "AI",
                    "pronunciation": "Artificial Intelligence",
                    "partial_match": False,
                },
                # partial_match=True: "TTS" will match inside "TTSAPI"
                {
                    "text": "TTS",
                    "pronunciation": "Text-to-Speech",
                    "partial_match": True,
                },
                # partial_match=False: exact word match only
                {
                    "text": "SDK",
                    "pronunciation": "Software Development Kit",
                    "partial_match": False,
                },
                # partial_match=True: "API" will match inside "TTSAPI"
                {
                    "text": "API",
                    "pronunciation": "Application Programming Interface",
                    "partial_match": True,
                },
            ],
            "description": "Test pronunciation dictionary that expands text beyond 300 chars (auto-chunking)",
        },
        {
            "name": "Pronunciation Dictionary - Technical terms",
            "text": "The CEO announced that NASA and MIT will collaborate on the new IOT project using AWS and GCP cloud services.",
            "language": "EN",
            "pronunciation_dictionary": [
                {
                    "text": "CEO",
                    "pronunciation": "Chief Executive Officer",
                    "partial_match": False,
                },
                {
                    "text": "NASA",
                    "pronunciation": "National Aeronautics and Space Administration",
                    "partial_match": False,
                },
                {
                    "text": "MIT",
                    "pronunciation": "Massachusetts Institute of Technology",
                    "partial_match": False,
                },
                # partial_match=True: would match "IOT" in "RIOT" if present
                {
                    "text": "IOT",
                    "pronunciation": "Internet of Things",
                    "partial_match": True,
                },
                {
                    "text": "AWS",
                    "pronunciation": "Amazon Web Services",
                    "partial_match": False,
                },
                {
                    "text": "GCP",
                    "pronunciation": "Google Cloud Platform",
                    "partial_match": False,
                },
            ],
            "description": "Test pronunciation dictionary with technical acronyms and organization names",
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"{'='*60}")
        print(f"🎬 Scenario {i}: {scenario['name']}")
        print(f"📝 Description: {scenario['description']}")
        print(f"🌐 Language: {scenario.get('language', 'EN')}")
        print(f"📏 Text length: {len(scenario['text'])} chars")
        if scenario.get("pronunciation_dictionary"):
            print(
                f"📖 Pronunciation dictionary: {len(scenario['pronunciation_dictionary'])} entries"
            )
            for entry in scenario["pronunciation_dictionary"]:
                print(
                    f"   '{entry['text']}' → '{entry['pronunciation']}' (partial_match={entry['partial_match']})"
                )
        print(f"{'='*60}")

        success = await streaming_tts_with_realtime_playback(
            voice_id,
            scenario["text"],
            scenario.get("pronunciation_dictionary"),
            scenario.get("language", "EN"),
        )

        if not success:
            print(f"❌ Scenario {i} failed")
            break

        if i < len(scenarios):
            print(f"\n⏳ Brief wait before next scenario...\n")
            await asyncio.sleep(1)  # Reduced from 5s to 1s

    print("\n🎉 All real-time streaming scenarios completed!")


def test_audio_playback():
    """Simple audio playback test"""
    print("🔊 Audio playback test")

    if not AUDIO_AVAILABLE:
        print("❌ sounddevice not installed")
        return False

    try:
        # 440Hz beep sound for 0.5 seconds
        duration = 0.5
        sample_rate = 24000
        frequency = 440

        t = np.linspace(0, duration, int(sample_rate * duration))
        tone = 0.3 * np.sin(2 * np.pi * frequency * t)

        print(f"📡 Playing test tone: {frequency}Hz, {duration}s")
        sd.play(tone, samplerate=sample_rate, blocking=True)

        print("✅ Audio test successful!")
        return True

    except Exception as e:
        print(f"❌ Audio test failed: {e}")
        return False


# Add to main function
def main():
    """Main execution function"""
    print("🎵 Real-time Streaming TTS Audio Player")
    print("=" * 50)

    if not AUDIO_AVAILABLE:
        print("\n⚠️ Audio library installation required:")
        print("pip install sounddevice numpy")
        print("brew install portaudio  # for macOS")
        print("\n📝 Proceeding with test using logs only without audio.\n")
    else:
        # Run simple audio test first
        print("\n🧪 Testing audio system...")
        if not test_audio_playback():
            print("⚠️ Audio system may have issues")
        print()

        # Check sounddevice initial settings
        try:
            print(f"🔊 Available audio devices:")
            devices = sd.query_devices()
            print(devices)
            print(f"🎯 Default output device: {sd.default.device[1]}")
        except Exception as e:
            print(f"⚠️ Audio device check error: {e}")

    try:
        # Run async demo
        asyncio.run(demo_realtime_streaming_scenarios())

    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Execution error: {e}")
        import traceback

        traceback.print_exc()

    print("\n👋 Real-time streaming TTS player terminated")


if __name__ == "__main__":
    main()
