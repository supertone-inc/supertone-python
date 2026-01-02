# TextToSpeech
(*text_to_speech*)

## Overview

Text-to-Speech API endpoints

### Available Operations

* [create_speech](#create_speech) - Convert text to speech
* [stream_speech](#stream_speech) - Convert text to speech with streaming response
* [predict_duration](#predict_duration) - Predict text-to-speech duration

## create_speech

Convert text to speech using the specified voice

### Example Usage

<!-- UsageSnippet language="python" operationID="create_speech" method="post" path="/v1/text-to-speech/{voice_id}" -->
```python
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                           | Type                                                                                                                                                | Required                                                                                                                                            | Description                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voice_id`                                                                                                                                          | *str*                                                                                                                                               | :heavy_check_mark:                                                                                                                                  | N/A                                                                                                                                                 |
| `text`                                                                                                                                              | *str*                                                                                                                                               | :heavy_check_mark:                                                                                                                                  | The text to convert to speech                                                                                                                       |
| `language`                                                                                                                                          | [models.APIConvertTextToSpeechUsingCharacterRequestLanguage](../../models/apiconverttexttospeechusingcharacterrequestlanguage.md)                   | :heavy_check_mark:                                                                                                                                  | The language code of the text                                                                                                                       |
| `style`                                                                                                                                             | *Optional[str]*                                                                                                                                     | :heavy_minus_sign:                                                                                                                                  | The style of character to use for the text-to-speech conversion                                                                                     |
| `model`                                                                                                                                             | [Optional[models.APIConvertTextToSpeechUsingCharacterRequestModel]](../../models/apiconverttexttospeechusingcharacterrequestmodel.md)               | :heavy_minus_sign:                                                                                                                                  | The model type to use for the text-to-speech conversion                                                                                             |
| `output_format`                                                                                                                                     | [Optional[models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat]](../../models/apiconverttexttospeechusingcharacterrequestoutputformat.md) | :heavy_minus_sign:                                                                                                                                  | The desired output format of the audio file (wav, mp3). Default is wav.                                                                             |
| `voice_settings`                                                                                                                                    | [Optional[models.ConvertTextToSpeechParameters]](../../models/converttexttospeechparameters.md)                                                     | :heavy_minus_sign:                                                                                                                                  | N/A                                                                                                                                                 |
| `include_phonemes`                                                                                                                                  | *Optional[bool]*                                                                                                                                    | :heavy_minus_sign:                                                                                                                                  | Return phoneme timing data with the audio                                                                                                           |
| `retries`                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                    | :heavy_minus_sign:                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                 |
| pronunciation_dictionary | Optional[List[dict]] | :heavy_minus_sign: | Optional pronunciation rules applied during text pre-processing to customize how specific words or phrases are spoken. |



### Response

**[models.CreateSpeechResponse](../../models/createspeechresponse.md)**

### Errors

| Error Type                          | Status Code                         | Content Type                        |
| ----------------------------------- | ----------------------------------- | ----------------------------------- |
| errors.BadRequestErrorResponse      | 400                                 | application/json                    |
| errors.UnauthorizedErrorResponse    | 401                                 | application/json                    |
| errors.PaymentRequiredErrorResponse | 402                                 | application/json                    |
| errors.ForbiddenErrorResponse       | 403                                 | application/json                    |
| errors.NotFoundErrorResponse        | 404                                 | application/json                    |
| errors.RequestTimeoutErrorResponse  | 408                                 | application/json                    |
| errors.TooManyRequestsErrorResponse | 429                                 | application/json                    |
| errors.InternalServerErrorResponse  | 500                                 | application/json                    |
| errors.SupertoneDefaultError        | 4XX, 5XX                            | \*/\*                               |

## stream_speech

Convert text to speech using the specified voice with streaming response. Returns binary audio stream.

### Example Usage

<!-- UsageSnippet language="python" operationID="stream_speech" method="post" path="/v1/text-to-speech/{voice_id}/stream" -->
```python
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.stream_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.PT, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                           | Type                                                                                                                                                | Required                                                                                                                                            | Description                                                                                                                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `voice_id`                                                                                                                                          | *str*                                                                                                                                               | :heavy_check_mark:                                                                                                                                  | N/A                                                                                                                                                 |
| `text`                                                                                                                                              | *str*                                                                                                                                               | :heavy_check_mark:                                                                                                                                  | The text to convert to speech                                                                                                                       |
| `language`                                                                                                                                          | [models.APIConvertTextToSpeechUsingCharacterRequestLanguage](../../models/apiconverttexttospeechusingcharacterrequestlanguage.md)                   | :heavy_check_mark:                                                                                                                                  | The language code of the text                                                                                                                       |
| `style`                                                                                                                                             | *Optional[str]*                                                                                                                                     | :heavy_minus_sign:                                                                                                                                  | The style of character to use for the text-to-speech conversion                                                                                     |
| `model`                                                                                                                                             | [Optional[models.APIConvertTextToSpeechUsingCharacterRequestModel]](../../models/apiconverttexttospeechusingcharacterrequestmodel.md)               | :heavy_minus_sign:                                                                                                                                  | The model type to use for the text-to-speech conversion                                                                                             |
| `output_format`                                                                                                                                     | [Optional[models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat]](../../models/apiconverttexttospeechusingcharacterrequestoutputformat.md) | :heavy_minus_sign:                                                                                                                                  | The desired output format of the audio file (wav, mp3). Default is wav.                                                                             |
| `voice_settings`                                                                                                                                    | [Optional[models.ConvertTextToSpeechParameters]](../../models/converttexttospeechparameters.md)                                                     | :heavy_minus_sign:                                                                                                                                  | N/A                                                                                                                                                 |
| `include_phonemes`                                                                                                                                  | *Optional[bool]*                                                                                                                                    | :heavy_minus_sign:                                                                                                                                  | Return phoneme timing data with the audio                                                                                                           |
| `retries`                                                                                                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                                    | :heavy_minus_sign:                                                                                                                                  | Configuration to override the default retry behavior of the client.                                                                                 |
| pronunciation_dictionary | Optional[List[dict]] | :heavy_minus_sign: | Optional pronunciation rules applied during text pre-processing to customize how specific words or phrases are spoken. |

### Response

**[models.StreamSpeechResponse](../../models/streamspeechresponse.md)**

### Errors

| Error Type                          | Status Code                         | Content Type                        |
| ----------------------------------- | ----------------------------------- | ----------------------------------- |
| errors.BadRequestErrorResponse      | 400                                 | application/json                    |
| errors.UnauthorizedErrorResponse    | 401                                 | application/json                    |
| errors.PaymentRequiredErrorResponse | 402                                 | application/json                    |
| errors.ForbiddenErrorResponse       | 403                                 | application/json                    |
| errors.NotFoundErrorResponse        | 404                                 | application/json                    |
| errors.RequestTimeoutErrorResponse  | 408                                 | application/json                    |
| errors.TooManyRequestsErrorResponse | 429                                 | application/json                    |
| errors.InternalServerErrorResponse  | 500                                 | application/json                    |
| errors.SupertoneDefaultError        | 4XX, 5XX                            | \*/\*                               |


## Pronunciation Dictionary

Customize pronunciations by providing a pronunciation dictionary in each request. This is useful for proper nouns, brand names, acronyms, or loanwords that the default TTS engine may pronounce inconsistently.

The dictionary is applied during **text pre-processing** before the TTS pipeline runs.

### How it works

Each rule contains:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | string | :heavy_check_mark: | The target text to replace |
| `pronunciation` | string | :heavy_check_mark: | The replacement pronunciation (e.g., words or phonetic spelling) |
| `partial_match` | boolean | :heavy_check_mark: | If `true`, replace all substrings. If `false`, replace only exact whole-word matches. |

**Matching behavior**

- `partial_match = false`
    
    Replaces only when `text` matches a whole word (word boundary match).
    
- `partial_match = true`
    
    Replaces all occurrences of `text` as a substring (no word boundary check).
    

**Rule order & conflicts**

- Rules are applied **in the order provided**.
- If multiple rules target the same text, the **first matching rule wins** and later rules do not re-replace that same text.

### Example Usage

```python
from supertoneimport Supertone, models

with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
)as s_client:

    res = s_client.text_to_speech.create_speech(
        voice_id="<id>",
        text="Supertone API provides support for TTS and STS.",
        language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.KO,
        model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1,
        output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV,
        include_phonemes=False,
        pronunciation_dictionary=[
            {
"text":"Supertone",
"pronunciation":"super tone",
"partial_match":False,
            },
            {
"text":"TTS",
"pronunciation":"text to speech",
"partial_match":True,
            },
        ],
    )

# Handle response
print(res)

```

> This parameter is optional. If pronunciation_dictionary is not provided, text-to-speech behaves as usual.

## predict_duration

Predict the duration of text-to-speech conversion without generating audio

### Example Usage

<!-- UsageSnippet language="python" operationID="predict_duration" method="post" path="/v1/predict-duration/{voice_id}" -->
```python
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.predict_duration(voice_id="<id>", text="<value>", language=models.PredictTTSDurationUsingCharacterRequestLanguage.JA, model=models.PredictTTSDurationUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.PredictTTSDurationUsingCharacterRequestOutputFormat.WAV)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                   | Type                                                                                                                                        | Required                                                                                                                                    | Description                                                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `voice_id`                                                                                                                                  | *str*                                                                                                                                       | :heavy_check_mark:                                                                                                                          | N/A                                                                                                                                         |
| `text`                                                                                                                                      | *str*                                                                                                                                       | :heavy_check_mark:                                                                                                                          | The text to convert to speech. Max length is 300 characters.                                                                                |
| `language`                                                                                                                                  | [models.PredictTTSDurationUsingCharacterRequestLanguage](../../models/predictttsdurationusingcharacterrequestlanguage.md)                   | :heavy_check_mark:                                                                                                                          | Language code of the voice                                                                                                                  |
| `style`                                                                                                                                     | *Optional[str]*                                                                                                                             | :heavy_minus_sign:                                                                                                                          | The style of character to use for the text-to-speech conversion                                                                             |
| `model`                                                                                                                                     | [Optional[models.PredictTTSDurationUsingCharacterRequestModel]](../../models/predictttsdurationusingcharacterrequestmodel.md)               | :heavy_minus_sign:                                                                                                                          | The model type to use for the text-to-speech conversion                                                                                     |
| `output_format`                                                                                                                             | [Optional[models.PredictTTSDurationUsingCharacterRequestOutputFormat]](../../models/predictttsdurationusingcharacterrequestoutputformat.md) | :heavy_minus_sign:                                                                                                                          | The desired output format of the audio file (wav, mp3). Default is wav.                                                                     |
| `voice_settings`                                                                                                                            | [Optional[models.ConvertTextToSpeechParameters]](../../models/converttexttospeechparameters.md)                                             | :heavy_minus_sign:                                                                                                                          | N/A                                                                                                                                         |
| `retries`                                                                                                                                   | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                            | :heavy_minus_sign:                                                                                                                          | Configuration to override the default retry behavior of the client.                                                                         |

### Response

**[models.PredictDurationResponse](../../models/predictdurationresponse.md)**

### Errors

| Error Type                          | Status Code                         | Content Type                        |
| ----------------------------------- | ----------------------------------- | ----------------------------------- |
| errors.BadRequestErrorResponse      | 400                                 | application/json                    |
| errors.UnauthorizedErrorResponse    | 401                                 | application/json                    |
| errors.PaymentRequiredErrorResponse | 402                                 | application/json                    |
| errors.ForbiddenErrorResponse       | 403                                 | application/json                    |
| errors.NotFoundErrorResponse        | 404                                 | application/json                    |
| errors.RequestTimeoutErrorResponse  | 408                                 | application/json                    |
| errors.TooManyRequestsErrorResponse | 429                                 | application/json                    |
| errors.InternalServerErrorResponse  | 500                                 | application/json                    |
| errors.SupertoneDefaultError        | 4XX, 5XX                            | \*/\*                               |
