# Supertone Python Library

![LOGO](https://github.com/supertone-inc/supertone-python/blob/3d19bcdad946bd3c7412f40818ef799b32b2e8e9/images/hero-light.png?raw=true)

<!-- Start Summary [summary] -->
## Summary

Supertone Public API: Supertone API is a RESTful API for using our state-of-the-art AI voice models.
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [Supertone Python Library](#supertone-python-library)
  * [SDK Installation](#sdk-installation)
  * [SDK Installation](#sdk-installation-1)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Authentication](#authentication)
  * [Models](#models)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [File uploads](#file-uploads)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Additional Example Code](#additional-example-code)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)

<!-- End Table of Contents [toc] -->

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

<!-- Start SDK Installation [installation] -->
## SDK Installation

> [!TIP]
> To finish publishing your SDK to PyPI you must [run your first generation action](https://www.speakeasy.com/docs/github-setup#step-by-step-guide).


> [!NOTE]
> **Python version upgrade policy**
>
> Once a Python version reaches its [official end of life date](https://devguide.python.org/versions/), a 3-month grace period is provided for users to upgrade. Following this grace period, the minimum python version supported in the SDK will be updated.

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

### Shell and script usage with `uv`

You can use this SDK in a Python shell with [uv](https://docs.astral.sh/uv/) and the `uvx` command that comes with it like so:

```shell
uvx --from supertone python
```

It's also possible to write a standalone Python script without needing to set up a whole project like so:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "supertone",
# ]
# ///

from supertone import Supertone

sdk = Supertone(
  # SDK arguments
)

# Rest of script here...
```

Once that is saved to a file, you can run it with `uv run script.py` where
`script.py` can be replaced with the actual file name.
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

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
| **SONA Speech 2**  | `sona_speech_2`   | ❌ Not supported                     | Supports **all** Voice Settings **except** `subharmonic_amplitude_control` |
| **SONA Speech 2 Flash**  | `sona_speech_2_flash`   | ❌ Not supported | Supports **all** Voice Settings **except** `similarity`, `text_guidance`,`subharmonic_amplitude_control` |


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
- **sona_speech_2_flash**
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
  - Supports **all** Voice Settings **except** `subharmonic_amplitude_control`.

- **sona_speech_2_flash**
  - Supports **all** Voice Settings **except** `similarity`, `text_guidance`, `subharmonic_amplitude_control`.


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

<!-- Start File uploads [file-upload] -->
## File uploads

Certain SDK methods accept file objects as part of a request body or multi-part request. It is possible and typically recommended to upload files as a stream rather than reading the entire contents into memory. This avoids excessive memory consumption and potentially crashing with out-of-memory errors when working with very large files. The following example demonstrates how to attach a file stream to a request.

> [!TIP]
>
> For endpoints that handle file uploads bytes arrays can also be used. However, using streams is recommended for large files.
>

```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.custom_voices.create_cloned_voice(files={
        "file_name": "example.file",
        "content": open("example.file", "rb"),
    }, name="<value>")

    # Handle response
    print(res)

```
<!-- End File uploads [file-upload] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from supertone import Supertone, models
from supertone.utils import BackoffStrategy, RetryConfig


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False,
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from supertone import Supertone, models
from supertone.utils import BackoffStrategy, RetryConfig


with Supertone(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

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

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from supertone import Supertone, models


with Supertone(
    server_url="https://supertoneapi.com",
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.text_to_speech.create_speech(voice_id="<id>", text="<value>", language=models.APIConvertTextToSpeechUsingCharacterRequestLanguage.JA, model=models.APIConvertTextToSpeechUsingCharacterRequestModel.SONA_SPEECH_1, output_format=models.APIConvertTextToSpeechUsingCharacterRequestOutputFormat.WAV, include_phonemes=False)

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from supertone import Supertone
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = Supertone(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from supertone import Supertone
from supertone.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = Supertone(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `Supertone` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from supertone import Supertone
def main():

    with Supertone(
        api_key="<YOUR_API_KEY_HERE>",
    ) as s_client:
        # Rest of application here...


# Or when using async:
async def amain():

    async with Supertone(
        api_key="<YOUR_API_KEY_HERE>",
    ) as s_client:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from supertone import Supertone
import logging

logging.basicConfig(level=logging.DEBUG)
s = Supertone(debug_logger=logging.getLogger("supertone"))
```
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->
