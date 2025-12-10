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