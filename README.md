# Supertone Python Library
<!-- Start Summary [summary] -->
## Summary

The official Python SDK for [Supertone API](https://www.supertone.ai/en/api)

<!-- End Summary [summary] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

The SDK can be installed with *uv*, *pip*, or *poetry* package managers.

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

<!-- Start SDK Example [usage] -->
## SDK Example

### Example

```python
# Synchronous Example
from supertone import Supertone, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model="sona_speech_1", output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

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

        res = await s_client.text_to_speech.create_speech_async(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model="sona_speech_1", output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->

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

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model="sona_speech_1", output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

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

### Example
```python
from supertone import Supertone, errors, models


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:
    res = None
    try:

        res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model="sona_speech_1", output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

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

<!-- End Error Handling [errors] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->
