# CustomVoices
(*custom_voices*)

## Overview

Custom Voice Management API endpoints

### Available Operations

* [create_cloned_voice](#create_cloned_voice) - Create cloned voice
* [list_custom_voices](#list_custom_voices) - Gets custom (cloned) voices
* [search_custom_voices](#search_custom_voices) - Search custom (cloned) voices
* [get_custom_voice](#get_custom_voice) - Get single cloned voice
* [edit_custom_voice](#edit_custom_voice) - Update cloned voice (partial update)
* [delete_custom_voice](#delete_custom_voice) - Delete cloned voice

## create_cloned_voice

Creates a custom (cloned) voice from uploaded audio files.

### Example Usage

<!-- UsageSnippet language="python" operationID="create_cloned_voice" method="post" path="/v1/custom-voices/cloned-voice" -->
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

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `files`                                                             | [models.Files](../../models/files.md)                               | :heavy_check_mark:                                                  | Audio file to clone voice from (WAV/MP3 format, max 3MB)            |
| `name`                                                              | *str*                                                               | :heavy_check_mark:                                                  | Name of the cloned voice                                            |
| `description`                                                       | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Description of the cloned voice                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.CreateClonedVoiceUploadResponse](../../models/createclonedvoiceuploadresponse.md)**

### Errors

| Error Type                               | Status Code                              | Content Type                             |
| ---------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| errors.BadRequestErrorResponse           | 400                                      | application/json                         |
| errors.UnauthorizedErrorResponse         | 401                                      | application/json                         |
| errors.ForbiddenErrorResponse            | 403                                      | application/json                         |
| errors.NotFoundErrorResponse             | 404                                      | application/json                         |
| errors.PayloadTooLargeErrorResponse      | 413                                      | application/json                         |
| errors.UnsupportedMediaTypeErrorResponse | 415                                      | application/json                         |
| errors.TooManyRequestsErrorResponse      | 429                                      | application/json                         |
| errors.InternalServerErrorResponse       | 500                                      | application/json                         |
| errors.SupertoneDefaultError             | 4XX, 5XX                                 | \*/\*                                    |

## list_custom_voices

Gets a paginated list of custom (cloned) voices available to the user, using token-based pagination.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_custom_voices" method="get" path="/v1/custom-voices" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.custom_voices.list_custom_voices()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[float]*                                                   | :heavy_minus_sign:                                                  | Number of items per page (default: 20, min: 10, max: 100)           |
| `next_page_token`                                                   | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Token for pagination (obtained from the previous page's response)   |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetCustomVoiceListResponse](../../models/getcustomvoicelistresponse.md)**

### Errors

| Error Type                         | Status Code                        | Content Type                       |
| ---------------------------------- | ---------------------------------- | ---------------------------------- |
| errors.UnauthorizedErrorResponse   | 401                                | application/json                   |
| errors.NotFoundErrorResponse       | 404                                | application/json                   |
| errors.InternalServerErrorResponse | 500                                | application/json                   |
| errors.SupertoneDefaultError       | 4XX, 5XX                           | \*/\*                              |

## search_custom_voices

Search and filter custom (cloned) voices based on various parameters. Space-separated terms in name/description fields use AND condition (all terms must be present).

### Example Usage

<!-- UsageSnippet language="python" operationID="search_custom_voices" method="get" path="/v1/custom-voices/search" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.custom_voices.search_custom_voices()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `page_size`                                                         | *Optional[float]*                                                   | :heavy_minus_sign:                                                  | Number of items per page (default: 20, min: 10, max: 100)           |
| `next_page_token`                                                   | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Token for pagination (obtained from the previous page's response)   |
| `name`                                                              | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Search across name. Space separated.                                |
| `description`                                                       | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Search across description. Space separated.                         |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetCustomVoiceListResponse](../../models/getcustomvoicelistresponse.md)**

### Errors

| Error Type                         | Status Code                        | Content Type                       |
| ---------------------------------- | ---------------------------------- | ---------------------------------- |
| errors.UnauthorizedErrorResponse   | 401                                | application/json                   |
| errors.NotFoundErrorResponse       | 404                                | application/json                   |
| errors.InternalServerErrorResponse | 500                                | application/json                   |
| errors.SupertoneDefaultError       | 4XX, 5XX                           | \*/\*                              |

## get_custom_voice

Gets details of a specific custom (cloned) voice by ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_custom_voice" method="get" path="/v1/custom-voices/{voice_id}" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.custom_voices.get_custom_voice(voice_id="<id>")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.GetSingleClonedVoiceResponse](../../models/getsingleclonedvoiceresponse.md)**

### Errors

| Error Type                         | Status Code                        | Content Type                       |
| ---------------------------------- | ---------------------------------- | ---------------------------------- |
| errors.UnauthorizedErrorResponse   | 401                                | application/json                   |
| errors.NotFoundErrorResponse       | 404                                | application/json                   |
| errors.InternalServerErrorResponse | 500                                | application/json                   |
| errors.SupertoneDefaultError       | 4XX, 5XX                           | \*/\*                              |

## edit_custom_voice

Partially updates properties of a custom (cloned) voice by ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="edit_custom_voice" method="patch" path="/v1/custom-voices/{voice_id}" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    res = s_client.custom_voices.edit_custom_voice(voice_id="<id>", name="My Updated Voice", description="An updated warm and friendly voice for customer service")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |                                                                     |
| `name`                                                              | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Name of the voice                                                   | My Updated Voice                                                    |
| `description`                                                       | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | Description of the voice                                            | An updated warm and friendly voice for customer service             |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.UpdateClonedVoiceResponse](../../models/updateclonedvoiceresponse.md)**

### Errors

| Error Type                         | Status Code                        | Content Type                       |
| ---------------------------------- | ---------------------------------- | ---------------------------------- |
| errors.UnauthorizedErrorResponse   | 401                                | application/json                   |
| errors.NotFoundErrorResponse       | 404                                | application/json                   |
| errors.InternalServerErrorResponse | 500                                | application/json                   |
| errors.SupertoneDefaultError       | 4XX, 5XX                           | \*/\*                              |

## delete_custom_voice

Deletes a custom (cloned) voice by ID.

### Example Usage

<!-- UsageSnippet language="python" operationID="delete_custom_voice" method="delete" path="/v1/custom-voices/{voice_id}" -->
```python
from supertone import Supertone


with Supertone(
    api_key="<YOUR_API_KEY_HERE>",
) as s_client:

    s_client.custom_voices.delete_custom_voice(voice_id="<id>")

    # Use the SDK ...

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `voice_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Errors

| Error Type                         | Status Code                        | Content Type                       |
| ---------------------------------- | ---------------------------------- | ---------------------------------- |
| errors.UnauthorizedErrorResponse   | 401                                | application/json                   |
| errors.NotFoundErrorResponse       | 404                                | application/json                   |
| errors.InternalServerErrorResponse | 500                                | application/json                   |
| errors.SupertoneDefaultError       | 4XX, 5XX                           | \*/\*                              |