# Supertone Python Library

![LOGO](https://github.com/supertone-inc/supertone-python/blob/3d19bcdad946bd3c7412f40818ef799b32b2e8e9/images/hero-light.png?raw=true)

<!-- Start Summary [summary] -->
## Summary

Supertone Public API: Supertone API is a RESTful API for using our state-of-the-art AI voice models.
<!-- End Summary [summary] -->

<!-- Start SDK Installation [installation] -->

## SDK Installation

The SDK can be installed with _uv_, _pip_, or _poetry_ package managers.

### uv

_uv_ is a fast Python package installer and resolver, designed as a drop-in replacement for pip and pip-tools. It's recommended for its speed and modern Python tooling capabilities.

```bash
uv add supertone
```

### PIP

_PIP_ is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install supertone
```

### Poetry

_Poetry_ is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add supertone
```

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

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

<!-- Start SDK Installation [installation] -->
## SDK Installation

### uv

*uv* is a fast Python package installer and resolver, designed as a drop-in replacement for pip and pip-tools. It's recommended for its speed and modern Python tooling capabilities.

```bash
uv add git+<UNSET>.git
```

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install git+<UNSET>.git
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+<UNSET>.git
```

<!-- End SDK Installation [installation] -->

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name      | Type   | Scheme  |
| --------- | ------ | ------- |
| `api_key` | apiKey | API key |

To authenticate with the API the `api_key` parameter must be set when initializing the SDK client instance. For example:
```python
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Models [models] -->

## Models

Supertone’s Text-to-Speech API provides multiple TTS models, each with different supported languages, available voice settings, and streaming capabilities.

### Model Overview

| Model Name         | Identifier        | Streaming Support (`stream_speech`) | Voice Settings Support                                   |
|--------------------|-------------------|--------------------------------------|----------------------------------------------------------|
| **SONA Speech 1**  | `sona_speech_1`   | ✅ Supported                         | Supports **all** Voice Settings                          |
| **Supertonic API 1** | `supertonic_api_1` | ❌ Not supported                  | Supports **only** the `speed` setting (others are ignored) |
| **SONA Speech 2**  | `sona_speech_2`   | ❌ Not supported                     | Supports **pitch_shift**, **pitch_variance**, **speed**   |

> [!NOTE]
> **Streaming Support**
>
> Streaming TTS using the `stream_speech` endpoint is **only available for the `sona_speech_1` model**.

---

### Supported Languages by Model

> [!NOTE]
> The set of supported input languages varies depending on the TTS model.

- **sona_speech_1**
  - `en`, `ko`, `ja`

- **supertonic_api_1**
  - `en`, `ko`, `ja`, `es`, `pt`

- **sona_speech_2**
  - `en`, `ko`, `ja`, `bg`, `cs`, `da`, `el`, `es`, `et`, `fi`, `hu`, `it`, `nl`, `pl`, `pt`, `ro`,  
    `ar`, `de`, `fr`, `hi`, `id`, `ru`, `vi`

---

### Voice Settings (Optional)

Some TTS models support optional voice settings that allow fine control over output speech characteristics (e.g., speed, pitch, pitch variance).

> [!NOTE]
> The available Voice Settings vary depending on the TTS model.

- **sona_speech_1**
  - Supports **all** available Voice Settings.

- **supertonic_api_1**
  - Supports **only** the `speed` setting.  
    All other settings will be ignored.

- **sona_speech_2**
  - Supports the following Voice Settings:
    - `pitch_shift`
    - `pitch_variance`
    - `speed`

> All Voice Settings are optional. When omitted, each model’s default values will be applied.

<!-- End Models [models] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [custom_voices](docs/sdks/customvoices/README.md)

* [create_cloned_voice](docs/sdks/customvoices/README.md#create_cloned_voice) - Create cloned voice
* [list_custom_voices](docs/sdks/customvoices/README.md#list_custom_voices) - Gets custom (cloned) voices
* [search_custom_voices](docs/sdks/customvoices/README.md#search_custom_voices) - Search custom (cloned) voices
* [get_custom_voice](docs/sdks/customvoices/README.md#get_custom_voice) - Get single cloned voice
* [edit_custom_voice](docs/sdks/customvoices/README.md#edit_custom_voice) - Update cloned voice (partial update)
* [delete_custom_voice](docs/sdks/customvoices/README.md#delete_custom_voice) - Delete cloned voice


### [text_to_speech](docs/sdks/texttospeech/README.md)

* [create_speech](docs/sdks/texttospeech/README.md#create_speech) - Convert text to speech
* [stream_speech](docs/sdks/texttospeech/README.md#stream_speech) - Convert text to speech with streaming response
* [predict_duration](docs/sdks/texttospeech/README.md#predict_duration) - Predict text-to-speech duration

### [usage](docs/sdks/usage/README.md)

* [get_voice_usage](docs/sdks/usage/README.md#get_voice_usage) - Retrieve TTS API usage data
* [get_usage](docs/sdks/usage/README.md#get_usage) - Retrieve advanced API usage analytics
* [get_credit_balance](docs/sdks/usage/README.md#get_credit_balance) - Retrieve credit balance

### [voices](docs/sdks/voices/README.md)

* [list_voices](docs/sdks/voices/README.md#list_voices) - Gets available voices
* [search_voices](docs/sdks/voices/README.md#search_voices) - Search voices.
* [get_voice](docs/sdks/voices/README.md#get_voice) - Get voice details by ID

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`SupertoneError`](./src/supertone/errors/supertoneerror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```python
from supertone import Supertone, errors, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:
    res = None
    try:

        res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

        # Handle response
        print(res)


    except errors.SupertoneError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, errors.BadRequestErrorResponse):
            print(e.data.status)  # str
            print(e.data.message)  # str
```

### Error Classes
**Primary error:**
* [`SupertoneError`](./src/supertone/errors/supertoneerror.py): The base class for HTTP error responses.

<details><summary>Less common errors (15)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`SupertoneError`](./src/supertone/errors/supertoneerror.py)**:
* [`UnauthorizedErrorResponse`](./src/supertone/errors/unauthorizederrorresponse.py): Unauthorized: Invalid API key. Status code `401`. Applicable to 10 of 15 methods.*
* [`InternalServerErrorResponse`](./src/supertone/errors/internalservererrorresponse.py): Status code `500`. Applicable to 10 of 15 methods.*
* [`NotFoundErrorResponse`](./src/supertone/errors/notfounderrorresponse.py): Status code `404`. Applicable to 9 of 15 methods.*
* [`BadRequestErrorResponse`](./src/supertone/errors/badrequesterrorresponse.py): Status code `400`. Applicable to 5 of 15 methods.*
* [`ForbiddenErrorResponse`](./src/supertone/errors/forbiddenerrorresponse.py): Status code `403`. Applicable to 4 of 15 methods.*
* [`RequestTimeoutErrorResponse`](./src/supertone/errors/requesttimeouterrorresponse.py): Status code `408`. Applicable to 4 of 15 methods.*
* [`TooManyRequestsErrorResponse`](./src/supertone/errors/toomanyrequestserrorresponse.py): Status code `429`. Applicable to 4 of 15 methods.*
* [`PaymentRequiredErrorResponse`](./src/supertone/errors/paymentrequirederrorresponse.py): Status code `402`. Applicable to 3 of 15 methods.*
* [`PayloadTooLargeErrorResponse`](./src/supertone/errors/payloadtoolargeerrorresponse.py): Payload Too Large: File size exceeds 3MB limit. Status code `413`. Applicable to 1 of 15 methods.*
* [`UnsupportedMediaTypeErrorResponse`](./src/supertone/errors/unsupportedmediatypeerrorresponse.py): Unsupported Media Type: Invalid audio file format. Status code `415`. Applicable to 1 of 15 methods.*
* [`ResponseValidationError`](./src/supertone/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>

\* Check [the method documentation](#available-resources-and-operations) to see if the error is applicable.
<!-- End Error Handling [errors] -->

<!-- Start Additional Example Code [examples] -->

## Additional Example Code

Additional example code can be found in the [examples](https://github.com/supertone-inc/supertone-python/tree/main/examples) directory.

<!-- End Additional Example Code [examples] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->
