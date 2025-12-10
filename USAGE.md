<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.
```python
# Asynchronous Example
import asyncio
from supertone import Supertone, models

async def main():

    async with Supertone(
        api_key="<YOUR_API_KEY_HERE>",
    ) as s_client:

        res = await s_client.text_to_speech.create_speech_async(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->