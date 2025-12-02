# SDK Examples

This directory contains practical examples demonstrating how to use the SDK.

## 📁 Directory Structure

```
examples/
├── usage/                      # Usage & Credit Management
│   ├── get_credit_balance.py
│   ├── get_credit_balance_async.py
│   ├── get_usage.py
│   ├── get_usage_async.py
│   ├── get_voice_usage.py
│   └── get_voice_usage_async.py
├── voices/                     # Voice Management
│   ├── list_voices.py
│   ├── list_voices_async.py
│   ├── search_voices.py
│   ├── search_voices_async.py
│   ├── get_voice.py
│   └── get_voice_async.py
├── custom_voices/              # Custom Voice Management
│   ├── list_custom_voices.py
│   ├── list_custom_voices_async.py
│   ├── search_custom_voices.py
│   ├── search_custom_voices_async.py
│   ├── get_custom_voice.py
│   ├── get_custom_voice_async.py
│   ├── create_cloned_voice.py
│   ├── create_cloned_voice_async.py
│   ├── edit_custom_voice.py
│   ├── edit_custom_voice_async.py
│   ├── delete_custom_voice.py
│   └── delete_custom_voice_async.py
└── text_to_speech/            # Text-to-Speech
    ├── create_speech.py
    ├── create_speech_async.py
    ├── stream_speech.py
    ├── stream_speech_async.py
    ├── predict_duration.py
    └── predict_duration_async.py
```

## 🚀 Getting Started

### Installation

```bash
pip install supertone
```

### Configuration

Set your API key as an environment variable:

```bash
export SUPERTONE_API_KEY="your-api-key-here"
```

Or pass it directly when initializing the SDK:

```python
from supertone import Supertone

client = Supertone(api_key="your-api-key-here")
```

## 📝 Example Categories

### 1️⃣ Usage & Credit Management

Learn how to check your credit balance and usage statistics:

- **Get Credit Balance**: `usage/get_credit_balance.py` / `usage/get_credit_balance_async.py`
  - Check your current credit balance
- **Get Usage Statistics**: `usage/get_usage.py` / `usage/get_usage_async.py`
  - View detailed usage history with pagination
- **Get Voice Usage (by Date Range)**: `usage/get_voice_usage.py` / `usage/get_voice_usage_async.py`
  - Retrieve TTS API usage filtered by date range (UTC+0 timezone)

### 2️⃣ Voice Management

Discover available voices and get voice details:

- **List Voices**: `voices/list_voices.py` / `voices/list_voices_async.py`
  - Browse all available voices with pagination
- **Search Voices**: `voices/search_voices.py` / `voices/search_voices_async.py`
  - Filter voices by language, gender, age, use case, style, and more
- **Get Voice Details**: `voices/get_voice.py` / `voices/get_voice_async.py`
  - Retrieve detailed information about a specific voice

### 3️⃣ Custom Voice Management

Create and manage custom cloned voices:

- **List Custom Voices**: `custom_voices/list_custom_voices.py` / `custom_voices/list_custom_voices_async.py`
  - View all your custom cloned voices with pagination
- **Search Custom Voices**: `custom_voices/search_custom_voices.py` / `custom_voices/search_custom_voices_async.py`
  - Search custom voices by name and description
- **Get Custom Voice Details**: `custom_voices/get_custom_voice.py` / `custom_voices/get_custom_voice_async.py`
  - Retrieve detailed information about a specific custom voice
- **Create Cloned Voice**: `custom_voices/create_cloned_voice.py` / `custom_voices/create_cloned_voice_async.py`
  - Create a new custom voice from audio samples
- **Edit Custom Voice**: `custom_voices/edit_custom_voice.py` / `custom_voices/edit_custom_voice_async.py`
  - Update name and/or description of a custom voice
- **Delete Custom Voice**: `custom_voices/delete_custom_voice.py` / `custom_voices/delete_custom_voice_async.py`
  - Permanently delete a custom voice (⚠️ irreversible)

### 4️⃣ Text-to-Speech

Convert text to speech with various options:

- **Create Speech**: `text_to_speech/create_speech.py` / `text_to_speech/create_speech_async.py`
  - Converts text to audio file
  - Supports WAV and MP3 formats
  - Automatically handles long texts (>300 characters)
  - Optional: Voice customization (pitch, speed)
  - Optional: Phoneme data for lip-sync
- **Stream Speech**: `text_to_speech/stream_speech.py` / `text_to_speech/stream_speech_async.py`
  - Real-time audio streaming
  - Lower latency for immediate playback
  - Sequential streaming for long texts
  - Same customization options as create_speech
- **Predict Duration**: `text_to_speech/predict_duration.py` / `text_to_speech/predict_duration_async.py`
  - Estimate TTS duration without generating audio
  - Useful for planning and resource allocation

**💡 All TTS examples include commented options for:**

- MP3 format (smaller file size for web/mobile)
- Voice settings (pitch_shift, speed)
- Phoneme data (for lip-sync and animation)

## 🔄 Sync vs Async

### Sync Examples

- Simple and straightforward
- Good for scripts and simple applications
- Blocking operations

```python
from supertone import Supertone

client = Supertone()
response = client.text_to_speech.create_speech(...)
client.close()
```

### Async Examples

- Non-blocking operations
- Parallel processing capabilities
- Ideal for web servers and high-throughput applications

```python
import asyncio
from supertone import Supertone

async with Supertone() as client:
    response = await client.text_to_speech.create_speech_async(...)
```

## 🎯 Key Features Demonstrated

### ✅ Automatic Text Chunking

The SDK automatically handles long texts (>300 characters):

- Splits text into manageable chunks
- Processes chunks in parallel (async) or sequentially (sync)
- Seamlessly merges results
- No manual intervention required

### ✅ Streaming Support

Real-time audio streaming for low-latency applications:

- Sync: `iter_bytes()`
- Async: `aiter_bytes()`
- Ideal for long texts and low-latency requirements

### ✅ Custom Voice Cloning

Create personalized voices from audio samples:

- Upload audio files for voice cloning
- Manage custom voice library
- Use custom voices in TTS

### ✅ Multiple Format Support

- WAV format for high quality
- MP3 format for smaller file sizes
- Multiple language support

## 📚 Additional Resources

- [API Documentation](../docs/)
- [GitHub Repository](https://github.com/your-org/sdk)
- [Support](mailto:support@example.com)

## 💡 Tips

1. **Use Async for Performance**: When processing multiple requests, async versions can be significantly faster due to non-blocking I/O.

2. **Streaming for Long Texts**: Use streaming for long texts to reduce latency and memory usage. The SDK automatically handles chunking for texts > 300 characters.

3. **Custom Voices**: Create custom cloned voices for personalized applications. Upload clear audio samples for best results.

4. **Error Handling**: All examples include basic error handling. Enhance it for production use with retry logic and proper logging.

5. **API Keys**: Never hardcode API keys in your code. Use environment variables or secure key management systems.

## 🐛 Troubleshooting

### ImportError: cannot import name 'Supertone'

Make sure the SDK is installed and you're importing from the correct package:

```bash
pip install supertone
```

### Authentication Error

Check that your API key is set correctly:

```bash
echo $SUPERTONE_API_KEY
```

### Voice ID Not Found

Get a list of available voices first:

```bash
python examples/voices/list_voices.py
```

## 🤝 Contributing

Found a bug or want to add an example? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Submit a pull request
